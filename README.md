# Discount Campaign Management System

This is a simple FastAPI-based backend application for managing **discount campaigns**, **users**, and **orders** using **JSON files** as the data store instead of a traditional database.

---

## 📁 Project Structure
```
discount_campaign/
├── app/
│   ├── __init__.py            # FastAPI app initializer
│   ├── routes.py              # All API endpoints for campaigns, users, and orders
│   ├── models.py              # Pydantic models for data validation
│   ├── utils.py               # Helpers for JSON read/write and datetime conversion
│   ├── campaign_data.json     # Stores campaign data
│   ├── user_data.json         # Stores customer/user data
│   └── order_data.json        # Stores order data
├── run.py                     # Entry point to start FastAPI app
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/discount_campaign.git
cd discount_campaign
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Server
```bash
uvicorn run:app --reload
```

---

## 🧾 API Endpoints

### 🔸 Campaign APIs
- `GET /campaigns`: List all campaigns
- `POST /campaigns`: Create a new campaign
- `GET /campaigns/{campaign_id}`: Get campaign details
- `PUT /campaigns/{campaign_id}`: Update campaign
- `DELETE /campaigns/{campaign_id}`: Delete campaign

### 🔸 User APIs
- `POST /users/`: Create a new user
- `GET /users/{user_id}`: Get user details
- `PUT /users/{user_id}`: Update user details

### 🔸 Order API
- `POST /create_order/`: Create a new order and apply discount based on the campaign and user's eligibility

---

## 📦 Data Storage
All data is stored in **JSON files**:
- `campaign_data.json` - holds campaigns
- `user_data.json` - holds users
- `order_data.json` - holds orders

Each entity includes timestamps (`created_at`, `updated_at`) and the respective fields defined in the `models.py`.

---

## 📚 Tech Stack
- **Python 3.11**
- **FastAPI** - for building APIs
- **Pydantic** - for data validation
- **Uvicorn** - for ASGI server

---

## ✅ Features
- Lightweight, JSON-file-based backend
- Full CRUD support for Campaigns and Users
- Discount application logic in Orders
- Validations and duplicate checks
- Modular and extensible architecture

---

## 📬 Future Improvements
- Replace JSON storage with a proper database (PostgreSQL/MongoDB)
- Add authentication (JWT or OAuth)
- Add filtering and pagination to listing APIs
- Write unit and integration tests

---

## 🧑 Author
**Saurabh Choudhary**
[GitHub](https://github.com/scphalswal) | [LinkedIn](https://linkedin.com/in/saurabh-choudhary-509a14207)
