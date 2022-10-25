from django.test import TestCase
from .models import Status
from users.models import TaskUser


class StatusesTest(TestCase):
    def setUp(self):
        self.user = TaskUser.objects.create_user(
            username='user1',
            password='Zde6v45rGBYx2LGx',
        )
        self.client.force_login(self.user)
        Status.objects.create(name='test')

    def test_create(self):
        response = self.client.post('/statuses/create/', {'name': 'test1'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="test1"))

    def test_update(self):
        response = self.client.post('/statuses/1/update/', {'name': 'test2'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="test2"))

    def test_delete(self):
        response = self.client.post('/statuses/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)

    def test_delete_used_status(self):
        self.client.post('/statuses/create/', {'name': 'used_status'})
        self.client.post('/tasks/create/', {
            'name': 'Task',
            'description': 'Task',
            'status': Status.objects.get(name='used_status').id,
            'executor': TaskUser.objects.get(username='user1').id,
        })
        response = self.client.post('/statuses/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="used_status"))
        self.assertEqual(Status.objects.count(), 1)
