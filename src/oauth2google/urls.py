from django.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

router = SimpleRouter()

router.register("", UserViewSet)

urlpatterns = [
    path("", include("allauth.urls")),
]
urlpatterns += router.urls
