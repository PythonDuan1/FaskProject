from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"  ## 表名
    ## id 主键 自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ## varchar , null=0字段不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=False)  ## 邮箱唯一，不能同一个邮箱注册多个账号
    join_time = db.Column(db.DateTime, default=datetime.now)  ##加入时间
