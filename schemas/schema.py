type_defs = """
    input CreateUserInput {
        name: String!
        username: String!
        password: String!
    }
    input UpdateUserInput {
        user_id: ID!
        username: String
        password: String
        name: String
    }
    input DeleteUserInput {
        user_id: ID
        username: String
    }
    type Login {
        csrf: String!
        refresh_csrf: String!
        user: User!
    }
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
        user(username: String user_id: ID): User
        users(usernames: [String!]!): [User]!
        post(post_id: ID): Post
        comment(comment_id: ID): Comment
    }
    type Mutation {
        create_user(data: CreateUserInput!): User
        create_post(user_id: ID! text: String!): Post
        create_comment(user_id: ID! post_id: ID! text: String!): Comment
        update_user(data: UpdateUserInput!): User
        update_post(post_id: ID! text: String!): Post
        update_comment(comment_id: ID! text: String!): Comment
        delete_user(data: DeleteUserInput): User
        delete_comment(comment_id: ID!): Comment
        delete_post(post_id:  ID!): Post
        login(username: String! password: String!): Login
    }
"""
