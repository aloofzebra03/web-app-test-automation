import pytest
import requests


@pytest.mark.api
def test_health_check(base_url):
    response = requests.get(f"{base_url}/api/health", timeout=5)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.api
def test_login_with_valid_credentials(base_url):
    response = requests.post(
        f"{base_url}/api/login",
        json={"email": "qa@example.com", "password": "Password123"},
        timeout=5,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


@pytest.mark.api
@pytest.mark.parametrize(
    "email,password",
    [
        ("qa@example.com", "wrong-password"),
        ("unknown@example.com", "Password123"),
        ("", ""),
    ],
)
def test_login_rejects_invalid_credentials(base_url, email, password):
    response = requests.post(
        f"{base_url}/api/login",
        json={"email": email, "password": password},
        timeout=5,
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.api
@pytest.mark.parametrize("age", [18, 65])
def test_profile_accepts_boundary_ages(base_url, age):
    response = requests.post(
        f"{base_url}/api/profile",
        json={"username": "tester", "age": age},
        timeout=5,
    )

    assert response.status_code == 200
    assert response.json()["age"] == age


@pytest.mark.api
@pytest.mark.parametrize("age", [17, 66, -1, 100])
def test_profile_rejects_out_of_range_ages(base_url, age):
    response = requests.post(
        f"{base_url}/api/profile",
        json={"username": "tester", "age": age},
        timeout=5,
    )

    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.parametrize("username", ["ab", "x" * 21])
def test_profile_rejects_invalid_username_lengths(base_url, username):
    response = requests.post(
        f"{base_url}/api/profile",
        json={"username": username, "age": 30},
        timeout=5,
    )

    assert response.status_code == 422


@pytest.mark.api
def test_item_search_is_case_insensitive(base_url):
    response = requests.get(
        f"{base_url}/api/items",
        params={"q": "MOUSE"},
        timeout=5,
    )

    assert response.status_code == 200
    assert response.json()["items"] == [{"id": 2, "name": "Mouse"}]


@pytest.mark.api
def test_empty_search_returns_all_items(base_url):
    response = requests.get(f"{base_url}/api/items", timeout=5)

    assert response.status_code == 200
    assert len(response.json()["items"]) == 4
