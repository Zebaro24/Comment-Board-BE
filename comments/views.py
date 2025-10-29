from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    @action(detail=False, methods=['post'])
    def preview(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
