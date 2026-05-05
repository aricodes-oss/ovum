import pytest

from rest_framework.test import APIClient


@pytest.mark.django_db
def test_admin_redirects_when_unauthenticated(api_client: APIClient) -> None:
    response = api_client.get("/api/admin/")
    assert response.status_code in (302, 301)


@pytest.mark.django_db
def test_allauth_session_endpoint_responds(api_client: APIClient) -> None:
    response = api_client.get("/api/_allauth/browser/v1/auth/session")
    assert response.status_code in (200, 401)
