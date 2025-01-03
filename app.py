from robyn import Robyn
import database as db

app = Robyn(__file__)


@app.get("/")
def index():
    return f"Hello World!"


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
