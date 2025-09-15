import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QProxyStyle, QStyle
)
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt
from cli.encryptor import encrypt_file, decrypt_file
from cli.key_vault import create_vault, add_key, get_key
import re
from ui.passwordDialog import PasswordDialog
from ui.aliasDialog import AliasDialog
from ui.aliasManagerDialog import AliasManagerDialog
from PyQt6.QtWidgets import QCheckBox

def password_strength(password: str) -> (bool, list):
    issues = []
    if len(password) < 12:
        issues.append("at least 12 characters")
    if not re.search(r"[A-Z]", password):
        issues.append("an uppercase letter")
    if not re.search(r"[a-z]", password):
        issues.append("a lowercase letter")
    if not re.search(r"\d", password):
        issues.append("a digit")
    if not re.search(r"[^A-Za-z0-9]", password):
        issues.append("a special character (!@#$ etc.)")
    return len(issues) == 0, issues

def prompt_strong_password(parent=None, prompt="Password:"):
    while True:
        dialog = PasswordDialog(prompt, parent)
        pwd = dialog.get_password()
        if not pwd:
            return 
        ok_strength, issues = password_strength(pwd)
        if ok_strength:
            return pwd
        QMessageBox.warning(parent, "Weak password", "Password must include: " + ", ".join(issues))

class BorderCheckboxStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        super().drawPrimitive(element, option, painter, widget)

        if element == QStyle.PrimitiveElement.PE_IndicatorCheckBox:
            rect = option.rect
            pen = QPen(QColor("#EAE0D5"), 1)
            painter.save()
            painter.setPen(pen)
            painter.drawRect(rect.adjusted(1, 1, 1, 1))  # custom border
            painter.restore()

class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure File Encryption")
        self.setGeometry(200, 200, 500, 300)
        self.init_ui()

    def open_key_manager(self):
        dialog = AliasManagerDialog(parent=self)
        dialog.exec()

    def init_ui(self):
        layout = QVBoxLayout()

        # Vault buttons
        self.create_vault_btn = QPushButton("Create Vault")
        self.create_vault_btn.clicked.connect(self.create_vault)
        layout.addWidget(self.create_vault_btn)

        self.add_key_btn = QPushButton("+ Add Key to Vault")
        self.add_key_btn.clicked.connect(self.add_key)
        layout.addWidget(self.add_key_btn)

        self.manage_keys_btn = QPushButton("Manage Keys")
        self.manage_keys_btn.clicked.connect(self.open_key_manager)
        layout.addWidget(self.manage_keys_btn)

        # File encryption
        file_label = QLabel("File:")
        file_label.setObjectName("fileLabel")
        layout.addWidget(file_label)
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Enter a full path to your file here")
        file_layout.addWidget(self.file_input)
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)
        layout.addLayout(file_layout)

        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Key Alias")
        layout.addWidget(self.alias_input)

        self.delete_checkbox = QCheckBox("Delete original file after operation")
        layout.addWidget(self.delete_checkbox)

        self.encrypt_btn = QPushButton("Encrypt File")
        self.encrypt_btn.clicked.connect(self.encrypt_file_action)
        layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton("Decrypt File")
        self.decrypt_btn.clicked.connect(self.decrypt_file_action)
        layout.addWidget(self.decrypt_btn)

        self.setLayout(layout)

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select File")
        if filename:
            self.file_input.setText(filename)

    def create_vault(self):
        pwd = prompt_strong_password(self, "Master password (strong):")
        if pwd:
            try:
                create_vault(pwd)
                QMessageBox.information(self, "Vault", "Vault created successfully.")
            except FileExistsError:
                QMessageBox.warning(self, "Vault", "Vault already exists.")

    def add_key(self):
        dialog = AliasDialog(parent=self)
        alias = dialog.get_alias()
        if alias:
            master_pwd = prompt_strong_password(self, "Master password:")
            if master_pwd:
                key = add_key(alias, master_pwd)
                QMessageBox.information(self, "Key Added", f"Key '{alias}' added successfully.\nBackup: {key.decode()}")

    def encrypt_file_action(self):
        filepath = self.file_input.text()
        alias = self.alias_input.text()
        if not filepath or not alias:
            QMessageBox.warning(self, "Error", "File path and key alias are required.")
            return
        master_pwd = prompt_strong_password(self, "Master password:")
        if master_pwd:
            try:
                key = get_key(alias, master_pwd)
                out_path = encrypt_file(filepath, key, delete_original=self.delete_checkbox.isChecked())
                QMessageBox.information(self, "Success", f"File encrypted:\n{out_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def decrypt_file_action(self):
        filepath = self.file_input.text()
        alias = self.alias_input.text()
        if not filepath or not alias:
            QMessageBox.warning(self, "Error", "File path and key alias are required.")
            return
        master_pwd = prompt_strong_password(self, "Master password:")
        if master_pwd:
            try:
                key = get_key(alias, master_pwd)
                out_path = decrypt_file(filepath, key, delete_original=self.delete_checkbox.isChecked())
                QMessageBox.information(self, "Success", f"File decrypted:\n{out_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

def load_stylesheet(filename):
    with open(filename, "r") as f:
        return f.read()

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(BorderCheckboxStyle())

    stylesheet = load_stylesheet("ui/style.qss")
    # Apply it to the entire app
    app.setStyleSheet(stylesheet)
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec())
