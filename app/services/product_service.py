from app import db
from app.models import Product

def add_product(data):
    product = Product(
        name=data['name'],
        price_per_unit=data['price_per_unit'],
        unit=data['unit']
    )
    db.session.add(product)
    db.session.commit()
    return product

def get_all_products():
    products = Product.query.all()
    return [{
        "id": p.id,
        "name": p.name,
        "price_per_unit": p.price_per_unit,
        "unit": p.unit
    } for p in products]

def is_unique_product_name(name):
    return Product.query.filter_by(name=name).first() is None
