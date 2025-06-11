from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton, 
    QHBoxLayout
)
import pandas as pd
from _2_table_widget import ExcelTableWidget

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("공사 대장 검색")
        self.resize(800, 500)
        layout = QVBoxLayout()

        # 공사명 입력란
        name_layout = QHBoxLayout()
        name_label = QLabel("공사명:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # 검색 버튼
        search_btn = QPushButton("검색")
        search_btn.clicked.connect(self.search_projects)
        layout.addWidget(search_btn)

        # 결과 테이블 (ExcelTableWidget 사용)
        self.result_table = ExcelTableWidget()  # 빈 경로로 생성, 데이터만 나중에 전달
        layout.addWidget(self.result_table)

        self.setLayout(layout)

    def search_projects(self):
        main_window = self.parent()
        excel_path = main_window.table_widget.excel_path
        df = pd.read_excel(excel_path)

        # 컬럼명이 없는(빈 문자열, NaN, Unnamed:) 열 제거
        df = df.loc[:, [
            col for col in df.columns
            if str(col).strip() and str(col).lower() != "nan" and not str(col).startswith("Unnamed:")
        ]]

        keyword = self.name_edit.text().strip()
        if keyword:
            df = df[df["공사명"].astype(str).str.contains(keyword, case=False, na=False)]

        # 검색 결과를 테이블에 표시 (ExcelTableWidget의 display_df 재사용)
        self.result_table.display_df(df)