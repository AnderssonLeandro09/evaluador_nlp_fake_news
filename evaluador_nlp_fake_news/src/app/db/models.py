from .database import db_session

def init_db():
    """
    Crea la tabla de resultados de evaluación si no existe.
    Se basa en el diseño de PSM definido en el MDA.
    """
    with db_session() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                label INTEGER,
                beto_prediction INTEGER NOT NULL,
                mbert_prediction INTEGER NOT NULL,
                beto_time_ms REAL NOT NULL,
                mbert_time_ms REAL NOT NULL,
                beto_accuracy REAL NOT NULL,
                mbert_accuracy REAL NOT NULL,
                beto_precision REAL NOT NULL,
                mbert_precision REAL NOT NULL,
                beto_recall REAL NOT NULL,
                mbert_recall REAL NOT NULL,
                beto_f1_score REAL NOT NULL,
                mbert_f1_score REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
