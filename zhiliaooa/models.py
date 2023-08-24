from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"  ## 表名
    ## id 主键 自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ## varchar , null=0字段不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=False)  ## 邮箱唯一，不能同一个邮箱注册多个账号
    join_time = db.Column(db.DateTime, default=datetime.now)  ##加入时间


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    # used = db.Column(db.Boolean, default=False)  ## 验证码是否已经被使用过，使用过的话就可以删除
