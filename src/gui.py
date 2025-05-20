# src/gui.py

from PyQt5.QtWidgets import (
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
from pdf_parser import extract_text_from_pdf
from encoder import encode_text, save_encoding

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table of Contents Encoder")
        self.setMinimumSize(800, 600)

        self.text_display = QTextEdit() # Text display area
        self.text_display.setReadOnly(True)

        self.load_button = QPushButton("Load PDF")
        self.load_button.clicked.connect(self.load_pdf)

        self.encode_button = QPushButton("Encode Text")
        self.encode_button.clicked.connect(self.encode_pdf_text)

        layout = QVBoxLayout() # Main layout
        layout.addWidget(QLabel("PDF Text Preview:"))
        layout.addWidget(self.text_display)

        button_layout = QHBoxLayout() # Button layout
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.encode_button)
        layout.addLayout(button_layout)

        container = QWidget() # Central widget
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.current_text = ""
        self.current_path = ""

    def load_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select TOC PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.current_path = file_path
            self.current_text = extract_text_from_pdf(file_path)
            self.text_display.setText(self.current_text)

    def encode_pdf_text(self):
        if self.current_text:
            encoded, mapping = encode_text(self.current_text)
            save_encoding(self.current_path, mapping)
            self.text_display.setText(encoded)
