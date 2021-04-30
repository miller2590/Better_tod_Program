# core/views.py
from todoapplication.models import TodoPost
from flask import render_template, request, Blueprint
from sqlalchemy import desc

core = Blueprint('core', __name__)


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    todo_posts = TodoPost.query.order_by(desc(TodoPost.date)).paginate(page=page, per_page=10)
    return render_template('index.html', todo_posts=todo_posts)


@core.route('/info')
def info():
    return render_template('info.html')
