from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.apps.users.models import TaskUser
from task_manager.apps.labels.models import Label
from task_manager.apps.statuses.models import Status


class LabelsTest(TestCase):
    def setUp(self):
        self.user = TaskUser.objects.create_user(
            username='user1',
            password='Zde6v45rGBYx2LGx',
        )
        self.client.force_login(self.user)
        self.label1 = Label.objects.create(name='first')
        self.label2 = Label.objects.create(name='second')
        self.label3 = Label.objects.create(name='third')

    def test_create(self):
        response = self.client.post('/labels/create/', {'name': 'Test1'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="Test1"))

    def test_labels_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='labels/labels.html',
        )

        tasks_list = list(response.context['object_list'])
        self.assertQuerysetEqual(
            tasks_list,
            [self.label1, self.label2, self.label3],
        )

    def test_update(self):
        response = self.client.post('/labels/1/update/', {'name': 'Test2'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="Test2"))

    def test_delete(self):
        response = self.client.post('/labels/1/delete/')
        response = self.client.post('/labels/2/delete/')
        response = self.client.post('/labels/3/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 0)

    def test_delete_used_label(self):
        self.client.post('/labels/create/', {'name': 'used_label'})
        self.client.post('/statuses/create/', {'name': 'used_status'})
        self.client.post('/tasks/create/', {
            'name': 'Task',
            'description': 'Task',
            'status': Status.objects.get(name='used_status').id,
            'executor': TaskUser.objects.get(username='user1').id,
            'labels': Label.objects.get(name='used_label').id,
        })
        response = self.client.post('/statuses/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="used_label"))
        self.assertEqual(Status.objects.count(), 1)
