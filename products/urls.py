from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('dashboard/stats/', views.dashboard_stats_view, name='dashboard-stats'),
    path('admin-only/', views.admin_only_view, name='admin-only'),
]