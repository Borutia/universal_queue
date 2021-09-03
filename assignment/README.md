## Реализовать универсальную очередь задач, используя блокировки PostgreSQL.

#### Что нужно сделать
1) Спроектировать базу данных.
2) Сервис, предоставляющий REST API обработчик для добавления задач в очередь. Параметры каждой задачи могут быть любыми (**kwargs), результат может быть представлен любым типом данных.
3) Воркер, получающий одну свободную задачу из PostgreSQL, выполняющий работу и записывающий результат в базу данных.

#### О чем стоит подумать
1) Может быть запущено много инстансов воркеров. Важно, чтобы одну задачу мог взять только один обработчик.
2) Бывают "зависающие" задачи, которые необходимо каким-то образом обрабатывать.
3) Помещенная в очередь задача должна гарантированно выполниться, даже в случае сбоя конкретного инстанса воркера.

#### Желаемый интерфейс создания задач
```
# Запрос
POST /tasks
{
	"queue": "example",
	"kwargs": {
		"param1": 1,
		"param2": 2
	}
}

# Ответ
HTTP/1.1 201 Created
{
    "task_id": 1
}
```

#### Желаемый интерфейс воркера
```python
import asyncio
import random
from typing import Callable, Awaitable


async def consume(queue: str, handler: Callable[..., Awaitable[None]]):
    ...


async def example_queue_handler(param1: int, param2: int):
    await asyncio.sleep(random.uniform(0.5, 3.))
    return param1 + param2


loop = asyncio.get_event_loop()
loop.create_task(consume("example", example_queue_handler))
loop.run_forever()
```
