
# 项目依赖
Python 3.10+
Django 4.1+

本机搭建好 Python， 安装过 pip, 以及 Django 后。 安装其他依赖：
```Bash
pip install -r requirements.txt
```

# 一、本机环境服务启动:

```Bash
 python manage.py runserver 127.0.0.1:9000

 # optional: expose to external user beside localhost
 # python manage.py runserver 0.0.0.0:9000
```

可以通过 http://localhost:9000 来访问服务。
如果要开放到其他机器访问，启动时可命令设定监听 0.0.0.0:9000， 命令如上。

数据库保存在  db.sqlite3 文件的文件数据库中。 上传的文件保存在 media 目录下.

# 二、云上服务环境启动：

```Bash
python manage.py collectstatic
# 将 static 文件拷贝到 nginx 服务中
uvicorn disease_control_policy_management.asgi:application --port 8000 --workers 2
```