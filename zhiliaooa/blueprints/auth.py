from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash

# url_prefix： 下面的视图函数的url前缀都是/auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


## 访问用户登录页面，url为 "/auth/login"
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data

        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


## 注册
## GET: 从服务器上获取数据
## POST: 将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        ## 验证用户提交的邮箱和验证码是否对应且正确
        ## 表单验证: flask-wtf (依赖于wtforms)
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # return redirect("/auth/login")
            return redirect(url_for("auth.login"))  ## url_for()将视图函数转化为对应的url

        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


## 发送邮箱验证码
## bp.route：如果没有指定methods参数，默认就是GET请求
@bp.route("/captcha/email")
def get_email_captcha():
    ##两种传参方式
    ## 1. /captcha/email/<email>  需要将email作为视图函数参数传入
    ## 2. /captcha/email?email=xxx@qq.com
    ## 访问url: http://127.0.0.1:5000/auth/captcha/email?email=1246579964@qq.com
    email = request.args.get("email")
    # print("email:", email)
    ## 验证码：4 / 6 ：随机数字，字母组合
    source = string.digits * 4
    captcha = random.sample(source, 4)  ## 生成4位数字验证码
    # print("captcha:", captcha, type(captcha))
    captcha = "".join(captcha)  ## list元素拼接成str
    print("captcha----:", captcha, type(captcha))
    ## I/O ：Input/Output 单线程比较耗时(应该交给任务队列，新开一个进程去做，一般用celery-redis)
    message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码为：{captcha}")
    mail.send(message)
    ## 发送完邮箱和验证码后，在服务器端要保留一份数据，注册页面点击注册的时候进行验证
    ## 可以将验证码数据存储在：memcached / redis / 等缓存机制中
    ## 本次讲 用数据库表的方式存储，由于不在内存中存储，所以数据读取较慢
    ## 将邮箱，验证码 提交到数据库中
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    ## 发送验证码应该是个ajax请求，所以要返回json数据(restful api 数据)
    ## {code:200/400/500, message:"", data:{}}
    return jsonify({"code": 200, "message": "", "data": None})


## 测试邮件发送
@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1246579964@qq.com"], body="小墩墩儿天天不知道忙啥呢！哼！！！")
    mail.send(message)
    return "邮件发送成功！！"
