from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(17))

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

# customer Schema
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'phone_number' )

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True,)

# Add customer 
@app.route('/customer', methods=['POST'])
def add_customer():
    name = request.json['name']
    phone_number = request.json['phone_number']
    new_customer = Customer(name, phone_number)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)

#get all customer
@app.route('/get-customer', methods=['GET'])
def get_customer():
    all_customer = Customer.query.all()
    result = customers_schema.dump(all_customer)
    return jsonify(result)

#update customer data
@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
  customer_object = Customer.query.get(id)

  name = request.json['name']
  phone_number = request.json['phone_number']

  customer_object.name = name
  customer_object.phone_number = phone_number
  db.session.commit()

  return customer_schema.jsonify(customer_object)

#delete customer
@app.route('/delete-customer/<id>', methods=['DELETE'])
def delete_customer(id):
  customer = Customer.query.get(id)
  db.session.delete(customer)
  db.session.commit()

  return customer_schema.jsonify(customer)

#runserver
if __name__ == '__main__':
    app.run(debug=True)
