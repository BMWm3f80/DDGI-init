from django.urls import path, include
from insurance import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()

router.register('position', viewset=views.PositionsViewSet)
router.register('profile', viewset=views.ProfileViewSet)
router.register('permission', viewset=views.PermissionViewSet)
router.register('grid', viewset=views.GridViewSet)
router.register('individual', viewset=views.IndividualClientViewSet)
router.register('registered-policies', viewset=views.RegisterPoliseViewSet)


urlpatterns = [
    path('test/', views.test_view),
    path('api/', include(router.urls)),
]+static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
