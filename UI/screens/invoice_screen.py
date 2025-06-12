from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QDateEdit,
    QTextEdit, QFormLayout, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt, QDate

class InvoiceScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 상단 버튼 영역
        button_layout = QHBoxLayout()
        
        # 청구서 작성 버튼
        self.create_btn = QPushButton('청구서 작성')
        self.create_btn.clicked.connect(self.create_invoice)
        button_layout.addWidget(self.create_btn)
        
        # 청구서 조회 버튼
        self.view_btn = QPushButton('청구서 조회')
        self.view_btn.clicked.connect(self.view_invoice)
        button_layout.addWidget(self.view_btn)
        
        layout.addLayout(button_layout)
        
        # 청구서 작성 폼
        form_layout = QFormLayout()
        
        # 계약 선택
        self.contract_combo = QComboBox()
        self.load_contracts()
        form_layout.addRow('계약 선택:', self.contract_combo)
        
        # 청구일
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow('청구일:', self.date_edit)
        
        # 청구금액
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0, 1000000000000)
        self.amount_spin.setDecimals(0)
        self.amount_spin.setSingleStep(1000000)
        form_layout.addRow('청구금액:', self.amount_spin)
        
        # 청구서 내용
        self.content_edit = QTextEdit()
        form_layout.addRow('청구서 내용:', self.content_edit)
        
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
            
    def create_invoice(self):
        """청구서 작성"""
        try:
            contract_id = self.contract_combo.currentData()
            date = self.date_edit.date().toString("yyyy-MM-dd")
            amount = self.amount_spin.value()
            content = self.content_edit.toPlainText()
            
            # TODO: 청구서 저장 로직 구현
            
            print("청구서가 작성되었습니다.")
        except Exception as e:
            print(f"청구서 작성 중 오류 발생: {str(e)}")
            
    def view_invoice(self):
        """청구서 조회"""
        try:
            contract_id = self.contract_combo.currentData()
            
            # TODO: 청구서 조회 로직 구현
            
            print("청구서를 조회합니다.")
        except Exception as e:
            print(f"청구서 조회 중 오류 발생: {str(e)}") 