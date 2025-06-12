MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 15px;
    min-height: 35px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QLineEdit, QTextEdit, QComboBox {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 5px;
    background-color: white;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #2196F3;
}

QTableWidget {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    background-color: white;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #E3F2FD;
    color: black;
}

QHeaderView::section {
    background-color: #F5F5F5;
    padding: 5px;
    border: 1px solid #BDBDBD;
    font-weight: bold;
}
""" 