# 使用说明

## Flask安装

http://flask.pocoo.org/docs/1.0/installation/#python-version

## 运行

进入`label-shot`文件夹所在目录，对于`Windows`在`cmd`里执行下列命令

```cmd
set FLASK_APP=label_shot
set FLASK_ENV=development
flask run
```

更多启动方法见：http://flask.pocoo.org/docs/1.0/tutorial/factory/#run-the-application

## 打开网页

访问：http://127.0.0.1:5000/

## 初始化数据库

```cmd
flask init-db
```

## 新加内容

2019.7.3

1. 更改`session`有效期为长久有效（30天）
2. 加入可视化数据功能，目前只能画一个图

2019.7.6

1. 可修改密码
2. 添加相关内容的提示功能，比如标签内容的解释
3. 增加管理员后台，共有4个管理权限等级，具体如下

| 权限（privilege） | Description |
| ----------- | ----------- |
| 0 | 普通用户，不能进入管理后台 |
| 1 | 普通管理员，能进入后台，但暂时不能进行改动，以后可以用来维护普通用户基本信息 |
| 2 | 高级管理员，可以添加和删除普通管理员和普通用户，只能由超级管理员产生 |
| 3 | 超级管理员，可以添加和删除所有用户，除了自己，目前只能在初始化数据库时产生一个，用户名和密码都为superAdmin，初次使用后记得及时修改密码 |

所有管理员都不能看见密码，密码以密文存储，采用带盐哈希加密，技术上也无法由密文得到明文。

## Serve with uWSGI and Nginx

Reference: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
