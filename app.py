from robyn import Robyn
import routers
import database as db  # noqa: F401

app = Robyn(__file__)


@app.get("/")
def index():
    return "Hello World!"

app.include_router(routers.user_router)
if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
