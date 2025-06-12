import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QWidget, QFormLayout, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from datetime import datetime

from db.db_manager import DatabaseManager

class ContractScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 상단 버튼 영역
        button_layout = QHBoxLayout()
        
        # 계약 추가 버튼 (공사 추가와 동일)
        self.add_btn = QPushButton('계약 추가')
        self.add_btn.clicked.connect(self.add_contract)
        button_layout.addWidget(self.add_btn)
        
        # 계약 수정 버튼 (공사 수정과 동일)
        self.edit_btn = QPushButton('계약 수정')
        self.edit_btn.clicked.connect(self.edit_contract)
        button_layout.addWidget(self.edit_btn)
        
        # 계약 삭제 버튼 (공사 삭제와 동일)
        self.delete_btn = QPushButton('계약 삭제')
        self.delete_btn.clicked.connect(self.delete_contract)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            '계약번호', '계약명', '계약일', '계약금액', '발주처', '비고'
        ])
        
        # 컬럼 너비 설정
        self.table.setColumnWidth(0, 100)  # 계약번호
        self.table.setColumnWidth(1, 200)  # 계약명
        self.table.setColumnWidth(2, 100)  # 계약일
        self.table.setColumnWidth(3, 120)  # 계약금액
        self.table.setColumnWidth(4, 150)  # 발주처
        self.table.setColumnWidth(5, 200)  # 비고
        
        layout.addWidget(self.table)
        
        # 데이터 로드
        self.load_contracts()
        
    def load_contracts(self):
        """계약 목록 로드 (공사 목록과 동일)"""
        try:
            # projects 테이블에서 데이터를 가져옴 (계약 = 공사)
            contracts = self.db.get_all_projects()
            
            # 진행중인 계약만 필터링
            contracts = [c for c in contracts if c['status'] == 'ongoing']
            
            self.table.setRowCount(len(contracts))
            
            for row, contract in enumerate(contracts):
                # 계약번호 (공사번호와 동일)
                self.table.setItem(row, 0, QTableWidgetItem(contract['number']))
                
                # 계약명 (공사명과 동일)
                self.table.setItem(row, 1, QTableWidgetItem(contract['name']))
                
                # 계약일
                self.table.setItem(row, 2, QTableWidgetItem(contract['contract_date']))
                
                # 계약금액 (공사금액과 동일)
                amount = f"{contract['total_amount']:,.0f}"
                self.table.setItem(row, 3, QTableWidgetItem(amount))
                
                # 발주처
                self.table.setItem(row, 4, QTableWidgetItem(contract['client']))
                
                # 비고
                self.table.setItem(row, 5, QTableWidgetItem(contract['note'] or ''))
                
        except Exception as e:
            print(f"계약 목록 로드 중 오류 발생: {str(e)}")
            
    def add_contract(self):
        """계약 추가 (공사 추가와 동일)"""
        dialog = ContractDialog(self)
        if dialog.exec():
            try:
                # projects 테이블에 데이터 추가 (계약 = 공사)
                self.db.add_project(
                    dialog.number_edit.text(),  # 계약번호 (공사번호와 동일)
                    dialog.name_edit.text(),    # 계약명 (공사명과 동일)
                    dialog.date_edit.date().toString("yyyy-MM-dd"),  # 계약일
                    float(dialog.amount_edit.text()),  # 계약금액 (공사금액과 동일)
                    dialog.client_edit.text(),  # 발주처
                    dialog.note_edit.text()     # 비고
                )
                self.load_contracts()
            except Exception as e:
                print(f"계약 추가 중 오류 발생: {str(e)}")
                
    def edit_contract(self):
        """계약 수정 (공사 수정과 동일)"""
        current_row = self.table.currentRow()
        if current_row < 0:
            print("수정할 계약을 선택해주세요.")
            return
            
        try:
            dialog = ContractDialog(self)
            
            # 현재 데이터로 폼 채우기
            dialog.number_edit.setText(self.table.item(current_row, 0).text())  # 계약번호
            dialog.name_edit.setText(self.table.item(current_row, 1).text())    # 계약명
            
            # 날짜 문자열을 QDate로 변환
            date_str = self.table.item(current_row, 2).text()
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            dialog.date_edit.setDate(date)
            
            # 금액에서 쉼표 제거
            amount_str = self.table.item(current_row, 3).text().replace(',', '')
            dialog.amount_edit.setText(amount_str)
            
            dialog.client_edit.setText(self.table.item(current_row, 4).text())  # 발주처
            dialog.note_edit.setText(self.table.item(current_row, 5).text())    # 비고
            
            if dialog.exec():
                # projects 테이블의 데이터 수정 (계약 = 공사)
                project_id = self.db.get_all_projects()[current_row]['id']
                self.db.update_project(
                    project_id,
                    dialog.number_edit.text(),  # 계약번호
                    dialog.name_edit.text(),    # 계약명
                    dialog.date_edit.date().toString("yyyy-MM-dd"),  # 계약일
                    float(dialog.amount_edit.text()),  # 계약금액
                    dialog.client_edit.text(),  # 발주처
                    dialog.note_edit.text()     # 비고
                )
                self.load_contracts()
        except Exception as e:
            print(f"계약 수정 중 오류 발생: {str(e)}")
            
    def delete_contract(self):
        """계약 삭제 (공사 삭제와 동일)"""
        current_row = self.table.currentRow()
        if current_row < 0:
            print("삭제할 계약을 선택해주세요.")
            return
            
        try:
            # projects 테이블에서 데이터 삭제 (계약 = 공사)
            project_id = self.db.get_all_projects()[current_row]['id']
            self.db.delete_project(project_id)
            self.load_contracts()
        except Exception as e:
            print(f"계약 삭제 중 오류 발생: {str(e)}")

class ContractDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('계약 정보')
        layout = QFormLayout(self)
        
        # 입력 필드
        self.number_edit = QLineEdit()  # 계약번호
        self.name_edit = QLineEdit()    # 계약명
        self.date_edit = QDateEdit()    # 계약일
        self.date_edit.setCalendarPopup(True)  # 달력 팝업 활성화
        self.date_edit.setDate(QDate.currentDate())  # 현재 날짜로 초기화
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # 날짜 표시 형식
        self.amount_edit = QLineEdit()  # 계약금액
        self.client_edit = QLineEdit()  # 발주처
        self.note_edit = QLineEdit()    # 비고
        
        # 폼에 필드 추가
        layout.addRow('계약번호:', self.number_edit)
        layout.addRow('계약명:', self.name_edit)
        layout.addRow('계약일:', self.date_edit)
        layout.addRow('계약금액:', self.amount_edit)
        layout.addRow('발주처:', self.client_edit)
        layout.addRow('비고:', self.note_edit)
        
        # 버튼
        button_layout = QHBoxLayout()
        save_btn = QPushButton('저장')
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton('취소')
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)

class ContractManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("계약 관리")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # 검색 영역
        search_layout = QHBoxLayout()
        search_label = QLabel("검색:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("계약 코드, 이름, 계약자로 검색")
        self.search_input.textChanged.connect(self.search_contracts)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "계약 코드", "계약명", "계약자", "계약일",
            "계약금액", "상태", "설명"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        add_button = QPushButton("추가")
        add_button.clicked.connect(self.add_contract)
        edit_button = QPushButton("수정")
        edit_button.clicked.connect(self.edit_contract)
        delete_button = QPushButton("삭제")
        delete_button.clicked.connect(self.delete_contract)
        refresh_button = QPushButton("새로고침")
        refresh_button.clicked.connect(self.load_contracts)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.load_contracts()
        
    def load_contracts(self):
        try:
            contracts = self.db.get_all_projects()
            self.display_contracts(contracts)
        except Exception as e:
            print(f"계약 목록을 불러오는 중 오류가 발생했습니다: {str(e)}")
            
    def display_contracts(self, contracts):
        self.table.setRowCount(len(contracts))
        for i, contract in enumerate(contracts):
            self.table.setItem(i, 0, QTableWidgetItem(contract['code']))
            self.table.setItem(i, 1, QTableWidgetItem(contract['name']))
            self.table.setItem(i, 2, QTableWidgetItem(contract['contractor']))
            self.table.setItem(i, 3, QTableWidgetItem(contract['contract_date']))
            self.table.setItem(i, 4, QTableWidgetItem(str(contract['amount'])))
            self.table.setItem(i, 5, QTableWidgetItem(contract['status']))
            self.table.setItem(i, 6, QTableWidgetItem(contract['description']))
            
    def search_contracts(self):
        search_text = self.search_input.text().lower()
        contracts = self.db.get_all_contracts()
        filtered_contracts = [
            c for c in contracts
            if search_text in c['code'].lower() or
               search_text in c['name'].lower() or
               search_text in c['contractor'].lower()
        ]
        self.display_contracts(filtered_contracts)
        
    def get_selected_contract(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            contract = {
                'id': current_row + 1,  # 임시 ID
                'code': self.table.item(current_row, 0).text(),
                'name': self.table.item(current_row, 1).text(),
                'contractor': self.table.item(current_row, 2).text(),
                'contract_date': self.table.item(current_row, 3).text(),
                'amount': float(self.table.item(current_row, 4).text()),
                'status': self.table.item(current_row, 5).text(),
                'description': self.table.item(current_row, 6).text()
            }
            return contract
        return None
        
    def add_contract(self):
        dialog = ContractDialog(self)
        if dialog.exec():
            self.load_contracts()
            
    def edit_contract(self):
        contract = self.get_selected_contract()
        if contract:
            dialog = ContractDialog(self, contract)
            if dialog.exec():
                self.load_contracts()
        else:
            QMessageBox.warning(self, "경고", "수정할 계약을 선택해주세요.")
            
    def delete_contract(self):
        contract = self.get_selected_contract()
        if contract:
            reply = QMessageBox.question(
                self, "확인",
                f"계약 '{contract['name']}'을(를) 삭제하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    self.db.delete_contract(contract['id'])
                    self.load_contracts()
                    QMessageBox.information(self, "성공", "계약이 삭제되었습니다.")
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"계약 삭제 중 오류가 발생했습니다: {str(e)}")
        else:
            QMessageBox.warning(self, "경고", "삭제할 계약을 선택해주세요.") 