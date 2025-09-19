
import re
from pathlib import Path
from PyPDF2 import PdfReader

def read_pdf_text(path: str) -> str:
    """Read and return text from PDF file at path."""
    text_parts = []
    reader = PdfReader(path)
    for p in reader.pages:
        try:
            text_parts.append(p.extract_text() or "")
        except Exception:
            continue
    return "\n".join(text_parts)

def extract_numbers(text: str):
    """
    Improved number extractor.
    Matches integers, decimals, and numbers with grouped commas like 1,234,567.89
    Filters unrealistic long digit runs (<=15).
    """
    flat = text.replace('\n', ' ')
    pattern = r'(?<!\w)(?:\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.\d+)(?!\w)'
    nums = re.findall(pattern, flat)
    nums = [n.replace(',','') for n in nums]
    nums = [n for n in nums if len(re.sub(r'\D','',n)) <= 15]
    return nums

def short_summary(text: str, max_sentences: int = 3) -> str:
    """Simple heuristic summary skipping headings."""
    txt = text.strip()
    sents = re.split(r'(?<=[\.!?])\s+', txt)
    def is_heading(s):
        s_strip = s.strip()
        if len(s_strip.split()) < 5:
            return True
        tokens = re.findall(r"[A-Za-z]+", s_strip)
        if tokens:
            upper_frac = sum(1 for t in tokens if t.isupper()) / len(tokens)
            if upper_frac > 0.6:
                return True
        if re.fullmatch(r'[\d\W]+', s_strip):
            return True
        return False
    filtered = [s.strip() for s in sents if len(s.strip())>0 and not is_heading(s)]
    if not filtered:
        return txt[:max_sentences*300].strip()
    return ' '.join(filtered[:max_sentences])
