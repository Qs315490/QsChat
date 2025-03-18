from database.db import create_db_and_tables, drop_db_and_tables  # noqa: F401
from database.models import *  # noqa: F403
from database.crud import *  # noqa: F403

create_db_and_tables()
