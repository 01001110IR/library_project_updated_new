from flask import Blueprint, request, jsonify
from models.init_db import db
from models.all_models import  Customer

customer_blueprint = Blueprint('customer', __name__)

@customer_blueprint.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        customer_list = [{
            'customer_id': customer.customer_id,
            'name': customer.name,
            'age': customer.age,       
            'city': customer.city      
        } for customer in customers]
        return jsonify(customer_list), 200

    if request.method == 'POST':
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

@customer_blueprint.route('/customer/<string:customer_customer_id>', methods=['GET', 'PUT', 'DELETE'])  # Changed int to string
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'GET':
        return jsonify({
            'customer_id': customer.customer_id,
            'name': customer.name,
            'age': customer.age,       
            'city': customer.city      
        }), 200

    if request.method == 'PUT':
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

    if request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({}), 204
