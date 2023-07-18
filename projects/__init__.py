from flask import Flask, render_template, request, redirect, session
# 要导入models模型文件，不然无法识别数据表，不会创建
from model import db, models
from flask_migrate import Migrate
from view import index, blog
from werkzeug.security import check_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object('projects.settings')
    app.add_url_rule('/index/', view_func=index.blog_index)
    # 404
    @app.errorhandler(404)
    def err_404(error):
        return render_template('404.html', err_data=error)
    
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if request.method == 'GET':
            if session.get('master'):
                users = models.User.query.all()
                return render_template('admin.html', users=users)
            else:
                return render_template('admin_pwd.html')
        recv_password = request.form.get('master_pwd')
        master_password = app.config['MASTER_PASSWORD']
        if check_password_hash(master_password, recv_password):
            users = models.User.query.all()
            session['master'] = 'True'
            return render_template('admin.html', users=users)
        else:
            return redirect('/')
        
    @app.route('/admin/user', methods=['GET'])
    def admin_user():
        user_id = request.args.get('user_id')
        active = request.args.get('active')
        is_silent = request.args.get('is_silent')
        permission = request.args.get('permission')
        user = models.User.query.get(user_id)
        if active is not None:
            user.active = bool(int(active))
        if is_silent is not None:
            user.is_silent = bool(int(is_silent))
        if permission is not None:
            user.permission = int(permission)
        db.session.commit()
        db.session.close()
        return redirect(request.referrer)
        
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        ##创建表结构
        db.create_all()
    app.register_blueprint(index.index)    
    app.register_blueprint(blog.blog)    
    
    return app