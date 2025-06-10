# Dermatologist Review & Recommendation API

## Setup Instructions
1. Clone the repository.
2. Create virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate (or venv\Scripts\activate on Windows)
   ```
3. Install dependencies:
   ```
   pip install fastapi uvicorn sqlalchemy
   ```
4. Run the app:
   ```
   uvicorn main:app --reload
   ```

## API Documentation
Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

### Endpoints Summary

#### Doctor
- `POST /doctor/` - Add new doctor
- `POST /doctor/{id}/review` - Add rating/review
- `GET /doctor/?min_rating=4` - List doctors by rating

#### Recommendation
- `POST /recommendation/{doctor_id}` - Create a recommendation
- `GET /recommendation/{uuid}` - Get shared recommendation

## Notes
- SQLite used as in-memory DB.
- Recommendations expire after 7 days.
- No external APIs used as per guidelines.
