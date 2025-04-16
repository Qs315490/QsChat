from robyn import Request, SubRouter

from database import crud, models
from utils import exception
from utils.models import api_result

user_router = SubRouter(__name__, prefix="/user")


@user_router.get("/:user_id")
def user(request: Request):
    """通过user_id获取用户信息
    Args:
        user_id (str): 用户id
    Returns:
        api_result: 返回用户信息
    """
    user_id = request.path_params.get("user_id")
    if user_id is None:
        return api_result(message="User id is required", data={})
    try:
        user_id = int(user_id)
        result = crud.get_user(user_id).model_dump(exclude=("password", "deleted_at"))
    except exception.UserNotFound as e:
        return api_result(message=str(e), data={})
    user_status = result.pop("status")
    if user_status == models.UserStatus.BANNED:
        return api_result(message="User is banned", data={})
    return api_result(message="User found", data=result)
