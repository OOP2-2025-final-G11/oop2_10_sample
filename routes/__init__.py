from .user import user_bp
from .rental import rental_bp
from .books import books_bp
from .book_request import book_request_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  rental_bp
  books_bp,
  book_request_bp,
]
