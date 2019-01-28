from django.contrib.auth import get_user_model
from django.test import TestCase

from .. import models


class UserFileListViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user_alice = User.objects.create(username='alice')
        self.user_bob = User.objects.create(username='bob')

    def testCantSeeOthersPrivateFiles(self):
        alice_file = models.UserFile.objects.create(user=self.user_alice, public=False)
        self.client.force_login(self.user_bob)
        response = self.client.get('/files/')
        self.assertNotIn(alice_file, response.context['object_list'])

    def testCanSeeOthersPublicFiles(self):
        alice_file = models.UserFile.objects.create(user=self.user_alice, public=True)
        self.client.force_login(self.user_bob)
        response = self.client.get('/files/')
        self.assertIn(alice_file, response.context['object_list'])

    def testCanSeeOwnFiles(self):
        file_one = models.UserFile.objects.create(user=self.user_alice, public=True)
        file_two = models.UserFile.objects.create(user=self.user_alice, public=True)
        self.client.force_login(self.user_alice)
        response = self.client.get('/files/')
        self.assertIn(file_one, response.context['object_list'])
        self.assertIn(file_two, response.context['object_list'])
