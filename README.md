

# 📑 Financial Document Analyzer (Fixed & Optimized)

This repository contains the **debugged and optimized** version of the Financial Document Analyzer system originally built with CrewAI.

✅ All deterministic bugs fixed
✅ Prompts rewritten for clarity & determinism
✅ Celery worker added for handling concurrent requests
✅ SQLite database integration for storing jobs & results
✅ Docker & docker-compose support
✅ Interactive API docs available at **`http://127.0.0.1:8000/docs`**

---

## 🔧 Bugs Fixed

1. **PDF Extraction**

   * *Issue*: PDF text extraction returned incomplete/garbled text.
   * *Fix*: Updated `tools.py` to use a reliable parser with error handling.

2. **Numeric Extraction**

   * *Issue*: Regex pulled random numbers (like page numbers).
   * *Fix*: Implemented stricter regex with context filters in `extract_numbers`.

3. **Summarization**

   * *Issue*: Short summaries included headings or junk.
   * *Fix*: `short_summary` improved to skip one-line headings.

4. **Prompt Instability**

   * *Issue*: CrewAI agents returned inconsistent outputs.
   * *Fix*: `app/prompts.md` now enforces **structured JSON** output.

5. **Task Handling**

   * *Issue*: Tasks were blocking the main app.
   * *Fix*: Added **Celery + Redis** for async background tasks.

6. **Results Persistence**

   * *Issue*: No tracking of jobs/results.
   * *Fix*: Added **SQLite database** with `jobs` and `results` tables.

---

## 🚀 Quick Start

### 1. Clone Repo

```bash
git clone https://github.com/<your-username>/financial-document-analyzer-fixed.git
cd financial-document-analyzer-fixed
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root:

```env
# API keys
CREWAI_API_KEY=ck_123456abcdef7890
# (If you want to use OpenAI instead, replace with your OPENAI_API_KEY)

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Database
FDA_DB=analyzer.db

# Upload directory
UPLOAD_DIR=uploads
```

---

## 🐳 Run with Docker (Recommended)

Make sure Docker and docker-compose are installed, then run:

```bash
docker-compose up --build
```

This will:

* Start Redis
* Build the app container
* Run Celery + FastAPI

Your app will be live at:
👉 API root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
👉 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🖥️ Run Locally (Manual)

### Start Redis (if not using Docker)

```bash
redis-server
```

### Start Celery Worker

```bash
celery -A app.celery_worker.app worker --loglevel=info -Q default
```

### Start FastAPI App

```bash
uvicorn app.main:app --reload
```

Then open:
👉 API root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
👉 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 Usage (via API)

### Submit a Document

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@sample.pdf"
```

**Response**:

```json
{
  "job_id": "12345",
  "status": "queued"
}
```

### Check Result

```bash
curl "http://127.0.0.1:8000/analyze?job_id=12345"
```

**Example Response**:

```json
{
  "job_id": "12345",
  "status": "completed",
  "result": {
    "summary": "This document contains Q1 financial highlights...",
    "numbers": [2023, 1500000, 42]
  }
}
```

### Download Original File

```bash
curl -O "http://127.0.0.1:8000/download/12345"
```

---

## 🧪 Testing

Run tests with **pytest**:

```bash
# run all tests quietly
python -m pytest -q

# run all tests verbosely
python -m pytest -v

# run a specific test file
python -m pytest tests/test_tools.py -q
```

---

## 📖 API Endpoints

* `POST /analyze` → Upload and enqueue PDF for analysis
* `GET /analyze?job_id={id}` → Get job status and result
* `GET /download/{job_id}` → Download original uploaded PDF
* **Interactive Docs** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🎯 Bonus Features Implemented

* ✅ **Queue Worker** (Celery + Redis) for async processing
* ✅ **Database Integration** (SQLite) for persistent results
* ✅ **Robust Prompt Design** ensuring deterministic JSON responses
* ✅ **Docker Support** for easy setup
* ✅ **Swagger UI** auto-generated docs at `/docs` ([http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs))

---
