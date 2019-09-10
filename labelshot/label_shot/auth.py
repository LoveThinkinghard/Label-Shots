import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from label_shot.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/manage', methods=('GET', 'POST'))
def manage():
    """Manage users.
    if privilege
        == 3 超级管理员，可以添加管理员
        == 2 高级管理员，可以添加普通管理员和普通用户
        == 1 普通管理员，维护普通用户基本信息
        == 0 普通用户
    """
    if g.user is None:
        return redirect(url_for('auth.login'))
    elif g.user['privilege'] in [2, 3]:
        error = None
        # 如果method == 'POST'，为添加用户操作
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            privilege = int(request.form['privilege'])
            if g.user['privilege'] <= privilege:
                error = 'You have no privilege to do that!'
            db = get_db()

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone() is not None:
                error = 'User {0} is already registered.'.format(username)

            if error is None:
                # the name is available, store it in the database and go to
                # the login page
                db.execute(
                    'INSERT INTO user (username, password, privilege) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), privilege)
                )
                db.commit()

        # 如果method == 'GET'，为删除操作
        if request.method == 'GET':
            user_id = request.args.get('user_id')
            db = get_db()
            if not user_id:
                error = None
            else:
                # 判断要删除的用户时候存在
                if db.execute(
                    'SELECT id FROM user WHERE id = ?', (user_id,)
                ).fetchone() is None: error = 'User which id is {} doesn\'t exist'.format(user_id)
                else:
                    # 判断权限是否够
                    target_privilege = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()['privilege']
                    self_privilege = db.execute('SELECT privilege FROM user WHERE id = ?', (g.user['id'],)).fetchone()['privilege']
                    if int(self_privilege) <= int(target_privilege):
                        error = 'You have no privilege to do that!'
                    else:
                        # 如果用户存在且权限够就执行删除指令
                        db.execute('DELETE FROM user WHERE id = ?', (user_id,))
                        db.commit()
        # 执行完添加或删除操作后，继续返回管理界面
        users = get_db().execute('SELECT * FROM user')
        return render_template('auth/manage.html', users=users, error=error)
    
    # 如果用户权限为1，则不能添加或删除用户，目前只能看有哪些用户
    elif g.user['privilege'] == 1:
        error = None
        if request.method in ['POST', 'GET']:
            error = 'You have no privilege to do that!'
        users = get_db().execute('SELECT * FROM user')
        return render_template('auth/manage.html', users=users, error=error)
    
    # 如果不是管理员，无法进入此页面
    else: 
        return redirect(url_for('main.label'))


@bp.route('/change_password', methods=('GET', 'POST'))
def change_password():
    """
    change password
    """
    if g.user is None:
        return redirect(url_for('auth.login'))
    error = None
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        db = get_db()

        if check_password_hash(g.user['password'], old_password):
            db.execute(
                'UPDATE user SET password = ? WHERE id = ?',
                (generate_password_hash(new_password), g.user['id'])
            )
            db.commit()
        else: error = "Wrong password!"
    return redirect(url_for('main.label', error=error))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if error is None:
            # store the user id in a new session and return to the label
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('label'))

        flash(error)

    return render_template('auth/login.html', error=error)


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('label'))
