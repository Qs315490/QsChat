
class UserNotFound(Exception):
    "用户不存在"
    def __init__(self):
        super().__init__("用户不存在")

class UserAlreadyExists(Exception):
    "用户已存在"
    def __init__(self):
        super().__init__("用户已存在")