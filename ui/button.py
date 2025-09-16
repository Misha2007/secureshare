from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton

class Button():
    def __init__(self, name = "", cursor = False, clicked = False):
        self.name = name
        self.cursor = cursor
        self.clicked = clicked
    
    def get_button(self) :
        button = QPushButton(self.name)
        if self.cursor:
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if callable(self.clicked):
            button.clicked.connect(self.clicked)
        return button