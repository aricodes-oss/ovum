import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db: None) -> AbstractUser:
    return get_user_model().objects.create_user(
        username="testuser",
        email="test@example.com",
        password="test-pass-123",  # noqa: S106
    )


@pytest.fixture
def authenticated_client(api_client: APIClient, user: AbstractUser) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client
