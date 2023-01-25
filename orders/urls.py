from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from orders.views import OrdersViewSet


router = DefaultRouter()
router.register(r"orders", OrdersViewSet, basename="orders")




urlpatterns = [

    path("api/v3/", include(router.urls)),
    

   
]