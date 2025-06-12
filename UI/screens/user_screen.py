from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox, QLabel,
                             QLineEdit, QFormLayout, QDialog)
from PySide6.QtCore import Qt
from datetime import datetime

class UserScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 상단 버튼 영역
        button_layout = QHBoxLayout()
        
        # 사용자 추가 버튼
        self.add_btn = QPushButton('사용자 추가')
        self.add_btn.clicked.connect(self.add_user)
        button_layout.addWidget(self.add_btn)
        
        # 사용자 수정 버튼
        self.edit_btn = QPushButton('사용자 수정')
        self.edit_btn.clicked.connect(self.edit_user)
        button_layout.addWidget(self.edit_btn)
        
        # 사용자 삭제 버튼
        self.delete_btn = QPushButton('사용자 삭제')
        self.delete_btn.clicked.connect(self.delete_user)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            '사용자명', '아이디', '역할', '비고'
        ])
        layout.addWidget(self.table)
        
        # 데이터 로드
        self.load_users()
        
    def load_users(self):
        """사용자 목록 로드"""
        try:
            users = self.db.get_all_users()
            self.table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.table.setItem(row, 0, QTableWidgetItem(user[1]))  # 사용자명
                self.table.setItem(row, 1, QTableWidgetItem(user[2]))  # 아이디
                self.table.setItem(row, 2, QTableWidgetItem(user[3]))  # 역할
                self.table.setItem(row, 3, QTableWidgetItem(user[4]))  # 비고
                
        except Exception as e:
            print(f"사용자 목록 로드 중 오류 발생: {str(e)}")
            
    def add_user(self):
        """사용자 추가"""
        dialog = UserDialog(self)
        if dialog.exec():
            try:
                self.db.add_user(
                    dialog.name_edit.text(),
                    dialog.id_edit.text(),
                    dialog.role_edit.text(),
                    dialog.note_edit.text()
                )
                self.load_users()
            except Exception as e:
                print(f"사용자 추가 중 오류 발생: {str(e)}")
                
    def edit_user(self):
        """사용자 수정"""
        current_row = self.table.currentRow()
        if current_row < 0:
            print("수정할 사용자를 선택해주세요.")
            return
            
        try:
            user_id = self.db.get_all_users()[current_row][0]
            dialog = UserDialog(self)
            
            # 현재 데이터로 폼 채우기
            dialog.name_edit.setText(self.table.item(current_row, 0).text())
            dialog.id_edit.setText(self.table.item(current_row, 1).text())
            dialog.role_edit.setText(self.table.item(current_row, 2).text())
            dialog.note_edit.setText(self.table.item(current_row, 3).text())
            
            if dialog.exec():
                self.db.update_user(
                    user_id,
                    dialog.name_edit.text(),
                    dialog.id_edit.text(),
                    dialog.role_edit.text(),
                    dialog.note_edit.text()
                )
                self.load_users()
        except Exception as e:
            print(f"사용자 수정 중 오류 발생: {str(e)}")
            
    def delete_user(self):
        """사용자 삭제"""
        current_row = self.table.currentRow()
        if current_row < 0:
            print("삭제할 사용자를 선택해주세요.")
            return
            
        try:
            user_id = self.db.get_all_users()[current_row][0]
            self.db.delete_user(user_id)
            self.load_users()
        except Exception as e:
            print(f"사용자 삭제 중 오류 발생: {str(e)}")

class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('사용자 정보')
        layout = QFormLayout(self)
        
        # 입력 필드
        self.name_edit = QLineEdit()
        self.id_edit = QLineEdit()
        self.role_edit = QLineEdit()
        self.note_edit = QLineEdit()
        
        # 폼에 필드 추가
        layout.addRow('사용자명:', self.name_edit)
        layout.addRow('아이디:', self.id_edit)
        layout.addRow('역할:', self.role_edit)
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