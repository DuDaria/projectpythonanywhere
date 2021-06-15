from django.urls import reverse, resolve

class TestUrls:
    def test_detail_url(self):
        path = reverse('index', )
        assert resolve(path).view_name == 'index'

    def test_category_url(self):
        path = reverse('advito:category_post', kwargs={'category_id': 1})
        assert resolve(path).view_name == 'category_post'

