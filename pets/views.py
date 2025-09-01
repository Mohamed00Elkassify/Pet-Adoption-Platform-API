from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Pet, AdoptionRequest
from .serializers import (
    PetSerializer, 
    SignupSerializer, 
    UserSerializer, 
    AdoptionRequestSerializer 
)

#* AUTH
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})

#* Pets
# class PetListAPI(generics.ListAPIView):
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['species', 'city', 'status']

# class PetDetailAPI(generics.RetrieveAPIView):
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer
#     lookup_field = 'id' 

# class PetCreateAPI(generics.CreateAPIView):
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class PetUpdateAPI(generics.UpdateAPIView):
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_update(self, serializer):
#         pet = self.get_object()
#         if pet.owner != self.request.user:
#             raise PermissionDenied('You can only update your own pets.')
#         serializer.save()

# class PetDeleteAPI(generics.DestroyAPIView):
#     queryset = Pet.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_destroy(self, instance):
#         if instance.owner != self.request.user:
#             raise PermissionDenied('You can only delete your own pets.')
#         instance.delete()
#! Combine the PetListAPI, PetDetailAPI, PetCreateAPI, PetUpdateAPI, and PetDeleteAPI into PetViewSet
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['species', 'city', 'status']
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ['update', 'partial_update', 'destroy']:
            if obj.owner != request.user:
                raise PermissionDenied('You can only modify your own pets.')