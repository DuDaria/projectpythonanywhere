from django.test import TestCase, Client, RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.urls import reverse, resolve
from ..models import Profile, CategoryPost, Post, FavoritePost, Comment, Message
from ..views import PostCreateView, PostDetailView
import datetime
from django.http import HttpResponse


class CategoryPostModel(TestCase):
    def setUp(self):
        self.category = CategoryPost.objects.create(name_category="техника")
        self.category.save()
        super().setUp()
    
    def test_category_post(self):
        self.assertEqual(self.category.name_category, 'техника')
        self.assertNotEqual(self.category.name_category, '')
        self.assertNotEqual(self.category.name_category, ' ')
        self.assertTrue(self.category.name_category, True)
        self.assertIsInstance(self.category.name_category, str)


class TestProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username ='test', email='test@test.com', password='password')
        self.user.save()
        super().setUp()

    def test_birth_date(self):
        profile = Profile.objects.get(user=self.user)
        profile.birth_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.assertRaises(ValidationError)
        profile.save()



class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username ='test', email='test@test.com', password='password')
        self.user.save()
        super().setUp()

    def test_post(self):
        self.category = CategoryPost.objects.create(name_category="техника")
        image = SimpleUploadedFile("boiler.jpg", content=b'', content_type="image/jpg")
        self.post_1 = Post.objects.create(
            author = self.user,
            category = self.category,
            price = 25,
            name_descript = 'boiler',
            description = "boiler sale",
            image = image,
            date_pub = timezone.now(),
        )
        self.assertEqual(self.post_1.price, int(25))
        self.assertNotEqual(self.post_1.price, '')
        return self.post_1.id

    def test_response_post_view(self):
        path = reverse('advito:post_detail', kwargs={'post_id': self.test_post()})
        request = RequestFactory().get(path)
        response = self.client.get(reverse('advito:post_detail', kwargs={'post_id': self.test_post()}))
        self.assertEqual(response.status_code, 200)


# python manage.py test advito.tests
