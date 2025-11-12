import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_healthcheck_success(client):
    """Test healthcheck returns healthy status with database connection."""
    url = reverse("healthcheck")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "connected"


@pytest.mark.django_db
def test_healthcheck_returns_json(client):
    """Test healthcheck returns valid JSON response."""
    url = reverse("healthcheck")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Type"] == "application/json"

    data = response.json()
    assert "status" in data
    assert "database" in data
