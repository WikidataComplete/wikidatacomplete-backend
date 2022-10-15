import json
from random import choice
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models import Fact
from backend.serializers import FactListCreateSerializer
from django.views.generic.base import TemplateView


class FactListCreateAPI(generics.ListCreateAPIView):
    queryset = Fact.objects.all()
    serializer_class = FactListCreateSerializer


class RetrieveFactWithQIdAPI(APIView):
    def get(self, request, *args, **kwargs):
        qid = self.kwargs.get("qid")
        try:
            custom_response = []
            facts_qs = Fact.objects.filter(
                entity=qid, feedback__value=None
            )  # only take those facts which have not received feedback yet
            for fact in facts_qs:
                evidence_highlight = fact.evidence_highlight
                property_data = fact.property_data
                value_data = fact.value_data
                references = fact.references
                evidence, wikipedia_link = None, None  # setting default values
                for refer in references:
                    if refer.get("type") == "string":
                        evidence = refer.get("value")
                    elif refer.get("type") == "url":
                        wikipedia_link = refer.get("value")
                custom_response.append(
                    {
                        "id": fact.id,
                        "property": property_data.get("property"),
                        "question": property_data.get("value"),
                        "wikipediaLink": wikipedia_link,
                        "wikidataLink": f"http://www.wikidata.org/entity/{fact.entity}",
                        "text": value_data.get("value"),
                        "evidence": evidence,
                        "startIdx": evidence_highlight.get("start_index"),
                        "endIdx": evidence_highlight.get("end_index"),
                        "object": [
                            {
                                "object": value_data.get("entity"),
                                "objectLabel": value_data.get("value"),
                            }
                        ],
                        "retrieved": fact.created_at,
                    }
                )
        except Exception:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(custom_response, status=status.HTTP_200_OK)


class RetrieveRandomFactAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            pk_list = Fact.objects.filter(feedback__value=None).values_list(
                "pk", flat=True
            )  # only take those facts which have not received feedback yet
            random_pk = choice(pk_list)
            fact = Fact.objects.get(pk=random_pk)
            evidence_highlight = fact.evidence_highlight
            property_data = fact.property_data
            value_data = fact.value_data
            references = fact.references
            evidence, wikipedia_link = None, None  # setting default values
            for refer in references:
                if refer.get("type") == "string":
                    evidence = refer.get("value")
                elif refer.get("type") == "url":
                    wikipedia_link = refer.get("value")
            custom_response = {
                "id": fact.id,
                "property": property_data.get("property"),
                "question": property_data.get("value"),
                "wikipediaLink": wikipedia_link,
                "wikidataLink": f"http://www.wikidata.org/entity/{fact.entity}",
                "text": value_data.get("value"),
                "evidence": evidence,
                "startIdx": evidence_highlight.get("start_index"),
                "endIdx": evidence_highlight.get("end_index"),
                "object": [
                    {
                        "object": value_data.get("entity"),
                        "objectLabel": value_data.get("value"),
                    }
                ],
                "retrieved": fact.created_at,
            }
        except Exception:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(custom_response, status=status.HTTP_200_OK)


class FactAcceptAPI(APIView):
    def post(self, request, *args, **kwargs):
        fact_id = request.data.get("fact_id")
        if not fact_id and not isinstance(fact_id, str):
            return Response(
                {"detail": "Invalid Fact ID."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            fact = Fact.objects.get(id=fact_id)
            feedback = {
                "value": True,
                "date": timezone.now(),
            }
            # to avoid TypeError: Object of type datetime is not JSON serializable
            feedback = json.dumps(feedback, cls=DjangoJSONEncoder)
            feedback = json.loads(feedback)
            fact.feedback = feedback
            fact.save()
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
            fact = Fact.objects.get(id=fact_id)
            feedback = {
                "value": False,
                "date": timezone.now(),
            }
            # to avoid TypeError: Object of type datetime is not JSON serializable
            feedback = json.dumps(feedback, cls=DjangoJSONEncoder)
            feedback = json.loads(feedback)
            fact.feedback = feedback
            fact.save()
        except Exception:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"message": "Fact Rejected successfully"}, status=status.HTTP_200_OK
        )


@method_decorator(login_required, name="dispatch")
class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "backend/profile.html", context)


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "backend/login.html", context)


@method_decorator(login_required, name="dispatch")
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class FactUploadAPI(APIView):
    serializer_class = FactListCreateSerializer

    def post(self, request, *args, **kwargs):
        uploaded_file = request.data.get("file")
        if uploaded_file == "null":
            return Response(
                {"detail": "Please upload file"}, status=status.HTTP_400_BAD_REQUEST
            )
        extension = str(uploaded_file).split(".")[-1]
        if extension != "jsonl":
            return Response(
                {"detail": "Only .jsonl file format is supported"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data_list = [json.loads(line) for line in uploaded_file]
        error_logs = []
        for data in data_list:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                try:
                    fact_object = Fact(
                        entity=validated_data.get("entity"),
                        property_data=validated_data.get("property_data"),
                        value_data=validated_data.get("value_data"),
                        references=validated_data.get("references"),
                    )
                    if validated_data.get("evidence_highlight"):
                        fact_object.evidence_highlight = validated_data.get(
                            "evidence_highlight"
                        )
                    fact_object.save()
                except Exception as e:
                    error_logs.append(
                        {
                            "entity": validated_data.get("entity"),
                            "error": e,
                        }
                    )
            else:
                return Response(
                    {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"detail": "Facts uploaded successfully"}, status=status.HTTP_201_CREATED
        )


# @method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "backend/coming_soon.html"


class DonateView(TemplateView):
    template_name = "backend/coming_soon.html"
