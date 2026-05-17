"""
test_e2eTestFramework.py
------------------------
End-to-end (E2E) test using the Page Object Model (POM) design pattern
with data-driven testing via a JSON file.

This test simulates a full user journey on rahulshettyacademy.com:
  Login → Browse Shop → Add Product to Cart → Checkout → Enter Address → Confirm Order

Design Patterns Used:
  - Page Object Model (POM): Each page of the app is represented by a class
    (LoginPage, ShopPage, CheckoutConfirmationPage) encapsulating its elements and actions.
  - Data-Driven Testing: Test input data is read from a JSON file, and the test
    is parameterized to run once for each dataset.

CLI Usage Examples:
  pytest -m smoke                                        # Run only smoke-tagged tests
  pytest -n 10                                           # Run 10 tests in parallel (pytest-xdist)
  pytest -n 2 -m smoke --browser_name firefox --html=reports/report.html
"""


import json
import os
import sys

import pytest
from selenium import webdriver

# Append the parent directory to sys.path so that the pageObjects package (which lives one level up) can be imported correctly
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# Page Object classes — each encapsulates a page's elements and user interactions
from pageObjects.login import LoginPage
from pageObjects.shop import ShopPage

# ---------------------------------------------------------------------------
# Load Test Data from JSON File
# ---------------------------------------------------------------------------

# Path to the JSON file containing test datasets (relative to this file's location)
test_data_path = '../data/test_e2eTestFramework.json'
with open( test_data_path ) as f:
    test_data = json.load( f )
    # Extract the list of test cases from the "data" key.
    # Each item in test_list is a dict with keys: userEmail, userPassword, productName
    test_list = test_data["data"]

# ---------------------------------------------------------------------------
# E2E Test Function
# ---------------------------------------------------------------------------

# Tag this test as part of the "smoke" test suite
@pytest.mark.smoke
# parametrize creates one test run per item in test_list.
# Each run uses a different set of {userEmail, userPassword, productName}
@pytest.mark.parametrize( "test_list_item", test_list )
def test_e2e(browserInstance, test_list_item):
    """
    Full end-to-end test for the login-to-order workflow.

    Args:
        browserInstance:  pytest fixture (from conftest.py) that provides an initialized
                             WebDriver instance pointed at the login page.
        test_list_item:   A single test dataset dict from the JSON file, e.g.:
                              {"userEmail": "user@test.com", "userPassword": "pass", "productName": "Iphone X"}
    """

    # Retrieve the WebDriver instance from the fixture
    driver = browserInstance

    # --- Step 1: Login ---
    # Instantiate the LoginPage Page Object with the current driver
    loginPage = LoginPage( driver )
    print(loginPage.getTitle())

    # Perform login using credentials from the test data.
    # loginPage.login() fills the form, submits it, and returns a ShopPage instance.
    shop_page = loginPage.login( test_list_item["userEmail"], test_list_item["userPassword"] )

    # --- Step 2: Add Product to Cart ---
    # Use the shop page's method to find the specified product and add it to the cart
    shop_page.add_product_to_cart( test_list_item["productName"] )
    print(shop_page.getTitle())

    # --- Step 3: Proceed to Cart ---
    # Clicking the cart icon navigates to the checkout confirmation page.
    # Returns a CheckoutConfirmationPage instance.
    checkout_confirmation = shop_page.goToCart()

    # --- Step 4: Checkout ---
    # Clicks the "Proceed To Checkout" button on the cart page
    checkout_confirmation.checkout()

    # --- Step 5: Enter Delivery Address ---
    # Types the country prefix ("ind") into the address field and selects "India"
    checkout_confirmation.enter_delivery_address( "ind" )

    # --- Step 6: Validate and Place Order ---
    # Checks the terms checkbox and clicks the "Place Order" button,
    # then asserts the success message appears
    checkout_confirmation.validate_order()