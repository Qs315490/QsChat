from datetime import datetime
from sqlmodel import select
from database import models
from database.db import get_session
from utils import exception as err


def add_user(user: models.Users):
    if user.email is not None:
        try:
            _ = get_user(email=user.email)
            raise err.UserAlreadyExists()
        except err.UserNotFound:
            pass

    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def del_user(user_id: int):
    user = get_user(user_id)
    with get_session() as session:
        user.status = models.UserStatus.BANNED.value
        user.deleted_at = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def edit_user(user: models.UsersUpdate):
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
            back = session.get(models.Users, user_id)
        elif email is not None:
            statement = select(models.Users).where(models.Users.email == email)
            back = session.exec(statement).one_or_none()
        if back is None:
            raise err.UserNotFound()
        return back
