from flask import Flask, render_template
# 要导入models模型文件，不然无法识别数据表，不会创建
from model import db, models
from flask_migrate import Migrate
from view import index, blog

def create_app():
    app = Flask(__name__)
    app.config.from_object('projects.settings')
    app.add_url_rule('/index/', view_func=index.blog_index)
    # 404
    @app.errorhandler(404)
    def err_404(error):
        return render_template('404.html', err_data=error)
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        ##创建表结构
        db.create_all()
    app.register_blueprint(index.index)    
    app.register_blueprint(blog.blog)    
    
    return app