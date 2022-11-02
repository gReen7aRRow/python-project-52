from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.apps.users.models import TaskUser
from task_manager.apps.statuses.models import Status


class UsersTest(TestCase):
    def setUp(self):
        self.user1 = TaskUser.objects.create_user(
            username='first_user',
            password='Zde6v45rGBYx2LGx',
        )
        self.user2 = TaskUser.objects.create_user(
            username='second_user',
            password='Zde6v45rGBYx2LGx',
        )
        self.client.force_login(self.user1)

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

    def test_users_list(self):
        response = self.client.get(reverse_lazy('users'))
        users_list = list(response.context['users'])
        test_user1, test_user2 = users_list

        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_user1.username, 'first_user')
        self.assertEqual(test_user2.username, 'second_user')

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

    def test_delete_another_user(self):
        self.client.force_login(self.user1)
        response = self.client.post('/users/2/delete/', follow=True)
        self.assertTrue(TaskUser.objects.filter(pk=self.user2.pk).exists())
        self.assertRedirects(response, '/users/', status_code=302)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя')

    def test_delete(self):
        response = self.client.post('/users/1/delete/')
        response = self.client.post('/users/2/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskUser.objects.count(), 1)

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
