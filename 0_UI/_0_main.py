import sys
import pandas as pd
import os

from PySide6.QtWidgets import (
    
    QApplication, 
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QTableWidget, 
    QTableWidgetItem, 
    QLabel,
    QTextEdit
    
)
from PySide6.QtGui import QAction

from _1_1_search_dialog import SearchDialog
from _2_table_widget import ExcelTableWidget
from _1_2_new_construction import NewConstructionDialog
from _1_3_completed_construction import CompletedConstructionDialog


# 아래 import들은 각 메뉴별 기능 구현 파일이 준비되면 추가하세요.
# from _1_construction_tab import ConstructionTabWidget
# from _2_contract_input_dialog import ContractInputDialog

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Automation project for construction records(APCR)")
        self.setGeometry(200, 200, 800, 500)
    
        menubar = self.menuBar()

        # 메뉴 생성
        menu_construction = menubar.addMenu("공사")
        menu_contract = menubar.addMenu("계약")
        menu_history = menubar.addMenu("내역")
        menu_bid = menubar.addMenu("입찰")
        menu_labor = menubar.addMenu("노무")
        menu_equipment = menubar.addMenu("장비")

        # 각 메뉴에 예시 액션 추가 (필요시 실제 기능 연결)
        action_construction = QAction("검색", self)
        action_construction.triggered.connect(self.open_search_dialog)  # 시그널 연결
        menu_construction.addAction(action_construction)
        action_new_construction = QAction("신규 공사", self)
        action_new_construction.triggered.connect(self.open_new_construction_dialog)  # 시그널 연결
        menu_construction.addAction(action_new_construction)
        action_completed = QAction("완료 공사", self)
        action_completed.triggered.connect(self.open_completed_construction_dialog)
        menu_construction.addAction(action_completed)

        action_contract = QAction("계약 관리", self)
        menu_contract.addAction(action_contract)

        action_history = QAction("내역 관리", self)
        menu_history.addAction(action_history)

        action_bid = QAction("입찰 관리", self)
        menu_bid.addAction(action_bid)

        action_labor = QAction("노무 관리", self)
        menu_labor.addAction(action_labor)

        action_equipment = QAction("장비 관리", self)
        menu_equipment.addAction(action_equipment)

 # 중앙 위젯에 제목 + 표 배치
        central_widget = QWidget()
        layout = QVBoxLayout()
        title_label = QLabel("진행중 공사")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(base_dir, "../Test.xlsx")
        self.table_widget = ExcelTableWidget(excel_path)
        layout.addWidget(self.table_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
        
    def open_search_dialog(self):
        dialog = SearchDialog(self)
        dialog.exec()
         
    def open_new_construction_dialog(self):
        dialog = NewConstructionDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            # 다음 번호 계산
            if "번호" in self.table_widget.df_all.columns:
                if not self.table_widget.df_all.empty:
                    next_no = int(self.table_widget.df_all["번호"].max()) + 1
                else:
                    next_no = 1
            else:
                next_no = 1
                self.table_widget.df_all["번호"] = []
            # 새 행 추가
            new_row = {
                "번호": next_no,
                "공사명": data["공사명"],
                "계약일": data["계약일"],
                "계약금액": data["계약금액"],
                "공사종료": 0
            }
            # 누락 컬럼 보완
            for col in self.table_widget.df_all.columns:
                if col not in new_row:
                    new_row[col] = ""
            self.table_widget.df_all = pd.concat(
                [self.table_widget.df_all, pd.DataFrame([new_row])],
                ignore_index=True
            )
            self.table_widget.df_all.to_excel(self.table_widget.excel_path, index=False)
            self.table_widget.show_active_projects()
    
    def open_completed_construction_dialog(self):
        dialog = CompletedConstructionDialog(self)
        dialog.exec()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()