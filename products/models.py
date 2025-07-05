from django.db import models
from django.conf import settings

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('home', 'Home & Garden'),
        ('sports', 'Sports & Recreation'),
        ('health', 'Health & Beauty'),
        ('automotive', 'Automotive'),
        ('other', 'Other'),
    ]
    
    sku = models.CharField(
        max_length=100, 
        unique=True, 
        help_text='Stock Keeping Unit - unique identifier'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Price in USD'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text='Available stock quantity'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products_created'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"
    
    @property
    def is_in_stock(self):
        return self.quantity > 0
    
    @property
    def stock_status(self):
        if self.quantity == 0:
            return 'Out of Stock'
        elif self.quantity < 10:
            return 'Low Stock'
        else:
            return 'In Stock'