from ariadne import graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from schemas.schema import type_defs
from resolvers.user import query, mutation, User
from resolvers.comment import Comment
from resolvers.post import Post
from flask_jwt_extended import (JWTManager,
                                set_access_cookies,
                                set_refresh_cookies)
from middlewares import get_var

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
jwt = JWTManager(app)


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
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    var = get_var()
    if var:
        result = jsonify(result)
        set_access_cookies(result, var["access_token"])
        set_refresh_cookies(result, var["refresh_token"])
    else:
        result = jsonify(result)
    status_code = 200 if success else 400
    return result, status_code


if __name__ == "__main__":
    from db import db
    @app.before_first_request
    def create_tables():
        db.create_all()
    db.init_app(app)
    app.run(debug=True)
