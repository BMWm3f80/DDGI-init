from django.urls import path, include
from insurance import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('position', viewset=views.PositionsViewSet)
router.register('profile', viewset=views.ProfileViewSet)


urlpatterns = [
    path('test/', views.test_view),
    path('api/', include(router.urls)),
]