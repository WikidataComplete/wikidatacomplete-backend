# https://github.com/WikidataComplete/Wikidata-Complete-Gadget/issues/43


# If LANGUAGE_OF_FILM(P364) is already present we should not show LANGUAGE_OF_WORK (407)

# get all facts from DB which have P407
# call wikidata API for those facts and check if it has P364
# if available remove those facts from DB

import requests
from backend.models import Fact
from tqdm import tqdm

WIKIDATA_API_URI = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
LANGUAGE_OF_WORK = "P407"
LANGUAGE_OF_FILM = "P364"


def get_claims_from_data(data, qid):
    entities = data.get("entities")
    if entities:
        qid_data = entities.get(qid)
        if qid_data:
            claims = qid_data.get("claims")
            return claims
    return None


def fix_p407_facts():
    delete_count = 0
    facts_to_delete = []
    errored_api_calls = []
    p407_facts = Fact.objects.filter(wikidata_property=LANGUAGE_OF_WORK)
    for fact in tqdm(p407_facts):
        qid = fact.wikidata_entity.split("/")[-1]
        uri = WIKIDATA_API_URI.format(qid=qid)
        response = requests.get(uri)
        if response.status_code == 200:
            data = response.json()
            claims = get_claims_from_data(data, qid)
            if claims and LANGUAGE_OF_FILM in claims.keys():
                facts_to_delete.append(fact.id)
                delete_count += 1
        else:
            errored_api_calls.append(qid)
    Fact.objects.filter(id__in=facts_to_delete).delete()  # Delete facts from DB
    print("--------------------RESULT--------------------")
    print(f"Total Facts which has Property {LANGUAGE_OF_WORK}: {p407_facts.count()}")
    print(
        f"Facts Deleted from these since Wikidata Entity associate with them already had property {LANGUAGE_OF_FILM}: {delete_count}"
    )
    if errored_api_calls:
        print(f"failed for these qids: {errored_api_calls}")


if __name__ == "__main__":
    fix_p407_facts()
