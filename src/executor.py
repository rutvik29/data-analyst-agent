"""SQL executor with error capture."""
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Tuple
import os


class QueryExecutor:
    def __init__(self, database_url: str = None):
        self.db_url = database_url or os.getenv("DATABASE_URL", "sqlite:///./demo.db")
        self.engine = create_engine(self.db_url)

    def run(self, state: dict) -> dict:
        sql = state.get("sql", "")
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql(text(sql), conn)
            return {
                "query_result": df.to_json(orient="records"),
                "error": None,
                "history": [f"[Executor] Returned {len(df)} rows"]
            }
        except Exception as e:
            return {
                "query_result": None,
                "error": str(e),
                "retry_count": state.get("retry_count", 0) + 1,
                "history": [f"[Executor] Error: {e}"]
            }
