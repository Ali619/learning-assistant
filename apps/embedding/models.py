import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class DocumetnType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,
                            unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True)
    disable_at = models.DateTimeField(blank=True, null=True)
    last_modifier_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "document_type"


class Documetns(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_type = models.ForeignKey(DocumetnType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    creator_id = models.IntegerField()
    last_modifier_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disable_at = models.DateTimeField(blank=True, null=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document {self.id} - type {self.document_type} - created at {self.created_at}"

    class Meta:
        db_table = "documents"
