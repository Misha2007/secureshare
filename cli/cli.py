import argparse
from getpass import getpass  # For securely handling passwords
from encryptor import encrypt_file, decrypt_file

def main():
    parser = argparse.ArgumentParser(description="Secure File Encryption CLI")
    
    # Make encrypt and decrypt mutually exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', action='store_true', help='Encrypt a file')
    group.add_argument('--decrypt', action='store_true', help='Decrypt a file')

    # --delete is no longer part of the mutually exclusive group
    parser.add_argument('--delete', action='store_true', help='Delete original file after encryption')

    parser.add_argument('--file', type=str, required=True, help='Path to file')
    parser.add_argument('--password', type=str, help='Encryption password (use --password or input via prompt)')
    parser.add_argument('--out', type=str, help='Optional output path')
    
    args = parser.parse_args()

    # Handle password securely (use getpass if --password is not provided)
    if not args.password:
        args.password = getpass("Enter password: ")

    try:
        if args.encrypt:
            out = encrypt_file(args.file, args.password, args.out, args.delete)
            print(f"Encrypted file saved to: {out}")
        elif args.decrypt:
            out = decrypt_file(args.file, args.password, args.out)
            print(f"Decrypted file saved to: {out}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
