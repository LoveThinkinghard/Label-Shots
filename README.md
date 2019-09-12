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

2019.9.10

为在生产环境部署做出必要改变，主要变化有：
1. 添加`labelshot.py`文件，用来启动应用
2. 添加`uwsgi.ini`文件，对启动`uwsgi`进行必要配置
3. 添加`nginx config/labelshot`，为反向代理服务器`nginx`的配置
4. 修改一个小bug——网页底部未固定在屏幕底

## 用uWSGI和Nginx部署

部署平台：`Ubuntu 16.04`

需要安装：`python3`，`virtualenv`（或`conda`的虚拟环境），`uwsgi`，`flask`，`nginx`

### 安装参考：

#### nginx

```
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx
```

#### flask

```
pip install flask
```

#### uwsgi

```
pip install uwsgi
```
如果在conda的虚拟环境下出现问题，可以使用：  
```
conda install -c conda-forge uwsgi
```
### 安装完之后

将`labelshot`整个文件夹放到Ubuntu服务器的`/var/www/`目录下（放到哪儿其实不重要）

将`nginx config`文件夹下的`labelshot`放到Ubuntu服务器的`/etc/nginx/sites-enabled/`目录下，并把原来的`default`文件删掉（这个得放对）

参考链接，里面有从安装到配置的完整详细步骤（如果想实现服务器启动自动运行网页，里面也有方法）：

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

### 启动

#### 启动uwsgi

在`python`虚拟环境中

```
uwsgi uwsgi.ini
```

#### 启动ngnix

启动或（重新配置后）重启Nginx

```
sudo systemctl restart nginx
```

如果开启了ufw，输入

```
sudo ufw allow 'Nginx Full'
```

如果没有开启，输入

```
sudo ufw enable
```

现在可以访问本机IP，应该一切ok

### 使用https

现在还没有，如果想弄可以参考:

https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04
