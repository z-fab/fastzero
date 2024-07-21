from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from .model.schemas.message import Message
from .model.schemas.user import UserDB, UserList, UserPublicSchema, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def read_user(user_id: int):
    if (user_id < 1) or (user_id > len(database)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND')

    return database[user_id - 1]


@app.put('/users/{user_id}', response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    if (user_id < 1) or (user_id > len(database)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND')

    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if (user_id < 1) or (user_id > len(database)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND')

    del database[user_id - 1]

    return {'message': 'User deleted'}
