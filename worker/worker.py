import asyncio
import random
import argparse
import json
from datetime import datetime
from typing import Callable, Awaitable

import asyncpg

from tools.const import CONNECTION_STRING, QUEUE_COMMON, QUANTITY_WORKERS, \
    TIMEOUT_TASK
from tools.utils import UPDATE_TASK, SELECT_TASK


async def get_pool():
    return await asyncpg.create_pool(CONNECTION_STRING)


async def put(conn, task_id, result_kwargs):
    """Изменение обработанного таска"""
    await asyncio.sleep(random.uniform(0.5, 3.))
    await conn.execute(
        UPDATE_TASK,
        datetime.now(),  # compete_time
        1,  # status
        json.dumps(result_kwargs),
        task_id,
    )


async def get(conn, queue):
    """Получение одного таска из очереди"""
    await asyncio.sleep(random.uniform(0.5, 3.))
    return await conn.fetchrow(SELECT_TASK, queue)


async def _consume(
        queue: str,
        handler: Callable[[dict], Awaitable[dict]],
        pool: asyncpg.Pool,
):
    """Обработка одного таска из очереди"""
    async with pool.acquire() as conn:
        async with conn.transaction():
            task = await get(conn, queue)
            if task:
                result_kwargs = await handler(**json.loads(task['kwargs']))
                await put(conn, task['id'], result_kwargs)
                print('Compete task %s' % task['id'])


async def consume(queue: str, handler: Callable[[dict], Awaitable[dict]]):
    """Обработка тасков из очереди"""
    pool = await get_pool()
    while True:
        try:
            await asyncio.wait_for(
                _consume(queue, handler, pool),
                timeout=TIMEOUT_TASK,
            )
        except asyncio.TimeoutError:
            print('Timeout!')


async def queue_handler(**kwargs: dict):
    """Обработчик для кваргов из таска"""
    await asyncio.sleep(random.uniform(0.5, 3.))
    return {'result': sum(kwargs.values())}


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue',
                        type=str,
                        help='Queue name',
                        required=False,
                        default=QUEUE_COMMON,
                        )
    parser.add_argument('--count',
                        type=int,
                        help='Quantity workers',
                        required=False,
                        default=QUANTITY_WORKERS,
                        )
    return parser.parse_args()


def main():
    args = get_args()
    loop = asyncio.get_event_loop()
    for _ in range(args.count):
        loop.create_task(consume(args.queue, queue_handler))
    loop.run_forever()


if __name__ == '__main__':
    main()
