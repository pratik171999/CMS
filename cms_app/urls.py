from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentItemViewSet, RegisterUserView

router = DefaultRouter()
router.register(r'content', ContentItemViewSet, basename='content')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('', include(router.urls)),  # This includes all router-registered views
]
