import sqlite3
from contextlib import contextmanager
from ..core.config import settings

def get_db_connection():
    """
    Crea una conexión a la base de datos SQLite.
    Se utiliza row_factory = sqlite3.Row para acceder a las columnas por nombre.
    """
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def db_session():
    """Context manager para manejar la sesión de base de datos y asegurar el cierre."""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
