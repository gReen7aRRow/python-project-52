from django.test import TestCase
from users.models import TaskUser
from statuses.models import Status


class UsersTest(TestCase):
    def setUp(self):
        self.user = TaskUser.objects.create_user(
            username='user1',
            password='Zde6v45rGBYx2LGx',
        )
        self.client.force_login(self.user)

    def test_register(self):
        response = self.client.post(
            '/users/create/',
            {
                'first_name': 'user2',
                'last_name': 'user2',
                'username': 'user2',
                'password1': 'Zde6v45rGBYx2LGx',
                'password2': 'Zde6v45rGBYx2LGx',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskUser.objects.filter(username="user2"))

    def test_update(self):
        response = self.client.post(
            '/users/1/update/',
            {
                'first_name': 'user3',
                'last_name': 'user3',
                'username': 'user3',
                'password1': 'Zde6v45rGBYx2LGx',
                'password2': 'Zde6v45rGBYx2LGx',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskUser.objects.filter(username="user3"))

    def test_delete(self):
        response = self.client.post('/users/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskUser.objects.count(), 0)

    def test_delete_used_user(self):
        self.client.post(
            '/users/create/',
            {
                'first_name': 'user',
                'last_name': 'user',
                'username': 'user_in_use',
                'password1': 'Zde6v45rGBYx2LGx',
                'password2': 'Zde6v45rGBYx2LGx',
            },
        )
        self.client.post('/statuses/create/', {'name': 'status'})
        self.client.post('/tasks/create/', {
            'name': 'Task',
            'description': 'Task',
            'status': Status.objects.get(name='status').id,
            'executor': TaskUser.objects.get(username='user_in_use').id,
        })
        response = self.client.post('/users/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskUser.objects.filter(username="user_in_use"))
