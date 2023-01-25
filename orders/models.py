from random import choices
from django.db import models
from duties.models import DutyModel
from carts.models import Cart
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save

# ORDER_STATUS
ORDER_STATUS = (

    ('placed','Placed'),
    ('ready_to_pickup','Ready to pick up'),
    ('picked','Picked'),
    ('delivered','Delivered'),
    ('cancelled','Cancelled'),

)

# ORDER_PAYMENT_TYPE
ORDER_PAYMENT_TYPE = (
    ('cash','Cash'),
    ('online','Online'),
)

# ORDER_PAYMENT_status
ORDER_PAYMENT_status = (
    ('paid','Paid'),
    ('unpaid','Unpaid'),
)

# Create your models here.
class OrderModel(models.Model):
    amount = models.FloatField(max_length=20)
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    payment_type = models.CharField(max_length=255, choices=ORDER_PAYMENT_TYPE)
    payment_status = models.CharField(max_length=255, choices=ORDER_PAYMENT_status)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    created_by = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
       
    )
    cart = models.ForeignKey(
        Cart,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
       
    )
    duty = models.ForeignKey(
        DutyModel,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="Duty"
    )
        
    

