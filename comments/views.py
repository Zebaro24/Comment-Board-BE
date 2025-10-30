from datetime import timedelta
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

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

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class CaptchaAPIView(APIView):
    permission_classes = []

    def get(self, request):
        key = CaptchaStore.generate_key()
        image_url = captcha_image_url(key)

        return Response({
            'key': key,
            'image': request.build_absolute_uri(image_url)
        })

class GetAnonymousTokenView(APIView):
    permission_classes = []

    def post(self, request):
        anon_user, _ = User.objects.get_or_create(username='anon', defaults={'is_active': True})
        token = RefreshToken.for_user(anon_user).access_token
        token.set_exp(lifetime=timedelta(days=365 * 100))
        return Response({'token': str(token)})