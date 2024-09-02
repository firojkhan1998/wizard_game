from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Configure WebDriver
service = Service('C:/webdriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Initialize report data
report = {
    'scenario_1': {
        'status': 'failed',
        'message': ''
    },
    'scenario_2': {
        'status': 'failed',
        'message': ''
    }
}


def login(username, password):
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)  # Wait for the page to load
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)  # Wait for the login action to complete


def verify_main_page():
    try:
        logo = driver.find_element(By.CLASS_NAME, "app_logo")
        assert logo.is_displayed(), "App Logo is not displayed"
        report['scenario_1']['status'] = 'passed'
        report['scenario_1']['message'] = "Successful login: App Logo is displayed."
    except AssertionError as e:
        report['scenario_1']['message'] = str(e)


def verify_error_message(expected_message):
    try:
        error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']")
        assert expected_message in error_message.text, "Error message is incorrect or not displayed"
        report['scenario_2']['status'] = 'passed'
        report['scenario_2']['message'] = "Failed login: Correct error message is displayed."
    except AssertionError as e:
        report['scenario_2']['message'] = str(e)


def generate_report():
    with open('Login_page_report.html', 'w') as file:
        file.write('<html><head><title>Test Report</title></head><body>')
        file.write('<h1>Test Report</h1>')

        for scenario, result in report.items():
            file.write(f'<h2>{scenario.replace("_", " ").title()}</h2>')
            file.write(f'<p>Status: {result["status"].capitalize()}</p>')
            file.write(f'<p>Message: {result["message"]}</p>')

        file.write('</body></html>')


def run_tests():
    # Scenario 1: Successful Login
    login("standard_user", "secret_sauce")
    verify_main_page()

    # Log out to reset the state before next scenario
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(2)

    # Scenario 2: Failed Login
    login("locked_out_user", "secret_sauce")
    verify_error_message("Sorry, this user has been banned.")

    # Close the browser
    driver.quit()

    # Generate report
    generate_report()


if __name__ == "__main__":
    run_tests()
