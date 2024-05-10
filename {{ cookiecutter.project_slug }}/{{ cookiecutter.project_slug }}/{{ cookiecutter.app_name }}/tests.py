from django.test import TestCase
from django.contrib.auth.models import User


class Test(TestCase):
    """Default Test Case for the Template Microservice."""

    def setUp(self):
        """Set up the test case."""
        pass

    def test_true(self):
        """Basic test case"""
        user, created = User.objects.get_or_create(username='john')
        self.assertTrue(created)
        self.assertEqual(user.username, 'john')
