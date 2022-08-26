from django.urls import path
from backend.views import (
    FactAcceptAPI,
    FactListCreateAPI,
    FactRejectAPI,
    RetrieveFactWithQIdAPI,
    RetrieveRandomFactAPI,
    UserProfileView,
    UserLoginView,
)

urlpatterns = [
    path("api/v1/facts/", FactListCreateAPI.as_view()),
    path("api/v1/facts/random/", RetrieveRandomFactAPI.as_view()),
    path("api/v1/facts/accept/", FactAcceptAPI.as_view()),
    path("api/v1/facts/reject/", FactRejectAPI.as_view()),
    path("api/v1/facts/<str:qid>/", RetrieveFactWithQIdAPI.as_view()),
    path("profile", UserProfileView.as_view(), name="profile"),
    path("accounts/login", UserLoginView.as_view(), name="login"),
]
