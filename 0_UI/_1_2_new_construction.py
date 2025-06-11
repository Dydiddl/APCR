from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate

class NewConstructionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("신규 공사 등록")
        layout = QVBoxLayout()

        # 공사명 입력
        name_layout = QHBoxLayout()
        name_label = QLabel("공사명:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # 계약일 입력
        date_layout = QHBoxLayout()
        date_label = QLabel("계약일:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        # 계약금액 입력
        amount_layout = QHBoxLayout()
        amount_label = QLabel("계약금액:")
        self.amount_edit = QLineEdit()
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_edit)
        layout.addLayout(amount_layout)

        # 등록 버튼
        btn = QPushButton("등록")
        btn.clicked.connect(self.on_accept)
        layout.addWidget(btn)

        self.setLayout(layout)

    def on_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "입력 오류", "공사명을 입력하세요.")
            return
        if not self.amount_edit.text().strip().replace(",", "").isdigit():
            QMessageBox.warning(self, "입력 오류", "계약금액을 숫자로 입력하세요.")
            return
        self.accept()

    def get_data(self):
        return {
            "공사명": self.name_edit.text().strip(),
            "계약일": self.date_edit.date().toString("yyyy-MM-dd"),
            "계약금액": self.amount_edit.text().replace(",", "").strip()
        }