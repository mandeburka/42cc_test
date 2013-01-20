from django.test import TestCase
from django.contrib.auth.models import User
from mandeburka_test.contact.models import Request
from random import randint


class ContactTest(TestCase):

    def test_user_exists(self):
        try:
            User.objects.get(username='admin')
        except User.DoesNotExist:
            self.fail('user not found')

    def test_main_page(self):
        user = User.objects.get(username='admin')
        response = self.client.get('/')
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, '14.02.1987')
        self.assertContains(response, 'Email: %s' % user.email)
        self.assertContains(response, 'Jabber: %s' % user.userprofile.jabber)
        self.assertContains(response, user.userprofile.bio)
        self.assertContains(response, user.userprofile.other_contacts)
        self.assertContains(response, 'Skype: %s' % user.userprofile.skype)

    def test_request_middleware(self):
        response = self.client.get('/')
        response = self.client.get('/requests')
        response = self.client.post('/')
        response = self.client.post('/requests')
        self.assertQuerysetEqual(
            Request.objects.order_by('created_at'),
            [
                '<Request: / GET>',
                '<Request: /requests GET>',
                '<Request: / POST>',
                '<Request: /requests POST>'
            ])
        response = self.client.get('/requests')
        self.assertContains(response, '/ POST')
        self.assertContains(response, '/requests POST')
        for i in range(10):
            response = self.client.post('/')
        response = self.client.get('/requests')
        self.assertNotContains(response, '/ GET')
        self.assertNotContains(response, '/requests POST')
        self.assertContains(response, '/ POST')

    def test_settings_in_context(self):
        response = self.client.get('/')
        self.assertIn('settings', response.context)
        settings = response.context['settings']
        self.assertEquals(settings.TIME_ZONE, 'Europe/Kiev')

    def test_secure_page(self):
        response = self.client.get('/edit')
        # redirect anonymous user to login page
        self.assertEquals(response.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/login')
        # authenticated user can see edit page
        self.client.login(username='admin', password='admin')
        response = self.client.get('/edit')
        self.assertEquals(response.status_code, 200)

    def test_edit_form(self):
        self.client.login(username='admin', password='admin')
        user = User.objects.get(username='admin')
        # valid form submission should update user record
        data = {
            'first_name': '%s_%d' % (user.first_name, randint(0, 100)),
            'last_name': '%s_%d' % (user.last_name, randint(0, 100)),
            'date_of_birth': '%02d.%02d.%d' %
            (randint(1, 28), randint(1, 12,), randint(1900, 2000)),
            'bio': '%s_%d' % (user.userprofile.bio, randint(0, 100)),
            'jabber': '%s_%d' % (user.userprofile.jabber, randint(0, 100)),
            'skype': '%s_%d' % (user.userprofile.skype, randint(0, 100)),
            'other_contacts': '%s_%d' %
            (user.userprofile.other_contacts, randint(0, 100)),
        }
        response = self.client.post('/edit', data)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/')
        # reload user
        user = User.objects.get(username='admin')
        for k, v in data.iteritems():
            if k in ('first_name', 'last_name'):
                user_value = getattr(user, k)
            else:
                user_value = getattr(user.userprofile, k)
            if k == 'date_of_birth':
                user_value = user_value.strftime('%d.%m.%Y')
            self.assertEquals(v, user_value)
