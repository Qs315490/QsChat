from sqlmodel import select
from database import models
from database.db import get_session
from utils import exception as err


def add_user(user: models.users):
    if user.email is not None:
        try:
            _ = get_user(email=user.email)
            raise err.UserAlreadyExists()
        except err.UserNotFound:
            ...

    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def del_user(user_id: int):
    back = get_user(user_id)
    with get_session() as session:
        session.delete(back)
        session.commit()


def edit_user(user: models.usersUpdate):
    back = get_user(user.id)
    tmp = back.sqlmodel_update(user.model_dump(exclude_unset=True))
    with get_session() as session:
        session.add(tmp)
        session.commit()
        session.refresh(tmp)
    return tmp


def get_user(user_id: int | None = None, email: str | None = None):
    if user_id is None and email is None:
        raise err.UserNotFound()
    with get_session() as session:
        back = None
        if user_id is not None:
            back = session.get(models.users, user_id)
        elif email is not None:
            statement = select(models.users).where(models.users.email == email)
            back = session.exec(statement).one_or_none()
        if back is None:
            raise err.UserNotFound()
        return back
