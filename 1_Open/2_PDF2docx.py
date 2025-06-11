from pdf2docx import Converter
import pdfplumber
import pandas as pd

pdf_path = "/Users/simsungwoo/Desktop/Design Document Automation Project(DDAP)/sample.pdf"
docx_path = "output.docx"
excel_path = "output.xlsx"

# 1. PDF의 글(텍스트) → Word로 변환
cv = Converter(pdf_path)
cv.convert(docx_path, start=0, end=None)
cv.close()

# 2. PDF의 표 → Excel로 추출
tables = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table[1:], columns=table[0])
            tables.append(df)

if tables:
    with pd.ExcelWriter(excel_path) as writer:
        for idx, df in enumerate(tables):
            df.to_excel(writer, sheet_name=f"Table_{idx+1}", index=False)
else:
    print("PDF에서 표를 찾을 수 없습니다.")