import random
import linked_list
import hash_table
import binary_search_tree
from flask import Flask, request, jsonify
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# app setup
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://mcodex:root@localhost:5432/data_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
now = datetime.now()

# creating User model in flask sqlalchemy
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200)) 
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<BlogPost: {self.title}>"
    

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User Created Successfully!"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_desc():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascen():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()

    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    user = all_users_ll.get_user_by_id(user_id)
    return jsonify(user), 200

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "user does not exists!"}), 400
    
    ht = hash_table.HashTable(10)

    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id")
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "Blog Post Craeted!"}), 200

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id" : post.id,
            "title" : post.title,
            "body" : post.body,
            "user_id" : post.user_id,
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"})

    return jsonify(post)

@app.route("/blog_post/descending_id", methods=["GET"])
def get_all_blog_post():
    blog_posts = BlogPost.query.all()
    all_blogs_ll = linked_list.LinkedList()

    for blog in blog_posts:
        all_blogs_ll.insert_beginning(
            {
            "id" : blog.id,
            "title" : blog.title,
            "body" : blog.body,
            }
        )

    return jsonify(all_blogs_ll.to_list()), 200

@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)