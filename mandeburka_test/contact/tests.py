from django.test import TestCase
from django.contrib.auth.models import User
from mandeburka_test.contact.models import Request, ModelLog
from random import randint
from mandeburka_test.contact.widgets import ContactDateInput
from django.template import Template, Context
from django.contrib.sites.models import Site
from django.core.management import call_command
from StringIO import StringIO
from django.contrib.contenttypes.models import ContentType
import subprocess
import os
from django.conf import settings
import datetime
import sys


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
        self.assertEquals(
            response.context['settings'].TIME_ZONE, settings.TIME_ZONE)

    def test_secure_page(self):
        response = self.client.get('/edit')
        # redirect anonymous user to login page
        self.assertEquals(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            'http://testserver/accounts/login/?next=/edit')
        # authenticated user can see edit page
        self.client.login(username='admin', password='admin')
        response = self.client.get('/edit')
        self.assertEquals(response.status_code, 200)

    def random_profile(self, user):
        return {
            'first_name': '%s_%d' % (user.first_name, randint(0, 100)),
            'last_name': '%s_%d' % (user.last_name, randint(0, 100)),
            'date_of_birth': '%d-%02d-%02d' %
            (randint(1900, 2000), randint(1, 12), randint(1, 28)),
            'bio': '%s_%d' % (user.userprofile.bio, randint(0, 100)),
            'jabber': '%s_%d' % (user.userprofile.jabber, randint(0, 100)),
            'skype': '%s_%d' % (user.userprofile.skype, randint(0, 100)),
            'other_contacts': '%s_%d' %
            (user.userprofile.other_contacts, randint(0, 100)),
        }

    def assertUserEqualsData(self, user, data):
        for k, v in data.iteritems():
            if k in ('first_name', 'last_name'):
                user_value = getattr(user, k)
            else:
                user_value = getattr(user.userprofile, k)
            if k == 'date_of_birth':
                user_value = user_value.strftime('%Y-%m-%d')
            self.assertEquals(v, user_value)

    def test_edit_form(self):
        user = User.objects.get(username='admin')
        # valid form submission should update user record
        data = self.random_profile(user)
        self.client.login(username='admin', password='admin')
        response = self.client.post('/edit', data)
        self.assertEquals(response.status_code, 200)
        # reload user
        user = User.objects.get(username='admin')
        self.assertUserEqualsData(user, data)

    def test_edit_ajax_response(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(
            '/edit',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        # edit view should return json content
        self.assertIn('application/json', response['Content-Type'])
        # empty call should return errors
        self.assertContains(response, 'errors')
        # valid call should not return errors
        user = User.objects.get(username='admin')
        data = self.random_profile(user)
        response = self.client.post(
            '/edit',
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotContains(response, 'errors')
        user = User.objects.get(username='admin')
        self.assertUserEqualsData(user, data)

    def test_date_widget(self):
        w = ContactDateInput()
        rendered = w.render('name', 'value', {'id': 'some_test_id'})
        self.assertIn('id="some_test_id"', rendered)
        self.assertIn('name="name"', rendered)
        self.assertIn('value="value"', rendered)
        self.assertIn('$(\'#some_test_id\').datepicker', rendered)

    def test_edit_link_tag(self):
        t = Template('{% load edit_link %}{% edit_link object %}')
        user = User.objects.get(username='admin')
        c = Context({'object': user})
        self.assertEquals(
            '<a href="/admin/auth/user/%d/">%s</a>' %
            (user.id, user.__class__.__name__),
            t.render(c)
        )
        site = Site.objects.get(pk=1)
        c = Context({'object': site})
        self.assertEquals(
            '<a href="/admin/sites/site/%d/">%s</a>' %
            (site.id, site.__class__.__name__),
            t.render(c)
        )

    def check_all_models_output(self, output):
        for model_type in ContentType.objects.all():
            self.assertIn('%s_%s - %d' % (
                model_type.app_label,
                model_type.model,
                model_type.model_class().objects.count()),
                output
            )

    def test_all_models_command(self):
        stdout = StringIO()
        stderr = StringIO()
        call_command('all_models', stderr=stderr, stdout=stdout)
        # check if stderr output is duplicated
        for l_out, l_err in zip(stdout.readlines(), stderr.readlines()):
            self.assertEquals(l_err, 'Error: %s' % l_out)
        self.check_all_models_output(stdout.getvalue())

    def test_all_models_bash_script(self):
        os.environ['PATH'] = '%s:%s' % (
            os.path.split(sys.executable)[0], os.environ['PATH'])
        p = subprocess.Popen(
            ['sh', os.path.join(settings.SITE_ROOT, '..', 'all_models.sh')],
            stdout=subprocess.PIPE)
        out, err = p.communicate()
        file_path = '%s.dat' % datetime.date.today().strftime('%Y-%m-%d')
        #check file created
        self.assertTrue(os.path.exists(file_path))
        f = open(file_path, 'r')
        for l_out, l_err in zip(out.split('\n'), f.readlines()):
            self.assertEquals(l_err.rstrip('\n'), 'Error: %s' % l_out)
        os.unlink(file_path)

    def check_last_log_entry_for_action(self, model, action):
        log = ModelLog.objects.order_by('-created_at')
        self.assertTrue(len(log) > 0)
        log_entry = log[0]
        self.assertEquals(log_entry.app_label, model._meta.app_label)
        self.assertEquals(log_entry.model_name, model.__class__.__name__)
        self.assertEquals(log_entry.action, action)

    def test_model_log(self):
        user = User.objects.get(username='admin')
        user.last_name = 'New Last_Name %d' % randint(0, 100)
        user.save()
        self.check_last_log_entry_for_action(user, ModelLog.ACTION_UPDATE)

        request = Request(path='/some/action', method='GET')
        request.save()
        self.check_last_log_entry_for_action(request, ModelLog.ACTION_CREATE)
        request.delete()
        self.check_last_log_entry_for_action(request, ModelLog.ACTION_DELETE)

    def test_priority_field(self):
        response = self.client.post('/requests')
        request = Request.objects.order_by('-created_at')[0]
        # check if default value of priority is 0
        self.assertEquals(request.priority, 0)
        request.priority = 10
        request.save()
        for i in range(15):
            self.client.get('/')
        response = self.client.get('/requests')
        # first item must be our request with priority 10
        first_request_item = response.context['requests'][0]
        self.assertEquals(first_request_item, request)
