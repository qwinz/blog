from flask import Blueprint, request, render_template, redirect, session, flash, url_for, g
from model import db
from model.models import User, Blog, Category, Comment
from sqlalchemy import exc

blog = Blueprint('blog', __name__, url_prefix='/blog', template_folder='../templates', static_folder='../static', static_url_path='')

@blog.before_request
def is_login():
    user_id = session.get('user_id')
    # 看博客和评论不用登录
    if 'blog' in request.path and 'blog_detail' not in request.path and 'comment' not in request.path:
        if not user_id:
            flash('请先登录')
            return redirect('/login')

def get_blog_by_user(blog_id=None, is_all=False) -> blog:
    user = User.query.get(session['user_id'])
    if is_all:
        blog = Blog.query.filter(Blog.user_id==user.id).order_by(Blog.create_time.desc()).all()
    else:
        blog = Blog.query.filter(Blog.id==blog_id, Blog.user_id==user.id).first()
    return blog

@blog.route('/write', methods=['POST', 'GET'])
@blog.route('/write/<int:blog_id>', methods=['POST', 'GET'])
def write_blog(blog_id=None):
    category_all = Category.query.all()
    if request.method == 'GET':
        if blog_id:
            blog = get_blog_by_user(blog_id)
            return render_template('write_blog.html', blog=blog, category_all=category_all)
        else:
            return render_template('write_blog.html', category_all=category_all)
    if request.method == 'POST':
        recv_data = request.form
        title = recv_data.get("title")
        text = recv_data.get('editor')
        category_name = recv_data.get('category_name')
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        category = Category.query.filter(Category.name==category_name).first()
        if blog_id:
            blog = Blog.query.filter(Blog.id==blog_id, Blog.user_id==user.id).first()
            blog.title = title
            blog.text = text
            blog.category_id = category.id if category else None
        else:
            if category is not None:
                blog = Blog(title=title, text=text, user_id=user.id, active=0, category_id=category.id)
            else:
                blog = Blog(title=title, text=text, user_id=user.id, active=0)
            db.session.add(blog)
        db.session.commit()
        db.session.close()
        return redirect(url_for('blog.blog_list'))

@blog.route('/del_post/<int:blog_id>')
def del_post(blog_id):
    blog = get_blog_by_user(blog_id)
    db.session.delete(blog)
    db.session.commit()
    db.session.close()
    return redirect(url_for('blog.blog_list'))

# 展示文章列表
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
    db.session.close()
    return redirect(url_for('blog.blog_detail', blog_id=blog_id))
    

@blog.route('/blog_edit/<int:blog_id>')
def blog_edit(blog_id):
    return redirect(url_for('blog.write_blog', blog_id=blog_id))

# 文章详情页面
@blog.route('/blog_detail/<int:blog_id>', methods=['GET'])
def blog_detail(blog_id):
    blog = Blog.query.get(blog_id)
    comments = Comment.query.filter(Comment.blog_id==blog_id).all()
    return render_template('blog_detail.html', blog=blog, comments=comments)

@blog.route('/blog_success')
def blog_success():
    
    return render_template('blog_success.html')

@blog.route('/comment', methods=['GET'])
@blog.route('/comment/<int:blog_id>', methods=['POST'])
def comment(blog_id=None):
    if request.method == 'GET':
        comments = Comment.query.filter(Comment.user_id==session.get('user_id')).all()
        return render_template('my_comments.html', comments=comments)
    user_id = session.get('user_id')
    text = request.form.get('mce_0')
    if len(text.replace('&nbsp;', '')) < 8:
        flash('评论字数不足')
        return redirect(request.referrer)
    if user_id is not None:
        # 如果已登录，不使用uuid身份
        user = User.query.get(user_id)
        comment = Comment(text=text, user_id=user.id, blog_id=blog_id)
    else:
        comment = Comment(text=text, uuid=session.get('uuid'), blog_id=blog_id)
    try:
        db.session.add(comment)
        db.session.commit()
        db.session.close()
    except:
        flash('评论格式错误')
    return redirect(request.referrer)


