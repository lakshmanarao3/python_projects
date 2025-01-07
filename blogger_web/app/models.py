from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for likes
likes = db.Table(
    "likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default="default.jpg")
    password = db.Column(db.String(256), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    liked_posts = db.relationship(
        "Post", secondary=likes, backref=db.backref("liked_by", lazy="dynamic")
    )
    notifications = db.relationship("Notification", backref="user", lazy="dynamic")
    is_admin = db.Column(db.Boolean, default=False)

    @staticmethod
    def initialize_first_user():
        """Ensures the first registered user is marked as admin."""
        if User.query.count() == 0:
            return True
        return False

    @classmethod
    def get_all_users(cls):
        """Fetch all users for admin dashboard."""
        return cls.query.order_by(cls.username).all()

    @classmethod
    def delete_user(cls, user_id):
        """Delete a user and associated data."""
        user = cls.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tags = db.relationship("Tag", secondary="post_tags", backref="posts")
    @classmethod
    def get_all_posts(cls):
        """Fetch all posts for admin dashboard."""
        return cls.query.order_by(cls.date_posted.desc()).all()

    @classmethod
    def delete_post(cls, post_id):
        """Delete a post and its associated data."""
        post = cls.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        return False
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    children = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic"
    )

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    @staticmethod
    def create_notification(user_id, message):
        """Create a new notification."""
        notification = Notification(user_id=user_id, message=message)
        db.session.add(notification)
        db.session.commit()
