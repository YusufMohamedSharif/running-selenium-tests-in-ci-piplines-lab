import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def setup_browser():
    """Configure browser differently for local vs CI (GitHub Actions)"""
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):  # Running in GitHub Actions
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    else:
        # Local (assumes chromedriver is on PATH)
        return webdriver.Chrome()

# Test 1
def test_invalid_email_shows_error_message():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        time.sleep(3)  # Wait for page to load
        # TODO: Enter valid name, invalid email
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("invalid-email")
        # TODO: Submit form
        driver.find_element(By.CSS_SELECTOR, "#signup-form > button").click() 
        # TODO: Confirm success message does NOT appear
        time.sleep(1)  # Wait for form submission
        assert "Thanks for subscribing, Test User!" not in driver.page_source
    finally:
        driver.quit()

# Test 2
def test_blank_password_prevents_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        time.sleep(3)  # Wait for page to load
        # TODO: Leave email blank
        driver.find_element(By.ID, "name").send_keys("Test User")
        # TODO: Submit form
        driver.find_element(By.CSS_SELECTOR, "#signup-form > button").click()
        # TODO: Check form validation blocks submit
        time.sleep(1)  # Wait for form submission
        email_input = driver.find_element(By.ID, "email")
        validation_msg = driver.execute_script("return arguments[0].validationMessage;", email_input)
        assert "fill out this field" in validation_msg.lower()


    finally:
        driver.quit()

# Test 3
def test_successful_signup_shows_thank_you():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        # TODO: Fill form with valid data
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("valid-email@example.com")
        # TODO: Submit
        driver.find_element(By.CSS_SELECTOR, "#signup-form > button").click()
        # TODO: Check thank-you message with name
        time.sleep(1)  # Wait for form submission
        assert "Thanks for subscribing, Test User!" in driver.page_source
    finally:
        driver.quit()

# Test 4
def test_form_resets_after_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        # TODO: Submit valid data
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "email").send_keys("valid-email@example.com")
        driver.find_element(By.CSS_SELECTOR, "#signup-form > button").click()
        # TODO: Confirm fields reset
        time.sleep(1)  # Wait for form submission
        name_input = driver.find_element(By.ID, "name")
        email_input = driver.find_element(By.ID, "email")
        assert name_input.get_attribute("value") == ""
        assert email_input.get_attribute("value") == ""
    finally:
        driver.quit()
