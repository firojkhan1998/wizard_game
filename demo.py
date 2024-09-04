from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


# Define a function to generate the report
def generate_report(status, details):
    report_path = 'Product_order_report.html'
    with open(report_path, 'w') as report_file:
        report_file.write('<html><head><title>Product Order Report</title></head><body>')
        report_file.write(f'<h1>Test Result</h1>')
        report_file.write(f'<p>Status: {status}</p>')
        report_file.write(f'<p>Details: {details}</p>')
        report_file.write('</body></html>')


def setup_driver():
    chrome_options = Options()
    # You can add options if needed, e.g., chrome_options.add_argument('--headless')
    service = Service(executable_path='C:/webdriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver


def login(driver):
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


def sort_and_add_product(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))).click()
    driver.find_element(By.XPATH, "//option[@value='hilo']").click()  # Sorting high to low

    # Add the highest priced product to the cart
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "(//div[@class='inventory_item_price'])[1]"))).click()
    driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()


def checkout(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.XPATH, "//button[text()='Checkout']").click()
    driver.find_element(By.ID, "first-name").send_keys("Firoj")
    driver.find_element(By.ID, "last-name").send_keys("Khan")
    driver.find_element(By.ID, "postal-code").send_keys("201301")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()


def verify_and_finish(driver):
    # Wait for Checkout overview page to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label")))
    total_amount = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    assert "$49.99" in total_amount, f"Expected total amount $49.99 but got {total_amount}"

    driver.find_element(By.XPATH, "//button[text()='Finish']").click()
    # Wait for Checkout Complete page to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
    thank_you_header = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU FOR YOUR ORDER" in thank_you_header, f"Expected 'THANK YOU FOR YOUR ORDER' but got {thank_you_header}"


def main():
    driver = setup_driver()
    try:
        status = "Failed"
        details = ""

        login(driver)
        sort_and_add_product(driver)
        checkout(driver)
        verify_and_finish(driver)

        status = "Passed"
        details = "All steps executed successfully."

    except AssertionError as e:
        details = str(e)
    except Exception as e:
        details = f"An error occurred: {str(e)}"
    finally:
        generate_report(status, details)
        driver.quit()
        print("Test completed. Report generated.")


if __name__ == "__main__":
    main()
