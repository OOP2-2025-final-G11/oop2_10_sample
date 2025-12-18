from flask import Blueprint, render_template, request, redirect, url_for
from models import User
#日時取得のため
from peewee import fn
from datetime import datetime

# Blueprint
user_bp = Blueprint('user', __name__, url_prefix='/users')


# ユーザー一覧
@user_bp.route('/')
def list():
    users = User.select()
    return render_template(
        'user_list.html',
        title='ユーザー一覧',
        items=users
    )


# ユーザー追加（手動日付入力）
@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        created_at_str = request.form['created_at']

        # YYYY-MM-DD → datetime
        created_at = datetime.strptime(created_at_str, '%Y-%m-%d')

        User.create(
            name=name,
            age=age,
            created_at=created_at
        )
        return redirect(url_for('user.list'))

    return render_template('user_add.html')


# ユーザー編集
@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
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


# ユーザー登録数グラフ（月別累計）
@user_bp.route('/chart')
def chart():
    # 表示する年を固定
    year = 2025

    # 月別ユーザー数を集計
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

    # 1月～12月のラベル
    labels = [f"{year}-{str(m).zfill(2)}" for m in range(1, 13)]

    # データ辞書化
    counts_dict = {row.month: row.count for row in monthly_users}

    # 累計カウントを作成
    counts = []
    cumulative = 0
    for month in labels:
        monthly_count = counts_dict.get(month, 0)
        cumulative += monthly_count
        counts.append(cumulative)

    return render_template(
        'user_graph.html',
        labels=labels,
        counts=counts
    )