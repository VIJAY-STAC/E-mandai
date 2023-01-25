from rest_framework import serializers
from seller_products.models import seller_products

class SellerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = seller_products
        fields = (

                'id',
                'sp_name',
                'sp_description',
                'sp_validity',
                'sp_img',
                'sp_amount',
                'sp_stock',
                'seller_id',
                'created_at',
                'updated_at'

        )
