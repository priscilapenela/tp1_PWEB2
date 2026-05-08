import sqlite3

DB_NAME = "heladitos.db"

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    
    productos_iniciales = [
    (1, "Ice Cream Vanilla", 1500),
    (2, "Ice Cream Strawberry", 2000),
    (3, "Ice Cream Blueberry", 2200),
    (4, "Ice Cream Chocolate", 1800)
    ]

    cursor.executemany("""
          INSERT OR IGNORE INTO productos (id, nombre, precio)
          VALUES (?, ?, ?)
     """, productos_iniciales)

    connection.commit()
    connection.close()