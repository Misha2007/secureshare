from cryptography.fernet import Fernet
import json, os
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
        decrypted = vault_key.decrypt(f.read())
    return json.loads(decrypted)

def save_vault(vault: dict, master_password: str):
    vault_key = Fernet(generate_key(master_password))
    encrypted = vault_key.encrypt(json.dumps(vault).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)

def add_key(alias: str, master_password: str) -> bytes: 
    """ Generates a new Fernet key and stores it under an alias. Returns the new key so the user can note it if desired. """ 
    vault = load_vault(master_password) 
    key = Fernet.generate_key().decode() 
    vault[alias] = key 
    save_vault(vault, master_password) 
    print(f"Key '{alias}' stored.") 
    return key.encode()

def list_aliases(master_password: str) -> list[str]:
    vault = load_vault(master_password)
    return list(vault.keys())

def delete_key(alias: str, master_password: str):
    vault = load_vault(master_password)
    if alias not in vault:
        raise KeyError(f"Alias '{alias}' not found.")
    del vault[alias]
    save_vault(vault, master_password)

def rename_key(old_alias: str, new_alias: str, master_password: str):
    vault = load_vault(master_password)
    if old_alias not in vault:
        raise KeyError(f"Alias '{old_alias}' not found.")
    if new_alias in vault:
        raise KeyError(f"Alias '{new_alias}' already exists.")
    vault[new_alias] = vault.pop(old_alias)
    save_vault(vault, master_password)

def get_key(alias: str, master_password: str) -> bytes: 
    vault = load_vault(master_password)
    if alias not in vault: 
        raise KeyError(f"Key '{alias}' not found in vault.") 
    return vault[alias].encode()