from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QDateEdit,
    QTextEdit, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt, QDate

class ContractDocumentScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 상단 버튼 영역
        button_layout = QHBoxLayout()
        
        # 계약서 작성 버튼
        self.create_btn = QPushButton('계약서 작성')
        self.create_btn.clicked.connect(self.create_contract_document)
        button_layout.addWidget(self.create_btn)
        
        # 계약서 조회 버튼
        self.view_btn = QPushButton('계약서 조회')
        self.view_btn.clicked.connect(self.view_contract_document)
        button_layout.addWidget(self.view_btn)
        
        layout.addLayout(button_layout)
        
        # 계약서 작성 폼
        form_layout = QFormLayout()
        
        # 계약 선택
        self.contract_combo = QComboBox()
        self.load_contracts()
        form_layout.addRow('계약 선택:', self.contract_combo)
        
        # 계약서 작성일
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow('계약서 작성일:', self.date_edit)
        
        # 계약서 내용
        self.content_edit = QTextEdit()
        form_layout.addRow('계약서 내용:', self.content_edit)
        
        layout.addLayout(form_layout)
        
    def load_contracts(self):
        """계약 목록 로드"""
        try:
            contracts = self.db.get_all_projects()
            self.contract_combo.clear()
            for contract in contracts:
                self.contract_combo.addItem(f"{contract['name']} ({contract['number']})", contract['id'])
        except Exception as e:
            print(f"계약 목록 로드 중 오류 발생: {str(e)}")
            
    def create_contract_document(self):
        """계약서 작성"""
        try:
            contract_id = self.contract_combo.currentData()
            date = self.date_edit.date().toString("yyyy-MM-dd")
            content = self.content_edit.toPlainText()
            
            # TODO: 계약서 저장 로직 구현
            
            print("계약서가 작성되었습니다.")
        except Exception as e:
            print(f"계약서 작성 중 오류 발생: {str(e)}")
            
    def view_contract_document(self):
        """계약서 조회"""
        try:
            contract_id = self.contract_combo.currentData()
            
            # TODO: 계약서 조회 로직 구현
            
            print("계약서를 조회합니다.")
        except Exception as e:
            print(f"계약서 조회 중 오류 발생: {str(e)}") 