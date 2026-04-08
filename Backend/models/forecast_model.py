import numpy as np
from sklearn.linear_model import LinearRegression

def moving_average(sales_data, window=3):
    if len(sales_data) < window:
        return float(np.mean(sales_data))
    return float(np.mean(sales_data[-window:]))

def linear_regression_forecast(sales_data, days_ahead=7):
    if len(sales_data) < 2:
        return [float(np.mean(sales_data))] * days_ahead

    X = np.array(range(len(sales_data))).reshape(-1, 1)
    y = np.array(sales_data)
    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array(range(len(sales_data), len(sales_data) + days_ahead)).reshape(-1, 1)
    predictions = model.predict(future_X)
    return [max(0, round(p, 2)) for p in predictions]

def get_reorder_suggestion(avg_daily_demand, lead_time_days=3, safety_stock=10):
    reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
    reorder_qty = avg_daily_demand * 7   # 1-week supply
    return {
        "reorder_point": round(reorder_point, 2),
        "suggested_order_qty": round(reorder_qty, 2)
    }