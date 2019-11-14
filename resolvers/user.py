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
def resolve_user(_, info, **kwargs):
    user_id = kwargs.get("user_id", None)
    username = kwargs.get("username", None)
    user = None
    print(user_id, username, "===", info, kwargs)
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


@query.field("post")
def resolve_post(_, info, post_id):
    post = PostModel.find_by_id(post_id)
    return post


@query.field("comment")
def resolve_post(_, info, comment_id):
    comment = CommentModel.find_by_id(comment_id)
    return comment


@mutation.field("create_user")
def resolve_create_user(_, info, name, username, password):
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


@Post.field('user')
def resolve_user(root, info):
    user = UserModel.find_by_id(root.user_id)
    return user


@Post.field("comments")
def resolve_comments(root, info):
    return root.comments


@User.field("posts")
def resolve_posts(root, info):
    return root.posts


@User.field("comments")
def resolve_comments(root, info):
    return root.comments


@Comment.field("user")
def resolve_user(root, info):
    return UserModel.find_by_id(root.user_id)


@Comment.field("post")
def resolve_post(root, info):
    return PostModel.find_by_id(root.post_id)
