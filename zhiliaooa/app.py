from flask import Flask
import config
from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
## 绑定配置文件
app.config.from_object(config)
## 可以先创建db，再绑定app
db.init_app(app)

## ORM模型映射成表
migrate = Migrate(app, db)

## ORM模型映射成表三部曲(终端terminal输入)
# 1.flask db init ## 这步只需要执行一次(下次更新表，不用再执行，初始化后生成migrations文件夹后就不用再初始化了)
# 2.flask db migrate  ## 识别ORM模型的改变，生成迁移脚本
# 3.flask db upgrade  ## 运行迁移脚本，同步到数据库中


## app绑定蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

## blueprint 蓝图：用来做模块化的
## 比如豆瓣网，有电影、读书、音乐、xx ,每个模块都可以定义成一个蓝图，然后和电影相关的视图函数全部放进电影蓝图中，
## 视图函数全部放到蓝图中

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == '__main__':
    app.run()
