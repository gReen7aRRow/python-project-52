from django.urls import path
from users.views import UserCreateView, UserListView, \
    UserUpdateView, UserDeleteView


urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='create-user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user',),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user',),
]
