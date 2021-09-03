import json
from datetime import datetime

SELECT_TASK = """
    SELECT task.id, task.kwargs
    FROM task, queue 
    WHERE queue.name = $1
    and task.status = 0
    and task.queue_id = queue.id
    limit 1
    FOR UPDATE SKIP LOCKED;
"""

SELECT_QUEUE = """
    SELECT queue.id
    FROM queue
    WHERE queue.name = $1;
"""

UPDATE_TASK = """
    UPDATE task
    SET complete_time = $1, status = $2, result = $3 
    WHERE task.id = $4; 
"""

INSERT_TASK = """
    INSERT INTO task(create_time, kwargs, queue_id) 
    values ($1, $2, $3) RETURNING id;
"""

INSERT_QUEUE = """
    INSERT INTO queue(name) 
    values ($1) RETURNING id;
"""


async def get_queue(request, queue_name):
    return await request.app['conn'].fetchrow(
        SELECT_QUEUE,
        queue_name,
    )


async def create_queue(request, queue_name):
    return await request.app['conn'].fetchrow(
        INSERT_QUEUE,
        queue_name,
    )


async def get_or_create_queue(request, queue_name):
    queue = await get_queue(request, queue_name)
    if queue:
        return queue['id']
    queue = await create_queue(request, queue_name)
    return queue['id']


async def create_task(request, queue_id, **kwargs):
    return await request.app['conn'].fetchrow(
        INSERT_TASK,
        datetime.now(),
        json.dumps(kwargs),
        queue_id,
    )


async def get_or_create_task(request, **data):
    queue = await get_queue(request, data['queue'])
    if not queue:
        return None, 'Queue not exist'
    task = await create_task(request, queue['id'], **data['kwargs'])
    return task['id'], None
