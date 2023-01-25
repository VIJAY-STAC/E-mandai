from pyrsistent import field
from rest_framework import serializers
from duties.models import DutyModel

class DutySerializer(serializers.ModelSerializer):
    class Meta:
        model = DutyModel
        fields = (
            'id',
            'status',
            'created_at',
            'updated_at',
            'created_by',
            'rider',
            'type'

        )