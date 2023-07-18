from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, current_app
from model.models import User, Blog, Category
from model import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, os, re

index = Blueprint('index', __name__, template_folder='../templates', static_folder='../static', static_url_path='')

def set_session(user):
    session['user_id'] = user.id
    session['user_permission'] = user.permission
    session['user_username'] = user.username
    session['user_name'] = user.name
    # 转义图片路径，可能Linux中有所不同
    session['user_avator_path'] = user.avator
    session.permanent = True

@index.route('/generate_uuid')
def generate_uuid():
    # 生成UUID
    user_uuid = str(uuid.uuid4())
    return user_uuid

@index.route('/')
def blog_index_red():
    return redirect(url_for('index.index'))

@index.route('/index', endpoint='index')
@index.route('/index/<int:category_id>', endpoint='index')
def blog_index(category_id=None):
    from werkzeug.security import check_password_hash, generate_password_hash
    if session.get('uuid') is None: session['uuid'] = generate_uuid()
    if category_id is None :
        blog_list = Blog.query.filter(Blog.active==True, Blog.is_logic_delete==False).order_by(Blog.create_time.desc()).all()
    else:
        blog_list = Blog.query.filter(Blog.category_id==category_id, Blog.active==True, Blog.is_logic_delete==False).all()
    return render_template('index.html', blog_list=blog_list)

# 登录请求
@index.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('user_id') is not None:
        return redirect('/')
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first();
        if not user:
            flash('用户名不存在')
            return redirect(url_for('index.login'))
        if not user.active:
            flash('该账号已封禁')
            return redirect(url_for('index.login'))
        if user.check_password(user.password, password):
            session.clear()
            g.user = user
            set_session(user)
            return redirect(url_for('index.index'))
        else:
            flash('密码错误')
            return redirect(url_for('index.login'))

@index.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('user_id') is not None:
        return redirect('/')
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        user = User.query.filter_by(username=username).first()
        if user and username == user.username:
            flash('用户名已被注册')
            return redirect(url_for('index.register'))
        if password != password_confirm:
            flash('两次密码不一致')
            return redirect(url_for('index.register'))
        
        # password = generate_password_hash(password)
        new_user = User(username=username, password=password, name=username)
        # new_user.sef_password_hash()
        db.session.add(new_user)
        db.session.commit()
        session.clear()
        set_session(new_user)
        g.user = new_user
        db.session.close()
        return redirect(url_for('index.index'))

@index.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('index.index'))
 
@index.route('/updatePwd')
def updatePwd():
    return render_template('update_pwd.html')

@index.route('/category', methods=['GET', 'POST'])
def category():
    user = User.query.get(session['user_id'])
    if user.permission > 2:
        return redirect('/')
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

@index.route('/category_list')
def category_list():
    # blog_list = Blog.query.all()
    blog_list = Blog.query.filter(Blog.active==True, Blog.is_logic_delete==False)
    category_list = Category.query.all()
    return render_template('category_list.html', blog_list=blog_list, category_list=category_list)
    
@index.route('/user_info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'GET':
        return render_template('user_info.html')
    if request.method == 'POST':
        base_img_path = current_app.config['STATIC_IMAGE_PATH']
        img_fold_name = 'avator'
        avator_img_folder_path = os.path.join(base_img_path, img_fold_name)
        user = User.query.get(session['user_id'])
        new_name = request.form.get('name')
        avator_file = request.files.get('file')
        if not os.path.exists(avator_img_folder_path):
            os.mkdir(avator_img_folder_path)
        if new_name is not None: new_name = new_name.strip()
        if new_name and (len(new_name) <= 1 or len(new_name) > 10):
            flash('用户名长度:2-10', 'user_info')
            return redirect(request.url)
        if avator_file:
            avator_file_name = f"{user.username}-avator{os.path.splitext(avator_file.filename)[-1]}"
            avator_file_path = os.path.join(avator_img_folder_path, avator_file_name)
            avator_file.save(avator_file_path)
            user.avator = f'/{img_fold_name}/{avator_file_name}'
            db.session.commit()
            session['user_avator_path'] = user.avator
            db.session.close()
            return {'status': 200}
        if new_name is not None:
            user.name = new_name
            db.session.commit()
            session['user_name'] = user.name
            db.session.close()
            return redirect(request.url)
           
@index.route('/password', methods=['POST'])
def password():
    old_pwd = request.form.get('old_pwd').strip()
    new_pwd = request.form.get('new_pwd').strip()
    user = User.query.get(session['user_id'])
    if not old_pwd or not new_pwd:
        flash('数据不合格', 'password')
        return redirect(request.referrer)
    if user.check_password(user.password, old_pwd):
        user.password = new_pwd
        user.set_password_hash()
        db.session.commit()
        db.session.close()
    else:
        flash('旧密码错误', 'password')
    return redirect(request.referrer)

@index.route('/search')
def search():
    # if request.method == 'POST':
        keyword = request.args.get('keyword')
        if not keyword.strip():
            return redirect('/')
        blog_list = Blog.query.filter(db.or_(Blog.title.like(f"%{keyword}%"), Blog.text.like(f"%{keyword}%"))).all()
        pattern = f'[^<>]*{keyword}.*[^<>]'
        blog_obj_list = []
        if not blog_list:
            return render_template('search.html', err_msg='没有搜索内容')
        for blog in blog_list:
            # 通过正则表达式搜索匹配内容
            text = re.search(pattern, blog.text, re.IGNORECASE)
            if not text:
                obj = {'blog': blog, 'keyword_centence': ''}
            else:
                html = text.group().replace(keyword, f'<span style="color:red">{keyword}</span>')
                obj = {'blog': blog, 'keyword_centence': html}
            blog_obj_list.append(obj)
        return render_template('search.html', blog_list=blog_obj_list)
