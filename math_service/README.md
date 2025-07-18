# Math Microservice API

Acest microserviciu expune o API REST pentru calcule matematice de bază (pow, fibonacci, factorial) cu procesare asincronă, cache in-memory și persistare în SQLite.

## Funcționalități
- POST `/api/operation` – trimite un request de calcul, primești `job_id` imediat (threaded).
- GET `/api/operation/<job_id>` – vezi status/resultat pentru job.
- GET `/api/history` – vezi toate operațiile calculate.

## Tehnologii
- Flask, Pydantic, SQLite, threading, cache in-memory.
- Organizat OOP și PEP8 (trece flake8).

## Rulare
```bash
pip install -r requirements.txt
python run.py
