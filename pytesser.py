import sys
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget 
from PyQt5.QtGui import QImage, QPixmap, QClipboard
from PyQt5.QtCore import Qt
from PIL import ImageGrab, Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            self.parent.keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class TextExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Text Extractor")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = CustomTextEdit(self)
        self.text_edit.setGeometry(10, 10, 580, 280)

        self.extract_button = QPushButton("Extrahieren", self)
        #extract_button.setGeometry(10, 300, 100, 30)
        self.extract_button.clicked.connect(self.extract_text)

        self.copy_button = QPushButton("In Zwischenablage kopieren", self)
        self.copy_button.setGeometry(120, 300, 200, 30)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.copy_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)




    def keyPressEvent(self, event):
        if event.key() == Qt.Key_V:
            self.extract_text()

    def extract_text(self):
        screenshot = ImageGrab.grabclipboard()
        #print(screenshot)
        if screenshot and isinstance(screenshot, Image.Image):
            extracted_text = pytesseract.image_to_string(np.array(screenshot), lang='eng')
            print(extracted_text)
            #self.text_edit.setPlainText(extracted_text)
            self.text_edit.append(extracted_text)

    def copy_to_clipboard(self):
        text = self.text_edit.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text, mode=QClipboard.Clipboard)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextExtractorApp()
    window.show()
    sys.exit(app.exec_())