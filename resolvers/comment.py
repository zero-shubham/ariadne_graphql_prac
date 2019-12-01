from resolvers.user import query, mutation
from ariadne import ObjectType
from models.comment import CommentModel

Comment = ObjectType("Comment")


@query.field("comment")
def resolve_post(_, info, comment_id):
    comment = CommentModel.find_by_id(comment_id)
    return comment


@mutation.field("create_comment")
def resolve_create_comment(_, info, user_id, post_id, text):
    comment = CommentModel(user_id=user_id, post_id=post_id, text=text)
    comment.save_to_db()
    return comment


@mutation.field("update_comment")
def resolve_update_comment(_, info, comment_id, text):
    comment = CommentModel.find_by_id(comment_id)
    comment.text = text
    comment.save_to_db()
    return comment


@mutation.field("delete_comment")
def resolve_delete_comment(_,info, comment_id):
    comment = CommentModel.find_by_id(comment_id)
    if comment:
        comment.delete_from_db()
    return comment


@Comment.field("user")
def resolve_user(root, info):
    return root.user


@Comment.field("post")
def resolve_post(root, info):
    return root.post