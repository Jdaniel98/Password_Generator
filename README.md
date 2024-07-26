# Advanced Password Generator and Manager

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Basic Password Generation](#basic-password-generation)
   - [Memorable Passwords](#memorable-passwords)
   - [Passphrase-based Passwords](#passphrase-based-passwords)
   - [Password Saving and Retrieval](#password-saving-and-retrieval)
   - [Password Complexity Enforcement](#password-complexity-enforcement)
   - [Export and Import](#export-and-import)
5. [Code Structure](#code-structure)
6. [Security Considerations](#security-considerations)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

This Advanced Password Generator and Manager is a powerful Python-based tool designed to create strong, secure passwords and manage them effectively. It offers a wide range of features including customizable password generation, memorable password creation, password strength assessment, secure storage, and more.

## Features

- Customizable password generation with options for length, character types, and exclusions
- Memorable password generation using word lists
- Passphrase-based password generation
- Password strength checker with visual representation
- Secure password encryption and storage
- Password expiration tracking
- Password complexity policy enforcement
- Password generation logging
- Export and import functionality for saved passwords
- Command-line interface for easy interaction

## Installation

1. Ensure you have Python 3.7+ installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/Jdaniel98/Password_Generator.git
   ```
3. Navigate to the project directory:
   ```
   cd advanced-password-generator
   ```
4. Install the required dependencies:
   ```
   pip install cryptography
   ```

## Usage

### Basic Password Generation

To generate a basic password:

```bash
python main.py --length 16 --count 2
```

This will generate two 16-character passwords.

Example output:
```
Password 1: 3X$mK9pL&fQ2wR7n
Strength: Very Strong 🟥🟥🟨🟨🟩🟩

Password 2: Jh5%zU8cN@bT4yE1
Strength: Very Strong 🟥🟥🟨🟨🟩🟩
```

### Memorable Passwords

To generate a memorable password:

```bash
python main.py --memorable --words 5 --separator "."
```

This will create a password using 5 words separated by dots.

Example output:
```
Password 1: apple.banana.cherry.date.elder
Strength: Strong 🟥🟥🟨🟨🟩
```

### Passphrase-based Passwords

To generate a password based on a passphrase:

```bash
python main.py --passphrase "my secret phrase" --length 20
```

This will create a 20-character password based on the provided passphrase.

### Password Saving and Retrieval

To save a generated password:

```bash
python main.py --length 16 --save --service "example.com" --username "user@example.com"
```

This will generate a password and save it for the specified service and username.

To retrieve a saved password, you would typically do this programmatically. Here's an example of how you might use the `PasswordManager` class to retrieve a password:

```python
password_manager = PasswordManager("master_password")
password_data = password_manager.get_password("example.com")
print(f"Username: {password_data['username']}")
print(f"Password: {password_data['password']}")
print(f"Expired: {'Yes' if password_data['is_expired'] else 'No'}")
print(f"Days until expiration: {password_data['days_until_expiration']}")
```

### Password Complexity Enforcement

The `enforce_complexity_policy` method can be used to ensure passwords meet specific criteria:

```python
generator = PasswordGenerator()
password = generator.generate_password(length=12)
is_complex = generator.enforce_complexity_policy(
    password,
    min_length=12,
    require_upper=True,
    require_lower=True,
    require_digit=True,
    require_special=True
)
print(f"Password meets complexity requirements: {is_complex}")
```

### Export and Import

To export saved passwords:

```bash
python main.py --export "passwords.json"
```

To import saved passwords:

```bash
python main.py --import "passwords.json"
```

## Code Structure

The project consists of two main classes:

1. `PasswordGenerator`: Handles password generation and strength assessment.

   Key methods:
   ```python
   def generate_password(self, length: int = 12, char_types: Set[str] = {'lowercase', 'uppercase', 'digits', 'special'}, exclude_similar: bool = False, custom_chars: str = '') -> str:
       # ... password generation logic ...

   def check_password_strength(self, password: str) -> str:
       # ... strength checking logic ...

   def generate_memorable_password(self, num_words: int = 4, separator: str = '-') -> str:
       # ... memorable password generation logic ...
   ```

2. `PasswordManager`: Manages password storage, retrieval, and related operations.

   Key methods:
   ```python
   def add_password(self, service: str, username: str, password: str, expiration_days: int = 90):
       # ... password saving logic ...

   def get_password(self, service: str) -> Dict:
       # ... password retrieval logic ...

   def export_passwords(self, filename: str):
       # ... export logic ...

   def import_passwords(self, filename: str):
       # ... import logic ...
   ```

## Security Considerations

- This tool uses strong encryption (Fernet) to secure stored passwords.
- The master password used for encryption is never stored and should be kept secret.
- For production use, consider using a unique salt for each user and storing it securely.
- Regularly update and rotate passwords, especially for sensitive accounts.
- Always use HTTPS when transmitting passwords over a network.

## Contributing

Contributions to this project are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
