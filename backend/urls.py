from django.urls import path
from backend.views import (
    FactAcceptAPI,
    FactListCreateAPI,
    FactRejectAPI,
    RetrieveFactWithQIdAPI,
    RetrieveRandomFactAPI,
)

urlpatterns = [
    path("api/v1/facts/", FactListCreateAPI.as_view()),
    path("api/v1/facts/random/", RetrieveRandomFactAPI.as_view()),
    path("api/v1/facts/accept/", FactAcceptAPI.as_view()),
    path("api/v1/facts/reject/", FactRejectAPI.as_view()),
    path("api/v1/facts/<str:qid>/", RetrieveFactWithQIdAPI.as_view()),
]
