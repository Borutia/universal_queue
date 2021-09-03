import asyncpg
from aiohttp import web

from tools.const import CONNECTION_STRING
from tools.utils import get_or_create_queue, get_or_create_task


async def add_queue(request):
    """Добавление очереди"""
    try:
        data = await request.json()
        queue_id = await get_or_create_queue(request, data['queue'])
        return web.json_response(
            {
                'queue_id': queue_id
            },
            status=201,
        )
    except Exception as e:
        return web.Response(
            text='Bad params',
            status=400,
        )


async def add_task(request):
    """Добавление таска(задача)"""
    try:
        data = await request.json()
        task_id, error = await get_or_create_task(
            request,
            **data,
        )
        if error:
            return web.json_response(
                {'Error': error},
                status=400,
            )
        return web.json_response(
            {
                'task_id': task_id
            },
            status=201,
        )
    except Exception as e:
        return web.Response(
            text='Bad params',
            status=400,
        )


def setup_routes(app):
    app.add_routes(
        [
            web.post('/queue', add_queue),
            web.post('/tasks', add_task),
        ]
    )


async def create_connect(app):
    app['conn'] = await asyncpg.connect(CONNECTION_STRING)


def setup_app(args=None):
    app = web.Application()
    app.on_startup.append(create_connect)
    setup_routes(app)
    return app


if __name__ == '__main__':
    app = setup_app()
    web.run_app(app)
