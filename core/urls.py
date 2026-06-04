from django.urls import path
from app.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
