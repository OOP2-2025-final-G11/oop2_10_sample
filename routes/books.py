from flask import Blueprint, render_template, request, redirect, url_for
from models import Books

# Blueprintの作成
books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('/')
def list():
    books = books.select()
    return render_template('books_list.html', title='本一覧', items=books)


@books_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        books.create(name=name)
        return redirect(url_for('books.list'))
    
    return render_template('books_add.html')


@books_bp.route('/edit/<int:books_id>', methods=['GET', 'POST'])
def edit(books_id):
    books = books.get_or_none(books.id == books_id)
    if not books:
        return redirect(url_for('books.list'))

    if request.method == 'POST':
        books.name = request.form['name']
        books.save()
        return redirect(url_for('books.list'))

    return render_template('books_edit.html', books=books)