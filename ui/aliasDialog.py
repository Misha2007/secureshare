from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class AliasDialog(QDialog):
    def __init__(self, prompt="Enter key alias:", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Key")
        layout = QVBoxLayout()

        self.label = QLabel(prompt)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Key alias")

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Create Vault")
        self.ok_btn.setMinimumWidth(100)
        self.ok_btn.setMaximumWidth(300)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.setMaximumWidth(300)
        self.cancel_button.setObjectName("cancel")
        self.cancel_button.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_button)
        btn_layout.addWidget(self.ok_btn)

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def get_alias(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            return self.line_edit.text()
        return None
