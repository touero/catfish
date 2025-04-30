from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        permissions = [
            ("can_delete_file", "Can delete file")
        ]

    def __str__(self):
        return self.name

    def get_uploaded_at_in_shanghai(self):
        return timezone.localtime(self.uploaded_at)
