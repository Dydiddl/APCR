import pdfplumber
import pandas as pd

pdf_path = "/Users/simsungwoo/Desktop/Design Document Automation Project(DDAP)/sample.pdf"  # 변환할 PDF 파일 경로
excel_path = "output.xlsx"  # 저장할 엑셀 파일 경로

tables = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table[1:], columns=table[0])
            tables.append(df)

if tables:
    # 여러 표가 있을 경우 하나의 엑셀 파일에 각각 시트로 저장
    with pd.ExcelWriter(excel_path) as writer:
        for idx, df in enumerate(tables):
            df.to_excel(writer, sheet_name=f"Table_{idx+1}", index=False)
else:
    print("PDF에서 표를 찾을 수 없습니다.")

