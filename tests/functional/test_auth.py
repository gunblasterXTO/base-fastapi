from fastapi import status
from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


class TestAuthRoutes:
    def test_login_success(self):
        json_body = {
            "username": "gunblasterXTO",
            "password": ""
        }
        response = client.post(url="/v1/login", json=json_body)
        response_body = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert response_body == {}

    def test_login_fail_by_username(self):
        ...

    def test_login_fail_by_password(self):
        ...
