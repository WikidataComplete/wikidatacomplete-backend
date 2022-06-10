from operator import mod
from django.db import models


class Fact(models.Model):
    category = models.CharField(max_length=90, blank=True, default="")
    correct = models.BooleanField()
    start_idx = models.IntegerField(null=True)
    end_idx = models.IntegerField(null=True)
    evidence = models.CharField(max_length=2000, blank=True, default="")
    is_published = models.BooleanField(null=True)
    null_odds = models.FloatField(null=True)
    _property = models.CharField(max_length=90, blank=True, default="")
    question = models.CharField(max_length=1000, blank=True, default="")
    score = models.FloatField(null=True)
    text = models.CharField(max_length=1000, blank=True, default="")
    wikidata_link = models.CharField(max_length=1000, blank=True, default="")
    wikipedia_link = models.CharField(max_length=1000, blank=True, default="")
    feeback_id = models.IntegerField(null=True)
