from ariadne import QueryType, MutationType, ObjectType
from models.user import UserModel

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
def resolve_update_user(_, info, data):
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


@User.field("posts")
def resolve_posts(root, info):
    return root.posts


@User.field("comments")
def resolve_comments(root, info):
    return root.comments
