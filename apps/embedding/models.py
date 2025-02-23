import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from pgvector.django import VectorField


class DocumentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=255,
                            unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    disable_at = models.DateTimeField(blank=True, null=True)
    last_modifier_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "document_type"


class Documents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="documents_created")
    last_modifier = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="documents_modified")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disable_at = models.DateTimeField(blank=True, null=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document {self.id} - type {self.document_type} - created at {self.created_at}"

    class Meta:
        db_table = "document"


class DocumentEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    document_id = models.ForeignKey(
        Documents, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    embedding = VectorField(1536)

    def __str__(self):
        return f"emnedd into {self.embedding} dim"

    class Meta:
        db_table = "document_embedding"
