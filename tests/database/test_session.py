from pytest import mark, raises

import utils.exception as err
from database import crud, db, models

db.drop_db_and_tables()


@mark.session
def test_add_session():
    session = models.Sessions(
        uuid="123",
        user_id=1,
    )
    crud.add_session(session)
    assert session.outdated_at is not None


@mark.session
def test_get_session():
    session = crud.get_session("123")
    assert isinstance(session, models.Sessions)
    with raises(err.SessionNotFound):
        crud.get_session("456")
