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
    #哈希加密后的后台管理密码，访问/admin可以进入用户管理界面，处理逻辑在projects中的init文件
    MASTER_PASSWORD = 'pbkdf2:sha256:600000$t0T......'
    #图片存储路径，此处为static/images
    STATIC_IMAGE_PATH = path.join(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'static'), 'images')
    ```
4. 执行app.py文件（.vscode文件可选）
## 模块介绍
- `migrations`：sqlaichemy数据库迁移文件
- `model`：数据库结构文件
- `projects`：项目配置文件及初始化应用
- `static`：静态文件目录，包括css、图片等
- `templates`：html模板文件
- `view`：视图函数，路由逻辑处理
- `app.py`：入口文件

