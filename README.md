# Health Data API — Render Deployment

## 1) Files included
- `main.py` — FastAPI app (expects `MONGO_URI` from environment)
- `requirements.txt` — Python dependencies
- `render.yaml` — Render infrastructure-as-code (web service)
- `.env.example` — Sample env file for local dev
- `.gitignore` — Ignore cache and secrets

## 2) Local run (optional)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
cp .env.example .env && edit .env  # put your Mongo connection string
pip install -r requirements.txt
# Export env for local run
export $(grep -v '^#' .env | xargs)  # Windows: set MONGO_URI=...
uvicorn main:app --reload
```

## 3) Deploy on Render (via GitHub)
1. Push these files to a **new GitHub repo**.
2. On Render, click **New > Web Service**, connect the repo.
3. Choose *Runtime: Python* (Render will detect via `render.yaml`).
4. On the service **Environment** tab, add an env var:
   - Key: `MONGO_URI`
   - Value: your MongoDB connection string (never commit secrets).
5. Deploy. Render will run:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Test the health endpoint:
   - `GET https://<your-service>.onrender.com/` -> `{ "status": "ok", ... }`

## 4) Notes
- Keep your Mongo user minimally privileged.
- Consider adding CORS if calling from browsers.
- For larger datasets, add pagination to `/healthdata`.