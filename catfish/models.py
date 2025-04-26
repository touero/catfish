from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_delete_file", "Can delete file")
        ]

    def __str__(self):
        return self.name
