from pytest import mark, raises

from database import db, models, crud
import utils.exception as err

db.drop_db_and_tables()

@mark.user
def test_add_user():
    user = models.Users(name="test", password="1234", email="test@test.com")
    crud.add_user(user)
    assert user.id is not None
    # 重复添加
    with raises(err.UserAlreadyExists):
        crud.add_user(user)
    # 添加第二个用户
    back = crud.add_user(models.Users(name="test1", password="2234"))
    assert back.id == 2

@mark.user
def test_get_user():
    back = crud.get_user(1)
    assert back.id == 1
    # 获取不存在的用户
    with raises(err.UserNotFound):
        back = crud.get_user(999)

@mark.user
def test_edit_user():
    back = crud.edit_user(models.UsersUpdate(id=1, name="test_user"))
    assert back.id == 1
    assert back.name == "test_user"
    assert back.password == "1234"
    # 修改不存在的用户
    with raises(err.UserNotFound):
        back = crud.edit_user(models.UsersUpdate(id=999, name="test_user1"))

@mark.user
def test_del_user():
    crud.del_user(1)
    user = crud.get_user(1)
    assert user.status == models.UserStatus.BANNED
    # 删除不存在的用户
    with raises(err.UserNotFound):
        crud.del_user(0)
