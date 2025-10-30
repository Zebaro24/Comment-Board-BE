from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Comment
from .serializers import RecursiveCommentSerializer, CommentSerializer
from .pagination import CommentPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent=None).order_by('-created_at')
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentSerializer
        return RecursiveCommentSerializer

class GetAnonymousTokenView(APIView):
    permission_classes = []

    def post(self, request):
        anon_user, _ = User.objects.get_or_create(username='anon', defaults={'is_active': True})
        token = RefreshToken.for_user(anon_user).access_token
        return Response({'token': str(token)})