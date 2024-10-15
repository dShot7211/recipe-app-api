"""Test for Django admin modifications"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    """
    Now we will set up an api client used for tesing
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test creating a user is successfull..
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        """
        this will make a post req to the url with the payload
        """
        res = self.client.post(CREATE_USER_URL, payload)

        """
        now check if the status is 201 of the res and compare it
        """
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        """
        now get the user from db of the same payload user
        """
        user = get_user_model().objects.get(email=payload['email'])
        """
        now we check the password of the user from db with checkpassword method
        """
        self.assertTrue(user.check_password(payload['password']))
        """
        dont send password back in the response
        """
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """
        Test error returned if user with email exists.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'tw',
            'name': 'Test Name',
        }
        """
        make a post req with short pass
        """
        res = self.client.post(CREATE_USER_URL, payload)
        """
        now we will see we should get bad request
        """

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        """
        Now we will se it the user is created or not /  it should not the below return boolen
        """
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        """
        we will check the user does not exist
        """
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):

        """
        Create user in the temp data base
        """        
        user_details ={
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }

        create_user(**user_details)

        """
        Create user with the post url and match them
        """        

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        """
        check the user with assert
        """        

        """
        assert in checks token is in res.data
        """        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """
        test returns error if the credentials invalid
        """

        payload = {'email': 'test@example.com',  'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test blank password return error
        """

        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

