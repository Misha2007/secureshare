import os
import hashlib
import base64
from cryptography.fernet import Fernet

def generate_key(password: str) -> bytes:
    """
    Generates a Fernet key from a password using SHA-256 hashing.
    """
    sha = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha)

def encrypt_file(filepath: str, key: bytes, output_path: str = None, delete_original: bool = False) -> str:
    """
    Encrypts a file using a Fernet key (already base64 encoded).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")

    fernet = Fernet(key)
    with open(filepath, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)
    output_path = output_path or (filepath + ".enc")

    with open(output_path, "wb") as f:
        f.write(encrypted)

    if delete_original:
        os.remove(filepath)

    return output_path

def decrypt_file(filepath: str, key: bytes, output_path: str = None) -> str:
    """
    Decrypts a file using a Fernet key.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Encrypted file '{filepath}' not found.")

    fernet = Fernet(key)
    with open(filepath, "rb") as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)

    if not output_path:
        output_path = filepath[:-4] if filepath.endswith(".enc") else filepath + ".dec"

    with open(output_path, "wb") as f:
        f.write(decrypted)

    return output_path
