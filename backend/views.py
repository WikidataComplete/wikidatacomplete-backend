import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Fact
from backend.serializers import FactListCreateSerializer


class FactListCreateAPI(generics.ListCreateAPIView):
    queryset = Fact.objects.all()
    serializer_class = FactListCreateSerializer


class FactRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fact.objects.all()
    serializer_class = FactListCreateSerializer


class RetrieveFactWithQId(APIView):
    def get(self, request, *args, **kwargs):
        qid = self.kwargs.get("qid")
        try:
            response = requests.get(
                f"https://qanswer-svc3.univ-st-etienne.fr/facts/get?qid={qid}&format=json"
            ).json()
        except Exception as e:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(response, status=status.HTTP_200_OK)
