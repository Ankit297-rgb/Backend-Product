def validate_product_input(data):
    if not isinstance(data, dict):
        return "Invalid input format. JSON expected."

    # Validate product name
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        return "Product name is required and must be a non-empty string."

    # Validate price per unit
    if 'price_per_unit' not in data:
        return "Price per unit is required."
    if not isinstance(data['price_per_unit'], (int, float)):
        return "Price per unit must be a number."
    if data['price_per_unit'] <= 0:
        return "Price per unit must be a positive number."

    # Validate unit
    if 'unit' not in data or not isinstance(data['unit'], str) or not data['unit'].strip():
        return "Unit is required and must be a non-empty string."

    return None

def validate_order_input(data):
    if not isinstance(data, dict):
        return "Invalid input format. JSON expected."

    # Validate customer name
    if 'customer_name' not in data or not isinstance(data['customer_name'], str) or not data['customer_name'].strip():
        return "Customer name is required and must be a non-empty string."

    # Validate items
    if 'items' not in data or not isinstance(data['items'], list) or not data['items']:
        return "Order must contain at least one item."

    for index, item in enumerate(data['items'], start=1):
        if not isinstance(item, dict):
            return f"Item {index} must be an object with product_id and quantity."
        if 'product_id' not in item:
            return f"Item {index} is missing 'product_id'."
        if 'quantity' not in item:
            return f"Item {index} is missing 'quantity'."
        if not isinstance(item['product_id'], int):
            return f"Item {index}: product_id must be an integer."
        if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
            return f"Item {index}: quantity must be a positive integer."

    return None
