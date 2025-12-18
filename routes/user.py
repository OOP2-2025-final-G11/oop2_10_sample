from flask import Blueprint, render_template, request, redirect, url_for
from models import User
from peewee import fn
from datetime import datetime

# Blueprint
user_bp = Blueprint('user', __name__, url_prefix='')


# =====================
# トップページ / index
# =====================
@user_bp.route('/')
def index():
    year = 2025

    monthly_users = (
        User
        .select(
            fn.strftime('%Y-%m', User.created_at).alias('month'),
            fn.COUNT(User.id).alias('count')
        )
        .where(fn.strftime('%Y', User.created_at) == str(year))
        .group_by(fn.strftime('%Y-%m', User.created_at))
        .order_by(fn.strftime('%Y-%m', User.created_at))
    )

    labels = [f"{year}-{str(m).zfill(2)}" for m in range(1, 13)]
    counts_dict = {row.month: row.count for row in monthly_users}

    counts = []
    cumulative = 0
    for month in labels:
        monthly_count = counts_dict.get(month, 0)
        cumulative += monthly_count
        counts.append(cumulative)

    return render_template(
        'index.html',
        labels=labels,
        counts=counts
    )


# =====================
# ユーザー一覧
# =====================
@user_bp.route('/users')
def list():
    users = User.select()
    return render_template(
        'user_list.html',
        title='ユーザー一覧',
        items=users
    )


# =====================
# ユーザー追加（日時自動取得）
# =====================
@user_bp.route('/users/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']

        # 現在日時を自動取得
        created_at = datetime.now()

        User.create(
            name=name,
            age=age,
            created_at=created_at
        )
        return redirect(url_for('user.list'))

    return render_template('user_add.html')


# =====================
# ユーザー編集
# =====================
@user_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)