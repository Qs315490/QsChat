from pytest import raises, mark
from database import *
from utils.exception import *

drop_db_and_tables()

@mark.user
def test_add_user():
    user = Users(id=1, username="test", password="1234")
    add_user(user)
    assert user.id is not None
    # 重复添加
    with raises(UserAlreadyExists):
        add_user(user)
    # 添加第二个用户
    back = add_user(Users(username="test1", password="2234"))
    assert back.id == 2

@mark.user
def test_get_user():
    back = get_user(1)
    assert back.id == 1
    # 获取不存在的用户
    with raises(UserNotFound):
        back = get_user(999)

@mark.user
def test_edit_user():
    back = edit_user(UsersUpdate(id=1, username="test_user"))
    assert back.id == 1
    assert back.username == "test_user"
    assert back.password == "1234"
    # 修改不存在的用户
    with raises(UserNotFound):
        back = edit_user(UsersUpdate(id=999, username="test_user1"))

@mark.user
def test_del_user():
    del_user(1)
    with raises(UserNotFound):
        get_user(1)
    # 删除不存在的用户
    with raises(UserNotFound):
        del_user(0)
