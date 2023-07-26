from django.contrib.auth.models import AbstractUser
from django.db import models

from model_utils.models import TimeStampedModel


class User(AbstractUser):
    pass


class Post(TimeStampedModel, models.Model):
    author = models.ForeignKey(
        "User",
        verbose_name=("Post Author"),
        related_name="authors",
        on_delete=models.CASCADE,
    )
    content = models.TextField("Post Content", max_length=150)

    def __str__(self):
        return f"{self.author} - {self.created}"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Reaction(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        "User", verbose_name=("User who reacts"), on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "Post", verbose_name=("Liked Post"), on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.created}"

    class Meta:
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"


class Follow(TimeStampedModel, models.Model):
    follower = models.ForeignKey(
        "User",
        verbose_name=("Follower"),
        related_name="followers",
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        "User",
        verbose_name=("Following"),
        related_name="followings",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.follower} follows to {self.following}"

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
