type_defs = """
    type User {
        id: ID!
        username: String!
        name: String!
        posts: [Post]
        comments: [Comment]
    }
    type Post {
        id: ID!
        text: String!
        user: User!
        comments: [Comment]
    }
    type Comment {
        id: ID!
        text: String!
        post: Post!
        user: User!
    }
    type Query {
        hello: String!
        user(username: String!): User!
        users(usernames: [String!]!): [User]!
    }
    type Mutation {
        create_user(name: String! username: String! password: String!): User
        create_post(user_id: ID! text: String!): Post
        create_comment(user_id: ID! post_id: ID! text: String!): Comment
    }
"""
