# Web Application Test Automation

A portfolio-ready QA automation project demonstrating **manual + automated testing** of a small web application and REST API using:

- **Playwright**
- **Selenium**
- **Pytest**
- **Postman**
- **Python**
- **FastAPI**

The project covers functional, regression, negative, boundary, and edge-case testing, with reproducible defect documentation and CI-friendly test organization.

## What this project demonstrates

- Test case design for happy-path, negative, boundary, and edge-case scenarios
- Browser automation with both Playwright and Selenium
- REST API validation with Pytest + Requests
- Postman collection for manual/API regression testing
- Reusable fixtures and Page Object-style helpers
- Clear expected-vs-actual assertions
- Defect reporting examples with severity and reproduction steps
- GitHub Actions workflow for automated regression checks

## Application under test

The included FastAPI demo application provides:

1. **Login**
   - Valid user: `qa@example.com`
   - Valid password: `Password123`
   - Invalid credentials return HTTP 401

2. **Profile validation**
   - Username length: 3–20 characters
   - Allowed age range: 18–65
   - Boundary and invalid-input cases are covered

3. **Item search**
   - Case-insensitive query filtering
   - Empty query returns all items

## Project structure

```text
web-app-test-automation/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_playwright_ui.py
│   └── test_selenium_ui.py
├── postman/
│   └── QA_Web_App.postman_collection.json
├── docs/
│   ├── test_strategy.md
│   └── bug_report_examples.md
├── .github/workflows/
│   └── tests.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## Local setup

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run the application

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

## Run tests

API tests:

```bash
pytest -m api -v
```

Playwright tests:

```bash
pytest -m playwright -v
```

Selenium tests:

```bash
pytest -m selenium -v
```

All tests:

```bash
pytest -v
```

The Pytest session fixture starts and stops the FastAPI app automatically when the tests run.

## Postman

Import:

```text
postman/QA_Web_App.postman_collection.json
```

The collection includes:

- Health check
- Valid login
- Invalid login
- Profile minimum-age boundary
- Profile maximum-age boundary
- Under-age negative test
- Invalid username negative test
- Item search

## Test coverage summary

| Area | Example coverage |
|---|---|
| Functional | Valid login, valid profile, item search |
| Negative | Invalid credentials, invalid username |
| Boundary | Ages 18 and 65 accepted; 17 and 66 rejected |
| Regression | Core login/profile/search workflows |
| API | Status codes, JSON payloads, validation errors |
| UI | User-visible success/error messages |
| Cross-layer | Browser action validated against backend behavior |

## Sample defect-report format

Each issue should contain:

- Title
- Environment
- Preconditions
- Steps to reproduce
- Expected result
- Actual result
- Severity / priority
- Evidence
- Reproducibility
- Retest status

See [`docs/bug_report_examples.md`](docs/bug_report_examples.md).

