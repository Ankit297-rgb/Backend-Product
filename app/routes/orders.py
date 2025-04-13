from flask import Blueprint, request, jsonify
from app import db
from app.models import Product, Order, OrderItem
from app.utils.validators import validate_order_input

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
def place_order():
    data = request.get_json()

    # Validate input
    error = validate_order_input(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        # Create order
        order = Order(customer_name=data['customer_name'])
        db.session.add(order)
        db.session.flush()  # Get order.id before commit

        total = 0

        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                db.session.rollback()
                return jsonify({"error": f"Invalid product ID {item['product_id']}"}), 400

            quantity = item['quantity']
            if quantity <= 0:
                db.session.rollback()
                return jsonify({"error": f"Quantity for product ID {item['product_id']} must be positive"}), 400

            price = quantity * product.price_per_unit
            total += price

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity
            )
            db.session.add(order_item)

        db.session.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total_amount": total
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@orders_bp.route('', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = []

    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        item_list = []
        total = 0

        for item in items:
            product = Product.query.get(item.product_id)
            if not product:
                continue  # skip invalid product references

            price = product.price_per_unit * item.quantity
            total += price

            item_list.append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": item.quantity,
                "price": price
            })

        result.append({
            "order_id": order.id,
            "customer_name": order.customer_name,
            "items": item_list,
            "total_amount": total
        })

    return jsonify(result), 200
