from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox
from ui.button import Button

class SettingsTab(QWidget):
    theme_changed = pyqtSignal(str)  # emit the theme name

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Theme selection
        layout.addWidget(QLabel("Theme"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo)

        # Vault info
        layout.addWidget(QLabel("Vault Options"))
        self.show_key_backup_checkbox = QCheckBox("Show backup keys in dialog")
        layout.addWidget(self.show_key_backup_checkbox)

        # Password policy
        layout.addWidget(QLabel("Password Policy"))
        self.require_strong_password_checkbox = QCheckBox("Require strong passwords for new keys")
        layout.addWidget(self.require_strong_password_checkbox)

        # Apply / Reset buttons
        button_layout = QVBoxLayout()
        self.apply_btn = Button("Apply Settings", cursor=True, clicked=self.apply_settings).get_button()
        self.reset_btn = Button("Reset to Default", cursor=True, clicked=self.reset_settings).get_button()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.reset_btn)
        layout.addLayout(button_layout)

        layout.addStretch()
        self.setLayout(layout)

    def on_theme_changed(self, theme_name):
        # Emit the theme name whenever the combo changes
        self.theme_changed.emit(theme_name)

    def apply_settings(self):
        selected_theme = self.theme_combo.currentText()
        print(f"Settings applied: Theme={selected_theme}, Show backup={self.show_key_backup_checkbox.isChecked()}, Require strong={self.require_strong_password_checkbox.isChecked()}")

    def reset_settings(self):
        self.theme_combo.setCurrentIndex(0)
        self.show_key_backup_checkbox.setChecked(False)
        self.require_strong_password_checkbox.setChecked(False)
        print("Settings reset to default")
        # Emit signal so app updates theme
        self.theme_changed.emit("Light")
