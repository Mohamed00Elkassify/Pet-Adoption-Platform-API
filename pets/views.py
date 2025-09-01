from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
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
from .permissions import IsOwnerOrReadOnly, IsPetOwner

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
    # IsOwnerOrReadOnly allows anyone to read, only owners (authenticated) can modify.
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['species', 'city', 'status']
    lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Adoption Requests
# class AdoptionRequestListAPI(generics.ListAPIView):
#     serializer_class = AdoptionRequestSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return AdoptionRequest.objects.filter(pet__owner=self.request.user)

# class AdoptionRequestCreateAPI(generics.CreateAPIView):
#     serializer_class = AdoptionRequestSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
#         serializer.save(pet=pet, requester=self.request.user)

#! Combine the AdoptionRequestListAPI and AdoptionRequestCreateAPI into AdoptionRequestViewSet
class AdoptionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AdoptionRequestSerializer
    # Auth required; object-level: only pet owner can access specific request objects (IsPetOwner)
    permission_classes = [permissions.IsAuthenticated, IsPetOwner]

    def get_queryset(self):
        return AdoptionRequest.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        pet_id = self.request.data.get('pet_id')  # type: ignore[attr-defined]
        if not pet_id:
            raise ValidationError({"pet_id": "This field is required."})
        pet = get_object_or_404(Pet, pk=pet_id)
        # Prevent owners from requesting adoption of their own pet
        if pet.owner == self.request.user:
            raise ValidationError("You cannot submit an adoption request for your own pet.")
        # Prevent duplicate requests by the same user for the same pet
        if AdoptionRequest.objects.filter(pet=pet, requester=self.request.user).exists():
            raise ValidationError("You have already submitted a request for this pet.")
        serializer.save(pet=pet, requester=self.request.user)