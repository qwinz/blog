from model import db, Base
from werkzeug.security import check_password_hash, generate_password_hash

class User(Base):
    # 设置表名
    __tablename__ = 'tb_user';
    # id，主键并自动递增
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(256), nullable=True)
    name = db.Column(db.String(64))
    permission = db.Column(db.Integer, default=3)
    avator = db.Column(db.String(256))


    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
        self.set_password_hash()
    
    def set_password_hash(self):
        self.password = generate_password_hash(self.password)
    
    def check_password(self,hashpwd, password):
        return check_password_hash(hashpwd, password)

class Blog(Base):
    __tablename__ = 'blog'
    title = db.Column(db.String(128))
    text = db.Column(db.TEXT)
    # 分类
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship('Category', backref='category')
    #关联用户id
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.id'))
    user = db.relationship('User', backref='user')

class Comment(Base):
    __tablename__ = 'comment'
    text = db.Column(db.String(256))    # 评论内容
    uuid = db.Column(db.String(256))    #用户未登录时的评论
    # 关联文章id
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))
    # 关联用户id
    user_id = db.Column(db.Integer, db.ForeignKey("tb_user.id"))
    blog = db.relationship("Blog", backref="blog")
    user = db.relationship("User", backref="use")

class Category(Base):
    __tablename__ = 'category'
    name = db.Column(db.String(64), nullable=False, unique=True)