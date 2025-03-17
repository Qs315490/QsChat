from datetime import datetime
from sqlmodel import SQLModel, Field


class users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str | None = None


class usersUpdate(SQLModel):
    id: int
    name: str | None = None
    password: str | None = None
    email: str | None = None


class messages(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    user: int = Field(nullable=False, foreign_key="users.id")
    session: int = Field(nullable=False, foreign_key="sessions.id")
    type: int = Field(default=0)
    data: str = Field(nullable=False)
    time: datetime = Field(default=datetime.now())
    deleted: bool = Field(default=False)

class sessions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    user: int = Field(nullable=False, foreign_key="users.id")
    role: int = Field(default=0)
    active: bool = Field(default=True)

class friends(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    user1: int = Field(nullable=False, foreign_key="users.id")
    user2: int = Field(nullable=False, foreign_key="users.id")
    status: int = Field(default=0)