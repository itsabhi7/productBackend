from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'quantity', 'stock_status', 'created_by', 'created_at']
    list_filter = ['category', 'created_at', 'updated_at']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('sku', 'name', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'quantity')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by when creating
            obj.created_by = request.user
        super().save_model(request, obj, form, change)