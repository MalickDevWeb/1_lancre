from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mock data for the SaaS UI to look real without database setup
        context['tenant_name'] = "Orange Business (Tenant Isolé)"
        context['metrics'] = {"users": 142, "revenue": "€45,200", "uptime": "99.99%"}
        context['products'] = [
            {"name": "Fibre Pro", "sku": "FB-PRO-01", "price": 120.00, "status": "Active"},
            {"name": "Cloud Backup 1To", "sku": "CL-BK-02", "price": 45.00, "status": "Active"},
            {"name": "Firewall Fortinet", "sku": "FW-FT-03", "price": 350.00, "status": "Soft Deleted"},
        ]
        return context
