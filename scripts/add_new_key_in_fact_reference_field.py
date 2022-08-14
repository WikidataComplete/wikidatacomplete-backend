from tqdm import tqdm
from backend.models import Fact

for fact in tqdm(Fact.objects.all()):
    for ref in fact.references:
        if ref.get("property") == "P143":
            ref["name"] = "evidence"
        elif ref.get("property") == "P4656":
            ref["name"] = "Wikimedia import URL"
    fact.save()
