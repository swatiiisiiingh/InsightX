from flask import Flask
from flask_cors import CORS          # ✅ Import only ONCE
from database.db import init_db
from routes.inventory import inventory_bp
from routes.forecast import forecast_bp
import os                            # ✅ Import os at the top

app = Flask(__name__)                # ✅ FIRST create the app
CORS(app)                            # ✅ THEN apply CORS

init_db(app)

app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(forecast_bp, url_prefix='/api/forecast')

if __name__ == "__main__":           # ✅ Only ONE app.run() block
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)