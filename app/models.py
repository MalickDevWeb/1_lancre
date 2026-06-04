from django.db import models
from django.core.validators import MinValueValidator


class Tenant(models.Model):
    """
    Représente un client B2B isolé dans l'architecture Multi-Tenant.
    Chaque Tenant possède ses propres données cloisonnées.
    """
    name = models.CharField(max_length=255, db_index=True)
    domain_url = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Produit SaaS rattaché à un Tenant.
    Implémente le pattern Soft Delete pour la conformité RGPD.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    is_deleted = models.BooleanField(default=False)  # Soft delete (RGPD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'name'], name='product_tenant_name_idx'),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"
