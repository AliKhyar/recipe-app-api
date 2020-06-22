from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """test if user is created with email"""
        email = "alikhyar2020@haha.org"
        password = "thisismymdp"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'chi@TKHRBIQA.FRR'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email,email.lower())

    def test_new_seper_user(self):
        """test creating a new super user"""
        user = get_user_model().objects.create_superuser(
            'ali@hi.fr',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')