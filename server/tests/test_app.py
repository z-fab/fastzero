from http import HTTPStatus

from src.model.schemas.user import UserPublicSchema


def test_read_root_deve_retornar_ok_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'Alice', 'email': 'alice@exemple.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Alice',
        'email': 'alice@exemple.com',
        'id': 1,
    }


def test_read_users_without_data(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_data(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={'username': 'User 2', 'email': 'teste@teste.com', 'password': '123456'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'User 2',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/100',
        json={'username': 'User 2', 'email': 'teste@teste.com', 'password': '123456'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_user(client, user):
    response = client.get('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/user/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
