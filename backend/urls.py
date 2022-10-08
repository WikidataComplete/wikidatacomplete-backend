from django.urls import path
from backend.views import (
    FactAcceptAPI,
    FactListCreateAPI,
    FactRejectAPI,
    RetrieveFactWithQIdAPI,
    RetrieveRandomFactAPI,
    UserProfileView,
    UserLoginView,
    UserLogoutView,
    FactUploadAPI,
    DashboardView,
)

urlpatterns = [
    path("api/v1/facts/", FactListCreateAPI.as_view()),
    path("api/v1/facts/random/", RetrieveRandomFactAPI.as_view()),
    path("api/v1/facts/accept/", FactAcceptAPI.as_view()),
    path("api/v1/facts/reject/", FactRejectAPI.as_view()),
    path("api/v1/facts/upload/", FactUploadAPI.as_view()),
    # keep all facts/<some string> urls above this otherwise
    # django will match str: to this and this api will get called
    path("api/v1/facts/<str:qid>/", RetrieveFactWithQIdAPI.as_view()),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/logout/", UserLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
