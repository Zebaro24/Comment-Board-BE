from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .file_queue import file_queue
from .models import Comment, File

from .validators import validate_allowed_html


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_type', 'file', 'uploaded_at']

    def validate(self, data):
        uploaded_file = data['file']
        if data['file_type'] == 'image':
            if not uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise serializers.ValidationError("Only JPG, PNG, or GIF allowed.")
        elif data['file_type'] == 'text':
            if not uploaded_file.name.lower().endswith('.txt'):
                raise serializers.ValidationError("Only TXT files allowed.")
            if uploaded_file.size > 100 * 1024:
                raise serializers.ValidationError("Text file must be <= 100KB.")
        return data

    def create(self, validated_data):
        file_instance = super().create(validated_data)

        if validated_data['file_type'] == 'image':
            file_queue.add_task(file_instance)

        return file_instance


class CommentSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'homepage', 'text', 'parent', 'created_at', 'updated_at', 'files']

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Username must contain only Latin letters and digits.")
        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_homepage(self, value):
        if value:
            validator = URLValidator()
            try:
                validator(value)
            except ValidationError:
                raise serializers.ValidationError("Invalid URL format for homepage.")
        return value

    def validate_text(self, value):
        return validate_allowed_html(value)

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(**validated_data)

        if request and hasattr(request, 'FILES'):
            files = request.FILES.getlist('file')
            for f in files:
                file_type = 'image' if f.content_type.startswith('image') else 'text'
                file_serializer = FileSerializer(data={'file': f, 'file_type': file_type})
                file_serializer.is_valid(raise_exception=True)
                file_serializer.save(comment=comment)

        return comment


class RecursiveCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'homepage', 'text', 'parent', 'created_at', 'replies', 'files']

    def get_replies(self, obj):
        serializer = RecursiveCommentSerializer(
            obj.replies.all(),
            many=True,
            context=self.context
        )
        return serializer.data
