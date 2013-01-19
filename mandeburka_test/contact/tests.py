"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class ContactTest(TestCase):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertContains(response, 'Artur')
        self.assertContains(response, 'ig_jupiter3')
