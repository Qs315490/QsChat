from sqlmodel import SQLModel, Field

class UsersBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    email: str | None = None

class Users(UsersBase, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)

class UsersUpdate(SQLModel):
    id: int
    username: str | None = None
    password: str | None = None
    email: str | None = None
