from tools import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(11),nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DATETIME,default=datetime.now)

    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('comments'))

    question_id = db.Column(db.INTEGER, db.ForeignKey('question.id'))
    question = db.relationship('Question', backref=db.backref('comments'))
