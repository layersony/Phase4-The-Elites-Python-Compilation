from flask_sqlalchemy import SQLAlchemy

# initialize
db = SQLAlchemy()

# models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(1000), nullable=False)
    ptime = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    comments = db.relationship('Comment', back_populates='post')

    # correction
    user = db.relationship('User', back_populates='posts')

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # error correction
    post = db.relationship('Post', back_populates='comments')
    user = db.relationship('User', back_populates='comments')