from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import shutil, uuid, sqlite3, json
from tools import read_pdf_text
from agents import analyze_text_deterministic
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

APP_DIR = Path(__file__).parent
UPLOAD_DIR = APP_DIR / "uploads"
OUTPUT_DIR = APP_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
DB_PATH = APP_DIR / "fda_results.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY,
        filename TEXT,
        result_json TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="Financial Document Analyzer (Fixed)", version="1.0")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf",):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")
    uid = str(uuid.uuid4())
    saved_path = UPLOAD_DIR / f"{uid}_{file.filename}"
    with open(saved_path, "wb") as out:
        shutil.copyfileobj(file.file, out)
    # extract text
    text = read_pdf_text(str(saved_path))
    # deterministic analysis
    result = analyze_text_deterministic(text)
    # persist
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO analyses (id, filename, result_json) VALUES (?, ?, ?)", 
              (uid, file.filename, json.dumps(result)))
    conn.commit()
    conn.close()
    return JSONResponse({"id": uid, "result": result})



@app.get("/download/{id}")
def download(id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename, result_json FROM analyses WHERE id=?", (id,))
    row = c.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Result not found.")

    filename, result_json = row
    result = json.loads(result_json)

    # Generate report
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / f"{id}_report.pdf"
    c = canvas.Canvas(str(report_path), pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Financial Document Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Original File: {filename}")
    c.drawString(50, height - 100, f"Job ID: {id}")

    y = height - 140
    for key, value in result.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50
    c.save()

    return FileResponse(report_path, media_type="application/pdf", filename=f"{id}_report.pdf")

@app.get("/list")
def list_jobs():
    """List all analysis jobs with filename and report availability"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, filename FROM analyses")
    rows = c.fetchall()
    conn.close()

    jobs = []
    for job_id, filename in rows:
        report_path = OUTPUT_DIR / f"{job_id}_report.pdf"
        jobs.append({
            "id": job_id,
            "filename": filename,
            "report_ready": report_path.exists(),
            "download_url": f"/download/{job_id}" if report_path.exists() else None
        })

    return {"jobs": jobs}
