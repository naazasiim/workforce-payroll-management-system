from django.urls import path
from .views import BulkAttendanceView

urlpatterns = [
    path("bulk/", BulkAttendanceView.as_view(), name="bulk-attendance"),
]
