from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout,
    QMessageBox, QInputDialog, QMenu
)
from PyQt6.QtCore import Qt
from cli.key_vault import list_aliases, delete_key, rename_key, get_key
from ui.passwordDialog import PasswordDialog

class AliasManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Alias Manager")
        self.resize(400, 300)
        layout = QVBoxLayout()

        # Prompt master password first
        pwd_dialog = PasswordDialog("Master password:", self)
        self.master_pwd = pwd_dialog.get_password()
        if not self.master_pwd:
            self.reject()
            return

        self.alias_list = QListWidget()
        # enable custom context menu
        self.alias_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.alias_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.alias_list)

        # Optional buttons (keep them if you like)
        btn_layout = QHBoxLayout()
        self.rename_btn = QPushButton("Rename")
        self.delete_btn = QPushButton("Delete")
        self.backup_btn = QPushButton("View Backup Key")
        for b in (self.rename_btn, self.delete_btn, self.backup_btn):
            btn_layout.addWidget(b)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_aliases()

        # Connect actions
        self.rename_btn.clicked.connect(self.rename_alias)
        self.delete_btn.clicked.connect(self.delete_alias)
        self.backup_btn.clicked.connect(self.view_backup)

    # ---------------- Context menu ---------------- #
    def show_context_menu(self, pos):
        item = self.alias_list.itemAt(pos)
        if not item:
            return
        alias = item.text()

        menu = QMenu(self)
        act_rename = menu.addAction("Rename")
        act_delete = menu.addAction("Delete")
        act_backup = menu.addAction("View Backup Key")
        action = menu.exec(self.alias_list.mapToGlobal(pos))

        if action == act_rename:
            self.rename_alias(alias)
        elif action == act_delete:
            self.delete_alias(alias)
        elif action == act_backup:
            self.view_backup(alias)

    # ---------------- Utility ---------------- #
    def load_aliases(self):
        try:
            self.alias_list.clear()
            for a in list_aliases(self.master_pwd):
                self.alias_list.addItem(a)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reject()

    def current_alias(self):
        item = self.alias_list.currentItem()
        return item.text() if item else None

    # ---------------- Operations ---------------- #
    def rename_alias(self, alias=None):
        alias = alias or self.current_alias()
        if not alias: return
        new_alias, ok = QInputDialog.getText(self, "Rename", f"New name for '{alias}':")
        if ok and new_alias:
            try:
                rename_key(alias, new_alias, self.master_pwd)
                self.load_aliases()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def delete_alias(self, alias=None):
        alias = alias or self.current_alias()
        if not alias: return
        if QMessageBox.question(self, "Confirm", f"Delete key '{alias}'?") \
                == QMessageBox.StandardButton.Yes:
            try:
                delete_key(alias, self.master_pwd)
                self.load_aliases()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def view_backup(self, alias=None):
        alias = alias or self.current_alias()
        if not alias: return
        try:
            key = get_key(alias, self.master_pwd).decode()
            QMessageBox.information(self, "Backup Key", f"{alias}:\n{key}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
