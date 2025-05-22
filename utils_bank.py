import fitz  # PyMuPDF
import pandas as pd
import re

def parse_bank_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    # תבנית לשליפת תאריך + תיאור + סכום
    pattern = r'(\\d{2}/\\d{2}/\\d{4}).*?([\\u0590-\\u05FF\\s"\\']+)([\\-\\d,\\.]+₪)'
    matches = re.findall(pattern, text)

    rows = []
    for date, desc, amount in matches:
        try:
            clean_amount = float(re.sub(r'[₪,]', '', amount))
            signed = -clean_amount if '-' in amount else clean_amount
            rows.append({"תאריך": date, "תיאור": desc.strip(), "signed_amount": signed})
        except:
            continue

    df = pd.DataFrame(rows)

    if 'signed_amount' not in df.columns or df.empty:
        return pd.DataFrame(), {"total_income": 0, "total_expense": 0, "net_flow": 0}

    summary = {
        "total_income": df[df.signed_amount > 0]["signed_amount"].sum(),
        "total_expense": df[df.signed_amount < 0]["signed_amount"].sum(),
        "net_flow": df["signed_amount"].sum()
    }
    return df, summary
