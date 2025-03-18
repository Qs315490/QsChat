from pytest import raises, mark
import database 
import utils.exception as err

database.drop_db_and_tables()

@mark.user
def test_add_user():
    user = database.Users(name="test", password="1234", email="test@test.com")
    database.add_user(user)
    assert user.id is not None
    # 重复添加
    with raises(err.UserAlreadyExists):
        database.add_user(user)
    # 添加第二个用户
    back = database.add_user(database.Users(name="test1", password="2234"))
    assert back.id == 2

@mark.user
def test_get_user():
    back = database.get_user(1)
    assert back.id == 1
    # 获取不存在的用户
    with raises(err.UserNotFound):
        back = database.get_user(999)

@mark.user
def test_edit_user():
    back = database.edit_user(database.UsersUpdate(id=1, name="test_user"))
    assert back.id == 1
    assert back.name == "test_user"
    assert back.password == "1234"
    # 修改不存在的用户
    with raises(err.UserNotFound):
        back = database.edit_user(database.UsersUpdate(id=999, name="test_user1"))

@mark.user
def test_del_user():
    database.del_user(1)
    user = database.get_user(1)
    assert user.status == database.models.UserStatus.BANNED
    # 删除不存在的用户
    with raises(err.UserNotFound):
        database.del_user(0)
