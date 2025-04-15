from pytest import mark, raises

import database
import utils.exception as err

database.drop_db_and_tables()


@mark.session
def test_add_session():
    session = database.Sessions(
        uuid="123",
        user_id=1,
    )
    database.add_session(session)
    assert session.outdated_at is not None


@mark.session
def test_get_session():
    session = database.get_session("123")
    assert isinstance(session, database.Sessions)
    with raises(err.SessionNotFound):
        database.get_session("456")
