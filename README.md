# Secure File Encryption App

This is a **Secure File Encryption App** built with PyQt6. It allows you to create secure vaults, add encryption keys, encrypt and decrypt files, and manage encrypted data easily and safely. The app also supports dynamic theme switching and includes features for managing file encryption tasks with a user-friendly interface.

---

## Features

* **Create a Vault:** Store sensitive data securely with encryption.
* **Add Keys:** Add encryption keys to the vault with unique aliases.
* **File Encryption & Decryption:** Encrypt and decrypt files with secure keys.
* **Delete Original Files:** Option to delete original files after encryption/decryption.
* **Manage Vault & Keys:** Manage your encryption vault and stored keys efficiently.
* **User-Friendly Interface:** Dynamic theme support with "Light" and "Dark" modes.
* **Cross-Platform Support:** Runs on any system that supports PyQt6 (Windows, macOS, Linux).

---

## Prerequisites

Ensure you have the following installed:

* Python 3.x
* PyQt6 (for the GUI)
* Required dependencies listed in `requirements.txt`

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/encryption-app.git
   cd encryption-app
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. **Create Vault:** When you first run the app, create a vault by setting a strong master password.

3. **Add Keys:** Add new keys with unique aliases to be used for file encryption and decryption.

4. **File Encryption:** Input a file path, select an encryption key (alias), and encrypt the file.

5. **File Decryption:** Input a file path, select an encryption key (alias), and decrypt the file.

---

## Theming

The app supports both **Light** and **Dark** themes. You can change the theme from the settings tab, and the application will update the UI dynamically. The app uses custom styles with `QSS` files for styling.

---

## Files and Directories

* `app.py`: Main application file.
* `cli/`: Contains logic for file encryption and key management.
* `ui/`: Contains UI components and styling.
* `requirements.txt`: List of Python dependencies.
* `ui/dark.qss` & `ui/light.qss`: Stylesheets for dark and light themes.

---

## Future Features

* **Browser Extensions:** For easy bookmarking and file management.
* **Support for more encryption algorithms** to improve security options.
* **Key Backup Options:** Securely back up and restore encryption keys.

---

## Contributing

Feel free to fork the repository and submit pull requests with new features or bug fixes. All contributions are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

* PyQt6 for building the GUI
* Python for its simplicity and flexibility
* All the open-source libraries used in this project

---

### Notes

* If you face any issues or discover bugs, feel free to file an issue or reach out using the contact form available in the app.
