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
router.register('client-individual', viewset=views.IndividualClientViewSet)
router.register('client-legal', viewset=views.LegalClientViewSet)
router.register('registered-policies', viewset=views.RegisterPoliseViewSet)
router.register('currency', viewset=views.CurrencyViewset)
router.register('group', viewset=views.GroupViewset)
router.register('klass', viewset=views.KlassViewset)
router.register('bank', viewset=views.BankViewset)
router.register('branch', viewset=views.BranchViewSet)


urlpatterns = [
    path('test/', views.test_view),
    path('api/', include(router.urls)),
]+static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
