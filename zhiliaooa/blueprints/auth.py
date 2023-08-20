from flask import Blueprint, render_template

# url_prefix： 下面的视图函数的url前缀都是/auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


## 访问用户登录页面，url为 "/auth/login"
@bp.route("/login")
def login():
    pass


## 注册
@bp.route("/register")
def register():
    return render_template("")

