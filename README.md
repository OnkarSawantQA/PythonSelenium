# Python Selenium Automation Framework

## Overview
This project is an End-to-End (E2E) Test Automation Framework developed using Python, Selenium WebDriver, and Pytest following the Page Object Model (POM) design pattern.

The framework automates a complete user journey on Rahul Shetty Academy's demo e-commerce application:

Login → Browse Shop → Add Product to Cart → Checkout → Enter Address → Confirm Order

The project demonstrates modern automation framework practices including:
- Page Object Model (POM)
- Data-Driven Testing using JSON
- Pytest Fixtures
- Parallel Execution
- HTML Reporting
- Screenshot Capture on Failure
- Cross-browser Execution
- Reusable Components

---

## Tech Stack

- Python
- Selenium WebDriver
- Pytest
- Pytest HTML Reports
- Pytest-xdist
- WebDriver Manager

---

## Framework Design Patterns

### Page Object Model (POM)
Each application page is represented by a separate class:
- LoginPage
- ShopPage
- CheckoutConfirmationPage

This improves:
- Maintainability
- Reusability
- Scalability

### Data-Driven Testing
Test data is stored in a JSON file and parameterized using Pytest.

---

## Project Structure

```text
PythonSelenium/
│
├── pageObjects/
├── pythonSel/
├── utils/
├── data/
├── reports/
├── requirements.txt
└── README.md
```

---

## Features

- End-to-End automation testing
- Reusable page objects
- Parallel test execution
- Smoke test execution using markers
- HTML report generation
- Screenshot capture on failure
- Browser selection through command line
- Data-driven framework

---

## Run Tests

### Run all tests
```bash
pytest
```

### Run smoke tests
```bash
pytest -m smoke
```

### Run tests in parallel
```bash
pytest -n 2
```

### Generate HTML Report
```bash
pytest -m smoke --html=reports/report.html
```

### Run on specific browser
```bash
pytest --browser_name chrome
```

---

## Pytest Configuration

The `conftest.py` file provides:
- Browser initialization fixture
- Command-line browser selection
- Screenshot capture on failure
- HTML report integration
- Shared setup and teardown

---

## Author
Onkar Sawant

