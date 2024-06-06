import time
from datetime import timedelta
from django.test import TestCase
from .models import Category, Post, Comment
from django.utils import timezone

# Create your tests here.
class CategoryModelTest(TestCase):

    def test_string_representation(self):
        category = Category(name="Django")
        self.assertEqual(str(category), category.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "categories")

class PostModelTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name="Django")
        self.category2 = Category.objects.create(name="Python")

    def test_string_representation(self):
        post = Post.objects.create(
            title="My first post",
            body="This is the body of my first post.",
        )
        self.assertEqual(str(post), post.title)

    def test_post_categories(self):
        post = Post.objects.create(
            title="My first post",
            body="This is the body of my first post.",
        )
        post.categories.add(self.category1, self.category2)
        self.assertEqual(post.categories.count(), 2)
        self.assertIn(self.category1, post.categories.all())
        self.assertIn(self.category2, post.categories.all())

class CommentModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title="My first post",
            body="This is the body of my first post.",
        )

    def test_string_representation(self):
        comment = Comment.objects.create(
            author="John Doe",
            body="This is a comment.",
            post=self.post,
        )
        expected_string = f"{comment.author} on '{comment.post}'"
        self.assertEqual(str(comment), expected_string)

    def test_comment_creation(self):
        comment = Comment.objects.create(
            author="John Doe",
            body="This is a comment.",
            post=self.post,
        )
        now = timezone.now()
        time_difference = now - comment.created_on
        self.assertLessEqual(time_difference, timedelta(seconds=1))

    def test_comment_post_relation(self):
        comment = Comment.objects.create(
            author="John Doe",
            body="This is a comment.",
            post=self.post,
        )
        self.assertEqual(comment.post, self.post)