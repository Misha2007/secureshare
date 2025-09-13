import argparse
from getpass import getpass
from encryptor import encrypt_file, decrypt_file, generate_key
from key_vault import create_vault, add_key, get_key
import re

def password_strength(password: str) -> (bool, list):
    issues = []
    if len(password) < 12:
        issues.append("at least 12 characters")
    if not re.search(r"[A-Z]", password):
        issues.append("an uppercase letter")
    if not re.search("[a-z]", password):
        issues.append("a lowercase letter")
    if not re.search("\d", password):
        issues.append("a digit")
    if not re.search("[^A-Za-z0-9]", password):
        issues.append("a special character (!@#$ etc.)")
    return (len(issues) == 0, issues)

def prompt_strong_password(prompt_msg="Password: ") -> str:
    while True:
        pwd = getpass(prompt_msg)
        ok, problems = password_strength(pwd)
        if ok:
            return pwd
        print("Weak password. Please include:", ", ".join(problems))

def main():
    parser = argparse.ArgumentParser(description="Secure File Encryption CLI with Key Vault")
    sub = parser.add_subparsers(dest="command", required=True)

    # Create vault
    sub.add_parser("create-vault", help="Create a new empty key vault")

    # Add a key to the vault
    add_parser = sub.add_parser("add-key", help="Generate & store a new Fernet key")
    add_parser.add_argument("--alias", required=True, help="Alias name for the key")

    # Encrypt/decrypt using vault key
    enc_parser = sub.add_parser("encrypt", help="Encrypt file using a stored key")
    enc_parser.add_argument("--alias", required=True, help="Key alias")
    enc_parser.add_argument("--file", required=True, help="File to encrypt")
    enc_parser.add_argument("--out", help="Optional output path")
    enc_parser.add_argument("--delete", action="store_true", help="Delete original file")

    dec_parser = sub.add_parser("decrypt", help="Decrypt file using a stored key")
    dec_parser.add_argument("--alias", required=True, help="Key alias")
    dec_parser.add_argument("--file", required=True, help="Encrypted file to decrypt")
    dec_parser.add_argument("--out", help="Optional output path")

    # Password-based encryption (no vault)
    pass_enc = sub.add_parser("encrypt-pass", help="Encrypt with password (no vault)")
    pass_enc.add_argument("--file", required=True)
    pass_enc.add_argument("--out")
    pass_enc.add_argument("--delete", action="store_true")

    pass_dec = sub.add_parser("decrypt-pass", help="Decrypt with password (no vault)")
    pass_dec.add_argument("--file", required=True)
    pass_dec.add_argument("--out")

    args = parser.parse_args()

    if args.command == "create-vault":
        master = prompt_strong_password("Master password (strong): ")
        create_vault(master)

    elif args.command == "add-key":
        master = getpass("Master password: ")
        key = add_key(args.alias, master)
        print("New key generated. Keep it safe if you want a backup.")

    elif args.command == "encrypt":
        master = getpass("Master password: ")
        key = get_key(args.alias, master)
        out = encrypt_file(args.file, key, args.out, args.delete)
        print("Encrypted file:", out)

    elif args.command == "decrypt":
        master = getpass("Master password: ")
        key = get_key(args.alias, master)
        out = decrypt_file(args.file, key, args.out)
        print("Decrypted file:", out)

    elif args.command == "encrypt-pass":
        password = prompt_strong_password("Password for encryption: ")
        key = generate_key(password)
        out = encrypt_file(args.file, key, args.out, args.delete)
        print("Encrypted file:", out)

    elif args.command == "decrypt-pass":
        password = getpass("Password: ")
        key = generate_key(password)
        out = decrypt_file(args.file, key, args.out)
        print("Decrypted file:", out)

if __name__ == "__main__":
    main()
