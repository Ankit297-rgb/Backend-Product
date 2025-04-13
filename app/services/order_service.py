from app import db
from app.models import Order, OrderItem, Product

def place_order(data):
    order = Order(customer_name=data['customer_name'])
    db.session.add(order)
    db.session.flush()  # So we can use order.id before committing

    total = 0
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            db.session.rollback()
            raise ValueError(f"Invalid product ID {item['product_id']}")

        quantity = item['quantity']
        price = quantity * product.price_per_unit
        total += price

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity
        )
        db.session.add(order_item)

    db.session.commit()
    return {"order_id": order.id, "total_amount": total}

def get_all_orders():
    orders = Order.query.all()
    result = []

    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        item_list = []
        total = 0

        for item in items:
            product = Product.query.get(item.product_id)
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

    return result
