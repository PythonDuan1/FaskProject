## 数据库的配置信息
HOSTNAME = "127.0.0.1"
PORT = '3306'
DATABASE = "zhiliaooa_course"
USERNAME = "root"
PASSWORD = "root"

DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

## xhjmsvizgjnubbai qq邮箱授权码
## 邮箱账号：duan_2830@foxmail.com

## 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "duan_2830@foxmail.com"
MAIL_PASSWORD = "xhjmsvizgjnubbai"
MAIL_DEFAULT_SENDER = "duan_2830@foxmail.com"
