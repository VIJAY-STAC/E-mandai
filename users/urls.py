from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")



urlpatterns = [

    path("api/v3/", include(router.urls)),
    
]