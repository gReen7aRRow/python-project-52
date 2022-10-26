from django.urls import path
from .views import (
    TasksCreateView,
    TasksDeleteView,
    TasksDetailView,
    TasksUpdateView,
    TasksView,
)

urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('create/', TasksCreateView.as_view(), name='create_task'),
    path('<int:pk>/update/', TasksUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete/', TasksDeleteView.as_view(), name='delete_task'),
    path('<int:pk>/', TasksDetailView.as_view(), name='detail_task'),
]
