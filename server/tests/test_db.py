from sqlalchemy import select

from src.model.orm.user import User


def test_create_user(session):
    user = User(username='Fabricio', email='fab@me.com', password='123456')

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'fab@me.com'))

    assert result.username == 'Fabricio'
