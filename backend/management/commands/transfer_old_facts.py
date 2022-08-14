import json
import os
from backend.models import Fact
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from tqdm import tqdm

FILENAME = "facts.jsonl"
EVIDENCE_PROPERTY = "P143"
WIKIPEDIALINK_PROPERTY = "P4656"


class Command(BaseCommand):
    help = "Transfer old facts to new schema"

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, FILENAME)
        with open(path, "r") as old_facts:
            data_list = [json.loads(line) for line in old_facts]

        facts_to_create = []
        error_logs = []
        for data in tqdm(data_list):
            references = [
                {
                    "property": EVIDENCE_PROPERTY,
                    "value": data.get("evidence"),
                    "type": "string",
                    "name": "evidence",
                },
                {
                    "property": WIKIPEDIALINK_PROPERTY,
                    "value": data.get("wikipediaLink"),
                    "type": "url",
                    "name": "Wikimedia import URL",
                },
            ]
            evidence_highlight = {
                "startIdx": data.get("startIdx"),
                "endIdx": data.get("endIdx"),
                "text": data.get("text"),
            }
            meta_information = {"question": data.get("question")}

            # caculation for feedback
            if data.get("published") is not None:
                feedback_date = timezone.now()
            else:
                feedback_date = None  # since feedback not given yet
            feedback = {
                "value": data.get("published"),
                "date": feedback_date,
            }
            if feedback_date:
                # to avoid TypeError: Object of type datetime is not JSON serializable
                feedback = json.dumps(feedback, cls=DjangoJSONEncoder)
                feedback = json.loads(feedback)

            try:
                fact_object = Fact(
                    wikidata_entity=data.get("wikidataLink"),
                    wikidata_property=data.get("property"),
                    data_type="Item",
                    evidence_highlight=evidence_highlight,
                    references=references,
                    data_value=data.get("object"),
                    meta_information=meta_information,
                    feedback=feedback,
                )
                facts_to_create.append(fact_object)
            except Exception as e:
                error_logs.append(
                    {"wikidata_entity": data.get("wikidataLink"), "error": e}
                )
        try:
            Fact.objects.bulk_create(facts_to_create)
        except Exception as e:
            print(f"Exception while creating fact records in bulk: {e}")
        if error_logs:
            print("Facts not created for these rows:")
            print(error_logs)
