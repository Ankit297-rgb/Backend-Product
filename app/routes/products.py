from flask import Blueprint, request, jsonify
from app import db
from app.models import Product
from app.utils.validators import validate_product_input

products_bp = Blueprint('products', __name__)

# Add a Product
@products_bp.route('', methods=['POST'])
def add_product():
    data = request.get_json()

    # Input validation
    error = validate_product_input(data)
    if error:
        return jsonify({"error": error}), 400

    # Unique product name check
    existing_product = Product.query.filter_by(name=data['name']).first()
    if existing_product:
        return jsonify({"error": "Product name must be unique"}), 400

    try:
        # Create and add the new product to the session
        product = Product(
            name=data['name'],
            price_per_unit=data['price_per_unit'],
            unit=data['unit']
        )
        db.session.add(product)
        db.session.commit()

        return jsonify({
            "message": "Product added successfully",
            "product_id": product.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add product", "details": str(e)}), 500

# Get All Products
@products_bp.route('', methods=['GET'])
def get_products():
    try:
        # Fetch all products from the database
        products = Product.query.all()
        result = [
            {
                "id": product.id,
                "name": product.name,
                "price_per_unit": product.price_per_unit,
                "unit": product.unit
            }
            for product in products
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch products", "details": str(e)}), 500
