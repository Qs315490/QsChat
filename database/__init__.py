from database.crud import *
from database.db import create_db_and_tables, drop_db_and_tables  # noqa: F401
from database.models import *

create_db_and_tables()
