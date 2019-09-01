from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort

from label_shot.auth import login_required
from label_shot.db import get_db
import random

bp = Blueprint('main', __name__)

def get_items(user_id):
    """
    根据user_id获取要打标签的项目和炮号
    """
    items = {"shot_no":1061874,
             "items":[{"name": "CqTime", "type": "float", "description": "CQ时间"},
                      {"name": "IsDisrupt", "type": "bool", "description": "这一炮时候破裂，强行凑字数看看效果"},
                      {"name": "Cause", "type": "multi", "value": ["Intentional", "MGI", "SPI", "DensityLimit"], "description": "导致破裂的原因"}
                      ]}
    return items


def get_visual_data(shot_no):
    """
    根据shot_no获取需要可视化的数据
    """
    name = 'ip'
    x = [t/10000-0.1 for t in range(10000)]
    y = [random.random() for i in range(10000)]
    visual_data = {"name":name, "x":x, "y":y}
    return visual_data

@bp.route('/')
def label():
    user_id = session.get('user_id')
    session.permanent = True
    if user_id:
        items = get_items(user_id=user_id)
        visual_data = get_visual_data(shot_no=items['shot_no'])
        return render_template('main/label.html', items=items, visual_data=visual_data, error=None)
    else:
        return redirect(url_for('auth.login', error=None))


@bp.route('/newlabel', methods=('POST',))
@login_required
def newlabel():
    user_id = session.get('user_id')
    data = request.get_json(force=True)
    """
    data = {"shot_no":112371
            "data":[{"name":"CqTime","value":"120"},
                    {"name":"IsDisrupt","value":"False"},
                    {"name":"Cause","value":"Intentional"}]}
    """
    """
    可以在这里把数据存入数据库
    """
    return jsonify(data)


@bp.route('/next')
@login_required
def next():
    """相当于刷新页面"""
    return redirect(url_for('main.label'))