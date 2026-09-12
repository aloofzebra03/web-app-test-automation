# Bug Report Examples

These examples demonstrate the level of detail expected in actionable QA reporting.

## Example 1 — High severity

**Title:** Valid login returns success but user session is not persisted  
**Environment:** Local QA build, Chrome, Windows/macOS/Linux  
**Severity:** High  
**Priority:** High  
**Reproducibility:** 5/5

### Preconditions

The application is running and the tester has valid credentials.

### Steps to reproduce

1. Open the application.
2. Enter `qa@example.com`.
3. Enter `Password123`.
4. Click **Login**.
5. Refresh the page.
6. Attempt to access a session-protected area.

### Expected result

A successful login should establish a session that remains valid until logout or expiration.

### Actual result

The UI reports a successful login, but no session is retained.

### Evidence

- HTTP 200 returned by `/api/login`
- No session cookie/token is stored

### Suggested follow-up

Confirm whether the product requirement expects persistent authentication. If yes, implement and regression-test session handling.

---

## Example 2 — Medium severity

**Title:** Search with leading/trailing spaces returns unexpected results  
**Severity:** Medium  
**Priority:** Medium  
**Reproducibility:** 5/5

### Steps to reproduce

1. Enter `  mouse  ` in the search field.
2. Click **Search**.

### Expected result

Whitespace should be trimmed and the result should contain `Mouse`.

### Actual result

If trimming is absent, no result may be returned.

### Test recommendation

Add API and UI regression cases for whitespace normalization.
