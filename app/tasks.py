from app.celery_worker import app
import os
from app.llm_client import call_llm
from app.models import save_result, update_job_status
@app.task(bind=True, max_retries=3, default_retry_delay=30)
def analyze_doc_task(self, doc_id, file_path, user_id=None):
    try:
        from app.tools import extract_text_from_pdf
        text = extract_text_from_pdf(file_path)
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts.md')
        if os.path.exists(prompt_path):
            prompt_template = open(prompt_path).read()
        else:
            prompt_template = "Document text:\n{document_text}"
        prompt = prompt_template.replace('{document_text}', text[:20000])
        llm_resp = call_llm(prompt, max_tokens=800, temperature=0.0)
        model_text = llm_resp.get('text') if isinstance(llm_resp, dict) else llm_resp
        save_result(doc_id, {'model_output': model_text})
        update_job_status(doc_id, 'completed')
        return {'status': 'ok', 'doc_id': doc_id}
    except Exception as exc:
        try:
            update_job_status(doc_id, 'failed')
        except Exception:
            pass
        raise self.retry(exc=exc)
