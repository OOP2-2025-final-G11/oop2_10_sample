from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from peewee import fn
from models import Rental, User, Books
from datetime import datetime

# Blueprintの作成
rental_bp = Blueprint('rental', __name__, url_prefix='/rentals')

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
        Rental.create(user=user_id, books=book_id, rental_date=rental_date)
        return redirect(url_for('rental.list'))
    
    users = User.select()
    books = Books.select()
    return render_template('rental_add.html', users=users, books=books)


@rental_bp.route('/edit/<int:rental_id>', methods=['GET', 'POST'])
def edit(rental_id):
    rental = Rental.get_or_none(Rental.id == rental_id)
    if not rental:
        return redirect(url_for('rental.list'))

    if request.method == 'POST':
        rental.user = request.form['user_id']
        rental.books = request.form['book_id']
        rental.save()
        return redirect(url_for('rental.list'))

    users = User.select()
    books = Books.select()
    return render_template('rental_edit.html', rental=rental, users=users, books=books)


@rental_bp.route('/return/<int:rental_id>', methods=['POST'])
def return_book(rental_id):
    rental = Rental.get_or_none(Rental.id == rental_id)

    if rental and rental.return_date is None:
        rental.return_date = datetime.now()
        rental.save()

    return redirect(url_for('rental.list'))

@rental_bp.route('/api/monthly_rentals')
def monthly_rentals_api():
    year = datetime.now().year
    query = (
        Rental
        .select(
            fn.strftime('%m', Rental.rental_date).alias('month'),
            fn.COUNT(Rental.id).alias('count')
        )
        .where(fn.strftime('%Y', Rental.rental_date) == str(year))
        .group_by(fn.strftime('%m', Rental.rental_date))
    )

    monthly_counts = {row.month: row.count for row in query}

    #1〜12月を必ず用意（無い月は0）
    labels = []
    data = []

    for m in range(1, 13):
        month_str = f"{m:02d}"
        labels.append(f"{m}月")
        data.append(monthly_counts.get(month_str, 0))

    return jsonify({
        "year": year,
        "labels": labels,
        "data": data
    })
