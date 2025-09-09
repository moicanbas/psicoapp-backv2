from rest_framework.routers import DefaultRouter
from .views import Cie10ViewSet

router = DefaultRouter()
router.register(r'cie10', Cie10ViewSet, basename='cie10')

urlpatterns = router.urls