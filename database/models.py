from datetime import datetime, timedelta
from enum import IntEnum, IntFlag, auto
from uuid import uuid4

from sqlmodel import Field, SQLModel, UniqueConstraint


class UserStatus(IntEnum):
    "用户状态"

    NORMAL = 0
    "正常"
    BANNED = auto()
    "封禁"


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    "用户名, 不唯一"
    password: str
    "密码, 默认明文。可使用插件添加加密"
    email: str | None = Field(default=None, unique=True, index=True)
    "邮箱, 唯一"
    status: int = Field(default=UserStatus.NORMAL)
    "用户状态"
    created_at: datetime = Field(default_factory=datetime.now)
    "创建时间"
    last_login: datetime | None = Field(default=None)
    "最后登录时间"
    deleted_at: datetime | None = Field(default=None)
    "删除时间"


class UsersUpdate(SQLModel):
    id: int
    name: str | None = None
    "用户名, 不唯一"
    password: str | None = None
    "密码, 默认明文。可使用插件添加加密"
    email: str | None = None
    "邮箱, 唯一"
    status: UserStatus | None = None
    "用户状态"
    last_login: datetime | None = None
    "最后登录时间"
    deleted_at: datetime | None = None
    "删除时间"


class Sessions(SQLModel, table=True):
    "会话"

    uuid: str = Field(primary_key=True, default_factory=uuid4)
    user_id: int = Field(foreign_key="users.id")
    "用户ID"
    created_at: datetime = Field(default_factory=datetime.now)
    "创建时间"
    outdated_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=7)
    )
    "过期时间, 默认7天后过期"


class MessagesType(IntEnum):
    "消息类型"

    TEXT = 0
    "文本"
    IMAGE = auto()
    "图片"
    FILE = auto()
    "文件"


class MessagesStatus(IntFlag):
    "消息状态"

    IS_READ = auto()
    "已读"
    IS_DELETED = auto()
    "已撤回"


class Messages(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    sender_id: int = Field(foreign_key="users.id")
    "发送者ID"
    group_id: int = Field(foreign_key="groups.id")
    "所属会话ID"
    type: MessagesType = Field(default=MessagesType.TEXT)
    "消息类型"
    data: str = Field()
    "消息内容"
    time: datetime = Field(default_factory=datetime.now)
    "发送时间"
    status: MessagesStatus = Field(default=0)
    "消息状态"


class GroupRole(IntFlag):
    "会话角色"

    IS_CREATER = auto()
    "创建者"
    IS_OWNER = auto()
    "拥有者"
    IS_ADMIN = auto()
    "管理员"
    IS_MEMBER = auto()
    "成员"


class Groups(SQLModel, table=True):
    "会话"

    id: int = Field(primary_key=True, default=None)
    name: str = Field()
    "会话名"
    deleted: bool = Field(default=False)
    "是否删除"
    created_at: datetime = Field(default_factory=datetime.now)
    "创建时间"


class GroupsMemBer(SQLModel, table=True):
    "会话成员"

    __tablename__ = "groups_members"  # type: ignore

    session_id: int = Field(foreign_key="groups.id", primary_key=True)
    "会话ID"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    "用户ID"
    role: GroupRole = Field(default=GroupRole.IS_MEMBER)
    "角色"


class FriendsStatus(IntFlag):
    "好友状态"

    IS_A_FRIEND_B = auto()
    "A关注B"
    IS_B_FRIEND_A = auto()
    "B关注A"
    IS_A_BLOCKED_B = auto()
    "A拉黑B"
    IS_B_BLOCKED_A = auto()
    "B拉黑A"


class Friends(SQLModel, table=True):
    "好友"

    __table_args__ = (UniqueConstraint("user_a_id", "user_b_id"),)
    id: int = Field(primary_key=True)
    user_a_id: int = Field(foreign_key="users.id", index=True)
    "用户A"
    user_b_id: int = Field(foreign_key="users.id", index=True)
    "用户B"
    status: FriendsStatus = Field(default=0)
    "状态"
    created_at: datetime = Field(default_factory=datetime.now)
    "创建时间"
