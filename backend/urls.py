from django.urls import path
from backend.views import FactListCreateAPI, FactRetrieveUpdateDestroyAPIView


urlpatterns = [
    path("api/v1/facts/", FactListCreateAPI.as_view()),
    path("api/v1/facts/<int:pk>/", FactRetrieveUpdateDestroyAPIView.as_view()),
]
