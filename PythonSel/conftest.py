"""
conftest.py
-----------
pytest configuration file for the PythonSel test suite.

conftest.py is automatically discovered by pytest and serves as a
shared setup/teardown and plugin configuration file for all tests
in the same directory and its subdirectories.

This file provides:
  1. A command-line option (--browser_name) to select the browser at runtime.
  2. A `browserInstance` fixture that initializes and tears down the WebDriver.
  3. A pytest hook (pytest_runtest_makereport) that captures screenshots on failure
     and embeds them into the HTML test report.

Usage:
  pytest --browser_name chrome --html=reports/report.html
  pytest --browser_name firefox --html=reports/report.html
"""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Module-level driver variable used by the screenshot helper function
# (needs to be accessible outside the fixture scope)
driver = None

# ---------------------------------------------------------------------------
# Custom CLI Option
# ---------------------------------------------------------------------------


def pytest_addoption(parser):
    """
       Registers a custom command-line option --browser_name.
       This allows users to specify which browser to run tests in
       without modifying the source code.

       Default value is "chrome" if not provided.
       Example: pytest --browser_name firefox
    """
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

# ---------------------------------------------------------------------------
# Browser Fixture
# ---------------------------------------------------------------------------

@pytest.fixture( scope="function" )
def browserInstance(request):
    """
        A pytest fixture that sets up a WebDriver instance before each test
        and tears it down (implicitly) after each test.

        scope="function" means a fresh browser is created for every individual test.

        Steps:
          1. Read the --browser_name option from the CLI.
          2. Launch the appropriate browser (Chrome or Firefox).
          3. Apply Chrome preferences to suppress password manager pop-ups.
          4. Navigate to the base URL of the application under test.
          5. yield the driver to the test function.
          6. Teardown would happen after yield — driver.close()

        The driver is also attached to the test node (request.node.driver) so the
        screenshot hook can access it even after the fixture scope ends.
    """
    global driver

    # Read the --browser_name value passed via the command line
    browser_name = request.config.getoption( "browser_name" )

    # Service() auto-detects the installed chromedriver/geckodriver
    service_obj = Service()
    if browser_name == "chrome":
        # Configure Chrome preferences to suppress pop-ups
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Launch Chrome with the configured options
        driver = webdriver.Chrome(service=service_obj, options=chrome_options)

        # Attach driver to the test item so the screenshot hook can access it
        request.node.driver = driver

    elif browser_name == "firefox":
        # Launch Firefox without any special options
        driver = webdriver.Firefox( service=service_obj)
        request.node.driver = driver

    # Implicit wait: up to 5 seconds for elements to be found before raising errors
    driver.implicitly_wait( 5 )

    # Navigate to the application's base URL before handing control to the test
    driver.get( "https://rahulshettyacademy.com/loginpagePractise/" )

    # yield passes the driver to the test function
    # Code BEFORE yield = setup (runs before the test)
    # Code AFTER yield = teardown (runs after the test)
    yield driver
    driver.close()

# ---------------------------------------------------------------------------
# Screenshot on Failure Hook
# ---------------------------------------------------------------------------

@pytest.hookimpl( hookwrapper=True )
def pytest_runtest_makereport(item):
    """
    A pytest hook that extends the HTML report plugin (pytest-html) to
    automatically capture and embed a screenshot whenever a test fails.

    hookwrapper=True allows this hook to wrap around pytest's built-in
    report generation and inspect/modify the result.

    Args:
        item: The pytest test item (contains test metadata and the driver reference).
    """


    pytest_html = item.config.pluginmanager.getplugin( 'html' )
    outcome = yield
    report = outcome.get_result()
    extra = getattr( report, 'extra', [] )


    if report.when == 'call' or report.when == "setup":
        xfail = hasattr( report, 'wasxfail' )
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join( os.path.dirname( __file__ ), 'reports' )
            file_name = os.path.join( reports_dir, report.nodeid.replace( "::", "_" ) + ".png" )
            print( "file name is " + file_name )
            _capture_screenshot( file_name )
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append( pytest_html.extras.html( html ) )
        report.extras = extra

# ---------------------------------------------------------------------------
# Screenshot Helper
# ---------------------------------------------------------------------------

def _capture_screenshot(file_name):
    """
       Helper function that saves a PNG screenshot of the current browser state.

       Uses the module-level `driver` variable set by the `browserInstance` fixture.
       Includes a guard in case the driver was never initialized (e.g., setup failure).

       Args:
           file_name (str): Full path where the screenshot PNG will be saved.
    """
    if driver is not None:
        # Save the current browser window as a PNG file at the given path
        driver.get_screenshot_as_file(file_name)
    else:
        # Driver may be None if the browser failed to launch (e.g., setup error)
        print("Driver is None, skipping screenshot capture.")