from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Product

class ProductListView(APIView):
    # Cache optimization with Redis (Numérique Responsable)
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        # Isolation Multi-Tenant & Optimization N+1
        products = Product.objects.filter(tenant=request.user.tenant)\
                                  .select_related('tenant')\
                                  .all()
        data = [{"id": p.id, "name": p.name, "tenant": p.tenant.name} for p in products]
        return Response(data)
