from http import HTTPStatus


def test_read_root_deve_retornar_ok_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_creat_user(client):
    response = client.post(
        '/users/',
        json={'username': 'John Doe', 'email': 'teste@teste.com', 'password': '123456'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'John Doe',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'John Doe',
                'email': 'teste@teste.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_user(client):
    test_creat_user(client)
    response = client.get('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'John Doe',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_read_user_not_found(client):
    response = client.get('/user/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'USER NOT FOUND'}
