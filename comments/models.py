from django.db import models


class Comment(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)

    text = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.text[:20]}"


class File(models.Model):
    FILE_TYPES = (
        ('image', 'Image'),
        ('text', 'Text'),
    )

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"
