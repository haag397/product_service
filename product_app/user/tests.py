import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .models import User

@pytest.fixture
def create_user(db):
    def make_user(password="strongpassword123", email="testuser@example.com"):
        user = User.objects.create_user(password=password, email=email)
        return user
    return make_user

@pytest.fixture
def api_client(client, create_user):
    user = create_user()
    refresh_token = RefreshToken.for_user(user)
    access_token = str(refresh_token.access_token)
    client.defaults['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"
    return client, user, refresh_token

@pytest.fixture
def urls():
    return {
        "register": reverse("register"),
        "login": reverse("token_obtain_pair"),
        "logout": reverse("logout"),
        "profile": "/api/profile/",
    }

@pytest.mark.django_db
def test_register_valid_user(client, urls):
    user_data = {
        "password": "strongpassword123",
        "email": "newuser@example.com",
    }
    response = client.post(urls["register"], user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "message" in response.data
    assert response.data["message"] == "User registered successfully!"
    assert User.objects.filter(email=user_data["email"]).exists()

@pytest.mark.django_db
def test_register_invalid_user(client, urls):
    invalid_data = {"password": "short", "email": "invalid-email"}
    response = client.post(urls["register"], invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data

def test_logout_success(api_client, urls):
    client, user, refresh_token = api_client
    response = client.post(urls["logout"], {"refresh": str(refresh_token)})
    assert response.status_code == status.HTTP_205_RESET_CONTENT
    assert response.data["message"] == "Logout successful"

def test_view_profile(api_client, urls):
    client, user, _ = api_client
    response = client.get(urls["profile"])
    print(urls["profile"])
    print(urls["login"])
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["email"] == user.email

@pytest.mark.django_db
def test_update_profile(api_client, urls):
    client, user, _ = api_client
    updated_data = {"email": "updateduser@example.com"}
    response = client.patch(f"{urls['profile']}{user.id}/", updated_data, content_type="application/json" )
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == updated_data["email"]

def test_delete_profile(api_client, urls):
    client, user, _ = api_client
    response = client.delete(f"{urls['profile']}{user.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
