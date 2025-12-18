from flask import Blueprint, jsonify
from peewee import fn
from models import Rental, Books

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/api/rental-ranking')
def rental_ranking_api():
    query = (
        Books
        .select(
            Books.title,
            fn.COUNT(Rental.id).alias('count')
        )
        .join(Rental)
        .group_by(Books.id)
        .order_by(fn.COUNT(Rental.id).desc())
    )

    return jsonify({
        "labels": [b.title for b in query],
        "data": [b.count for b in query]
    })
