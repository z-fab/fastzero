import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.app import app
from src.controller.database import get_session
from src.model.orm.user import User, table_registry


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    def fake_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = fake_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
