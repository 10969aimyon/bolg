from flask import Flask, url_for, redirect, g, request, render_template, session
from tools import db
from sqlalchemy import or_
from models import User, Question, Comment
from decorators import login_required
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user:
        g.user = user

@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

@app.route('/')
def index():
    context = {
        "questions":Question.query.all()
    }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            if password == user.password:
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                return '密码错误'
        else:
            return '该用户不存在'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user1 = User.query.filter(or_(User.telephone == telephone, User.username==username)).all()
        if user1:
            return '该用户名/手机号码已被注册'
        elif password2 != password1:
            return '两次输入的密码不一致'
        else:
            user2 = User(username=username, telephone=telephone, password=password1)
            db.session.add(user2)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/loginout/')
def loginout():
    del session['user_id']
    return redirect(url_for('index'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        if content:
            question1 = Question(title=title, content=content)
            user_id = session['user_id']
            user1 = User.query.filter(User.id == user_id).first()
            question1.author = user1
            db.session.add(question1)
            db.session.commit()
        return redirect(url_for('index'))

@app.route('/comment_info/<id>/')
@login_required
def comment_info(id):
    question = Question.query.filter(Question.id == id).first()
    return render_template('comment_info.html', question= question)

@app.route('/put_comment/',methods=['POST'])
def put_comment():
    content = request.form.get('comment')
    if content:
        question_id = request.form.get('question_id')
        question = Question.query.filter(Question.id == question_id).first()
        comment = Comment(content=content)
        user = User.query.filter(User.id==question.author_id).first()
        comment.question=question
        comment.user=user
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('comment_info',id=question_id))

@app.route('/user_info/<id>')
def user_info(id):
    user = User.query.filter(User.id == id).first()
    return render_template('user-info.html', user=user)

@app.route('/change_psw',methods=['POST','GET'])
def change_psw():
    if request.method=='GET':
        return render_template('change_psw.html')
    else:
        ps1 = request.form.get('password1')
        ps2 = request.form.get('password2')
        ps3 = request.form.get('password3')
        if ps1 == g.user.password:
            if ps2 == ps3:
                g.user.password = ps2
                db.session.add(g.user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return '两次输入的密码不一致'
        else:
            return '密码错误'


@app.route('/delete/',methods=['POST'])
def delete():
    comment_id = request.form.get('delete_comment')
    question_id = request.form.get('delete_question')
    comment_demol = Comment.query.filter(Comment.id == comment_id).first()
    question_demol = Question.query.filter(Question.id == question_id).first()
    if comment_demol:
        db.session.delete(comment_demol)
        db.session.commit()
        return redirect(url_for('user_info', id = g.user.id))
    if question_demol:
        for comment in question_demol.comments:
            db.session.delete(comment)
            db.session.commit()

        db.session.delete(question_demol)
        db.session.commit()
        return redirect(url_for('user_info', id = g.user.id))


if __name__ == '__main__':
    app.run(debug=True)
