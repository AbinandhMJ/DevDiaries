import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_successful_registration():
    client = Client()
    # Submit registration form data
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'testpassword',
        'password2': 'testpassword'
    })
    # Check if registration is successful by checking if the user is created
    assert response.status_code == 302  # Redirects to homepage upon successful registration
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_successful_login():
    client = Client()
    # Create a user for testing login
    User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    # Submit login form data
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword'
    })
    # Check if login is successful by checking if the user is authenticated
    assert response.status_code == 302  # Redirects to dashboard upon successful login
    assert '_auth_user_id' in client.session

@pytest.mark.django_db
def test_invalid_login():
    client = Client()
    # Submit login form data with invalid credentials
    response = client.post(reverse('login'), {
        'username': 'invaliduser',
        'password': 'invalidpassword'
    })
    # Check if login fails by checking if the user is not authenticated
    assert response.status_code == 200  # Stay on the login page upon invalid login
    assert '_auth_user_id' not in client.session
