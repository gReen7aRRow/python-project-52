from django.db import models
from django.db.models import Model
from django.utils.translation import gettext
from task_manager.apps.statuses.models import Status
from task_manager.apps.users.models import TaskUser
from task_manager.apps.labels.models import Label


class Task(Model):
    name = models.CharField(
        max_length=100,
        verbose_name=gettext('TaskName'),
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=gettext('TaskDesc'),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=gettext('TaskStatus'),
    )
    executor = models.ForeignKey(
        TaskUser,
        on_delete=models.PROTECT,
        related_name="task_executor",
        null=True,
        blank=True,
        verbose_name=gettext('TaskExec'),
    )
    creator = models.ForeignKey(
        TaskUser,
        on_delete=models.PROTECT,
        related_name='task_creator',
        null=True,
    )
    added_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=gettext('TaskLabels'),
    )

    def __str__(self):
        return self.name
