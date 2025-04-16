from robyn import Robyn

import database as db
import routers

db.create_db_and_tables()

app = Robyn(__file__)


@app.get("/")
def index():
    return {"msg": "Hello World"}


app.include_router(routers.user_router)


@app.exception
def handle_exception(error: Exception):
    """异常处理"""
    return {"message": str(error)}, 500


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
