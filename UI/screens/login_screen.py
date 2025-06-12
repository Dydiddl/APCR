from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.db_manager import DatabaseManager

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.current_user = None
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('로그인')
        self.setFixedSize(400, 200)
        
        # 메인 레이아웃
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # 제목
        title_label = QLabel('건설 프로젝트 관리 시스템')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 사용자명 입력
        username_layout = QHBoxLayout()
        username_label = QLabel('사용자명:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('사용자명을 입력하세요')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # 비밀번호 입력
        password_layout = QHBoxLayout()
        password_label = QLabel('비밀번호:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('비밀번호를 입력하세요')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        # 로그인 버튼
        login_button = QPushButton('로그인')
        login_button.setFixedWidth(100)
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)
        
        # 취소 버튼
        cancel_button = QPushButton('취소')
        cancel_button.setFixedWidth(100)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # 엔터 키 이벤트 연결
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(self.login)
        
        self.setLayout(layout)
    
    def login(self):
        """로그인 처리"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, '경고', '사용자명과 비밀번호를 입력하세요.')
            return
        
        try:
            if self.db.verify_user(username, password):
                self.current_user = self.db.get_user(username)
                self.accept()
            else:
                QMessageBox.warning(self, '로그인 실패', '사용자명 또는 비밀번호가 올바르지 않습니다.')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'로그인 중 오류가 발생했습니다: {str(e)}')
    
    def closeEvent(self, event):
        """창 닫을 때 데이터베이스 연결 종료"""
        self.db.close()
        event.accept() 