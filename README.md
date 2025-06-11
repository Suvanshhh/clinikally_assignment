
# Dermatologist Review & Recommendation API

A backend service built with FastAPI that enables:
- Customers to rate and review dermatologists
- Dermatologists to recommend products to users
- Publicly shareable recommendation links (like a prescription)

---
## Project Working Video: https://drive.google.com/file/d/1cERFNwdo-fAejzb88aBvSdqL1l-D-bz8/view?usp=drive_link
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

Here’s a clean, markdown-formatted version of your API documentation — with **support for resizing images** using HTML tags (since GitHub Markdown doesn't natively support image resizing):

---

## 📚 API Documentation

### **Authentication**

#### `POST /auth/token`

* **Description:** Authenticate user and receive a JWT access token.
* **Form data:**

  * `username`
  * `password`
* **Returns:** Access token.

<img src="https://github.com/user-attachments/assets/15bb1a7f-c9e0-4ea1-81d3-26e405270c1f" width="500"/>  
<img src="https://github.com/user-attachments/assets/674a7ab5-bc90-4ebe-944c-5fd212decb9d" width="500"/>

---

### **Doctors**

#### `POST /doctor/` (Protected)

* **Description:** Create a new doctor profile.
* **Headers:** Authorization (Bearer token required)

<img src="https://github.com/user-attachments/assets/e91f8eae-4dce-4877-8d44-e22f55566a65" width="500"/>  
<img src="https://github.com/user-attachments/assets/923e87cc-97c6-4631-aea6-81c78b98d29f" width="500"/>

#### `GET /doctor/`

* **Description:** List all doctors.
* **Query params (optional):**

  * `min_rating`: Minimum average rating filter
  * `skip`: Pagination start
  * `limit`: Number of records to fetch

<img src="https://github.com/user-attachments/assets/2e62b3bb-33b6-411f-a6b1-6a4cdd0ed8a9" width="500"/>  
<img src="https://github.com/user-attachments/assets/7d4c4caa-575b-4693-99f4-e6648b5d8159" width="500"/>

#### `POST /doctor/{doctor_id}/review` (Protected)

* **Description:** Submit a rating (1–5) and review (up to 100 words).
* **Headers:** Authorization required.

<img src="https://github.com/user-attachments/assets/3e982cd7-3f90-4072-a19b-0c07494b3002" width="500"/>  
<img src="https://github.com/user-attachments/assets/5aaf76a7-9a6d-4338-9953-b66f5d5acb6a" width="500"/>

---

### **Recommendations**

#### `POST /recommendation/{doctor_id}` (Protected)

* **Description:** Create a recommendation with product IDs.
* **Returns:** Recommendation data + UUID.
* **Headers:** Authorization required.

<img src="https://github.com/user-attachments/assets/bd93b3ad-e55d-4991-8fa5-f0cb93500587" width="500"/>  
<img src="https://github.com/user-attachments/assets/2d7af12e-77af-4206-837b-964eb134dd62" width="500"/>  
<img src="https://github.com/user-attachments/assets/b0a5972f-5e43-42b4-a015-0e4bdc6896d7" width="500"/>

#### `GET /recommendation/{uuid}`

* **Description:** Fetch a public recommendation using UUID.
* **Returns:** Patient name, notes, expiry date, and full product details.

<img src="https://github.com/user-attachments/assets/6ac03681-9327-46f5-9925-1d7fd7b00103" width="500"/>  
<img src="https://github.com/user-attachments/assets/29bc9bac-05bd-4e67-af84-1feaa6eb55d7" width="500"/>

---

Let me know if you want me to help automate this markdown generation for future endpoints using a script or generator.


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
  "name": "Dr. Sagar",
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
  "patient_name": "Sameer Shah",
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
