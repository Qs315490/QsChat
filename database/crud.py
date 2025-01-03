from sqlmodel import select
from database.models import *
from database.db import get_session
from utils.exception import *


def add_user(user: Users):
    if user.id is not None:
        try:
            back = get_user(user.id)
            raise UserAlreadyExists()
        except UserNotFound:
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


def edit_user(user: UsersUpdate):
    back = get_user(user.id)
    tmp = back.sqlmodel_update(user.model_dump(exclude_unset=True))
    with get_session() as session:
        session.add(tmp)
        session.commit()
        session.refresh(tmp)
    return tmp


def get_user(user_id: int):
    with get_session() as session:
        back = session.get(Users, user_id)
        if back is None:
            raise UserNotFound()
        return back
