from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import StatusForm
from .models import Status
from django.shortcuts import redirect
from django.contrib import messages
from task_manager.apps.tasks.models import Task


class StatusesView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    template_name = 'statuses/create_status.html'
    success_message = gettext('SuccessCreateStatus')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext('SuccessUpdateStatus')


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext('SuccessDeleteStatus')

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.all().filter(status_id=obj.id):
            messages.error(self.request, gettext('CannotDeleteStatus'))
            return redirect('tasks')
        else:
            super(StatusDeleteView, self).delete(self.request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
