from django.test import TestCase
from urllib import response
from xmlrpc import client
from matplotlib.pyplot import cla
from django.urls import reverse


class HomeViewtest(TestCase):

    def test_root_url_resolves_to_home_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_view_uses_right_template(self):
        response = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(response, 'home.html')
