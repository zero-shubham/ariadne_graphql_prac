from ariadne import QueryType, MutationType, ObjectType
from models.user import UserModel
from models.comment import CommentModel
from models.post import PostModel

query = QueryType()
mutation = MutationType()
User = ObjectType("User")
Post = ObjectType("Post")
Comment = ObjectType("Comment")


@query.field("user")
def resolve_user(_, info, username):
    user = UserModel.find_by_username(username)
    return user


@query.field("users")
def resolve_users(_, info, usernames):
    users = list()
    for username in usernames:
        users.append(UserModel.find_by_username(username))
    return users


@mutation.field("create_user")
def resolve_create_user(_, info, name, username, password):
    print(name, "=============")
    user = UserModel(name=name, username=username, password=password)
    user.save_to_db()
    return user


@mutation.field("create_post")
def resolve_create_post(_, info, user_id, text):
    post = PostModel(user_id=user_id, text=text)
    post.save_to_db()
    return post


@mutation.field("create_comment")
def resolve_create_comment(_, info, user_id, post_id, text):
    comment = CommentModel(user_id=user_id, post_id=post_id, text=text)
    comment.save_to_db()
    return comment
