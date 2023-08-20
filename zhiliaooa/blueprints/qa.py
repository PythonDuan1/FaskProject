from flask import Blueprint

## 问答页面就是首页，所以url_prefix="/" 根路由
bp = Blueprint("qa", __name__, url_prefix="/")

## 首页  http://127.0.0.1:5000
@bp.route("/")
def index():
    pass