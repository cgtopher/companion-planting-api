import pytest


@pytest.fixture(autouse=True)
def prevent_neo4j_calls(monkeypatch):
    monkeypatch.delattr('neo4j.Driver.execute_query', raising=False)
    monkeypatch.delattr('neo4j.Transaction.commit',raising=False)
