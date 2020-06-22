from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """test the users API public"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test if user is created successfuly"""
        payload = {
            'email': 'test@ali.com',
            'password': 'test123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.chack_password(payload['password']))
        self.assertNotIn('password', res.data)
        
    def test_user_exists(self):
        """test user that already exists fails"""
        payload = {
            'email': 'test@ali.com',
            'password': 'test123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """should't create user"""
        payload = {
            'email': 'test@ali.com',
            'password': 'test',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
    
    def create_token_for_user(self):
        """test if a token is created for the user"""
        payload = {
            'email':'email@ali.com',
            'password':'test1234'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """test that token is not created if invalid credentials are given"""
        create_user(email='test@ali.com', password='test1234')
        payload = {
            'email':'test@ali.com',
            'password':'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email':'test@ali.com',
            'password':'test1234'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email':'fake', "password":'haha'})
        self.assertNotIn('token', res)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unautherized(self):
        """test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """test api requests that requires authentification"""
    def steUp(self):
        self.user = create_user(
            email='test@ali.com',
            password='test1234',
            name='my name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test retrieving profile for logged in users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name':self.user.name,
            'email':self.user.email
        })
    
    def test_post_me_not_allowed(self):
        """test that post is not alowed on me url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating the user profile for uthenticated users"""
        payload = {'name':'new name', 'password':'newpassword123'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        