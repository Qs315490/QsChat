from datetime import datetime

from sqlmodel import select

from database import models
from database.db import get_db_sessions
from utils import exception as err


def add_user(user: models.Users):
    """添加用户
    Args:
        user (models.Users): 用户信息
    Returns:
        models.Users: 添加后的用户信息
    Raises:
        err.UserAlreadyExists: 用户已存在
    """
    if user.email is not None:
        try:
            _ = get_user(email=user.email)
            raise err.UserAlreadyExists
        except err.UserNotFound:
            pass

    with get_db_sessions() as sessions:
        sessions.add(user)
        sessions.commit()
        sessions.refresh(user)
    return user


def del_user(user_id: int):
    """删除用户
    Args:
        user_id (int): 用户id
    Returns:
        models.Users: 删除后的用户信息
    Raises:
        err.UserNotFound: 用户不存在
    """
    user = get_user(user_id)
    with get_db_sessions() as sessions:
        user.status = models.UserStatus.BANNED.value
        user.deleted_at = datetime.now()
        sessions.add(user)
        sessions.commit()
        sessions.refresh(user)
    return user


def edit_user(user: models.UsersUpdate):
    """编辑用户信息
    Args:
        user (models.UsersUpdate): 要更新的用户信息
    Returns:
        models.Users: 更改后的用户信息
    Raises:
        err.UserNotFound: 用户不存在
    """
    back = get_user(user.id)
    tmp = back.sqlmodel_update(user.model_dump(exclude_unset=True))
    with get_db_sessions() as sessions:
        sessions.add(tmp)
        sessions.commit()
        sessions.refresh(tmp)
    return tmp


def get_user(user_id: int | None = None, email: str | None = None):
    """获取用户信息
    Args:
        user_id (int | None, optional): 用户id. Defaults to None.
        email (str | None, optional): 用户邮箱. Defaults to None.
    Returns:
        models.Users: 用户
    Raises:
        err.UserNotFound: 用户不存在
    """
    if user_id is None and email is None:
        raise err.UserNotFound
    with get_db_sessions() as sessions:
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
    """添加session
    Args:
        session (models.Sessions): session
    Returns:
        models.Sessions: session
    Raises:
        err.SessionAlreadyExists: session已存在
    """
    try:
        _ = get_session(session.uuid)
        raise err.SessionAlreadyExists
    except err.SessionNotFound:
        pass
    with get_db_sessions() as sessions:
        sessions.add(session)
        sessions.commit()
        sessions.refresh(session)
    return session


def get_session(session_id: str):
    """获取session
    Args:
        session_id (str): session id
    Returns:
        models.Sessions: session
    Raises:
        err.SessionNotFound: session不存在
    """
    with get_db_sessions() as sessions:
        session = sessions.get(models.Sessions, session_id)
        if session is None:
            raise err.SessionNotFound
    return session


def session_is_outdated(session_id: str) -> bool:
    """session是否过期
    Args:
        session_id (str): session id
    Returns:
        bool: 过期返回True, 未过期返回False
    Raises:
        err.SessionNotFound: session不存在
    """
    session = get_session(session_id)
    if datetime.now() > session.outdated_at:
        return True
    return False
