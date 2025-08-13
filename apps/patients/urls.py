from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    IdentificationTypeViewSet,
    GenderViewSet,
    MaritalStatusViewSet,
    EPSViewSet,
    EtniaViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'identification-types', IdentificationTypeViewSet, basename='identification-type')
router.register(r'genders', GenderViewSet, basename='gender')
router.register(r'marital-statuses', MaritalStatusViewSet, basename='marital-status')
router.register(r'eps', EPSViewSet, basename='eps')
router.register(r'etnia', EtniaViewSet, basename='etnia')

urlpatterns = router.urls
