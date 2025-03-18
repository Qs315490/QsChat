class ErrorMsgFormDocument(Exception):
    def __init__(self):
        super().__init__(self.__doc__)


class UserNotFound(ErrorMsgFormDocument):
    "用户不存在"


class UserAlreadyExists(ErrorMsgFormDocument):
    "用户已存在"


class SessionNotFound(ErrorMsgFormDocument):
    "会话不存在"


class SessionAlreadyExists(ErrorMsgFormDocument):
    "会话已存在"
