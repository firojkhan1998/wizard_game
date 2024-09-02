from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
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

# Set up the Chrome WebDriver
chrome_options = Options()
service = Service(executable_path='C:/webdriver/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

try:
    # Initialize the report
    status = "Failed"
    details = ""

    # Step 1: Navigate to the login page
    driver.get("https://www.saucedemo.com/")
    time.sleep(3)

    # Step 2: Log in with provided credentials
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    time.sleep(3)

    # Step 3: Sort products from high price to low price
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    driver.find_element(By.XPATH, "//option[@value='hilo']").click()  # Sorting high to low

    time.sleep(5)

    # Step 4: Add the highest priced product to the cart
    highest_priced_product = driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[1]")
    highest_priced_product.click()
    driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()

    # Step 5: Click on the cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Step 6: Click on checkout
    driver.find_element(By.XPATH, "//button[text()='Checkout']").click()

    # Step 7: Enter checkout information
    driver.find_element(By.ID, "first-name").send_keys("Firoj")
    driver.find_element(By.ID, "last-name").send_keys("Khan")
    driver.find_element(By.ID, "postal-code").send_keys("201301")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    # Wait for Checkout overview page to load
    time.sleep(5)

    # Step 8: Verify total amount
    total_amount = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    assert "$49.99" in total_amount, f"Expected total amount $49.99 but got {total_amount}"

    # Step 9: Click Finish button
    driver.find_element(By.XPATH, "//button[text()='Finish']").click()

    # Wait for Checkout Complete page to load
    time.sleep(3)

    # Step 10: Verify "Thank You" header is shown
    thank_you_header = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU FOR YOUR ORDER" in thank_you_header, f"Expected 'THANK YOU FOR YOUR ORDER' but got {thank_you_header}"

    # Update report status
    status = "Passed"
    details = "All steps executed successfully."

except AssertionError as e:
    details = str(e)
except Exception as e:
    details = f"An error occurred: {str(e)}"
finally:
    # Generate the report
    generate_report(status, details)

    # Clean up and close the browser
    driver.quit()

    print("Test completed. Report generated.")
