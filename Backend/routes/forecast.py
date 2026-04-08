from flask import Blueprint, request, jsonify
from models.forecast_model import linear_regression_forecast, moving_average, get_reorder_suggestion
from database.db import db

forecast_bp = Blueprint('forecast', __name__)

class SalesRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    units_sold = db.Column(db.Integer, default=0)
    date = db.Column(db.String(20))

@forecast_bp.route('/sales', methods=['POST'])
def add_sale():
    data = request.json
    record = SalesRecord(
        product_id=data['product_id'],
        units_sold=data['units_sold'],
        date=data['date']
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Sale recorded"}), 201

@forecast_bp.route('/forecast/<int:product_id>', methods=['GET'])
def forecast(product_id):
    days = int(request.args.get('days', 7))  # 7, 14, or 30
    records = SalesRecord.query.filter_by(product_id=product_id).all()

    if not records:
        return jsonify({"error": "No sales data found"}), 404

    sales_data = [r.units_sold for r in records]
    predictions = linear_regression_forecast(sales_data, days_ahead=days)
    avg_demand = sum(predictions) / len(predictions)
    reorder = get_reorder_suggestion(avg_demand)

    return jsonify({
        "product_id": product_id,
        "forecast_days": days,
        "predictions": predictions,
        "moving_average": moving_average(sales_data),
        "reorder_suggestion": reorder
    })