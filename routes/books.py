from flask import Blueprint, render_template, request, redirect, url_for
from models import Books

# Blueprintの作成
books_bp = Blueprint('books', __name__, url_prefix='/books')


@books_bp.route('/')
def list():
    books = Books.select()
    return render_template('books_list.html', title='本一覧', items=books)


@books_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        Books.create(title=title, author=author, isbn=isbn)
        return redirect(url_for('books.list'))
    
    return render_template('books_add.html')


@books_bp.route('/edit/<int:books_id>', methods=['GET', 'POST'])
def edit(books_id):
    books = Books.get_or_none(Books.id == books_id)
    if not books:
        return redirect(url_for('books.list'))

    if request.method == 'POST':
        books.title = request.form['title']
        books.author = request.form['author']
        books.isbn = request.form['isbn']
        books.save()
        return redirect(url_for('books.list'))

    return render_template('books_edit.html', books=books)