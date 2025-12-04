import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt

class AccidentViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Accident CSV Viewer - PyQt Version")
        self.resize(1200, 700)

        layout = QVBoxLayout()

        # Top controls (Load + Search)
        control_layout = QHBoxLayout()

        self.load_btn = QPushButton("Load CSV")
        self.load_btn.clicked.connect(self.load_csv)
        control_layout.addWidget(self.load_btn)

        control_layout.addWidget(QLabel("Search Year:"))

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("2024")
        control_layout.addWidget(self.search_entry)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_year)
        control_layout.addWidget(self.search_btn)

        layout.addLayout(control_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.setLayout(layout)

    # CSV Loading Function
    def load_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )

        if not filepath:
            return

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        header = rows[0]
        data = rows[1:]

        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        self.table.setRowCount(len(data))

        # Fill table
        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(value))

    # Search Function
    def search_year(self):
        year = self.search_entry.text().strip()

        if not year.isdigit():
            return

        for row in range(self.table.rowCount()):
            crash_date = self.table.item(row, 0).text()  # index 0 = Crash Date

            if crash_date.startswith(year):
                self.table.showRow(row)
            else:
                self.table.hideRow(row)


# ------------------------------
# Run App
# ------------------------------
app = QApplication(sys.argv)
viewer = AccidentViewer()
viewer.show()
sys.exit(app.exec_())

