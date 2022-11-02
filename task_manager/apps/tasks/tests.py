from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from task_manager.apps.statuses.models import Status
from task_manager.apps.users.models import TaskUser
from .models import Task
from .filters import TasksFilter


class TasksTest(TestCase):
    def setUp(self):
        self.user1 = TaskUser.objects.create_user(
            username='user1',
            password='Zde6v45rGBYx2LGx',
        )
        self.client.force_login(self.user1)
        self.user2 = TaskUser.objects.create_user(
            username='user2',
            password='Zde6v45rGBYx2LGx',
        )
        Status.objects.create(name='New')
        Status.objects.create(name='InProgress')
        self.task1 = Task.objects.create(
            name='Task',
            description='Task',
            status=Status.objects.get(name='New'),
            executor=TaskUser.objects.get(username='user2'),
            creator=self.user1,
        )
        self.task2 = Task.objects.create(
            name='Test',
            description='Test',
            status=Status.objects.get(name='New'),
            executor=TaskUser.objects.get(username='user2'),
            creator=self.user1,
        )
    
    def test_tasks_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/tasks.html'
        )

        tasks_list = list(response.context['tasks'])
        self.assertQuerysetEqual(tasks_list, [self.task1, self.task2])

    def test_create(self):
        response = self.client.post('/tasks/create/', {
            'name': 'Task2',
            'description': 'Task2',
            'status': Status.objects.get(name='New').id,
            'executor': TaskUser.objects.get(username='user2').id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Task2"))
        self.assertTrue(Task.objects.filter(status=1))

    def test_update(self):
        response = self.client.post('/tasks/1/update/', {
            'name': 'Task3',
            'description': 'Task3',
            'status': Status.objects.get(name='InProgress').id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Task3"))
        self.assertTrue(Task.objects.filter(status=2))

    def test_delete_task_without_rights(self):
        self.client.force_login(self.user2)
        url = '/tasks/2/delete/'
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())
        self.assertRedirects(response, '/tasks/', status_code=302)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задачу может удалить только её автор')

    def test_delete(self):
        response = self.client.post('/tasks/1/delete/')
        response = self.client.post('/tasks/2/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_filter(self):
        Task.objects.create(
            name='TestFilter',
            description='TestFilter',
            status=Status.objects.get(name='New'),
            executor=TaskUser.objects.get(username='user1'),
            creator=self.user1,
        )
        result_executor = TaskUser.objects.get(username='user1')
        qs = Task.objects.all()
        filtered = TasksFilter(
            data={'executor': result_executor},
            queryset=qs,
        )
        filtrated_tasks = filtered.qs
        expected_tasks = Task.objects.filter(executor=result_executor)
        self.assertQuerysetEqual(filtrated_tasks, expected_tasks)
