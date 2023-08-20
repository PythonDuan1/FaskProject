from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "database_learn"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


## ORM模型映射成表三部曲(终端terminal输入)
# 1.flask db init ## 这步只需要执行一次(下次更新表，不用再执行，初始化后生成migrations文件夹后就不用再初始化了)
# 2.flask db migrate  ## 识别ORM模型的改变，生成迁移脚本
# 3.flask db upgrade  ## 运行迁移脚本，同步到数据库中


# ## 测试数据库是否连接成功
# with app.app_context():
#     with db.engine.connect() as conn:
#         # rs = conn.execute("select 1")   ## 语法错误
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())  ##(1,) 代表连接成功

## ORM模型
## 一个类对应一个表，一个类属性对应一个表字段，这个类的每个对象对应表的每行数据
## 用户表
class User(db.Model):
    __tablename__ = "user"  ## 表名
    ## id 主键 自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ## varchar , null=0字段不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    ## 新增email字段
    email = db.Column(db.String(100))
    ## 新增字段
    signature = db.Column(db.String(100))

    # articles = db.relationship("Article", back_populates="author")


# user = User(username="张三", password="111")
## sql: insert user(username,password) values("张三","111")


## 外键关联
## 文章表
class Article(db.Model):
    __tablename__ = "article"  ## 表名
    ## id 主键 自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    ## 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ##  "User" 相当于 article.author = User.query.get(article.author_id)
    ## back_populates 反向引用，User对象可以通过articles找到所有与之相关的Article对象, 需要在User对象中也写一个articles属性与之对应
    # author = db.relationship("User", back_populates="articles")
    ## backref 这样写，不用再User对象中手动创建articels属性，会自动的给User模型添加一个articles属性，用来获取文章列表
    author = db.relationship("User", backref="articles")


# article = Article(title="flask学习", content="flaskxxxxx")
# article.author_id = user.id
# user = User.query.get(article.author_id)
# print(article.author)


## 将所有的表映射到数据库中(有很大局限性，如果在原有表中新增字段，那么这个操作并不能使数据库的表中新增字段)
## 所以实战一般不用这种方式进行映射，而是使用flask-migrate
# with app.app_context():  ## app应用上下文
#     db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


##增加数据
@app.route("/user/add")
def add_user():
    ## 1.创建ORM对象
    user = User(username="张三", password="111")
    ## 2.将ORM对象添加到db.session中
    db.session.add(user)
    ## 3.将db.session中的改变同步到数据库中
    db.session.commit()
    return "用户创建成功！！"


## 查询
@app.route("/user/query")
def query_user():
    ## 1.get查找，根据主键查找
    # user=User.query.get(5)
    # print(f"{user.id}:{user.username}--{user.password}")
    ## 2.filter_by查找（可查找多条）,返回一个 Query 类列表对象
    users = User.query.filter_by(username="张三")
    print(type(users))
    for user in users:
        print(f"用户名:{user.username}")
    return "数据查询成功！！"


## 修改
@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="张三").first()  ## 返回第一个user对象
    user.password = "222"
    db.session.commit()
    return "数据修改好了！！！"


## 删除
@app.route("/user/delete")
def delete_user():
    ##1.查找要删除的数据
    user = User.query.get(5)
    ##2.从db.session中删除
    db.session.delete(user)
    ##3.将db.session中的修改，同步到数据库中
    db.session.commit()
    return "数据删除了！"


## 增加文章到user作者
@app.route("/article/add")
def article_add():
    ## 添加两篇文章到同一个作者
    article1 = Article(title="flask学习", content="flaskxxxxx")
    article1.author = User.query.get(6)

    article2 = Article(title="django学习", content="djangoxxxxx")
    article2.author = User.query.get(6)

    ## 添加到session中
    db.session.add_all([article1, article2])
    ## 同步session中的数据到数据库中
    db.session.commit()

    return "文章添加成功！！"


## 查询文章
## 查询某个作者的所有文章
@app.route("/article/query")
def query_article():
    user = User.query.get(6)  ##查询主键id为6的作者
    for article in user.articles:
        print(f"user的id为 {6}的文章标题: {article.title}")
    return "查找文章成功！！！"


if __name__ == '__main__':
    app.run()
