from flask import Blueprint, render_template, request, redirect, url_for
from models import Rental, User, Book
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')

@rental_bp.route('/')
def list():
    rental = Rental.select()
    return render_template('rental_list.html', title='貸し出し', items=rental)

@rental_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        rental_date = datetime.now()
        Rental.create(user=user_id, book=book_id, rental_date=rental_date)
        return redirect(url_for('rental.list'))
    
    users = User.select()
    books = Book.select()
    return render_template('rental_add.html', users=users, books=books)


@rental_bp.route('/edit/<int:rental_id>', methods=['GET', 'POST'])
def edit(rental_id):
    rental = Rental.get_or_none(Rental.id == rental_id)
    if not rental:
        return redirect(url_for('rental.list'))

    if request.method == 'POST':
        rental.user = request.form['user_id']
        rental.book = request.form['book_id']
        rental.save()
        return redirect(url_for('rental.list'))

    users = User.select()
    books = Book.select()
    return render_template('rental_edit.html', rental=rental, users=users, books=books)


@rental_bp.route('/return/<int:rental_id>', methods=['POST'])
def return_book(rental_id):
    rental = Rental.get_or_none(Rental.id == rental_id)

    if rental and rental.return_date is None:
        rental.return_date = datetime.now()
        rental.save()

    return redirect(url_for('rental.list'))