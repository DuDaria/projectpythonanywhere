from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, CategoryPost, Profile
from ..views import IndexView, DetailView


class TestIndexView(TestCase):
    def test_index_page_without_posts(self):
        response = self.client.get(reverse('advito:index'))
        self.assertContains(response, 'Постов еще нет')

    def test_status_index_page_without_posts(self):
        response = self.client.get(reverse('advito:index'))
        self.assertEqual(response.status_code, 200)
