from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, AdoptionRequestViewSet, SignupView

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'adoption-requests', AdoptionRequestViewSet, basename='adoptionrequest')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', include(router.urls)),
]