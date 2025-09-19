from pydantic import BaseModel
from typing import Optional

class AnalysisTask(BaseModel):
    query: Optional[str] = None
    file_path: Optional[str] = "data/TSLA-Q2-2025-Update.pdf"
