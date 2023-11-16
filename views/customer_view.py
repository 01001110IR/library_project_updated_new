from flask import Blueprint, request, jsonify
from models.init_db import db
from models.all_models import Customer

customer_blueprint = Blueprint('customer', __name__)

@customer_blueprint.route('/customers', methods=['GET', 'POST'])
@customer_blueprint.route('/customers/<string:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_customers(customer_id=None):
    if request.method == 'GET':
        if customer_id is None:
            # Fetch and return all customers
            customers = Customer.query.all()
            customer_list = [{
                'customer_id': customer.customer_id,
                'name': customer.name,
                'age': customer.age,
                'city': customer.city
            } for customer in customers]
            return jsonify(customer_list), 200
        else:
            # Fetch and return a single customer
            customer = Customer.query.get_or_404(customer_id)
            return jsonify({
                'customer_id': customer.customer_id,
                'name': customer.name,
                'age': customer.age,
                'city': customer.city
            }), 200

    elif request.method == 'POST':
        # Add a new customer
        data = request.json
        new_customer = Customer(
            name=data.get('name'),
            age=data.get('age'),
            city=data.get('city')
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({
            'customer_id': new_customer.customer_id,
            'name': new_customer.name,
            'age': new_customer.age,
            'city': new_customer.city
        }), 201

    elif request.method == 'PUT' and customer_id is not None:
        # Update an existing customer
        customer = Customer.query.get_or_404(customer_id)
        data = request.json
        customer.name = data.get('name', customer.name)
        customer.age = data.get('age', customer.age)
        customer.city = data.get('city', customer.city)
        db.session.commit()
        return jsonify({
            'customer_id': customer.customer_id,
            'name': customer.name,
            'age': customer.age,
            'city': customer.city
        }), 200

    elif request.method == 'DELETE' and customer_id is not None:
        # Delete a customer
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({}), 204

    return jsonify({'error': 'Method not allowed'}), 405
