# Secure Password Generator

A Python-based secure password generator that creates strong, customizable passwords suitable for production use.

## Features

- Generates cryptographically secure passwords
- Customizable password length
- Flexible character type selection (lowercase, uppercase, digits, special characters)
- Ensures at least one character from each selected type
- Complies with common password security standards
- Efficient and optimized for performance

## Requirements

- Python 3.6+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/secure-password-generator.git
   cd secure-password-generator
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies (if any in the future):
   ```
   pip install -r requirements.txt
   ```

## Usage

### As a standalone script

Run the script directly:

```
python password_generator.py
```

This will generate a password using default settings (16 characters, all character types).

### As a module in your project

```python
from password_generator import PasswordGenerator

generator = PasswordGenerator()

# Generate a password with default settings
password = generator.generate_password()

# Generate a custom password
custom_password = generator.generate_password(
    length=20,
    char_types={'lowercase', 'uppercase', 'digits'}
)

print(f"Default password: {password}")
print(f"Custom password: {custom_password}")
```

## Customization

You can customize the password generation by modifying the `generate_password` method parameters:

- `length`: Integer, minimum 8 (default: 12)
- `char_types`: Set of strings, can include 'lowercase', 'uppercase', 'digits', 'special' (default: all four types)

Example:
```python
password = generator.generate_password(length=15, char_types={'lowercase', 'digits', 'special'})
```

## Security Considerations

- This generator uses Python's `secrets` module for cryptographically strong random number generation.
- The minimum password length is set to 8 characters, but longer passwords are recommended for better security.
- While this generator creates strong passwords, always follow your organization's security policies and best practices.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This password generator is provided as-is, without any guarantees. Always ensure that generated passwords meet your specific security requirements before use in production environments.
