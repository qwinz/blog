from flask import Blueprint, request, render_template, redirect, session, flash, url_for
from model import db
from model.models import User, Blog

blog = Blueprint('blog', __name__, url_prefix='/blog', template_folder='../templates', static_folder='../static', static_url_path='')

@blog.before_request
def is_login():
    username = session.get('username')
    if 'blog' in request.path:
        if not username:
            flash('请先登录')
            return redirect('/login')

def get_blog_by_user(blog_id=None, is_all=False) -> blog:
    user = User.query.filter(User.username == session['username']).first()
    if is_all:
        blog = Blog.query.filter(Blog.user_id==user.id).order_by(Blog.create_time.desc()).all()
    else:
        blog = Blog.query.filter(Blog.id==blog_id, Blog.user_id==user.id).first()
    return blog

@blog.route('/write', methods=['POST', 'GET'])
@blog.route('/write/<int:blog_id>', methods=['POST', 'GET'])
def write_blog(blog_id=None):
    if request.method == 'GET':
        if blog_id:
            blog = get_blog_by_user(blog_id)
            return render_template('write_blog.html', blog=blog)
        else:
            return render_template('write_blog.html')
    if request.method == 'POST':
        recv_data = request.form
        title = recv_data.get("title")
        text = recv_data.get('editor')
        username = session.get('username')
        user = User.query.filter(User.username == username).first()
        if blog_id:
            blog = Blog.query.filter(Blog.id==blog_id, Blog.user_id==user.id).first()
            blog.title = title
            blog.text = text
            db.session.commit()
        else:
            blog = Blog(title=title, text=text, user_id=user.id, active=0)
            db.session.add(blog)
            db.session.commit()
        return redirect(url_for('blog.blog_list'))

@blog.route('/del_post/<int:blog_id>')
def del_post(blog_id):
    blog = get_blog_by_user(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('blog.blog_list'))

# 展示博客列表
@blog.route('/blog_list')
def blog_list():
    blog_list = get_blog_by_user(is_all=True)
    return render_template('my_blog_list.html', blog_list=blog_list)

# 列表提交blog
@blog.route('/blog_post/<int:blog_id>')
def blog_post(blog_id):
    blog = Blog.query.filter(Blog.id == blog_id).first()
    blog.active = True
    db.session.commit()
    return redirect(url_for('blog.detail_blog', blog_id=blog_id))
    

@blog.route('/blog_edit/<int:blog_id>')
def blog_edit(blog_id):
    return redirect(url_for('blog.write_blog', blog_id=blog_id))

# 博客详情页面
@blog.route('/blog_detail/<int:blog_id>')
def detail_blog(blog_id):
    return render_template('blog_detail.html')

@blog.route('/blog_success')
def blog_success():
    
    return render_template('blog_success.html')


