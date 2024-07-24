"""Test for models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    """
    Test Models
    """
    def test_case_user_with_email_successfull(self):
        """
        Test creating a user with email is successfull
        """
        email= 'test@example.com'
        password= 'testpass123'
        user= get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test email is normalized for new users
        so this =>  user= get_user_model().objects.create_user(email, 'sample123')
        and this => user= get_user_model().objects.create_user(
            email=email,
            password=password,
        ) Are Same .........!!!!!!!
        """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user= get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test creating a new user without email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'tests1234')

    def test_create_superuser(self):
        """
        Test creating super user
        """
        user = get_user_model().objects.create_superuser(
            'test123@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)