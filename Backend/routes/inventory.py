from flask import Blueprint, request, jsonify
from database.db import db

inventory_bp = Blueprint('inventory', __name__)

# Inline model (or import from a separate models file)
from flask_sqlalchemy import SQLAlchemy

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    low_stock_threshold = db.Column(db.Integer, default=10)

@inventory_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id, "name": p.name, "category": p.category,
        "stock": p.stock, "price": p.price,
        "low_stock": p.stock <= p.low_stock_threshold
    } for p in products])

@inventory_bp.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product = Product(
        name=data['name'], category=data.get('category', ''),
        stock=data.get('stock', 0), price=data.get('price', 0.0),
        low_stock_threshold=data.get('threshold', 10)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added", "id": product.id}), 201

@inventory_bp.route('/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    product = Product.query.get_or_404(pid)
    data = request.json
    product.stock = data.get('stock', product.stock)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify({"message": "Updated"})

@inventory_bp.route('/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Deleted"})

@inventory_bp.route('/alerts', methods=['GET'])
def low_stock_alerts():
    alerts = Product.query.filter(Product.stock <= Product.low_stock_threshold).all()
    return jsonify([{"id": p.id, "name": p.name, "stock": p.stock} for p in alerts])