from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout
)

class ProjectOverviewDialog(QDialog):
    def __init__(self, project_info, parent=None, save_callback=None):
        super().__init__(parent)
        self.setWindowTitle("공사 개요")
        self.project_info = project_info
        self.save_callback = save_callback

        layout = QVBoxLayout()
        
        title = QLabel(f"<h2>{project_info.get('공사명', '공사명 없음')}</h2>")
        layout.addWidget(title)
         
        # # 예시: 주요 정보 한 줄에 표시
        # info_layout = QHBoxLayout()
        # info_layout.addWidget(QLabel(f"<b>계약일:</b> {project_info.get('계약일', '')}"))
        # info_layout.addWidget(QLabel(f"<b>착공일:</b> {project_info.get('착공일', '')}"))
        # info_layout.addWidget(QLabel(f"<b>준공일:</b> {project_info.get('준공일', '')}"))
        # layout.addLayout(info_layout)
        
        # # 나머지 정보
        # for key, value in project_info.items():
        #     if key not in ["공사명", "계약일", "착공일", "준공일", "메모"]:
        #         layout.addWidget(QLabel(f"<b>{key}</b>: {value}"))
              
        for key, value in project_info.items():
            if key != "메모":
                layout.addWidget(QLabel(f"<b>{key}</b>: {value}")) 

        # 메모 입력란        
        layout.addWidget(QLabel("메모:"))
        self.memo_edit = QTextEdit()
        self.memo_edit.setText(project_info.get("메모", ""))
        layout.addWidget(self.memo_edit)

        save_btn = QPushButton("메모 저장")
        save_btn.clicked.connect(self.save_memo)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_memo(self):
        memo = self.memo_edit.toPlainText()
        if self.save_callback:
            self.save_callback(memo)
        QMessageBox.information(self, "저장", "메모가 저장되었습니다.")