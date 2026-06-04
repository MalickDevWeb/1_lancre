from django.urls import path
from app.views import (
    DashboardView,
    ProductCreateView,
    ProductDeleteView,
    ProductRestoreView,
    ProductHardDeleteView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('api/products/<int:pk>/restore/', ProductRestoreView.as_view(), name='product-restore'),
    path('api/products/<int:pk>/hard-delete/', ProductHardDeleteView.as_view(), name='product-hard-delete'),
]
