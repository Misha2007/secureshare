import os
import json
from cryptography.fernet import Fernet
from cli.encryptor import generate_key

VAULT_FILE = "key_vault.enc"

def create_vault(master_password: str):
    if os.path.exists(VAULT_FILE):
        raise FileExistsError("Vault already exists.")
    vault_key = Fernet(generate_key(master_password))
    encrypted = vault_key.encrypt(json.dumps({}).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
    print("Vault created.")

def load_vault(master_password: str) -> dict:
    vault_key = Fernet(generate_key(master_password))
    with open(VAULT_FILE, "rb") as f:
        data = f.read()
    decrypted = vault_key.decrypt(data)
    return json.loads(decrypted)

def save_vault(data: dict, master_password: str):
    vault_key = Fernet(generate_key(master_password))
    encrypted = vault_key.encrypt(json.dumps(data).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)

def add_key(alias: str, master_password: str) -> bytes:
    """
    Generates a new Fernet key and stores it under an alias.
    Returns the new key so the user can note it if desired.
    """
    vault = load_vault(master_password)
    key = Fernet.generate_key().decode()
    vault[alias] = key
    save_vault(vault, master_password)
    print(f"Key '{alias}' stored.")
    return key.encode()

def get_key(alias: str, master_password: str) -> bytes:
    vault = load_vault(master_password)
    if alias not in vault:
        raise KeyError(f"Key '{alias}' not found in vault.")
    return vault[alias].encode()
