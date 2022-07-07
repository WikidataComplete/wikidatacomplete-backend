from django.urls import path
from backend.views import (
    FactListCreateAPI,
    FactRetrieveUpdateDestroyAPIView,
    RetrieveFactWithQId,
    RetrieveRandomFact,
    FactAcceptAPI,
    FactRejectAPI,
)


urlpatterns = [
    path("api/v1/facts/", FactListCreateAPI.as_view()),
    path("api/v1/facts/<int:pk>/", FactRetrieveUpdateDestroyAPIView.as_view()),
    path("api/v1/facts/random/", RetrieveRandomFact.as_view()),
    path("api/v1/facts/accept/", FactAcceptAPI.as_view()),
    path("api/v1/facts/reject/", FactRejectAPI.as_view()),
    path("api/v1/facts/<str:qid>/", RetrieveFactWithQId.as_view()),
]
