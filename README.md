# SkyPay & Rewards Hub (Prototype)

[![CI](https://img.shields.io/github/actions/workflow/status/<your-username>/skypay-rewards-hub/ci.yml?branch=main)](https://github.com/<your-username>/skypay-rewards-hub/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112.x-brightgreen.svg)](https://fastapi.tiangolo.com/)

A **FastAPI** reference project for a unified **Airline Payments & Loyalty** layer.

## Quickstart

### Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Open http://127.0.0.1:8000/docs
```

### Docker
```bash
docker build -t skypay:dev .
docker run -p 8000:8000 skypay:dev
```

### Tests
```bash
pytest -q
```

## API (prototype)
- `GET /health` – service health
- `GET /wallet/{user_id}` – points, tier, history
- `POST /checkout` – simulate checkout with optional points usage

## Roadmap (Chunks)
See `docs/ROADMAP.md` for the stepwise plan (Chunks 1–18).

---

**License:** MIT
