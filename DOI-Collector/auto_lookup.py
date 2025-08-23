import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont

class ArticleFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DOI Article Finder")
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        # Keyword input
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Enter keywords...")
        self.keyword_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.keyword_input)

        # Rows input
        rows_layout = QHBoxLayout()
        rows_label = QLabel("Number of results:")
        rows_label.setFont(QFont("Arial", 14))
        rows_layout.addWidget(rows_label)

        self.rows_input = QLineEdit()
        self.rows_input.setPlaceholderText("10")
        self.rows_input.setFont(QFont("Arial", 14))
        rows_layout.addWidget(self.rows_input)

        layout.addLayout(rows_layout)

        # Search button
        self.search_button = QPushButton("Search Articles")
        self.search_button.setFont(QFont("Arial", 14))
        self.search_button.clicked.connect(self.search_articles)
        layout.addWidget(self.search_button)

        # Results table
        self.table = QTableWidget()
        self.table.setFont(QFont("Arial", 14))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Title", "DOI", "Publisher"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def search_articles(self):
        keyword = self.keyword_input.text().strip()
        if not keyword:
            return

        # Get number of rows (default = 10)
        try:
            rows = int(self.rows_input.text().strip())
            if rows <= 0:
                rows = 10
        except ValueError:
            rows = 10

        url = f"https://api.crossref.org/works?query={keyword}&rows={rows}"
        response = requests.get(url).json()

        items = response["message"]["items"]

        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            title = item.get("title", [""])[0]
            doi = item.get("DOI", "")
            publisher = item.get("publisher", "")

            self.table.setItem(row, 0, QTableWidgetItem(title))
            self.table.setItem(row, 1, QTableWidgetItem(doi))
            self.table.setItem(row, 2, QTableWidgetItem(publisher))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 14))

    window = ArticleFinder()
    window.showMaximized() 
    sys.exit(app.exec_())
