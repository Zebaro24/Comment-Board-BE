from rest_framework import serializers
from .models import Comment, File
import re

ALLOWED_TAGS = ['a', 'code', 'i', 'strong']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_type', 'file', 'uploaded_at']

class CommentSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'homepage', 'text', 'parent', 'created_at', 'updated_at', 'files']

    def validate_text(self, value):
        tags = re.findall(r'<(\/?\w+)[^>]*>', value)
        for tag in tags:
            clean_tag = tag.replace('/', '')
            if clean_tag not in ALLOWED_TAGS:
                raise serializers.ValidationError(f"Tag <{clean_tag}> is not allowed.")
        return value
