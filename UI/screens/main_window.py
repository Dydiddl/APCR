import sys
import os
from pathlib import Path

# 현재 파일 기준으로 프로젝트 루트 경로를 sys.path에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QStackedWidget, QMessageBox, QDialog, QDateEdit, QFormLayout, QLineEdit, QSpinBox,
                              QDoubleSpinBox, QTextEdit, QComboBox, QTabWidget)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon, QAction

from db.db_manager import DatabaseManager
from UI.screens.project_screen import ProjectScreen
from UI.screens.contract_screen import ContractScreen
from UI.screens.user_screen import UserScreen
from UI.screens.login_screen import LoginDialog
from UI.screens.project_dialog import ProjectDialog
from UI.screens.contract_document_screen import ContractDocumentScreen
from UI.screens.start_report_screen import StartReportScreen
from UI.screens.completion_report_screen import CompletionReportScreen
from UI.screens.invoice_screen import InvoiceScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_user = {'username': 'admin', 'role': 'admin'}  # 임시 테스트용 사용자
        self.init_ui()
        # self.show_login()  # 로그인 화면 표시 주석 처리

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('건설 프로젝트 관리 시스템')
        self.setMinimumSize(1200, 800)
        
        # 메뉴바 생성
        menubar = self.menuBar()
        
        # 계약 관리 메뉴
        contract_menu = menubar.addMenu('계약 관리')
        
        # 계약 관리
        contract_management_action = QAction('계약 관리', self)
        contract_management_action.triggered.connect(self.show_contract_management)
        contract_menu.addAction(contract_management_action)
        
        # 구분선 추가
        contract_menu.addSeparator()
        
        # 계약서 작성
        contract_doc_action = QAction('계약서 작성', self)
        contract_doc_action.triggered.connect(self.show_contract_document)
        contract_menu.addAction(contract_doc_action)
        
        # 착공계 작성
        start_report_action = QAction('착공계 작성', self)
        start_report_action.triggered.connect(self.show_start_report)
        contract_menu.addAction(start_report_action)
        
        # 준공계 작성
        completion_report_action = QAction('준공계 작성', self)
        completion_report_action.triggered.connect(self.show_completion_report)
        contract_menu.addAction(completion_report_action)
        
        # 청구서 작성
        invoice_action = QAction('청구서 작성', self)
        invoice_action.triggered.connect(self.show_invoice)
        contract_menu.addAction(invoice_action)
        
        # 공사 대장 메뉴
        project_menu = menubar.addMenu('공사 대장')
        
        # 진행중 공사
        ongoing_action = QAction('진행중 공사', self)
        ongoing_action.triggered.connect(self.show_ongoing_projects)
        project_menu.addAction(ongoing_action)
        
        # 구분선 추가
        project_menu.addSeparator()
        
        # 공사 목록
        project_action = QAction('공사 목록', self)
        project_action.triggered.connect(self.show_all_projects)
        project_menu.addAction(project_action)
        
        # 완료된 공사
        completed_action = QAction('완료된 공사', self)
        completed_action.triggered.connect(self.show_completed_projects)
        project_menu.addAction(completed_action)
        
        # 사용자 관리 메뉴 (관리자만 표시)
        if self.current_user.get('role') == 'admin':
            user_menu = menubar.addMenu('사용자 관리')
            user_action = QAction('사용자 목록', self)
            user_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_screen))
            user_menu.addAction(user_action)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 레이아웃 설정
        layout = QVBoxLayout(central_widget)
        
        # 스택 위젯 생성
        self.stacked_widget = QStackedWidget()
        
        # 각 화면 초기화
        self.project_screen = ProjectScreen(self.db)
        self.contract_screen = ContractScreen(self.db)
        self.user_screen = UserScreen(self.db)
        self.contract_document_screen = ContractDocumentScreen(self.db)
        self.start_report_screen = StartReportScreen(self.db)
        self.completion_report_screen = CompletionReportScreen(self.db)
        self.invoice_screen = InvoiceScreen(self.db)
        
        # 스택 위젯에 화면 추가
        self.stacked_widget.addWidget(self.project_screen)
        self.stacked_widget.addWidget(self.contract_screen)
        self.stacked_widget.addWidget(self.user_screen)
        self.stacked_widget.addWidget(self.contract_document_screen)
        self.stacked_widget.addWidget(self.start_report_screen)
        self.stacked_widget.addWidget(self.completion_report_screen)
        self.stacked_widget.addWidget(self.invoice_screen)
        
        layout.addWidget(self.stacked_widget)
        
        # 초기 화면을 진행중 공사로 설정
        self.show_ongoing_projects()
        
        # 상태 표시줄
        self.statusBar().showMessage(f'환영합니다, {self.current_user["username"]}님!')

    def show_login(self):
        login_dialog = LoginDialog(self)
        if login_dialog.exec() == QDialog.Accepted:
            self.current_user = login_dialog.current_user
            self.user_btn.setVisible(self.current_user.get('role') == 'admin')
            print(f"로그인 성공: {self.current_user['username']}")
        else:
            print("로그인 실패")
            self.close()

    def closeEvent(self, event):
        """창 닫을 때 이벤트 처리"""
        event.accept()

    def add_project(self):
        """공사 추가"""
        dialog = ProjectDialog(self)
        if dialog.exec():
            try:
                self.db.add_project(
                    dialog.number_edit.text(),  # 공사번호
                    dialog.name_edit.text(),    # 공사명
                    dialog.date_edit.date().toString("yyyy-MM-dd"),  # 계약일
                    float(dialog.amount_edit.text()),  # 공급가액
                    dialog.client_edit.text(),  # 발주처
                    dialog.note_edit.text()     # 비고
                )
                self.project_screen.load_projects()
            except Exception as e:
                print(f"공사 추가 중 오류 발생: {str(e)}")
                
    def edit_project(self):
        """공사 수정"""
        current_row = self.project_screen.table.currentRow()
        if current_row < 0:
            print("수정할 공사를 선택해주세요.")
            return
            
        try:
            project_id = self.project_screen.table.item(current_row, 0).data(Qt.UserRole)
            dialog = ProjectDialog(self)
            
            # 현재 데이터로 폼 채우기
            dialog.number_edit.setText(self.project_screen.table.item(current_row, 1).text())
            dialog.name_edit.setText(self.project_screen.table.item(current_row, 2).text())
            
            # 날짜 문자열을 QDate로 변환
            date_str = self.project_screen.table.item(current_row, 3).text()
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            dialog.date_edit.setDate(date)
            
            dialog.amount_edit.setText(self.project_screen.table.item(current_row, 4).text())
            dialog.client_edit.setText(self.project_screen.table.item(current_row, 7).text())
            dialog.note_edit.setText(self.project_screen.table.item(current_row, 8).text())
            
            if dialog.exec():
                self.db.update_project(
                    project_id,
                    dialog.number_edit.text(),  # 공사번호
                    dialog.name_edit.text(),    # 공사명
                    dialog.date_edit.date().toString("yyyy-MM-dd"),  # 계약일
                    float(dialog.amount_edit.text()),  # 공급가액
                    dialog.client_edit.text(),  # 발주처
                    dialog.note_edit.text()     # 비고
                )
                self.project_screen.load_projects()
        except Exception as e:
            print(f"공사 수정 중 오류 발생: {str(e)}")
            
    def delete_project(self):
        """공사 삭제"""
        current_row = self.project_screen.table.currentRow()
        if current_row < 0:
            print("삭제할 공사를 선택해주세요.")
            return
            
        try:
            project_id = self.project_screen.table.item(current_row, 0).data(Qt.UserRole)
            self.db.delete_project(project_id)
            self.project_screen.load_projects()
        except Exception as e:
            print(f"공사 삭제 중 오류 발생: {str(e)}")

    def show_contract_document(self):
        """계약서 작성 화면 표시"""
        self.stacked_widget.setCurrentWidget(self.contract_document_screen)
        self.setWindowTitle('계약서 작성')
        
    def show_start_report(self):
        """착공계 작성 화면 표시"""
        self.stacked_widget.setCurrentWidget(self.start_report_screen)
        self.setWindowTitle('착공계 작성')
        
    def show_completion_report(self):
        """준공계 작성 화면 표시"""
        self.stacked_widget.setCurrentWidget(self.completion_report_screen)
        self.setWindowTitle('준공계 작성')
        
    def show_invoice(self):
        """청구서 작성 화면 표시"""
        self.stacked_widget.setCurrentWidget(self.invoice_screen)
        self.setWindowTitle('청구서 작성')
        
    def show_contract_management(self):
        """계약 관리 화면 표시"""
        self.stacked_widget.setCurrentWidget(self.contract_screen)
        self.setWindowTitle('계약 관리')
        
    def show_ongoing_projects(self):
        """진행중인 공사 표시"""
        self.stacked_widget.setCurrentWidget(self.project_screen)
        self.project_screen.show_ongoing_projects()
        
    def show_all_projects(self):
        """모든 공사 표시"""
        self.stacked_widget.setCurrentWidget(self.project_screen)
        self.project_screen.show_all_projects()
        
    def show_completed_projects(self):
        """완료된 공사 표시"""
        self.stacked_widget.setCurrentWidget(self.project_screen)
        self.project_screen.show_completed_projects() 