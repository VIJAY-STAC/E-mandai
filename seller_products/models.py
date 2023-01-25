from django.db import models
from users.models import User


PRODUCTS_NAME =(

    ("potato", "Potato"),
    ("tomato", "Tomato"),
    ("onion", "Onion"),
    ("spinach", "Spinach"),
    ("spring_onion", "Spring Onion"),
    
)

# Create your models here.

class seller_products(models.Model):
    sp_name = models.CharField(max_length=255, blank=False, choices=PRODUCTS_NAME)
    sp_description = models.CharField(max_length=255, blank=True)
    sp_validity = models.DateField(auto_now_add=False)
    sp_img = models.ImageField(upload_to= "products_images")
    sp_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sp_stock = models.IntegerField(null=False, blank=False)
    seller_id = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="seller",
    )
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)


    def __str__(self):
        return self.sp_name