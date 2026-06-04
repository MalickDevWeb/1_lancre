import json
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.models import Tenant, Product


class DashboardView(TemplateView):
    """Vue principale du tableau de bord SaaS Multi-Tenant."""
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Auto-créer un tenant de démo si la BDD est vide
        tenant, _ = Tenant.objects.get_or_create(
            domain_url="orange-business.lancre.io",
            defaults={"name": "Orange Business", "is_active": True}
        )

        # Créer des produits de démo s'il n'y en a pas
        if not Product.objects.filter(tenant=tenant).exists():
            Product.objects.bulk_create([
                Product(tenant=tenant, name="Fibre Pro 1Gbps", sku="FB-PRO-01", price=120.00),
                Product(tenant=tenant, name="Cloud Backup 1To", sku="CL-BK-02", price=45.00),
                Product(tenant=tenant, name="SD-WAN Enterprise", sku="SD-WAN-03", price=280.00),
                Product(tenant=tenant, name="Firewall Fortinet", sku="FW-FT-04", price=350.00, is_deleted=True),
            ])

        products = Product.objects.filter(tenant=tenant).order_by('-created_at')
        active_count = products.filter(is_deleted=False).count()
        total_revenue = sum(p.price for p in products.filter(is_deleted=False))

        context['tenant'] = tenant
        context['products'] = products
        context['metrics'] = {
            "users": 142,
            "revenue": f"€{total_revenue:,.0f}",
            "uptime": "99.99%",
            "active_products": active_count,
        }
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ProductCreateView(View):
    """API pour créer un nouveau produit (AJAX)."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            tenant = Tenant.objects.first()
            if not tenant:
                return JsonResponse({"error": "Aucun tenant trouvé"}, status=400)

            # Validation
            name = data.get("name", "").strip()
            sku = data.get("sku", "").strip()
            price = data.get("price")

            if not name or not sku or price is None:
                return JsonResponse({"error": "Tous les champs sont obligatoires"}, status=400)

            if Product.objects.filter(sku=sku).exists():
                return JsonResponse({"error": f"Le SKU '{sku}' existe déjà"}, status=400)

            product = Product.objects.create(
                tenant=tenant, name=name, sku=sku, price=float(price)
            )
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "price": str(product.price),
                "is_deleted": product.is_deleted,
            }, status=201)

        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ProductDeleteView(View):
    """API pour soft-delete un produit (AJAX)."""

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.is_deleted = True
            product.save()
            return JsonResponse({"status": "deleted", "id": pk})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Produit introuvable"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class ProductRestoreView(View):
    """API pour restaurer un produit soft-deleted (AJAX)."""

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.is_deleted = False
            product.save()
            return JsonResponse({"status": "restored", "id": pk})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Produit introuvable"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class ProductHardDeleteView(View):
    """API pour supprimer définitivement un produit (RGPD - Droit à l'oubli)."""

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return JsonResponse({"status": "hard_deleted", "id": pk})
        except Product.DoesNotExist:
            return JsonResponse({"error": "Produit introuvable"}, status=404)
