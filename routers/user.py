from robyn import SubRouter

user_router = SubRouter(__name__, prefix="/user")


@user_router.get("/")
def user():
    return {"message": "Hello, User!"}
