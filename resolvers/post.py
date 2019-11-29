from resolvers.user import query, mutation
from ariadne import ObjectType
from models.post import PostModel

Post = ObjectType("Post")


@query.field("post")
def resolve_post(_, info, post_id):
    post = PostModel.find_by_id(post_id)
    return post


@mutation.field("create_post")
def resolve_create_post(_, info, user_id, text):
    post = PostModel(user_id=user_id, text=text)
    post.save_to_db()
    return post


@mutation.field("update_post")
def resolve_update_post(_, info, post_id, text):
    post = PostModel.find_by_id(post_id)
    post.text = text
    post.save_to_db()
    return post


@Post.field('user')
def resolve_user(root, info):
    return root.user


@Post.field("comments")
def resolve_comments(root, info):
    return root.comments