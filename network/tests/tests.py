from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Reaction, Follow

User = get_user_model()


# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            password="user123",
            username="AlexC",
            first_name="Alex",
            last_name="Cuenca",
            email="alex@alex.com",
        )

    def test_user_full_name(self):
        user_alex = User.objects.get(first_name="Alex")
        self.assertEqual(user_alex.get_username(), "AlexC")
