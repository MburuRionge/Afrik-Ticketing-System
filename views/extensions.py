from flask_caching import Cache
# extensions.py
from flask_sqlalchemy import SQLAlchemy

# Create a single instance of SQLAlchemy
db = SQLAlchemy()
cache = Cache()