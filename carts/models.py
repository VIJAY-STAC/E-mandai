from django.db import models
from django.dispatch import receiver
from seller_products.models import seller_products
from users.models import User
from django.db.models.signals import pre_save,post_save
from django.db.models import Avg, Max, Min, Sum
# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
      
    )
    ordered = models.BooleanField(default=False)
    amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)

class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart"
     )
    user= models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="user",
    )
    product = models.ForeignKey(
            seller_products,
            on_delete=models.CASCADE,
     )
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.sp_name

@receiver(pre_save, sender=CartItems)
def amount_update(sender, **kwargs):
    cart_items =kwargs['instance']
    product_amount = seller_products.objects.get(id=cart_items.product.id)
    cart_items.price =cart_items.quantity * float(product_amount.sp_amount)
   

@receiver(post_save, sender=CartItems)
def amount_update(sender, **kwargs):
    cart_items =kwargs['instance']
    cart = Cart.objects.get(id=cart_items.cart.id)
    total_amount = CartItems.objects.filter(cart=cart.id).aggregate(Sum('price'))
    cart.amount = total_amount['price__sum']
    cart.save()