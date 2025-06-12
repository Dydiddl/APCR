from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QFormLayout, QDateEdit)
from PySide6.QtCore import Qt, QDate

class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('공사 정보')
        layout = QFormLayout(self)
        
        # 입력 필드
        self.number_edit = QLineEdit()  # 공사번호
        self.name_edit = QLineEdit()    # 공사명
        self.date_edit = QDateEdit()    # 계약일
        self.date_edit.setCalendarPopup(True)  # 달력 팝업 활성화
        self.date_edit.setDate(QDate.currentDate())  # 현재 날짜로 초기화
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # 날짜 표시 형식
        self.amount_edit = QLineEdit()  # 공급가액
        self.client_edit = QLineEdit()  # 발주처
        self.note_edit = QLineEdit()    # 비고
        
        # 폼에 필드 추가
        layout.addRow('공사번호:', self.number_edit)
        layout.addRow('공사명:', self.name_edit)
        layout.addRow('계약일:', self.date_edit)
        layout.addRow('공급가액:', self.amount_edit)
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