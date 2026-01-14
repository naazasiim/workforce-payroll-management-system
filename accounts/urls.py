from django.urls import path
from .views import *

urlpatterns = [
    path("users/", UserCreateView.as_view(), name="user-create"),
    path("onboarding/", OnboardingView.as_view(), name="onboarding"),
]
