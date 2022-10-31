from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from .forms import TaskForm
from .models import Task
from django.shortcuts import redirect
from django_filters.views import FilterView  # type: ignore
from .filters import TasksFilter


class TasksDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TasksView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    filterset_class = TasksFilter
    context_object_name = 'tasks'


class TasksCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/task_create.html'
    success_message = gettext('SuccessCreateTask')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TasksUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks')
    success_message = gettext('SuccessUpdateTask')


class TasksDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                      SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = gettext('SuccessDeleteTask')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TasksDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().creator.id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, gettext('CannotDeleteTask'))
        return redirect('tasks')
