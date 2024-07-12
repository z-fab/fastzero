from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app


def test_read_root_deve_retornar_ok_ola_mundo():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Hello': 'World'}