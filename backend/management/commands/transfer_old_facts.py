import json
import os
from backend.models import Fact
from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

FILENAME = "facts.jsonl"


class Command(BaseCommand):
    help = "Transfer old facts to new schema"

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, FILENAME)
        with open(path, "r") as old_facts:
            data_list = [json.loads(line) for line in old_facts]

        facts_to_create = []
        for data in tqdm(data_list):
            references = [
                {"property": "P143", "value": data.get("evidence"), "type": "string"},
                {
                    "property": "P4656",
                    "value": data.get("wikipediaLink"),
                    "type": "url",
                },
            ]
            evidence_highlight = {
                "startIdx": data.get("startIdx"),
                "endIdx": data.get("endIdx"),
                "text": data.get("text"),
            }
            try:
                fact_object = Fact(
                    wikidata_entity=data.get("wikidataLink"),
                    wikidata_property=data.get("property"),
                    data_type="Item",
                    evidence_highlight=evidence_highlight,
                    references=references,
                    question=data.get("question"),
                    data_value=data.get("object"),
                )
                facts_to_create.append(fact_object)
            except Exception as e:
                print(e)
        try:
            Fact.objects.bulk_create(facts_to_create)
        except Exception as e:
            print(e)
