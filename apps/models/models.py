from django.contrib.auth.models import User
from django.db import models


class AIModel(models.Model):
    model_name = models.CharField(max_length=255)
    model_type = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    top_p = models.FloatField(default=0.7)
    top_k = models.FloatField(default=0)

    base_model = models.CharField(max_length=255, blank=True, null=True)
    model_path = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    craetor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modifier_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Model {self.model_name} - Type {self.model_type}"

    class Meta:
        db_table = 'ai_models'
