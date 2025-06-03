import pytest
from PyQt6.QtWidgets import QApplication, QTabWidget, QPushButton
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from password_manager.gui import PasswordManagerGUI
import sys

@pytest.fixture(scope="session")
def app():
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def window(app):
    window = PasswordManagerGUI()
    window.show()
    return window

def test_window_title(window):
    assert window.windowTitle() == "Password Manager"

def test_initial_state(window):
    tab_widget = window.findChild(QTabWidget)
    assert tab_widget is not None
    assert tab_widget.count() == 2
    assert tab_widget.tabText(0) == "Generate Password"
    assert tab_widget.tabText(1) == "Manage Passwords"

def test_password_generation(window):
    generate_btn = None
    for btn in window.findChildren(QPushButton):
        if btn.text() == "Generate Password":
            generate_btn = btn
            break
    assert generate_btn is not None
    password_display = window.password_display
    assert password_display is not None
    assert password_display.text() == ""
    QTest.mouseClick(generate_btn, Qt.MouseButton.LeftButton)
    assert password_display.text() != ""
    assert len(password_display.text()) == 12

def test_password_strength_indicator(window):
    window.generate_password()
    assert window.strength_label.text() != ""
    assert any(strength in window.strength_label.text()
              for strength in ["Weak", "Moderate", "Strong", "Very Strong"])

def test_copy_password(window, monkeypatch):
    class MockClipboard:
        def setText(self, text): self.text = text
    mock_clipboard = MockClipboard()
    monkeypatch.setattr(QApplication, "clipboard", lambda: mock_clipboard)
    window.generate_password()
    password = window.password_display.text()
    copy_btn = None
    for btn in window.findChildren(QPushButton):
        if btn.text() == "Copy to Clipboard":
            copy_btn = btn
            break
    assert copy_btn is not None
    QTest.mouseClick(copy_btn, Qt.MouseButton.LeftButton)
    assert hasattr(mock_clipboard, "text")
    assert mock_clipboard.text == password

def test_master_password_validation(window):
    view_btn = None
    for btn in window.findChildren(QPushButton):
        if btn.text() == "View Password":
            view_btn = btn
            break
    assert view_btn is not None
    QTest.mouseClick(view_btn, Qt.MouseButton.LeftButton)

def test_2fa_setup_dialog(window):
    setup_2fa_btn = None
    for btn in window.findChildren(QPushButton):
        if btn.text() == "Setup 2FA":
            setup_2fa_btn = btn
            break
    assert setup_2fa_btn is not None
    QTest.mouseClick(setup_2fa_btn, Qt.MouseButton.LeftButton)

def test_password_history_dialog(window):
    history_btn = None
    for btn in window.findChildren(QPushButton):
        if btn.text() == "View History":
            history_btn = btn
            break
    assert history_btn is not None
    QTest.mouseClick(history_btn, Qt.MouseButton.LeftButton)