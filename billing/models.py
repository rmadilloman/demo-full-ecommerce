from django.db import models
from django.contrib.auth.models import User
from addresses.models import Address

class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='billing_profile')
    email = models.EmailField(max_length=255, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username