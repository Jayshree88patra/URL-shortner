# URL Shortener - FastAPI (SQLite)

This repository contains a minimal URL Shortener RESTful API implemented with FastAPI and SQLModel using SQLite for local development.

Features
- Create short URLs (POST /shorten)
- Retrieve URL metadata (GET /shorten/{code})
- Update URL target (PUT /shorten/{code})
- Delete short URL (DELETE /shorten/{code})
- Get stats (GET /shorten/{code}/stats)
- Redirect endpoint (GET /{code}) increments accessCount

Requirements
- Python 3.10+

Quickstart (local)
1. Create and activate a virtualenv
   python -m venv venv
   source venv/bin/activate   # or .\venv\Scripts\Activate.ps1 on Windows
2. Install dependencies
   pip install -r requirements.txt
3. Run the app
   uvicorn app.main:app --reload
4. Open docs
   http://127.0.0.1:8000/docs

Notes
- This scaffold uses SQLite (file: shortener.db) so you do not need to install a database server.
- For production use, migrate to Postgres and add migrations (alembic), Redis for caching/rate-limiting, and authentication.
