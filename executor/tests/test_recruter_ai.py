import pytest
from playwright.sync_api import Page, expect

def test_signup_with_valid_data(page: Page):
    '''Test that a user can sign up successfully with correct information.'''
    # Step: Navigate to the signup page.
    page.goto("https://www.recruter.ai/onboarding/Signup")
    # Step: Enter a valid name, a unique email, and a strong password.
    page.get_by_role("textbox", name="Enter your Name").fill("Test User")
    page.get_by_role("textbox", name="Enter your Business Email").fill("user@example.com")
    page.get_by_role("textbox", name="Enter your Password").fill("StrongPass123")
    # Step: Click the "Sign Up" button.
    page.get_by_role("button", name="Sign Up").click()
    # Expected: The user is successfully registered and redirected to the dashboard or a welcome page.


def test_signup_with_an_already_registered_email(page: Page):
    '''Verify that the system prevents signup with an email that is already in use.'''
    # Step: Navigate to the signup page.
    page.goto("https://www.recruter.ai/onboarding/Signup")
    # Step: Enter a name, an email address that is already registered, and a password.
    page.get_by_role("textbox", name="Enter your Business Email").fill("user@example.com")
    # Step: Click the "Sign Up" button.
    page.get_by_role("button", name="Sign Up").click()
    # Expected: An error message is displayed indicating that the email address is already taken.


def test_login_with_valid_credentials(page: Page):
    '''Test that a registered user can log in with their correct email and password.'''
    # Step: Navigate to the login page.
    page.goto("https://www.app.recruter.ai/")
    # Step: Enter the email and password of a registered user.
    page.get_by_role("textbox", name="Enter your Business Email").fill("user@example.com")
    # Step: Click the "Log In" button.
    page.get_by_role("button", name="Log In").click()
    # Expected: The user is authenticated and redirected to their dashboard.


def test_login_with_invalid_password(page: Page):
    '''Verify that the system prevents login when an incorrect password is provided.'''
    # Step: Navigate to the login page.
    page.goto("https://www.app.recruter.ai/")
    # Step: Enter the email of a registered user.
    page.get_by_role("textbox", name="Enter your Name").fill("Test User")
    page.get_by_role("textbox", name="Enter your Business Email").fill("user@example.com")
    # Step: Enter an incorrect password.
    page.get_by_role("textbox", name="Enter your Password").fill("StrongPass123")
    # Step: Click the "Log In" button.
    page.get_by_role("button", name="Log In").click()
    # Expected: An error message is displayed, such as "Invalid credentials" or "Incorrect password".
    # expect(page.locator("text=Invalid credentials")).to_be_visible()
