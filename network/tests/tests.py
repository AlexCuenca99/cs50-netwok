from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Reaction, Follow

User = get_user_model()


# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
