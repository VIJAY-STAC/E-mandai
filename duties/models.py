from django.db import models
from users.models import User

DUTY_TYPES=(
    ('customer','Customer '),
    ('internal','Internal  ')
)

DUTY_STATUS = (
    ('assigned','Assigned'),
    ('started','Started'),
    ('completed','completed'),
)
# Create your models here.
class DutyModel(models.Model):
    type = models.CharField(max_length=255, choices = DUTY_TYPES , null=False,
        blank=False,)
    status = models.CharField(max_length=255, choices=DUTY_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
       User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="user_id"
    )
    rider = models.ForeignKey(
       User,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="rider_id"
    )

def __str__(self):
    return self.id