import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout,
    QProxyStyle, QStyle, QTabWidget, QCheckBox
)
from PyQt6.QtGui import QPainter, QColor, QPen, QCursor
from PyQt6.QtCore import Qt
import re
from cli.encryptor import encrypt_file, decrypt_file
from cli.key_vault import create_vault, add_key, get_key
from ui.passwordDialog import PasswordDialog
from ui.aliasDialog import AliasDialog
from ui.aliasManagerDialog import AliasManagerDialog
from ui.button import Button
from ui.settings import SettingsTab

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
        QMessageBox.warning(parent, "Weak password",
                            "Password must include: " + ", ".join(issues))


class BorderCheckboxStyle(QProxyStyle):
    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme

    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PrimitiveElement.PE_IndicatorCheckBox:
            rect = option.rect
            border_color = QColor("#EAE0D5") if self.theme == "dark" else QColor("#222222")
            painter.save()
            painter.setRenderHint(painter.RenderHint.Antialiasing)
            painter.setPen(QPen(border_color, 1))
            painter.drawRect(rect.adjusted(1, 1, -1, -1))

            # ✅ draw a simple check mark if checked
            if option.state & QStyle.StateFlag.State_On:
                pen = QPen(border_color, 2)
                painter.setPen(pen)
                painter.drawLine(rect.left()+4, rect.center().y(),
                                 rect.center().x(), rect.bottom()-4)
                painter.drawLine(rect.center().x(), rect.bottom()-4,
                                 rect.right()-4, rect.top()+4)

            painter.restore()
        else:
            super().drawPrimitive(element, option, painter, widget)



class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure File Encryption")
        self.setGeometry(200, 200, 600, 400)

        # Create the tab widget
        self.tabs = QTabWidget()

        # Create and add individual tabs
        self.tabs.addTab(self.create_encryption_tab(), "Encryption")
        self.settings_tab = SettingsTab()
        self.settings_tab.theme_changed.connect(self.update_theme)
        self.tabs.addTab(self.settings_tab, "Settings")

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    # ------------------- Styles ------------------- #
    def update_theme(self, theme_name):
        """Update app stylesheet dynamically."""
        if theme_name == "Light":
            stylesheet = load_stylesheet("ui/light.qss")
        else:
            stylesheet = load_stylesheet("ui/dark.qss")

        app.setStyle(BorderCheckboxStyle(theme=theme_name.lower()))
        self.setStyleSheet(stylesheet)
        print(f"Theme changed to: {theme_name}")

    # ------------------- TAB CREATION ------------------- #
    def create_encryption_tab(self):
        """Original encryption UI moved here."""
        page = QWidget()
        layout = QVBoxLayout()

        # Vault buttons
        self.create_vault_btn  = Button("Create Vault", cursor=True, clicked = self.create_vault).get_button()
        layout.addWidget(self.create_vault_btn)

        self.add_key_btn = Button("+ Add Key to Vault", cursor=True, clicked = self.add_key).get_button()
        layout.addWidget(self.add_key_btn)

        self.manage_keys_btn = Button("Manage Keys", cursor=True, clicked = self.open_key_manager).get_button()
        layout.addWidget(self.manage_keys_btn)

        # File encryption
        file_label = QLabel("File:")
        layout.addWidget(file_label)
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Enter a full path to your file here")
        file_layout.addWidget(self.file_input)
        self.browse_btn = Button("Browse", cursor=True, clicked = self.browse_file).get_button()
        file_layout.addWidget(self.browse_btn)
        layout.addLayout(file_layout)

        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Key Alias")
        layout.addWidget(self.alias_input)

        self.delete_checkbox = QCheckBox("Delete original file after operation")
        layout.addWidget(self.delete_checkbox)

        self.encrypt_btn = Button("Encrypt File", cursor=True, clicked = self.encrypt_file_action).get_button()
        layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = Button("Decrypt File", cursor=True, clicked = self.decrypt_file_action).get_button()
        layout.addWidget(self.decrypt_btn)

        page.setLayout(layout)
        return page

    def create_settings_tab(self):
        """Example second tab for future settings."""
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("⚙️ Settings"))
        layout.addWidget(QLabel("Here you can add future options such as:"))
        layout.addWidget(QLabel("• Theme selection\n• Vault info\n• Logs"))

        page.setLayout(layout)
        return page

    # ------------------- APP LOGIC ------------------- #
    def open_key_manager(self):
        dialog = AliasManagerDialog(parent=self)
        dialog.exec()

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
                QMessageBox.information(
                    self, "Key Added",
                    f"Key '{alias}' added successfully.\nBackup: {key.decode()}"
                )

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
                out_path = encrypt_file(filepath, key,
                                        delete_original=self.delete_checkbox.isChecked())
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
                out_path = decrypt_file(filepath, key,
                                        delete_original=self.delete_checkbox.isChecked())
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

    # Optional: load your stylesheet
    stylesheet = load_stylesheet("ui/dark.qss")
    app.setStyleSheet(stylesheet)

    window = EncryptionApp()
    window.show()
    sys.exit(app.exec())
