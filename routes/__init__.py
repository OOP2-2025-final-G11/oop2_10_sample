from .user import user_bp
from .books import books_bp
from .order import order_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  books_bp,
  order_bp
]
