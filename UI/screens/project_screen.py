import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QWidget, QFormLayout, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime

from db.db_manager import DatabaseManager

class ProjectScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_filter = None
        self.is_updating = False  # 상태 업데이트 중인지 확인하는 플래그
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 검색 영역
        search_layout = QHBoxLayout()
        search_label = QLabel("검색:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("공사번호, 공사명, 발주처로 검색")
        self.search_input.textChanged.connect(self.search_projects)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(10)  # 컬럼 수 증가
        self.table.setHorizontalHeaderLabels([
            'ID', '공사번호', '공사명', '계약일', '공급가액', '부가세', '계약금액', '발주처', '비고', '공사 종료'
        ])
        
        # 컬럼 너비 설정
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 100)  # 공사번호
        self.table.setColumnWidth(2, 200)  # 공사명
        self.table.setColumnWidth(3, 100)  # 계약일
        self.table.setColumnWidth(4, 120)  # 공급가액
        self.table.setColumnWidth(5, 100)  # 부가세
        self.table.setColumnWidth(6, 120)  # 계약금액
        self.table.setColumnWidth(7, 150)  # 발주처
        self.table.setColumnWidth(8, 200)  # 비고
        self.table.setColumnWidth(9, 100)  # 상태
        
        # ID 컬럼 숨기기
        self.table.hideColumn(0)
        
        # itemChanged 이벤트 연결
        self.table.itemChanged.connect(self.handle_status_change)
        
        layout.addWidget(self.table)
        
        # 초기 데이터 로드
        self.load_projects()
        
    def search_projects(self):
        """공사 검색"""
        if self.is_updating:  # 업데이트 중이면 검색 중단
            return
            
        search_text = self.search_input.text().lower()
        try:
            projects = self.db.get_all_projects()
            
            # 필터링
            if self.current_filter:
                projects = [p for p in projects if p['status'] == self.current_filter]
            
            # 검색어로 필터링
            if search_text:
                projects = [p for p in projects if 
                    search_text in p['number'].lower() or
                    search_text in p['name'].lower() or
                    search_text in p['client'].lower()
                ]
            
            self.table.setRowCount(len(projects))
            
            # itemChanged 이벤트 일시 중단
            self.table.blockSignals(True)
            
            for row, project in enumerate(projects):
                # ID (UserRole로 저장)
                id_item = QTableWidgetItem()
                id_item.setData(Qt.UserRole, project['id'])
                self.table.setItem(row, 0, id_item)
                
                # 공사번호
                self.table.setItem(row, 1, QTableWidgetItem(project['number']))
                
                # 공사명
                self.table.setItem(row, 2, QTableWidgetItem(project['name']))
                
                # 계약일
                self.table.setItem(row, 3, QTableWidgetItem(project['contract_date']))
                
                # 공급가액
                supply_amount = f"{project['supply_amount']:,.0f}"
                self.table.setItem(row, 4, QTableWidgetItem(supply_amount))
                
                # 부가세
                tax_amount = f"{project['tax_amount']:,.0f}"
                self.table.setItem(row, 5, QTableWidgetItem(tax_amount))
                
                # 계약금액
                total_amount = f"{project['total_amount']:,.0f}"
                self.table.setItem(row, 6, QTableWidgetItem(total_amount))
                
                # 발주처
                self.table.setItem(row, 7, QTableWidgetItem(project['client']))
                
                # 비고
                self.table.setItem(row, 8, QTableWidgetItem(project['note'] or ''))
                
                # 상태 (1: 완료, 빈칸: 진행중)
                status_item = QTableWidgetItem('1' if project['status'] == 'completed' else '')
                status_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 9, status_item)
            
            # itemChanged 이벤트 다시 활성화
            self.table.blockSignals(False)
                
        except Exception as e:
            print(f"공사 검색 중 오류 발생: {str(e)}")
            
    def handle_status_change(self, item):
        """상태 변경 처리"""
        if item.column() == 9:  # 상태 컬럼
            try:
                self.is_updating = True  # 업데이트 시작
                
                row = item.row()
                project_id = self.table.item(row, 0).data(Qt.UserRole)
                
                # 입력값이 1이면 완료, 그 외는 진행중
                status = 'completed' if item.text() == '1' else 'ongoing'
                
                # 데이터베이스 업데이트
                self.db.update_project_status(project_id, status)
                
                # 현재 필터에 따라 목록 새로고침
                if self.current_filter:
                    self.search_projects()
                else:
                    self.load_projects()
                    
            except Exception as e:
                print(f"상태 변경 중 오류 발생: {str(e)}")
                # 오류 발생 시 이전 상태로 복원
                item.setText('1' if status == 'completed' else '')
            finally:
                self.is_updating = False  # 업데이트 종료
            
    def load_projects(self, status_filter=None):
        """공사 목록 로드"""
        self.current_filter = status_filter
        self.search_projects()  # 검색 기능을 통해 목록 로드
        
    def show_ongoing_projects(self):
        """진행중인 공사 표시"""
        self.load_projects('ongoing')
        
    def show_completed_projects(self):
        """완료된 공사 표시"""
        self.load_projects('completed')
        
    def show_all_projects(self):
        """모든 공사 표시"""
        self.load_projects(None)

class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('공사 정보')
        layout = QFormLayout(self)
        
        # 입력 필드
        self.name_edit = QLineEdit()
        self.number_edit = QLineEdit()
        self.period_edit = QLineEdit()
        self.amount_edit = QLineEdit()
        self.contractor_edit = QLineEdit()
        self.builder_edit = QLineEdit()
        self.note_edit = QLineEdit()
        
        # 폼에 필드 추가
        layout.addRow('공사명:', self.name_edit)
        layout.addRow('공사번호:', self.number_edit)
        layout.addRow('공사기간:', self.period_edit)
        layout.addRow('공사금액:', self.amount_edit)
        layout.addRow('계약자:', self.contractor_edit)
        layout.addRow('시공사:', self.builder_edit)
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

class ProjectManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("공사 관리")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # 검색 영역
        search_layout = QHBoxLayout()
        search_label = QLabel("검색:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("프로젝트 코드, 이름, 발주처, 계약자로 검색")
        self.search_input.textChanged.connect(self.search_projects)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "프로젝트 코드", "프로젝트명", "발주처", "계약자", "계약일",
            "계약금액", "상태", "위치", "설명"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        add_button = QPushButton("공사 추가")
        add_button.clicked.connect(self.add_project)
        edit_button = QPushButton("공사 수정")
        edit_button.clicked.connect(self.edit_project)
        delete_button = QPushButton("공사 삭제")
        delete_button.clicked.connect(self.delete_project)
        refresh_button = QPushButton("새로고침")
        refresh_button.clicked.connect(self.load_projects)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.load_projects()
        
    def load_projects(self):
        try:
            projects = self.db.get_all_projects()
            self.display_projects(projects)
        except Exception as e:
            print(f"프로젝트 목록을 불러오는 중 오류가 발생했습니다: {str(e)}")
            
    def display_projects(self, projects):
        self.table.setRowCount(len(projects))
        for i, project in enumerate(projects):
            self.table.setItem(i, 0, QTableWidgetItem(project['code']))
            self.table.setItem(i, 1, QTableWidgetItem(project['name']))
            self.table.setItem(i, 2, QTableWidgetItem(project['client']))
            self.table.setItem(i, 3, QTableWidgetItem(project['contractor']))
            self.table.setItem(i, 4, QTableWidgetItem(project['contract_date']))
            self.table.setItem(i, 5, QTableWidgetItem(str(project['amount'])))
            self.table.setItem(i, 6, QTableWidgetItem(project['status']))
            self.table.setItem(i, 7, QTableWidgetItem(project['location']))
            self.table.setItem(i, 8, QTableWidgetItem(project['description']))
            
    def search_projects(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(4):  # 프로젝트 코드, 이름, 발주처, 계약자 컬럼만 검색
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
            
    def get_selected_project(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "경고", "프로젝트를 선택하세요.")
            return None
        
        row = selected_rows[0].row()
        return {
            'id': int(self.table.item(row, 0).text()),
            'code': self.table.item(row, 0).text(),
            'name': self.table.item(row, 1).text(),
            'client': self.table.item(row, 2).text(),
            'contractor': self.table.item(row, 3).text(),
            'contract_date': self.table.item(row, 4).text(),
            'amount': float(self.table.item(row, 5).text()),
            'status': self.table.item(row, 6).text(),
            'location': self.table.item(row, 7).text(),
            'description': self.table.item(row, 8).text()
        }
        
    def add_project(self):
        dialog = ProjectDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.load_projects()
            
    def edit_project(self):
        project = self.get_selected_project()
        if project:
            dialog = ProjectDialog(self, project)
            if dialog.exec() == QDialog.Accepted:
                self.load_projects()
                
    def delete_project(self):
        project = self.get_selected_project()
        if project:
            reply = QMessageBox.question(
                self, "프로젝트 삭제",
                f"프로젝트 '{project['name']}'을(를) 삭제하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    self.db.delete_project(project['id'])
                    self.load_projects()
                    print("프로젝트가 삭제되었습니다.")
                except Exception as e:
                    print(f"프로젝트 삭제 중 오류가 발생했습니다: {str(e)}") 