from datetime import datetime

from sqlmodel import select

from database import models
from database.db import get_sessions
from utils import exception as err


def add_user(user: models.Users):
    if user.email is not None:
        try:
            _ = get_user(email=user.email)
            raise err.UserAlreadyExists
        except err.UserNotFound:
            pass

    with get_sessions() as sessions:
        sessions.add(user)
        sessions.commit()
        sessions.refresh(user)
    return user


def del_user(user_id: int):
    user = get_user(user_id)
    with get_sessions() as sessions:
        user.status = models.UserStatus.BANNED.value
        user.deleted_at = datetime.now()
        sessions.add(user)
        sessions.commit()
        sessions.refresh(user)
    return user


def edit_user(user: models.UsersUpdate):
    back = get_user(user.id)
    tmp = back.sqlmodel_update(user.model_dump(exclude_unset=True))
    with get_sessions() as sessions:
        sessions.add(tmp)
        sessions.commit()
        sessions.refresh(tmp)
    return tmp


def get_user(user_id: int | None = None, email: str | None = None):
    if user_id is None and email is None:
        raise err.UserNotFound
    with get_sessions() as sessions:
        back = None
        if user_id is not None:
            back = sessions.get(models.Users, user_id)
        elif email is not None:
            statement = select(models.Users).where(models.Users.email == email)
            back = sessions.exec(statement).one_or_none()
        if back is None:
            raise err.UserNotFound
        return back


def add_session(session: models.Sessions):
    try:
        _ = get_session(session.uuid)
        raise err.SessionAlreadyExists
    except err.SessionNotFound:
        pass
    with get_sessions() as sessions:
        sessions.add(session)
        sessions.commit()
        sessions.refresh(session)
    return session


def get_session(session_id: str):
    with get_sessions() as sessions:
        session = sessions.get(models.Sessions, session_id)
        if session is None:
            raise err.SessionNotFound
    return session
