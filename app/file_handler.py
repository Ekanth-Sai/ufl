import pandas as pd
import pdfplumber
from docx import Document
from io import BytesIO

def extract_file_data(filename, file_bytes):
    ext = filename.split('.')[-1].lower()
    buffer = BytesIO(file_bytes)

    if ext == "csv":
        return pd.read_csv(buffer)
    elif ext in ["xls", "xlsx"]:
        return pd.read_excel(buffer)
    elif ext == "pdf":
        with pdfplumber.open(buffer) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return pd.DataFrame({"text": text.split('\n')})
    elif ext == "docx":
        doc = Document(buffer)
        lines = [para.text for para in doc.paragraphs if para.text.strip()]
        return pd.DataFrame({"text": lines})
    else:
         raise ValueError("Unsupported File Format")