import secrets
import string
import argparse
from typing import Set, List, Dict
import re
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import json
from datetime import datetime, timedelta

class PasswordGenerator:
    def __init__(self):
        self.char_sets = {
            'lowercase': set(string.ascii_lowercase),
            'uppercase': set(string.ascii_uppercase),
            'digits': set(string.digits),
            'special': set("!@#$%^&*()_+-=[]{}|;:,.<>?")
        }
        self.similar_chars = {'l', '1', 'I', '0', 'O'}
        self.password_history = []
        self.word_list = ["apple", "banana", "cherry", "date", "elder", "fig", "grape", "huckleberry", "ivy", "juniper"]

    def generate_password(self, length: int = 12, char_types: Set[str] = {'lowercase', 'uppercase', 'digits', 'special'}, exclude_similar: bool = False, custom_chars: str = '') -> str:
        if length < 8:
            raise ValueError("Password length must be at least 8 characters.")
        
        if not char_types and not custom_chars:
            raise ValueError("No character types or custom characters specified.")

        all_chars = custom_chars if custom_chars else ''.join(''.join(self.char_sets[char_type]) for char_type in char_types)
        if exclude_similar:
            all_chars = ''.join(char for char in all_chars if char not in self.similar_chars)

        if not all_chars:
            raise ValueError("No valid characters available for password generation.")

        password = ''.join(secrets.choice(all_chars) for _ in range(length))

        if password in self.password_history:
            return self.generate_password(length, char_types, exclude_similar, custom_chars)

        self.password_history.append(password)
        if len(self.password_history) > 10:
            self.password_history.pop(0)

        return password

    def generate_multiple_passwords(self, count: int, **kwargs) -> List[str]:
        return [self.generate_password(**kwargs) for _ in range(count)]

    def check_password_strength(self, password: str) -> str:
        length = len(password)
        has_lower = re.search(r"[a-z]", password) is not None
        has_upper = re.search(r"[A-Z]", password) is not None
        has_digit = re.search(r"\d", password) is not None
        has_special = re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password) is not None

        score = 0
        score += 1 if length >= 8 else 0
        score += 1 if length >= 12 else 0
        score += 1 if has_lower else 0
        score += 1 if has_upper else 0
        score += 1 if has_digit else 0
        score += 1 if has_special else 0

        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Moderate"
        elif score <= 5:
            return "Strong"
        else:
            return "Very Strong"

    def generate_from_passphrase(self, passphrase: str, length: int = 12) -> str:
        seed = int.from_bytes(passphrase.encode(), 'big')
        rng = secrets.SystemRandom(seed)
        all_chars = ''.join(char_set for char_set in self.char_sets.values())
        return ''.join(rng.choice(all_chars) for _ in range(length))

    def visualize_strength(self, password: str) -> str:
        strength = self.check_password_strength(password)
        if strength == "Weak":
            return "🟥🟥⬜⬜⬜"
        elif strength == "Moderate":
            return "🟥🟥🟨🟨⬜"
        elif strength == "Strong":
            return "🟥🟥🟨🟨🟩"
        else:  # Very Strong
            return "🟥🟥🟨🟨🟩🟩"

    def generate_memorable_password(self, num_words: int = 4, separator: str = '-') -> str:
        return separator.join(secrets.choice(self.word_list) for _ in range(num_words))

    def enforce_complexity_policy(self, password: str, min_length: int = 12, require_upper: bool = True, require_lower: bool = True, require_digit: bool = True, require_special: bool = True) -> bool:
        if len(password) < min_length:
            return False
        if require_upper and not re.search(r"[A-Z]", password):
            return False
        if require_lower and not re.search(r"[a-z]", password):
            return False
        if require_digit and not re.search(r"\d", password):
            return False
        if require_special and not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
            return False
        return True

class PasswordManager:
    def __init__(self, master_password: str):
        salt = b'saltysalt'  # In a real application, use a unique salt for each user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.fernet = Fernet(key)
        self.passwords = {}
        self.generation_log = []

    def encrypt_password(self, password: str) -> bytes:
        return self.fernet.encrypt(password.encode())

    def decrypt_password(self, encrypted_password: bytes) -> str:
        return self.fernet.decrypt(encrypted_password).decode()

    def add_password(self, service: str, username: str, password: str, expiration_days: int = 90):
        encrypted_password = self.encrypt_password(password)
        expiration_date = datetime.now() + timedelta(days=expiration_days)
        self.passwords[service] = {
            "username": username,
            "password": encrypted_password,
            "created_at": datetime.now().isoformat(),
            "expires_at": expiration_date.isoformat()
        }
        self.log_generation(service, username)

    def get_password(self, service: str) -> Dict:
        if service not in self.passwords:
            raise ValueError(f"No password found for service: {service}")
        
        password_data = self.passwords[service]
        decrypted_password = self.decrypt_password(password_data["password"])
        expiration_date = datetime.fromisoformat(password_data["expires_at"])
        
        is_expired = datetime.now() > expiration_date
        days_until_expiration = (expiration_date - datetime.now()).days if not is_expired else 0

        return {
            "username": password_data["username"],
            "password": decrypted_password,
            "is_expired": is_expired,
            "days_until_expiration": days_until_expiration
        }

    def log_generation(self, service: str, username: str):
        self.generation_log.append({
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "username": username
        })

    def export_passwords(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.passwords, f)

    def import_passwords(self, filename: str):
        with open(filename, 'r') as f:
            self.passwords = json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Advanced Password Generator and Manager")
    parser.add_argument("-l", "--length", type=int, default=12, help="Password length")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate")
    parser.add_argument("--no-lowercase", action="store_true", help="Exclude lowercase characters")
    parser.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase characters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-special", action="store_true", help="Exclude special characters")
    parser.add_argument("--exclude-similar", action="store_true", help="Exclude similar characters")
    parser.add_argument("--custom-chars", type=str, help="Custom character set for password generation")
    parser.add_argument("--passphrase", type=str, help="Generate password based on a passphrase")
    parser.add_argument("--memorable", action="store_true", help="Generate a memorable password")
    parser.add_argument("--words", type=int, default=4, help="Number of words for memorable password")
    parser.add_argument("--separator", type=str, default="-", help="Separator for memorable password")
    parser.add_argument("--save", action="store_true", help="Save generated password")
    parser.add_argument("--service", type=str, help="Service name for saved password")
    parser.add_argument("--username", type=str, help="Username for saved password")
    parser.add_argument("--export", type=str, help="Export passwords to file")
    parser.add_argument("--import", type=str, dest="import_file", help="Import passwords from file")
    args = parser.parse_args()

    generator = PasswordGenerator()
    
    char_types = {'lowercase', 'uppercase', 'digits', 'special'}
    if args.no_lowercase:
        char_types.remove('lowercase')
    if args.no_uppercase:
        char_types.remove('uppercase')
    if args.no_digits:
        char_types.remove('digits')
    if args.no_special:
        char_types.remove('special')

    try:
        if args.memorable:
            passwords = [generator.generate_memorable_password(args.words, args.separator) for _ in range(args.count)]
        elif args.passphrase:
            passwords = [generator.generate_from_passphrase(args.passphrase, args.length) for _ in range(args.count)]
        else:
            passwords = generator.generate_multiple_passwords(
                count=args.count,
                length=args.length,
                char_types=char_types,
                exclude_similar=args.exclude_similar,
                custom_chars=args.custom_chars
            )

        if args.save or args.export or args.import_file:
            master_password = getpass.getpass("Enter master password: ")
            password_manager = PasswordManager(master_password)

            if args.import_file:
                password_manager.import_passwords(args.import_file)
                print(f"Passwords imported from {args.import_file}")

        for i, password in enumerate(passwords, 1):
            strength = generator.check_password_strength(password)
            strength_visual = generator.visualize_strength(password)
            print(f"Password {i}: {password}")
            print(f"Strength: {strength} {strength_visual}")
            
            if args.save:
                if not args.service or not args.username:
                    raise ValueError("Service and username are required to save a password")
                password_manager.add_password(args.service, args.username, password)
                print(f"Password saved for {args.service}")
            
            print()  # Add a blank line between passwords

        if args.export:
            password_manager.export_passwords(args.export)
            print(f"Passwords exported to {args.export}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()