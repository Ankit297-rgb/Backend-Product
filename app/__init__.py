from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Setup path to the database file
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../grocery.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Import and register Blueprints
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp

    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')

    # Test route
    @app.route('/')
    def home():
        return {"message": "Welcome to the Smart Grocery Order API!"}

    # Create all tables if they do not exist
    with app.app_context():
        db.create_all()

    return app
