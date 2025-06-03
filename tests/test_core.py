import pytest
from password_manager.core import PasswordGenerator, PasswordManager, TwoFactorAuth

def test_password_generator():
    generator = PasswordGenerator()
    password = generator.generate_password(length=12)
    assert len(password) == 12
    strength = generator.check_password_strength(password)
    assert strength in ["Weak", "Moderate", "Strong", "Very Strong"]
    memorable = generator.generate_memorable_password(num_words=4)
    assert len(memorable.split("-")) == 4

def test_password_manager():
    manager = PasswordManager("test_master_password")
    manager.add_password("test_service", "test_user", "test_password")
    password_data = manager.get_password("test_service")
    assert password_data["username"] == "test_user"
    assert password_data["password"] == "test_password"
    manager.delete_password("test_service")
    with pytest.raises(ValueError):
        manager.get_password("test_service")

def test_two_factor_auth():
    tfa = TwoFactorAuth()
    setup_data = tfa.setup_2fa("test_service")
    assert "secret" in setup_data
    assert "qr_code_path" in setup_data
    code = tfa.get_current_code("test_service")
    assert tfa.verify_2fa("test_service", code)
    tfa.disable_2fa("test_service")
    assert tfa.get_current_code("test_service") is None