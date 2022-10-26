from users.models import TaskUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from users.forms import RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task


class UserCreateView(SuccessMessageMixin, CreateView):
    """User registration view."""

    template_name = 'users/create_user.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = gettext('SuccessCreateUser')


class UserListView(ListView):
    """User list view."""

    template_name = 'users/users.html'
    model = TaskUser
    context_object_name = 'users'


class UserLoginView(SuccessMessageMixin, LoginView):
    """User login view."""

    template_name = 'users/login.html'
    success_message = gettext('SuccessLoginUser')

    def get_success_url(self):
        return reverse_lazy('index')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """User logout view."""

    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, gettext('SuccessLogoutUser'))
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    """Change user data view."""

    template_name = 'users/update_user.html'
    model = TaskUser
    form_class = RegistrationForm
    success_url = reverse_lazy('users')
    success_message = gettext('SuccessUpdateUser')

    def test_func(self):
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, gettext('ErrorUserDoNotHaveRights'))
        return redirect('users')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, DeleteView):
    """Delete user view."""

    model = TaskUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users')
    success_message = gettext('SuccessDeleteUser')
    error_message = gettext('CannotDeleteUser')

    def test_func(self):
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, gettext('ErrorUserDoNotHaveRights'))
        return redirect('users')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if Task.objects.all().filter(executor=obj.id) or Task.objects.all().filter(creator=obj.id):  # noqa E501
            messages.error(self.request, self.error_message)
            return redirect('users')
        else:
            super(UserDeleteView, self).delete(self.request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
