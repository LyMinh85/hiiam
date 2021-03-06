from app import db
from flask_login import UserMixin


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates='posts')

    comments = db.relationship('Comment', back_populates='post', lazy='dynamic')
    post_likes = db.relationship('LikedPost', back_populates='post', lazy='dynamic')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    posts = db.relationship("Post", back_populates='user', lazy='dynamic')
    comments = db.relationship("Comment", back_populates='user', lazy='dynamic')
    liked_posts = db.relationship('LikedPost', back_populates='user', lazy='dynamic')
    liked_comments = db.relationship('LikedComment', back_populates='user', lazy='dynamic')
    user_messages = db.relationship('Message', back_populates='user', lazy='dynamic')
    read_messages = db.relationship('MessageReadState')
    thread_participants = db.relationship('ThreadParticipant', back_populates='user', lazy='dynamic')

    def like_post(self, post_id):
        like = LikedPost(user_id=self.id, post_id=post_id)
        db.session.add(like)

    def unlike_post(self, post_id):
        LikedPost.query.filter_by(
            user_id=self.id,
            post_id=post_id).delete()

    def has_liked_post(self, post_id):
        return LikedPost.query.filter(
            LikedPost.user_id == self.id,
            LikedPost.post_id == post_id).count() > 0

    def like_comment(self, comment_id):
        like = LikedComment(user_id=self.id, comment_id=comment_id)
        db.session.add(like)

    def unlike_comment(self, comment_id):
        LikedComment.query.filter_by(
            user_id=self.id,
            comment_id=comment_id).delete()

    def has_liked_comment(self, comment_id):
        return LikedComment.query.filter(
            LikedComment.user_id == self.id,
            LikedComment.comment_id == comment_id).count() > 0


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    likes = db.relationship('LikedComment', back_populates='comment', lazy='dynamic')


class LikedPost(db.Model):
    __tablename__ = 'liked_posts'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    post = db.relationship('Post', back_populates='post_likes')
    user = db.relationship('User', back_populates='liked_posts')


class LikedComment(db.Model):
    __tablename__ = 'liked_comments'

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    comment = db.relationship('Comment', back_populates='likes')
    user = db.relationship('User', back_populates='liked_comments')


class Thread(db.Model):
    __tablename__ = 'threads'

    id = db.Column(db.Integer, primary_key=True)

    participants = db.relationship('ThreadParticipant', back_populates='thread')
    thread_messages = db.relationship('Message', back_populates='thread', lazy='dynamic')


class ThreadParticipant(db.Model):
    __tablename__ = 'thread_participants'

    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    thread = db.relationship('Thread', back_populates='participants')
    user = db.relationship('User', back_populates='thread_participants')


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))
    send_date = db.Column(db.DateTime, nullable=False)
    sending_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='user_messages')
    read_state = db.relationship('MessageReadState')
    thread = db.relationship('Thread', back_populates='thread_messages')


class MessageReadState(db.Model):
    __tablename__ = 'messages_read_state'

    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    read_date = db.Column(db.DateTime, nullable=False)

    message = db.relationship('Message')
    user = db.relationship('User')


db.create_all()
