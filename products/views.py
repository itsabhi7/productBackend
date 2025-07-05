from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer
from .permissions import IsAdminOrManager, IsAdmin, IsManagerOrAdmin

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrManager]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(sku__icontains=search) | 
                Q(description__icontains=search)
            )
        
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        
        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManager]
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAdminOrManager()]

@api_view(['GET'])
def dashboard_stats_view(request):
    """
    Dashboard statistics for all authenticated users
    """
    total_products = Product.objects.count()
    total_value = Product.objects.aggregate(
        total=Sum('price')
    )['total'] or 0
    
    low_stock_count = Product.objects.filter(quantity__lt=10).count()
    out_of_stock_count = Product.objects.filter(quantity=0).count()
    
    category_stats = Product.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    recent_products = ProductListSerializer(
        Product.objects.all()[:5], 
        many=True
    ).data
    
    return Response({
        'total_products': total_products,
        'total_value': float(total_value),
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'category_stats': list(category_stats),
        'recent_products': recent_products,
    })

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_only_view(request):
    """
    Admin-only endpoint for testing RBAC
    """
    return Response({
        'message': 'This is an admin-only endpoint!',
        'user': request.user.username,
        'role': request.user.role,
    })