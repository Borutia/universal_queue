SQL_TABLES = """
    CREATE TABLE queue(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    
    CREATE TABLE task(
        id SERIAL PRIMARY KEY,
        create_time TIMESTAMP NOT NULL,
        complete_time TIMESTAMP,
        status INTEGER NOT NULL DEFAULT 0,
        kwargs JSON NOT NULL,
        result JSON,
        queue_id INTEGER NOT NULL,
        FOREIGN KEY(queue_id) REFERENCES queue(id)
    );
"""