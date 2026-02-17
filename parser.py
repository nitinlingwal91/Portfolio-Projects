import json
import re
from pathlib import Path
import pdfplumber
import pandas as pd

def extract_tables_from_page(page):
    table_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "text",
        "intersection_tolerance": 5,
        "snap_tolerance": 5,
        "join_tolerance": 2,
        "edge_min_length": 3,
    }
    table = page.extract_table(table_settings=table_settings)
    if not table:
        return None
    df = pd.DataFrame(table[1:], columns=table[0])
    return df

def extract_header_fields(words):
    
    full_text = " ".join(w["text"] for w in words)

    def find(pattern):
        m = re.search(pattern, full_text, flags=re.IGNORECASE)
        return m.group(1).strip() if m else None

    return {
        "invoice_number": find(r"Invoice\s*#\s*([A-Za-z0-9\-]+)"),
        "invoice_date": find(r"Invoice\s*Date[:\s]+([\d\-\/]+)"),
        "due_date": find(r"Due\s*Date[:\s]+([\d\-\/]+)"),
    }


def extract_totals(words):
    totals = {}
    for w in words:
        text = w["text"]
        if re.match(r"(?i)total", text):
            # Find nearest numeric to the right
            x0 = w["x1"]
            y0 = (w["top"] + w["bottom"]) / 2
            candidates = []
            for w2 in words:
                if w2["x0"] > x0 and abs(((w2["top"] + w2["bottom"]) / 2) - y0) < 10:
                    candidates.append(w2)
            if candidates:
                value = max(candidates, key=lambda c: c["x0"])["text"]
                label = text.lower().replace(" ", "_")
                totals[label] = value
    return totals


def parse_pdf(path: str):
    path = Path(path)
    result = {
        "document_type": "invoice",
        "file_name": path.name,
        "pages": 0,
        "header_fields": {},
        "line_items": [],
        "totals": {},
    }

    with pdfplumber.open(path) as pdf:
        result["pages"] = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            words = page.extract_words(
                use_text_flow=True,
                keep_blank_chars=False,
            )
            if i == 0:
                result["header_fields"] = extract_header_fields(words)
            if i == len(pdf.pages) - 1:
                totals = extract_totals(words)
                result["totals"].update(totals)

            df = extract_tables_from_page(page)
            if df is not None and not df.empty:
                # Assume only one main line-item table
                result["line_items"] = df.to_dict(orient="records")
                break

    return result


if __name__ == "__main__":
    # debug run
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py <pdf_path>")
        raise SystemExit(1)
    data = parse_pdf(sys.argv[1])
    print(json.dumps(data, indent=2, ensure_ascii=False))    