from flask import Flask, request, render_template
from datetime import datetime

## __name__:代表当前app.py这个模块
##1.以后出现bug,可以帮助快速定位
##2.对于寻找模板文件，有一个相对路径
app = Flask(__name__)


## 自定义过滤器
def datetime_format(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)


## 添加过滤器
app.add_template_filter(datetime_format, "dformat")


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


## 创建一个路由和视图函数的映射
@app.route('/')
def hello_world():
    # return "修改主机ip，使得其他电脑也可以访问到本机的flask项目 !"
    # return render_template("index.html")
    ## 模板文件中传入对象的属性
    user = User("萝北", "xx@qq.com")
    person = {
        "username": "张三",
        "email": "zhangsan@qq.com"
    }
    return render_template("index.html", user=user, person=person)


@app.route("/profile")
def profile():
    return "--个人中心--"


@app.route("/blog/list")
def blog_list():
    return "欢迎来到博客列表页面!"


# ## 带参数的url
# @app.route("/blog/<blog_id>")
# def blog_detail(blog_id):
#     return "您当前访问的博客是 %s 页" % blog_id

# ## 带参数的url,定义参数类型 blog_id为int类型
# @app.route("/blog/<int:blog_id>")
# def blog_detail(blog_id):
#     return "您当前访问的博客是 %s 页" % blog_id

## 模板传参（将参数传递给html文件中）
@app.route("/blog/<blog_id>")
def blog_detail(blog_id):
    return render_template("blog_detail.html", b_id=blog_id, username="萝北")


## 查询字符串的方式传参
## /book/list  会返回第一页数据
## /book/list?page=2  获取第2页数据
@app.route("/book/list")
def book_list():
    ## request.args  类字典类型
    page = request.args.get("page", default=1, type=int)
    return f"当前访问的是{page}页！"


## 过滤器的使用（给模板传参前将参数进行处理）
## 管道符 |
@app.route("/filter")
def filter_demo():
    user = User("萝北和小宝贝", "xx@qq.com")
    ## 内置过滤器
    ## 自定义过滤器  过滤器名：dformat
    mytime = datetime.now()
    # print("mytime:", mytime)
    return render_template("filter.html", user=user, mytime=mytime)


## 控制语句
@app.route("/control")
def control_statement():
    age = 18
    books = [
        {"name": "三国演义", "author": "罗贯中"},
        {"name": "水浒传", "author": "施耐庵"}
    ]
    return render_template("control.html", age=age, books=books)

## 模板继承
@app.route("/child1")
def child1():
    return  render_template("child1.html")

@app.route("/child2")
def child2():
    return  render_template("child2.html")

## 加载静态文件
@app.route("/static")
def static_demo():
    return  render_template("static.html")


if __name__ == '__main__':
    # app.run()
    # app.run(debug=True)  ## 开启debug模式
    app.run(debug=True, host="0.0.0.0", port=8001)  ## 修改主机和端口
