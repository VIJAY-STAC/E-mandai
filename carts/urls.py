from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from carts.views import CartItemViewSet, CartViewSet


router = DefaultRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cartitem", CartItemViewSet, basename="cartitem")



urlpatterns = [

    path("api/v3/", include(router.urls)),
    

   
]