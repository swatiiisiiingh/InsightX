# InsightX — AI-Powered Hyperlocal Smart Inventory & Demand Forecasting Platform

**Live Demo:** [ubiquitous-bienenstitch-ca52ce.netlify.app](https://ubiquitous-bienenstitch-ca52ce.netlify.app/index.html)

InsightX helps local online sellers (kirana stores, medical shops, small grocery/clothing/handicraft sellers) run their inventory the way large quick-commerce platforms do — with real-time stock tracking, AI-driven demand forecasting, and smart restock alerts — without the cost or complexity of enterprise tools.

> 🎓 Built as a CSE major project. Frontend is complete and live; backend (Flask + ML) is in active development — see [Roadmap](#roadmap--current-status).

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [System Modules](#system-modules)
- [AI / ML Forecasting](#ai--ml-forecasting)
- [Getting Started](#getting-started)
- [Planned API Reference](#planned-api-reference)
- [Roadmap / Current Status](#roadmap--current-status)
- [Limitations](#limitations)
- [Hardware & Software Requirements](#hardware--software-requirements)
- [License](#license)

---

## Problem Statement

Local sellers lack access to hyperlocal selling infrastructure combined with AI-based inventory intelligence, leading to stockouts, overstocking, and reduced competitiveness against centralized quick-commerce platforms like Blinkit/Instamart — which use warehouse models, charge high commissions, and give sellers little control.

## Objectives

- Design a hyperlocal e-commerce platform for local sellers
- Implement AI-based demand forecasting
- Provide smart inventory recommendations (what to reorder, how much, when)
- Support sustainable digital growth of small businesses

## Features

### 📊 Dashboard
- Live KPIs: total stock, monthly revenue, low-stock alerts, inventory turnover
- Revenue & units-sold trend charts, stock-health donut chart
- Low-stock alert feed with one-click restock ordering
- Sortable/filterable/searchable inventory table
- AI demand forecast preview (7-day) with model accuracy stats

### 📦 Inventory Management
- Full CRUD on products (name, SKU, category, stock, reorder point, pricing, supplier)
- Table & grid views, bulk select/restock/delete, CSV import & export
- Category filters, low-stock-only view, live stats bar (total units, critical/warning counts, avg. margin)

### 🧠 AI Demand Forecasting
- Per-product forecast charts (7 / 14 / 30-day horizons) with confidence bands
- Seasonal demand pattern & category-wise forecast breakdown
- Product-level forecast summary table with restock urgency labels
- Model retraining flow with live progress steps
- "How the ML Model Works" walkthrough + documented API contract for backend integration

### 🔐 Authentication
- Login / Register with tabbed UI, demo credentials, form validation
- Session-based redirect to dashboard on success

### 🛒 Marketplace / Customer Flow *(in progress)*
- Location-based nearby shop browsing, product discovery, simulated ordering, cart & checkout

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (ES6), Chart.js |
| Fonts | Orbitron, Syne, JetBrains Mono (Google Fonts) |
| Backend *(planned)* | Python 3.11, Flask, Flask-CORS |
| Database *(planned)* | SQLite (via Flask-SQLAlchemy) |
| AI / ML *(planned)* | scikit-learn (Random Forest Regressor), pandas, numpy, joblib |
| Hosting | Netlify (frontend) · Render.com (backend, planned) |

## Project Structure

```
InsightX/
├── index.html              # Landing page + login/signup section
├── login.html               # Standalone auth page (calls Flask API)
├── dashboard.html            # Seller overview dashboard
├── inventory.html            # Full inventory management (CRUD, CSV import/export)
├── forecast.html             # AI demand forecasting dashboard
├── marketplace.html           # Customer-facing marketplace (WIP)
├── cart.html                 # Shopping cart (WIP)
├── checkout.html              # Checkout flow (WIP)
├── consumer_dashboard.html     # Customer-side dashboard (WIP)
└── backend/                  # Flask API + ML models (planned)
    ├── app.py
    ├── models.py
    ├── routes/
    ├── ml/
    │   ├── train.py
    │   └── forecast_model_<id>.pkl
    └── insightx.db
```

## System Modules

**1. Seller (Shopkeeper) Module** — add/update products, view stock, receive low-stock alerts, view AI predictions, get reorder suggestions.

**2. Customer Module** — select location (mock pincode/area), view nearby local shops, browse products, place simulated orders.

**3. Admin / Analytics Module** — view sales reports, analyze revenue trends, monitor stock movement, overall system monitoring.

## AI / ML Forecasting

The forecasting pipeline (see `forecast.html` → "How the ML Model Works"):

1. **Data Collection** — daily sales logged per product (`product_id, date, units_sold, price, day_of_week`), minimum 7 days needed to train.
2. **Feature Engineering** — rolling averages (7d/14d), lag features (previous day's sales), day-of-week encoding, seasonal flags.
3. **Model Training** — a `RandomForestRegressor` (100 estimators) trained per product, cross-validated to avoid overfitting.
4. **Serving** — trained model saved as `.pkl`, loaded by Flask, served through a REST API the frontend calls in real time.

**Models used:** Linear Regression & Moving Average as simple/explainable baselines suited to small datasets, with Random Forest as the primary model. LSTM-based time-series forecasting is planned as a future enhancement.

## Getting Started

### Frontend (available now)
```bash
git clone <your-repo-url>
cd InsightX
# open index.html directly, or serve locally:
python -m http.server 5500
```
Then visit `http://localhost:5500/index.html`. No build step required — pure HTML/CSS/JS.

### Backend (once implemented)
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # runs at http://127.0.0.1:5000
```
Update the `API` constant at the top of `login.html`'s script block if your backend runs on a different host/port.

## Planned API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Create a new seller account |
| POST | `/api/auth/login` | Authenticate and start a session |
| POST | `/api/auth/logout` | End the current session |
| GET | `/api/products` | List all products |
| POST | `/api/products` | Add a new product |
| PUT | `/api/products/<id>` | Update a product |
| DELETE | `/api/products/<id>` | Remove a product |
| POST | `/api/products/<id>/restock` | Add stock to a product |
| POST | `/api/products/import` | Bulk import via CSV |
| GET | `/api/products/export` | Export inventory as CSV |
| POST | `/api/sales/add` | Log a sale (feeds the forecasting model) |
| GET | `/api/forecast/<product_id>?days=7` | Get AI forecast for one product |
| GET | `/api/forecast/all` | Forecast summary for all products |
| POST | `/api/model/retrain` | Retrain the forecasting model on latest data |
| GET | `/api/dashboard/summary` | KPI data for the dashboard |

Example response for `GET /api/forecast/<id>`:
```json
{
  "product_id": 1,
  "forecast": [48, 55, 51, 60, 58, 66, 63],
  "confidence": 0.94,
  "trend": "up"
}
```

## Roadmap / Current Status

- [x] Landing page, auth UI, dashboard, inventory, forecast pages (frontend, static/mock data)
- [ ] Flask backend with SQLite persistence
- [ ] Real authentication (hashed passwords, sessions/JWT)
- [ ] Random Forest forecasting models trained on real sales history
- [ ] Marketplace / customer ordering flow
- [ ] Deploy backend (Render) and connect to the live Netlify frontend
- [ ] Mobile app, UPI integration, live GPS delivery tracking (future scope)

## Limitations

- No real payment gateway integration yet
- No live delivery tracking
- Current data (sales, stock, forecasts) is simulated/mocked in the frontend pending backend integration

## Hardware & Software Requirements

**Hardware:** Laptop/Desktop, minimum 4GB RAM, internet connection (for AI API calls)

**Software:** Windows/Linux · Chrome or Edge · Python (Flask) for backend · SQLite/JSON for storage

## License

This project was built for academic purposes as part of a CSE major project. Feel free to fork and extend it for your own learning.
