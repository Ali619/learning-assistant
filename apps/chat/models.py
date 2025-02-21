import uuid

from django.contrib.auth.models import User
from django.db import models

from apps.models.models import AIModel


class Message(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL)
    model = models.ForeignKey(AIModel, on_delete=models.SET_NULL)
    session_id = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} at {self.created_at}"

    class Meta:
        db_table = "message"


class HistoryMessage(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, blank=True, null=True)
    user_message = models.TextField(blank=True, null=True)
    model_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_modifier_id = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"HistoryMessage {self.id} - session {self.session_id}"

    class Meta:
        db_table = "history_message"
