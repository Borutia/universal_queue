## Универсальная очередь задач, используя блокировки PostgreSQL.

### Зависимости

Зависимости для проекта описаны в файле requirements.txt

### Установка
1)Склонировать репозиторий с приложением в домашнюю директорию
```
git clone https://github.com/Borutia/homework2.git
```
2)Создать базу данных для приложения и его тестирования
```
sudo su -c "sh database/create_db.sh" postgres
```
3)Создать виртуальное окружение
```
python3 -m venv venv
```
4)Активировать виртуальное окружение
```
source ./venv/bin/activate
```
5)Установить зависимости для приложения
```
pip install -r requirements.txt
```
6)Применить миграции к базе данных PostgreSQL
```
python3 database/schema.py
```
7)Запуск setup
```
python3 setup install
```

### Использование
#### Запуск сервера
```
python3 -m aiohttp.web -H localhost -P 8080 server.api:setup_app
```
API
```
# Cоздание queue
POST /queue
{
	"queue": "example"
}

# Ответ
HTTP/1.1 201 Created
{
    "queue_id": 1
}
```
```
# Cоздание task
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

#### Запуск воркера 
Не обязательные параметры
1) название очереди --queue. Default queue: common
2) количество воркеров --count. Default count: 1
```
python3 worker/worker.py --queue example --count 2
```

#### Запуск тестов
TODO: add tests
```
pytest tests
```
