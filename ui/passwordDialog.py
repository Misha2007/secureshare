from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt

class PasswordDialog(QDialog):
    def __init__(self, prompt="Enter password:", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Input")
        self.setModal(True)

        self.password = None

        layout = QVBoxLayout()

        self.label = QLabel(prompt)
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input)

        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.setMinimumWidth(100)
        self.ok_button.setMaximumWidth(300)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.setMaximumWidth(300)
        self.cancel_button.setObjectName("cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.resize(300, 100)

    def get_password(self):
        if self.exec():
            return self.input.text()
        return None
