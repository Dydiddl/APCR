from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit
from PySide6.QtCore import QDate
from datetime import datetime
import pandas as pd
from _2_table_widget import ExcelTableWidget

class CompletedConstructionDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setWindowTitle("완료 공사 목록")
        self.resize(900, 550)
        self.main_window = main_window

        layout = QVBoxLayout()

        # 기간 설정 위젯
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("기간 설정:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("~"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date)

        self.filter_btn = QPushButton("필터 적용")
        self.filter_btn.clicked.connect(self.filter_by_period)
        filter_layout.addWidget(self.filter_btn)

        # 올해공사 버튼
        self.this_year_btn = QPushButton("올해공사")
        self.this_year_btn.clicked.connect(self.set_this_year_and_filter)
        filter_layout.addWidget(self.this_year_btn)

        # 작년공사 버튼
        self.last_year_btn = QPushButton("작년공사")
        self.last_year_btn.clicked.connect(self.set_last_year_and_filter)
        filter_layout.addWidget(self.last_year_btn)

        # 2년전공사 버튼
        self.two_years_ago_btn = QPushButton("2년전공사")
        self.two_years_ago_btn.clicked.connect(self.set_two_years_ago_and_filter)
        filter_layout.addWidget(self.two_years_ago_btn)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # 완료 공사 데이터만 추출
        df_all = self.main_window.table_widget.df_all
        if "공사종료" in df_all.columns:
            self.df_completed = df_all[df_all["공사종료"] == 1].reset_index(drop=True)
        else:
            self.df_completed = df_all.copy()

        # 표 위젯 생성 및 데이터 표시
        self.table = ExcelTableWidget()
        self.table.display_df(self.df_completed)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def filter_by_period(self):
        # 실제 준공일 기준으로 필터링
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.max.time())
        df = self.df_completed.copy()
        if "실제 준공일" in df.columns:
            df["실제 준공일"] = pd.to_datetime(df["실제 준공일"], errors="coerce")
            mask = (df["실제 준공일"] >= start_dt) & (df["실제 준공일"] <= end_dt)
            df = df[mask].reset_index(drop=True)
        self.table.display_df(df)

    def set_this_year_and_filter(self):
        today = QDate.currentDate()
        year = today.year()
        start = QDate(year, 1, 1)
        end = QDate(year, 12, 31)
        self.start_date.setDate(start)
        self.end_date.setDate(end)
        self.filter_by_period()

    def set_last_year_and_filter(self):
        today = QDate.currentDate()
        year = today.year() - 1
        start = QDate(year, 1, 1)
        end = QDate(year, 12, 31)
        self.start_date.setDate(start)
        self.end_date.setDate(end)
        self.filter_by_period()

    def set_two_years_ago_and_filter(self):
        today = QDate.currentDate()
        year = today.year() - 2
        start = QDate(year, 1, 1)
        end = QDate(year, 12, 31)
        self.start_date.setDate(start)
        self.end_date.setDate(end)
        self.filter_by_period()