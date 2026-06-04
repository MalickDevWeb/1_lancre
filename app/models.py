from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class Tenant(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    domain_url = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        indexes = [models.Index(fields=['domain_url'])]

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(
        max_length=50, 
        choices=[('ADMIN', 'Admin'), ('MANAGER', 'Manager'), ('USER', 'User')],
        default='USER'
    )
    
    class Meta:
        # Un utilisateur ne peut exister qu'une seule fois par tenant
        unique_together = ('username', 'tenant')

class Product(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    metadata = models.JSONField(default=dict, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    is_deleted = models.BooleanField(default=False) # Soft delete

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'name'], name='product_tenant_name_idx'),
        ]

