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
            property_data = {
                "property": data.get("property"),
                "value": data.get("question"),
            }

            value_data = {
                "entity": data.get("object")[0].get("object").split("/")[-1],
                "value": data.get("object")[0].get("objectLabel"),
            }

            references = [
                {
                    "property": EVIDENCE_PROPERTY,
                    "value": data.get("evidence"),
                    "type": "string",
                },
                {
                    "property": WIKIPEDIALINK_PROPERTY,
                    "value": data.get("wikipediaLink"),
                    "type": "url",
                },
            ]

            evidence_highlight = {
                "start_index": data.get("startIdx"),
                "end_index": data.get("endIdx"),
            }

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
                    entity=data.get("wikidataLink").split("/")[-1],
                    property_data=property_data,
                    value_data=value_data,
                    data_type="Item",
                    references=references,
                    evidence_highlight=evidence_highlight,
                    feedback=feedback,
                )
                fact_object.save()
            except Exception as e:
                error_logs.append({"entity": data.get("wikidataLink"), "error": e})
        if error_logs:
            print("Facts not created for these rows:")
            print(error_logs)
