from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    domain_url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=50, choices=[('ADMIN', 'Admin'), ('USER', 'User')])

class Product(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='product_name_idx'),
            GinIndex(fields=['metadata'], name='product_meta_gin')
        ]
