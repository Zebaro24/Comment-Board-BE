from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, GetAnonymousTokenView, CaptchaAPIView

router = DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('captcha/', CaptchaAPIView.as_view(), name='captcha_api'),
    path('token-anon/', GetAnonymousTokenView.as_view(), name='token_anon'),
]
