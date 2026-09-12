# Test Strategy

## Objective

Validate the demo application's critical user and API workflows with a compact regression suite that demonstrates professional QA fundamentals.

## In scope

- Authentication
- Profile validation
- Search
- REST API status codes and payloads
- UI feedback after success and failure
- Boundary validation
- Negative-input handling

## Out of scope

- Performance/load testing
- Security penetration testing
- Cross-browser matrix beyond Chromium/Chrome
- Accessibility certification

## Test types

### Functional testing
Verify that supported user workflows behave according to requirements.

### Regression testing
Re-run login, profile, and search suites after code changes.

### Negative testing
Use incorrect credentials, invalid usernames, and unsupported ages.

### Boundary testing
Verify the inclusive age boundaries:
- 18: accepted
- 65: accepted
- 17: rejected
- 66: rejected

### API testing
Validate:
- HTTP status codes
- JSON response bodies
- validation failures
- case-insensitive search behavior

### Browser automation
Use:
- Playwright for reliable locator-based browser tests
- Selenium for WebDriver-based regression checks

## Entry criteria

- Dependencies installed
- Local port 8000 available
- Chromium/Chrome available for browser tests

## Exit criteria

- All critical API tests pass
- All supported browser regression tests pass
- No unresolved high-severity defects in tested flows
