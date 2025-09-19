
from tools import extract_numbers, short_summary

def test_extract_numbers_basic():
    s = "Revenue was $1,234,567.89 and growth was 12.5% in 2024. Odd table: 020000400006000080000100000120000"
    nums = extract_numbers(s)
    assert "1234567.89" in nums
    assert "12.5" in nums
    assert not any(len(n) > 15 for n in nums)

def test_short_summary_basic():
    s = "Q2 2025 Update\nHIGHLIGHTS\nThis quarter we launched a new product. Revenue increased by 10% year over year. More details in the following sections."
    summary = short_summary(s, max_sentences=2)
    assert "launched a new product" in summary or "Revenue increased" in summary
