from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../grocery.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)

    
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp

    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')

    
    @app.route('/')
    def home():
        return {"message": "Welcome to the Smart Grocery Order API!"}

    
    with app.app_context():
        db.create_all()

    return app
