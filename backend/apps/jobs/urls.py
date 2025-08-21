from rest_framework.routers import DefaultRouter
from .views import JobViewSet, NoteViewSet

router = DefaultRouter()  # use DefaultRouter(trailing_slash=False)
# if you want no trailing slashes
router.register(r"jobs", JobViewSet, basename="job")
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = router.urls
