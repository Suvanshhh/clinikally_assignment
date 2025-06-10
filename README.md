
# Dermatologist Review & Recommendation API

A backend service built with FastAPI that enables:
- Customers to rate and review dermatologists
- Dermatologists to recommend products to users
- Publicly shareable recommendation links (like a prescription)

---

## 🚀 Features

1. **Rate & Review Dermatologist**
   - Users can rate (1–5 stars) and review (max 100 words) a dermatologist after consultation.
   - Average rating is updated automatically.

2. **Doctor Listing**
   - Fetch doctors filtered by minimum rating.
   - Each doctor includes name, specialization, average rating, and reviews.
   - Supports pagination (`skip`, `limit`).

3. **Product Recommendation**
   - Doctors can recommend products (using product IDs from [dummyjson.com/products](https://dummyjson.com/products)).
   - Recommendations are accessible via a unique, shareable link (`/recommendation/{uuid}`).
   - Each recommendation expires after 7 days.

4. **Authentication**
   - JWT-based authentication for protected endpoints.
   - Role-based access: only authenticated users can create doctors, reviews, and recommendations.

---

## 🏗️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** SQLite (file-based, simulating in-memory for dev)
- **ORM:** SQLAlchemy
- **Auth:** JWT (via `python-jose`)
- **HTTP Client:** httpx (for product API)
- **Other:** Uvicorn (ASGI server)

---

## 🛠️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone 
   cd 
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API docs:**
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 API Documentation

### **Authentication**

- **POST /auth/token**
  - Form data: `username`, `password`
  - Returns: JWT access token

### **Doctors**

- **POST /doctor/** (Protected)
  - Create a new doctor

- **GET /doctor/**
  - List doctors (`min_rating`, `skip`, `limit` supported)

- **POST /doctor/{doctor_id}/review** (Protected)
  - Add a rating (1–5) and review (max 100 words)

### **Recommendations**

- **POST /recommendation/{doctor_id}** (Protected)
  - Create a recommendation for a patient with product IDs (from dummyjson)
  - Returns: recommendation details + `uuid`

- **GET /recommendation/{uuid}**
  - Fetch a public recommendation by UUID
  - Returns: patient name, notes, expiry, and full product info

---

## 🧪 Example Usage

**1. Authenticate:**
```json
POST /auth/token
{
  "username": "user1",
  "password": "pass1"
}
```
Copy the `access_token` for use in protected endpoints.

**2. Create a Doctor:**
```json
POST /doctor/
{
  "name": "Dr. Jane Doe",
  "specialization": "Dermatology"
}
```

**3. Review a Doctor:**
```json
POST /doctor/1/review
{
  "rating": 5,
  "review": "Excellent consultation and advice!"
}
```

**4. Recommend Products:**
```json
POST /recommendation/1
{
  "patient_name": "John Smith",
  "notes": "Use these products daily.",
  "products": [1, 2]
}
```
Response includes a `uuid` for sharing.

**5. Get a Recommendation:**
```json
GET /recommendation/{uuid}
```

---

## ⚠️ Limitations & Extra Features

- No persistent user registration (dummy users only).
- Product data is fetched live from the dummy API.
- Recommendations store full product data as JSON, not normalized.
- No email or notification system.
- All core and bonus features from the assignment are implemented.

---

## 🏗️ Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── utils/
│   │   └── product_fetcher.py
│   └── routes/
│       ├── __init__.py
│       ├── doctor.py
│       ├── recommendation.py
│       └── auth.py
├── main.py
├── requirements.txt
├── README.md
└── DESIGN.md
```
