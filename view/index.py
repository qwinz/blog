from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model.models import User, Blog, Category
from model import db
from werkzeug.security import generate_password_hash, check_password_hash

index = Blueprint('index', __name__, template_folder='../templates', static_folder='../static', static_url_path='')

@index.route('/')
def blog_index_red():
    return redirect(url_for('index.index'))

@index.route('/index', endpoint='index')
def blog_index():
    blog_all = Blog.query.filter(Blog.active==True).all()
    return render_template('index.html', blog_all=blog_all)

# 登录请求
@index.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first();
        if not user:
            flash('用户名不存在')
            return redirect(url_for('index.login'))
        if user.check_password(user.password, password):
            session.clear()
            session['username'] = user.username
            session.permanent = True
            return redirect(url_for('index.index'))
        else:
            flash('密码错误')
            return redirect(url_for('index.login'))

@index.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        sql_username = User.query.filter_by(username=username).first()
        if username == sql_username:
            flash('改用户名已被注册')
            return redirect(url_for('index.register'))
        if password != password_confirm:
            flash('两次密码不一致')
            return redirect(url_for('index.register'))
        
        # password = generate_password_hash(password)
        new_user = User(username=username, password=password, name=username)
        # new_user.sef_password_hash()
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        session.clear()
        session['username'] = username
        session.permanent = True
        return redirect(url_for('index.index'))

@index.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.index'))
 
@index.route('/updatePwd')
def updatePwd():
    return render_template('update_pwd.html')

@index.route('/category', methods=['GET', 'POST'])
def category():
    if session['username'] !='qwinz':
        return redirect(url_for('/'))
    if request.method == 'GET':
        category_list = Category.query.all()
        return render_template('category.html', category_list=category_list)
    if request.method == 'POST':
        category_name = request.form['category_name']
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        db.session.close()
        return redirect(url_for('index.category'))

@index.route('/del_category/<int:category_id>')
def del_category(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    db.session.close()
    return redirect(url_for('index.category'))
