from sqlmodel import SQLModel, create_engine, Session

engine = create_engine(
    "sqlite:///database.sqlite3", connect_args={"check_same_thread": False}
)

def get_db_sessions():
    return Session(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    create_db_and_tables()