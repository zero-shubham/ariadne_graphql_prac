from ariadne import graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from schemas.schema import type_defs
from resolvers.user import query, mutation, User
from resolvers.comment import Comment
from resolvers.post import Post
from flask_jwt_extended import (set_access_cookies,
                                set_refresh_cookies,
                                unset_access_cookies,
                                unset_refresh_cookies)
from db import jwt
from tokens import get_tokens, set_tokens
from blacklist import BLACKLIST

schema = make_executable_schema(type_defs, [query, mutation, Post, User, Comment])

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:zero@localhost/graphql"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config['JWT_CSRF_IN_COOKIES'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE', 'GET']

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = "/"

app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

app.secret_key = "secretive"
jwt.init_app(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()
    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request

    # if the cookie contains "access_token_cookie" and "refresh_token_cookie"
    # set those tokens to tokens global variable
    # this way we can make sure  every has token
    if request.cookies:
        set_tokens(request.cookies)
    try:
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
    except Exception as e:
        return {
            "message": "Something went wrong."
        }, 500
    tokens = get_tokens()
    result = jsonify(result)
    if tokens:
        set_access_cookies(result, tokens["access_token_cookie"])
        set_refresh_cookies(result, tokens["refresh_token_cookie"])
    else:
        unset_access_cookies(result)
        unset_refresh_cookies(result)
    status_code = 200 if success else 400
    return result, status_code


if __name__ == "__main__":
    from db import db


    @app.before_first_request
    def create_tables():
        db.create_all()


    db.init_app(app)
    app.run(debug=True)
