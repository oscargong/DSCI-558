import json
import ujson
from collections import defaultdict
from pathlib import Path
from typing import *
from snorkel import SnorkelSession
from snorkel.models import StableLabel, GoldLabel, GoldLabelKey, candidate_subclass
from snorkel.db_helpers import reload_annotator_labels

def get_candidate_class():
    return candidate_subclass('Education', ['person', 'organization'])

def reload_external_labels(session: SnorkelSession, input_file: Union[str, Path], annotator_name: str="gold"):
    Education = get_candidate_class()
    with open(str(input_file), "r") as f:
        lbls = ujson.load(f)

    for lbl in lbls:
        # we check if the label already exists, in case this cell was already executed
        context_stable_ids = "~~".join((lbl['person'], lbl['organization']))
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)
        if query.count() == 0:
            session.add(StableLabel(
                context_stable_ids=context_stable_ids,
                annotator_name=annotator_name,
                value=lbl['value']
            ))

    # commit session
    session.commit()

    # reload annotator labels
    reload_annotator_labels(session, Education, annotator_name, split=1, filter_label_split=False)
    reload_annotator_labels(session, Education, annotator_name, split=2, filter_label_split=False)

def get_gold_labels(session: SnorkelSession, annotator_name: str="gold") -> List[dict]:
    # define relationship in case it is not defined
    ak = session.query(GoldLabelKey).filter(GoldLabelKey.name == annotator_name).first()
    return session.query(GoldLabel).filter(GoldLabel.key == ak).all()

def extract_gold_labels(session: SnorkelSession, annotator_name: str="gold", split: int=None) -> List[dict]:
    ''' Extract pairwise gold labels and store in a file. '''
    gold_labels = get_gold_labels(session, annotator_name)

    results = []
    for gold_label in gold_labels:
        rel = gold_label.candidate
        if split is not None and rel.split != split:
            continue

        results.append({
            "person": rel.person.stable_id,
            "organization": rel.organization.stable_id,
            "value": gold_label.value
        })

    return results

def save_gold_labels(session: SnorkelSession, output_file: Union[str, Path], annotator_name: str="gold", split: int=None):
    gold_labels = extract_gold_labels(session, annotator_name, split=split)
    with open(str(output_file), "w") as f:
        json.dump(gold_labels, f, indent=4)

def save_gold_relations(session: SnorkelSession, output_file: str, annotator_name: str="gold", split: int=None):
    gold_labels = get_gold_labels(session, annotator_name)
    relation = defaultdict(lambda: [])
    for gold_label in gold_labels:
        if gold_label.value == 1:
            candidate = gold_label.candidate
            if split is not None and candidate.split != split:
                continue

            cast_uri = candidate.person.sentence.document.name
            relation[cast_uri].append([
                candidate.person.get_span(),
                candidate.organization.get_span()
            ])

    with open(str(output_file), "w") as f:
        json.dump(relation, f, indent=4)

def save_predicted_relations(output_file: str, candidates: list, predicted_labels: list):
    assert len(candidates) == len(predicted_labels)
    relation = defaultdict(lambda: [])
    for lbl, candidate in zip(predicted_labels, candidates):
        if lbl == 1:
            cast_uri = candidate.person.sentence.document.name
            relation[cast_uri].append([
                candidate.person.get_span(),
                candidate.organization.get_span()
            ])
    with open(str(output_file), "w") as f:
        json.dump(relation, f, indent=4)

def get_dev_doc_ids(dev_file: Union[Path, str]) -> Set[str]:
    with open(str(dev_file), "r") as f:
        return {l.rstrip() for l in f}

def get_test_doc_ids(test_file: Union[Path, str]) -> Set[str]:
    with open(str(test_file), "r") as f:
        return {l.rstrip() for l in f}

def number_of_people(sentence):
    active_sequence = False
    count = 0
    for tag in sentence.ner_tags:
        if tag == 'PERSON' and not active_sequence:
            active_sequence = True
            count += 1
        elif tag != 'PERSON' and active_sequence:
            active_sequence = False
    return count

if __name__ == '__main__':
    save_gold_labels(SnorkelSession(), "gold_labels.json", "rook")