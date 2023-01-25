from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from seller_products.views import SellerProductsViewSet


router = DefaultRouter()
router.register(r"seller_products", SellerProductsViewSet, basename="seller_products")



urlpatterns = [

    path("api/v3/", include(router.urls)),
    

   
]