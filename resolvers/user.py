from ariadne import QueryType, MutationType, ObjectType
from MyErrors import RequiredAtLeastOne
from models.user import UserModel
from models.post import PostModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    fresh_jwt_required,
    create_access_token,
    create_refresh_token,
    get_csrf_token
)
import datetime
from middlewares import set_var, yo

query = QueryType()
mutation = MutationType()
User = ObjectType("User")


@query.field("user")
def resolve_user(_, info, **kwargs):
    user_id = kwargs.get("user_id", None)
    username = kwargs.get("username", None)
    user = None
    if username:
        user = UserModel.find_by_username(username)
    elif user_id:
        user = UserModel.find_by_id(user_id)
    return user


@query.field("users")
def resolve_users(_, info, usernames):
    users = list()
    for username in usernames:
        users.append(UserModel.find_by_username(username))
    return users


@mutation.field("create_user")
def resolve_create_user(_, info, data):
    user = UserModel(name=data["name"], username=data["username"], password=data["password"])
    user.save_to_db()
    return user


@mutation.field("update_user")
@yo
def resolve_update_user(_, info, data):
    fresh_jwt_required(info[-1])
    user = UserModel.find_by_id(data["user_id"])
    for key in data.keys():
        if key == "password":
            user.password = data[key]
        elif key == "username":
            user.username = data[key]
        elif key == "name":
            user.name = data[key]
    user.save_to_db()
    return user


@mutation.field("delete_user")
def resolve_delete_user(_, info, data):
    if "username" not in data.keys():
        if "user_id" not in data.keys():
            raise RequiredAtLeastOne("Required at least username or user_id.")
        else:
            user = UserModel.find_by_id(data["user_id"])
    else:
        user = UserModel.find_by_username(data["username"])
    if user:
        # need to delete these posts? or cascade handled it?
        posts = PostModel.find_all_by_user_id(user.id)
        user.delete_from_db()
    return user


@mutation.field("login")
def resolve_login(_, info, username, password):
    user = UserModel.find_by_username(username)
    print(user, password)
    if user and check_password_hash(user.password, password):
        expires = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(user.id)
        set_var({"access_token": access_token, "refresh_token": refresh_token})
        return {
            "csrf": get_csrf_token(access_token),
            "refresh_csrf": get_csrf_token(refresh_token),
            "user": user
        }


@User.field("posts")
def resolve_posts(root, info):
    return root.posts


@User.field("comments")
def resolve_comments(root, info):
    return root.comments
