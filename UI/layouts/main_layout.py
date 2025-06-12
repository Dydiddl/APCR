from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class MainLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        # 메인 레이아웃
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # 상단 툴바 레이아웃
        self.toolbar_layout = QHBoxLayout()
        self.main_layout.addLayout(self.toolbar_layout)
        
        # 컨텐츠 영역 레이아웃
        self.content_layout = QVBoxLayout()
        self.main_layout.addLayout(self.content_layout)
        
        # 상태바 레이아웃
        self.statusbar_layout = QHBoxLayout()
        self.main_layout.addLayout(self.statusbar_layout)
        
        # 레이아웃 간격 설정
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10) 