from django.forms import CheckboxInput
from django_filters import BooleanFilter  # type: ignore
from django_filters import FilterSet, ModelChoiceFilter
from .models import Task, Label


class TasksFilter(FilterSet):
    labels = ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
    )
    self_task = BooleanFilter(
        method='filter_self_tasks',
        widget=CheckboxInput,
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_task']
