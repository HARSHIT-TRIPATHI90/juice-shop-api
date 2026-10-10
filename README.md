# Juice Lab API

A from-scratch FastAPI rebuild of the OWASP Juice Shop product and user data,
built as a **clean, working baseline** before intentional vulnerabilities are
layered in for API pentesting practice.

> ⚠️ **This application is, and will become, intentionally insecure.**
> Never deploy it on a public server or a shared network. Run it only on
> `localhost` or in an isolated lab network. Treat it like you would treat
> any deliberately exploitable target.

## What this is

- Product and user seed data extracted from [OWASP Juice Shop](https://github.com/juice-shop/juice-shop)
  (MIT licensed — see `THIRD_PARTY_NOTICES.md`), rebuilt on a new FastAPI/SQLAlchemy
  backend instead of the original Node.js app.
- Right now (this baseline commit), the API is written **correctly**: auth is
  scoped, ownership is checked, passwords are hashed with bcrypt, JWTs are
  verified against a pinned algorithm. This is the "before" picture.
- Vulnerabilities (BOLA, BFLA, mass assignment, SSRF, injection, etc.) get
  added on top of this in later stages, each tracked in a `vulns.yaml`
  catalog with a flag, so you can turn individual challenges on/off.

## Requirements

- Docker + Docker Compose (recommended), **or**
- Python 3.12+ if running it directly

## Run it (Docker — recommended)

```bash
docker compose up --build
```

The API comes up at `http://127.0.0.1:8000`. Interactive docs (Swagger UI)
at `http://127.0.0.1:8000/docs`.

## Run it (without Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The SQLite database (`juicelab.db`) and seed data load automatically on
first startup.

## Default accounts

All 24 Juice Shop seed users are loaded with their original (deliberately
weak) passwords — e.g. `admin` / `admin123`. Full list visible by reading
`app/seed_data/users.json`. These are intentionally weak for the lab;
don't reuse them anywhere real.

## Project layout

```
app/
├── main.py              # FastAPI app, router wiring, startup seeding
├── seed.py               # loads seed_data/*.json into the DB on first boot
├── seed_data/             # extracted Juice Shop products & users (JSON)
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py        # password hashing, JWT issue/verify, auth deps
├── models/
│   ├── db_models.py       # SQLAlchemy ORM models
│   └── schemas.py          # Pydantic request/response models
└── routers/
    ├── auth.py
    ├── products.py
    ├── basket.py
    ├── orders.py
    ├── addresses.py
    ├── feedback.py
    └── admin.py
```

## Status

- [x] Clean, correctly-scoped baseline API
- [ ] Vulnerability layer (OWASP API Top 10 + injections, etc.)
- [ ] Flag system
- [ ] Hardened report-writing portal (separate service/network)

## License

Code in this repository: MIT. Product/user seed data adapted from OWASP
Juice Shop, also MIT — see `THIRD_PARTY_NOTICES.md`.
