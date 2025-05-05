from uuid import uuid4
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    password: str

USER_ONE_ID = str(uuid4())
USER_TWO_ID = str(uuid4())

user_one = User(id=USER_ONE_ID, username="admin", password="admin")
user_two = User(id=USER_TWO_ID, username="user", password="user")

STATIC_USERS = [user_one, user_two]

def get_current_user():
    return STATIC_USERS[0]