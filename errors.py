from flask import redirect, url_for
from app import app


# 自定义检查登录错误类
class CheckLoginError(Exception):
    pass


# 自定义未知错误
class UnknownError(Exception):
    pass


# 捕捉自定义 登录状态异常
@app.errorhandler(CheckLoginError)
def error_no_login(error):
    return redirect(url_for('login'))


@app.errorhandler(404)
def error_404(error):
    return '找不到页面'


@app.errorhandler(500)
def error_500(error):
    return '服务器去吃饭了，请稍后再试'


@app.errorhandler(UnknownError)
def error_unknown(error):
    return '未知错误\n'


