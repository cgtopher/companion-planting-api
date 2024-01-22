import os

import neo4j
from neo4j import GraphDatabase, Driver, Session, Transaction
from pandas import DataFrame

from migrations import MIGRATIONS

connection = os.environ.get('NEO4J_URL') or "bolt://localhost:7687"
username = os.environ.get('NEO4J_USERNAME') or ""
password = os.environ.get('NEO4J_PASSWORD') or ""


class Neo4JDriverManager:
    def __init__(self):
        self._driver = None

    def execute_query(self, query) -> DataFrame:
        with self._get_driver().session() as _:
            result = self._get_driver().execute_query(query, result_transformer_=neo4j.Result.to_df)
        return result

    def close(self):
        self._driver.close()

    def get_transaction(self) -> Transaction:
        return self._get_session().begin_transaction()

    def _get_session(self) -> Session:
        return self._get_driver().session()
    def _get_driver(self) -> Driver:
        if self._driver is not None:
            self._driver.verify_connectivity()
            return self._driver
        else:
            return self._init_driver()

    def _init_driver(self) -> Driver:
        self._driver = GraphDatabase.driver(connection, auth=(username, password))
        self._driver.verify_connectivity()
        self._run_migrations()
        return self._driver

    def _run_migrations(self) -> None:
        for migration in MIGRATIONS:
            transaction = self.get_transaction()
            try:
                transaction.run(migration)
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e
