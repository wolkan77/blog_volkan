from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import os

post_status = [
    ("t", "Taslak"),
    ("y", "Yayınlandı"),
    ("k", "Kaldırıldı")
]


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class PublishedPost(models.Manager):
    def get_queryset(self):

        return super().get_queryset().filter(status="y")


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_photo = models.FileField(upload_to="", blank=True, null=True)
    status = models.CharField(max_length=1, choices=post_status, default="t")
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = models.Manager()
    published_posts = PublishedPost()

    def __str__(self):
        return self.title

    class Meta:
        # default_manager_name = "published_posts"
        ordering = ["-created"]