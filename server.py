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
    posts = db.relationship("BlogPost")


class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<BlogPost: {self.title}>"
    

@app.route("/user", methods=["POST"])
def create_user():
    pass

@app.route("/user/descending_id", methods=["GET"])
def get_all_users_desc():
    pass


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascen():
    pass


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    pass

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_post(user_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass
    
@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)