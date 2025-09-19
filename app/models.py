import os, sqlite3, json
from datetime import datetime
DB_PATH = os.getenv('FDA_DB', 'fda_results.db')

def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS results
                    (id TEXT PRIMARY KEY, created_at TEXT, payload TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS jobs
                    (id TEXT PRIMARY KEY, created_at TEXT, file_path TEXT, status TEXT)''')
    return conn

def save_result(doc_id, payload):
    conn = _get_conn()
    now = datetime.utcnow().isoformat()
    conn.execute('INSERT OR REPLACE INTO results(id, created_at, payload) VALUES (?, ?, ?)',
                 (doc_id, now, json.dumps(payload)))
    conn.commit()
    conn.close()

def get_result(doc_id):
    conn = _get_conn()
    cur = conn.execute('SELECT id, created_at, payload FROM results WHERE id=?', (doc_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {'id': row[0], 'created_at': row[1], 'payload': json.loads(row[2])}

def create_job(doc_id, file_path, status='pending'):
    conn = _get_conn()
    now = datetime.utcnow().isoformat()
    conn.execute('INSERT OR REPLACE INTO jobs(id, created_at, file_path, status) VALUES (?, ?, ?, ?)',
                 (doc_id, now, file_path, status))
    conn.commit()
    conn.close()

def update_job_status(doc_id, status):
    conn = _get_conn()
    conn.execute('UPDATE jobs SET status=? WHERE id=?', (status, doc_id))
    conn.commit()
    conn.close()

def get_job(doc_id):
    conn = _get_conn()
    cur = conn.execute('SELECT id, created_at, file_path, status FROM jobs WHERE id=?', (doc_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {'id': row[0], 'created_at': row[1], 'file_path': row[2], 'status': row[3]}
