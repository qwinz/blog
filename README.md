## 演示地址
[https://77v036v609.yicp.fun/index](http://116.204.101.20:5000/index)
## 使用方法
1. 安装依赖文件，进入`requirements.txt`文件的目录。
2. 执行命令：`pip install -r requirements.txt`
3. 在projects文件夹创建`local_settings.py`配置文件：
    ```
    from os import path
    DB_HOST = 'xx'
    DB_PORT = xx
    DB_NAME = 'xx'
    DB_USER = 'xx'
    DB_PWD  = 'xx'
    #werkzeug.security.generate_password_hash加密后的后台管理密码，访问/admin可以进入用户管理界面，处理逻辑在projects中的init文件
    MASTER_PASSWORD = 'pbkdf2:sha256:600000$t0T......'
    #图片存储路径，此处为static/images
    STATIC_IMAGE_PATH = path.join(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'static'), 'images')
    ```
4. 数据库迁移：
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```
6. 执行app.py文件（.vscode文件可选）
## 模块介绍
- `migrations`：sqlaichemy数据库迁移文件
- `model`：数据库结构文件
- `projects`：项目配置文件及初始化应用
- `static`：静态文件目录，包括css、图片等
- `templates`：html模板文件
- `view`：视图函数，路由逻辑处理
- `app.py`：入口文件
## 预览
主页
![image](https://github.com/qwinz/blog/assets/72587888/b3c74566-49b4-42c7-85d0-17bb4a42cceb)
后台
![image](https://github.com/qwinz/blog/assets/72587888/9f2c21a7-5928-4515-b9a5-2c093a788ff8)
搜索
![image](https://github.com/qwinz/blog/assets/72587888/3bfd06aa-cb88-4ee6-aa8b-11c1c243842a)
正文
![image](https://github.com/qwinz/blog/assets/72587888/01e076be-e2f7-4e8d-a476-6a9927fee898)
评论
![image](https://github.com/qwinz/blog/assets/72587888/c8a1c668-a514-41da-ba1b-b7fd3906e06e)
评论汇总
![image](https://github.com/qwinz/blog/assets/72587888/73dc0f71-c7ce-46bb-8ff6-a1a9a612d861)

