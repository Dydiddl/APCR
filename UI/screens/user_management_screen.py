from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.db_manager import DatabaseManager

class UserManagementDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('사용자 관리')
        self.setGeometry(100, 100, 800, 600)
        
        # 메인 레이아웃
        layout = QVBoxLayout()
        
        # 검색 영역
        search_layout = QHBoxLayout()
        search_label = QLabel('검색:')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('사용자명 또는 이메일로 검색')
        self.search_input.textChanged.connect(self.search_users)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 사용자 목록 테이블
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(['ID', '사용자명', '이메일', '역할', '상태', '마지막 로그인'])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.user_table)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 사용자 추가 버튼
        add_button = QPushButton('사용자 추가')
        add_button.clicked.connect(self.add_user)
        button_layout.addWidget(add_button)
        
        # 사용자 수정 버튼
        edit_button = QPushButton('사용자 수정')
        edit_button.clicked.connect(self.edit_user)
        button_layout.addWidget(edit_button)
        
        # 사용자 삭제 버튼
        delete_button = QPushButton('사용자 삭제')
        delete_button.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_button)
        
        # 새로고침 버튼
        refresh_button = QPushButton('새로고침')
        refresh_button.clicked.connect(self.load_users)
        button_layout.addWidget(refresh_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_users(self):
        """사용자 목록 로드"""
        try:
            users = self.db.get_all_users()
            self.user_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user['user_id'])))
                self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))
                self.user_table.setItem(row, 2, QTableWidgetItem(user['email']))
                self.user_table.setItem(row, 3, QTableWidgetItem(user['role']))
                self.user_table.setItem(row, 4, QTableWidgetItem('활성' if user['is_active'] else '비활성'))
                self.user_table.setItem(row, 5, QTableWidgetItem(user['last_login'] or '-'))
        except Exception as e:
            QMessageBox.critical(self, '오류', f'사용자 목록을 불러오는 중 오류가 발생했습니다: {str(e)}')
    
    def search_users(self):
        """사용자 검색"""
        search_text = self.search_input.text().lower()
        for row in range(self.user_table.rowCount()):
            show_row = False
            for col in range(2):  # 사용자명과 이메일 컬럼만 검색
                item = self.user_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.user_table.setRowHidden(row, not show_row)
    
    def get_selected_user(self):
        """선택된 사용자 정보 반환"""
        selected_rows = self.user_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, '경고', '사용자를 선택하세요.')
            return None
        
        row = selected_rows[0].row()
        return {
            'user_id': int(self.user_table.item(row, 0).text()),
            'username': self.user_table.item(row, 1).text(),
            'email': self.user_table.item(row, 2).text(),
            'role': self.user_table.item(row, 3).text(),
            'is_active': self.user_table.item(row, 4).text() == '활성'
        }
    
    def add_user(self):
        """사용자 추가"""
        dialog = UserDialog(self.db)
        if dialog.exec() == QDialog.Accepted:
            self.load_users()
    
    def edit_user(self):
        """사용자 수정"""
        user = self.get_selected_user()
        if user:
            dialog = UserDialog(self.db, user)
            if dialog.exec() == QDialog.Accepted:
                self.load_users()
    
    def delete_user(self):
        """사용자 삭제"""
        user = self.get_selected_user()
        if user:
            reply = QMessageBox.question(
                self, '사용자 삭제',
                f'사용자 "{user["username"]}"을(를) 삭제하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    self.db.delete_user(user['username'])
                    self.load_users()
                    QMessageBox.information(self, '성공', '사용자가 삭제되었습니다.')
                except Exception as e:
                    QMessageBox.critical(self, '오류', f'사용자 삭제 중 오류가 발생했습니다: {str(e)}')

class UserDialog(QDialog):
    def __init__(self, db_manager, user_data=None, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.user_data = user_data
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('사용자 추가' if not self.user_data else '사용자 수정')
        self.setFixedSize(400, 300)
        
        # 메인 레이아웃
        layout = QVBoxLayout()
        
        # 사용자명 입력
        username_layout = QHBoxLayout()
        username_label = QLabel('사용자명:')
        self.username_input = QLineEdit()
        if self.user_data:
            self.username_input.setText(self.user_data['username'])
            self.username_input.setReadOnly(True)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # 비밀번호 입력
        password_layout = QHBoxLayout()
        password_label = QLabel('비밀번호:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        if not self.user_data:
            self.password_input.setPlaceholderText('새 사용자의 비밀번호를 입력하세요')
        else:
            self.password_input.setPlaceholderText('변경하려면 입력하세요')
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # 이메일 입력
        email_layout = QHBoxLayout()
        email_label = QLabel('이메일:')
        self.email_input = QLineEdit()
        if self.user_data:
            self.email_input.setText(self.user_data['email'])
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)
        
        # 역할 선택
        role_layout = QHBoxLayout()
        role_label = QLabel('역할:')
        self.role_combo = QComboBox()
        self.role_combo.addItems(['관리자', '일반사용자'])
        if self.user_data:
            self.role_combo.setCurrentText(self.user_data['role'])
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)
        
        # 상태 선택
        status_layout = QHBoxLayout()
        status_label = QLabel('상태:')
        self.status_combo = QComboBox()
        self.status_combo.addItems(['활성', '비활성'])
        if self.user_data:
            self.status_combo.setCurrentText('활성' if self.user_data['is_active'] else '비활성')
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_combo)
        layout.addLayout(status_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 저장 버튼
        save_button = QPushButton('저장')
        save_button.clicked.connect(self.save_user)
        button_layout.addWidget(save_button)
        
        # 취소 버튼
        cancel_button = QPushButton('취소')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_user(self):
        """사용자 정보 저장"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        email = self.email_input.text().strip()
        role = self.role_combo.currentText()
        is_active = self.status_combo.currentText() == '활성'
        
        if not username or not email:
            QMessageBox.warning(self, '경고', '사용자명과 이메일은 필수 입력 항목입니다.')
            return
        
        if not self.user_data and not password:
            QMessageBox.warning(self, '경고', '새 사용자의 비밀번호를 입력하세요.')
            return
        
        try:
            if self.user_data:  # 사용자 수정
                user_data = {
                    'email': email,
                    'role': role,
                    'is_active': is_active
                }
                self.db.update_user(username, user_data)
                
                if password:  # 비밀번호 변경
                    self.db.update_password(username, password)
                
                QMessageBox.information(self, '성공', '사용자 정보가 수정되었습니다.')
            else:  # 새 사용자 추가
                user_data = {
                    'username': username,
                    'password': password,
                    'email': email,
                    'role': role,
                    'is_active': is_active
                }
                self.db.add_user(user_data)
                QMessageBox.information(self, '성공', '새 사용자가 추가되었습니다.')
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, '오류', f'사용자 정보 저장 중 오류가 발생했습니다: {str(e)}') 