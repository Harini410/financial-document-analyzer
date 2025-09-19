import os, uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from app.models import create_job, get_job, get_result
from app.tasks import analyze_doc_task

UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title='Financial Document Analyzer')

@app.post('/analyze')
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF uploads are supported.')
    job_id = str(uuid.uuid4())
    save_path = f"{UPLOAD_DIR}/{job_id}.pdf"
    with open(save_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    create_job(job_id, save_path, status='pending')
    analyze_doc_task.delay(job_id, save_path)
    return JSONResponse({'job_id': job_id, 'status': 'queued'})

@app.get('/status/{job_id}')
def status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    result = get_result(job_id)
    response = {'job_id': job_id, 'status': job.get('status')}
    if result:
        response['result'] = result.get('payload')
    return JSONResponse(response)

@app.get('/download/{job_id}')
def download(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    file_path = job.get('file_path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(path=file_path, filename=f"{job_id}.pdf", media_type='application/pdf')
