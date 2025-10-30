from rest_framework import viewsets
from .models import Comment
from .serializers import RecursiveCommentSerializer, CommentSerializer
from .pagination import CommentPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None).order_by('-created_at')
    pagination_class = CommentPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentSerializer
        return RecursiveCommentSerializer
