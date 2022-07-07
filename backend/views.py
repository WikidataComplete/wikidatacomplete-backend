import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Fact
from backend.serializers import FactListCreateSerializer
from backend.constants import USER_COOKIE, ACCEPT_CORRECTION, REJECT_CORRECTION


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


class RetrieveRandomFact(APIView):
    def get(self, request, *args, **kwargs):
        try:
            response = requests.get(
                "https://qanswer-svc3.univ-st-etienne.fr/fact/get?id=EMPTY&category=EMPTY&property=EMPTY"
            ).json()
        except Exception:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(response, status=status.HTTP_200_OK)


class FactAcceptAPI(APIView):
    def post(self, request, *args, **kwargs):
        fact_id = request.data.get("fact_id")
        if not fact_id and not isinstance(fact_id, str):
            return Response(
                {"detail": "Invalid Fact ID."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            accept_uri = f"https://qanswer-svc3.univ-st-etienne.fr/fact/correct?userCookie={USER_COOKIE}&factId={fact_id}&correction={ACCEPT_CORRECTION}"
            requests.post(accept_uri)  # returns text data
        except Exception:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Fact Accepted successfully"}, status=status.HTTP_200_OK
        )


class FactRejectAPI(APIView):
    def post(self, request, *args, **kwargs):
        fact_id = request.data.get("fact_id")
        if not fact_id and not isinstance(fact_id, str):
            return Response(
                {"detail": "Invalid Fact ID."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            reject_uri = f"https://qanswer-svc3.univ-st-etienne.fr/fact/correct?userCookie={USER_COOKIE}&factId={fact_id}&correction={REJECT_CORRECTION}"
            requests.post(reject_uri)  # returns text data
        except Exception:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Fact Rejected successfully"}, status=status.HTTP_200_OK
        )
