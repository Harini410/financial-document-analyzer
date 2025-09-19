Got it 👍 — since you noticed **[http://127.0.0.1:8000](http://127.0.0.1:8000)** (root) doesn’t show much, but **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** is the real entrypoint for interacting with the API, let’s make `/docs` the **primary link** in the README.

Here’s the adjusted README.md:

---

# 📑 Financial Document Analyzer (Fixed & Optimized)

This repository contains the **debugged and optimized** version of the Financial Document Analyzer system originally built with CrewAI.

✅ All deterministic bugs fixed
✅ Prompts rewritten for clarity & determinism
✅ Celery worker added for handling concurrent requests
✅ SQLite database integration for storing jobs & results
✅ Docker & docker-compose support
✅ Interactive API docs available at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🔧 Bugs Fixed

*(same bug list as before — trimmed here for brevity)*

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
CREWAI_API_KEY=ck_123456abcdef7890
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
FDA_DB=analyzer.db
UPLOAD_DIR=uploads
```

---

## 🐳 Run with Docker (Recommended)

```bash
docker-compose up --build
```

Your app will be live at:
👉 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🖥️ Run Locally (Manual)

```bash
# Start Redis
redis-server

# Start Celery worker
celery -A app.celery_worker.app worker --loglevel=info -Q default

# Start FastAPI
uvicorn app.main:app --reload
```

Then open:
👉 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 Usage

Use the **Swagger UI** at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** to:

* Upload a PDF (`POST /analyze`)
* Check analysis result (`GET /analyze?job_id=...`)
* Download uploaded file (`GET /download/{job_id}`)

---

## 🧪 Testing

```bash
python -m pytest -q
```

---

## 📖 API Endpoints

* `POST /analyze` → Upload and enqueue PDF for analysis
* `GET /analyze?job_id={id}` → Get job status and result
* `GET /download/{job_id}` → Download original uploaded PDF
* **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

----
