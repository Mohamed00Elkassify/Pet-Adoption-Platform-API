from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    SPECIES_CHOICES = [('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird')]
    STATUS_CHOICES = [('available', 'Available'), ('adopted', 'Adopted')]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='pet_photos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.species}) - {self.status}"

class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    requester_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adoption Request for {self.pet.name} by {self.requester_name}"