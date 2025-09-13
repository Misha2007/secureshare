from cryptography.fernet import Fernet
import hashlib
import base64
import os

def generate_key(password: str) -> bytes:
    """
    Generates a Fernet key from the provided password using SHA-256 hashing.
    The password is hashed to create a 32-byte key, which is then base64 encoded.
    """
    sha = hashlib.sha256(password.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(sha)

def encrypt_file(filepath: str, password: str, output_path: str = None, delete_original: bool = False) -> str:
    """
    Encrypts a file with the given password and saves it to the output path.
    Optionally deletes the original file after encryption.
    """
    print(f"Encrypting file: {filepath}")
    
    # Check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")
    
    key = generate_key(password)
    fernet = Fernet(key)

    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        print(f"File {filepath} read successfully.")
    except FileNotFoundError:
        raise Exception(f"File '{filepath}' not found.")
    except IOError as e:
        raise Exception(f"Error reading file: {e}")

    encrypted = fernet.encrypt(data)
    print(f"Encryption completed successfully.")

    # If no output path provided, default to adding .enc extension
    output_path = output_path or (filepath + ".enc")
    print(f"Output path: {output_path}")

    try:
        with open(output_path, 'wb') as f:
            f.write(encrypted)
        print(f"Encrypted file saved to: {output_path}")
    except IOError as e:
        raise Exception(f"Error writing encrypted file: {e}")

    # Optionally delete the original file
    if delete_original:
        try:
            os.remove(filepath)
            print(f"Original file '{filepath}' deleted successfully.")
        except IOError as e:
            print(f"Error deleting original file: {e}")
    
    return output_path

def decrypt_file(filepath: str, password: str, output_path: str = None) -> str:
    """
    Decrypts an encrypted file with the given password and saves it to the output path.
    If no output path is provided, the decrypted file will have the same name as the encrypted file with a '.dec' extension.
    """
    key = generate_key(password)
    fernet = Fernet(key)

    try:
        with open(filepath, 'rb') as f:
            encrypted = f.read()
    except FileNotFoundError:
        raise Exception(f"Encrypted file '{filepath}' not found.")
    except IOError as e:
        raise Exception(f"Error reading file: {e}")

    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception as e:
        raise Exception("Decryption failed. Possible wrong password or corrupt file.")

    if not output_path:
        if filepath.endswith(".enc"):
            output_path = filepath[:-4]  # Remove '.enc' for the decrypted file
        else:
            output_path = filepath + ".dec"  # Add '.dec' if the file doesn't have '.enc'

    try:
        with open(output_path, 'wb') as f:
            f.write(decrypted)
    except IOError as e:
        raise Exception(f"Error writing decrypted file: {e}")

    return output_path
