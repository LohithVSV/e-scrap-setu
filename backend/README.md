# E-Setu Backend

## Run locally

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Main endpoints

- GET /
- POST /auth/citizen/signup
- POST /auth/citizen/login
- POST /auth/officer/login
- GET /dropoffs
- GET /dropoffs/qr/{qr_code}
- GET /collections
- POST /collections
- GET /rewards/{citizen_id}
- POST /rewards/redeem
- GET /dashboard/ward/{ward_id}
- GET /dashboard/alerts
- POST /feedback
- POST /assistant/ask
