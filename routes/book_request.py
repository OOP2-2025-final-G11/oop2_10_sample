from flask import Blueprint, render_template, request, redirect, url_for
from models import BookRequest, User
from datetime import datetime

book_request_bp = Blueprint('book_request', __name__, url_prefix='/request-books')


@book_request_bp.route('/')
def list():
    items = BookRequest.select()
    return render_template('book_request_list.html', title='新刊リクエスト一覧', items=items)


@book_request_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        author = request.form['author']
        request_date = datetime.now()

        BookRequest.create(
            user=user_id,
            title=title,
            author=author,
            request_date=request_date
        )
        return redirect(url_for('book_request.list'))

    users = User.select()
    return render_template('book_request_add.html', users=users)


@book_request_bp.route('/edit/<int:request_id>', methods=['GET', 'POST'])
def edit(request_id):
    req = BookRequest.get_or_none(BookRequest.id == request_id)
    if not req:
        return redirect(url_for('book_request.list'))

    if request.method == 'POST':
        req.user = request.form['user_id']
        req.title = request.form['title']
        req.author = request.form['author']
        req.save()
        return redirect(url_for('book_request.list'))

    users = User.select()
    return render_template('book_request_edit.html', req=req, users=users)
