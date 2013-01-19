from django.test import TestCase
from django.contrib.auth.models import User
from mandeburka_test.contact.models import Request


class ContactTest(TestCase):

    def test_user_exists(self):
        try:
            User.objects.get(username='admin')
        except User.DoesNotExist:
            self.fail('user not found')

    def test_main_page(self):
        response = self.client.get('/')
        self.assertContains(response, 'Artur')
        self.assertContains(response, 'Gavkaliuk')
        self.assertContains(response, '14.02.1987')
        self.assertContains(response, 'Email: admin@mail.com')
        self.assertContains(response, 'Jabber: test@jabber.com')
        self.assertContains(response, 'My Bio')
        self.assertContains(response, 'My other contacts')
        self.assertContains(response, 'Skype: skype_id_test')

    def test_request_middleware(self):
        response = self.client.get('/')
        response = self.client.get('/admin')
        response = self.client.post('/')
        response = self.client.post('/admin')
        self.assertQuerysetEqual(
            Request.objects.order_by('created_at'),
            [
                '<Request: / GET>',
                '<Request: /admin GET',
                '<Request: / POST>',
                '<Request: /admin POST>'
            ])
