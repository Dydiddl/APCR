from PySide6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QPushButton
)
import pandas as pd
from datetime import datetime

class ExcelTableWidget(QTableWidget):
    def __init__(self, excel_path=None):
        super().__init__()
        self.excel_path = excel_path
        self.df_all = None
        if excel_path:  # 경로가 있을 때만 엑셀 로드
            self.df_all = pd.read_excel(excel_path)
            self.show_active_projects()
        # 나중에 display_df(df)로 데이터만 표시 가능
        self.cellDoubleClicked.connect(self.show_project_overview)
    
    def show_active_projects(self):
        # 화면에 표시할 데이터만 필터링
        df = self.df_all.copy()
        if "공사종료" in df.columns:
            df = df[df["공사종료"] != 1].reset_index(drop=True)
            df = df.drop(columns=["공사종료"])
        self.display_df(df)
    
    def display_df(self, df):
        # 컬럼명이 없는(빈 문자열, NaN) 열 제거
        df = df.loc[:, [
            col for col in df.columns
            if str(col).strip() and str(col).lower() != "nan" and not str(col).startswith("Unnamed:")
        ]]
        # "메모" 컬럼이 없으면 추가
        if "메모" not in df.columns:
            df["메모"] = ""
        
        # "세금계산서 발행" 컬럼이 없으면 추가
        if "세금계산서 발행" not in df.columns:
            df["세금계산서 발행"] = ""
        self.df = df
        self.setRowCount(len(df) + 1 )
        self.setColumnCount(len(df.columns))
        self.setHorizontalHeaderLabels([str(col) for col in df.columns])
        
        for row in range(len(df)):
            for col in range(len(df.columns)):
                col_name = str(df.columns[col])
                if col_name == "세금계산서 발행":
                    cell_value = str(df.iloc[row, col]).strip()
                    if cell_value and cell_value.lower() != "nan":
                        self.setItem(row, col, QTableWidgetItem(cell_value[:16]))
                    else:
                        btn = QPushButton("발행")
                        btn.clicked.connect(lambda checked, r=row, c=col: self.issue_invoice(r, c))
                        self.setCellWidget(row, col, btn)
                else:
                    value = df.iloc[row, col]
                    # NaN, None, "nan" 모두 빈 문자열로 처리
                    if pd.isna(value) or str(value).lower() == "nan":
                        value = ""
                    else:
                        # 숫자(정수/실수) 또는 숫자형 문자열이면 천단위 콤마 표시
                        try:
                            float_val = float(str(value).replace(",", ""))
                            # int로 변환 가능하면 정수, 아니면 소수
                            if float_val.is_integer():
                                value = f"{int(float_val):,}"
                            else:
                                value = f"{float_val:,.2f}"
                        except Exception:
                            # 숫자가 아니면 기존 방식
                            if pd.api.types.is_datetime64_any_dtype(df.iloc[:, col]):
                                value = str(value)[:10]
                            else:
                                value = str(value)
                    self.setItem(row, col, QTableWidgetItem(value))
                    
                        # 마지막 행: 합계 표시
        for col in range(len(df.columns)):
            col_name = str(df.columns[col])
            sum_value = ""
            # 숫자형 컬럼만 합계 계산
            try:
                # 콤마 제거 후 float 변환
                col_data = pd.to_numeric(df[col_name].astype(str).str.replace(",", ""), errors="coerce")
                if col_data.notna().any():
                    total = col_data.sum()
                    if pd.api.types.is_integer_dtype(col_data):
                        sum_value = f"{int(total):,}"
                    else:
                        sum_value = f"{total:,.2f}"
            except Exception:
                sum_value = ""
            if sum_value and sum_value != "0":
                self.setItem(len(df), col, QTableWidgetItem(f"{sum_value}"))
            else:
                self.setItem(len(df), col, QTableWidgetItem(""))

        # 합계 행 강조(선택)
        for col in range(len(df.columns)):
            item = self.item(len(df), col)
            if item:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                
        # 열 너비 지정 (예시: 번호, 공사명, 계약일, 착공일, 준공일, 메모)
        widths = [60, 200, 120, 120, 120, 300]
        for i, w in enumerate(widths):
            if i < self.columnCount():
                self.setColumnWidth(i, w)
        self.resizeColumnsToContents()
    
    def issue_invoice(self, row, col):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.removeCellWidget(row, col)
        self.setItem(row, col, QTableWidgetItem(now))
        col_name = self.df.columns[col]
        # "번호" 컬럼이 없으면 첫 번째 컬럼 사용
        if "번호" in self.df.columns:
            key_col = "번호"
        else:
            key_col = self.df.columns[0]  # 첫 번째 컬럼 사용(예: "공사명" 등)
        key_value = self.df.iloc[row][key_col]
        idx_all = self.df_all[self.df_all[key_col] == key_value].index[0]
        self.df_all.at[idx_all, col_name] = str(now)
        self.df.at[row, col_name] = str(now)
        self.df_all.to_excel(self.excel_path, index=False)

    def show_project_overview(self, row, col):
        from _2_project_overview_dialog import ProjectOverviewDialog

        project_info = {
            str(self.df.columns[i]): str(self.item(row, i).text()) if self.item(row, i) is not None else ""
            for i in range(self.columnCount())
        }
        
        def save_memo_callback(memo):
            self.df.at[row, "메모"] = memo
            # df_all에도 반영
            key_col = "번호"
            key_value = self.df.iloc[row][key_col]
            idx_all = self.df_all[self.df_all[key_col] == key_value].index[0]
            self.df_all.at[idx_all, "메모"] = memo
            self.setItem(row, self.df.columns.get_loc("메모"), QTableWidgetItem(memo))
            self.df_all.to_excel(self.excel_path, index=False)
            
            pass

        dialog = ProjectOverviewDialog(project_info, self, save_callback=save_memo_callback)
        dialog.exec()