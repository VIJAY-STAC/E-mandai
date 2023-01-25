from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter

from duties.views import DutiesViewSet

router = DefaultRouter()
router.register(r"duties", DutiesViewSet, basename="duties")



urlpatterns = [

    path("api/v3/", include(router.urls)),
    

   
]