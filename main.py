import secrets
import string
from typing import Set

class PasswordGenerator:
    def __init__(self):
        self.char_sets = {
            'lowercase': set(string.ascii_lowercase),
            'uppercase': set(string.ascii_uppercase),
            'digits': set(string.digits),
            'special': set("!@#$%^&*()_+-=[]{}|;:,.<>?")
        }

    def generate_password(self, length: int = 12, char_types: Set[str] = {'lowercase', 'uppercase', 'digits', 'special'}) -> str:
        if length < 8:
            raise ValueError("Password length must be at least 8 characters.")
        
        if not char_types or not char_types.issubset(self.char_sets.keys()):
            raise ValueError("Invalid character types specified.")

        all_chars = ''.join(''.join(self.char_sets[char_type]) for char_type in char_types)
        
        # Ensure at least one character from each type
        password = [secrets.choice(''.join(self.char_sets[char_type])) for char_type in char_types]
        
        # Fill the rest of the password
        password.extend(secrets.choice(all_chars) for _ in range(length - len(password)))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)

def main():
    generator = PasswordGenerator()
    
    try:
        password = generator.generate_password(
            length=16,
            char_types={'lowercase', 'uppercase', 'digits', 'special'}
        )
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()