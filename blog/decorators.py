#登陆限制函数-装饰器
from functools import wraps
from flask import session, url_for, redirect

def login_required(func):
    @wraps(func)
    def warpper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return warpper