# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from main import app
from api.tasks import db
from db.repository import Repository


@pytest.fixture
def mock_session():
    engine = create_engine("postgresql+psycopg2:///:memory:")
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
    session = Session()
    yield Session
    session.close()

@pytest.fixture
def client(mock_session):
    rep = Repository(mock_session)
    rep.session = mock_session
    app.dependency_overrides[db] = lambda: rep
    with TestClient(app) as client:
        yield client
