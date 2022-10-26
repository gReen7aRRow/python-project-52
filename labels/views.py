from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import LabelForm
from .models import Label
from tasks.models import Task


class LabelsView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    template_name = 'labels/create_label.html'
    success_message = gettext('SuccessCreateLabel')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')
    success_message = gettext('SuccessUpdateLabel')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels')
    success_message = gettext('SuccessDeleteLabel')

    def delete(self, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.filter(labels__id=obj.id):
            messages.error(self.request, gettext('CannotDeleteLabel'))
            return redirect('labels')
        else:
            super(LabelDeleteView, self).delete(self.request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
