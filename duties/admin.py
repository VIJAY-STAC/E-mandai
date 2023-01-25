from django.contrib import admin
from duties.models import DutyModel

# Register your models here.
@admin.register(DutyModel)
class DutyAdmin(admin.ModelAdmin):
    list_display =['id', 'status', 'created_at', 'updated_at', 'created_by', 'rider']