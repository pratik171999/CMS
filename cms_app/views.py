from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import ContentItem, CustomUser
from .serializers import ContentItemSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ContentItemViewSet(viewsets.ModelViewSet):
    serializer_class = ContentItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'summary', 'categories__name']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ContentItem.objects.all()
        return ContentItem.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)