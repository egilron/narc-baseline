# Read jsonlines files predicted with wl-coref and evaluate them with coreference-eval
# coreference-eval presently requires python 3.9

import corefeval
import jsonlines
import os

gold_folder = "/home/egil/datasets/narc/data/wl-formatted"
predicted_folder = "/home/egil/datasets/narc"
wl_naming = {"dev":"development", "test":"test"}


def read_clusters(source_path:str, key="clusters"):
    """ read the clusters from multiline jsonlines,
    return list of clusters """
    with jsonlines.open(source_path) as rf:
        clusters = [doc[key] for doc in rf]
    return clusters





for experiment in ["POC2_000", "POC2_001"]:
    for split in ["dev", "test"]:
        gold_path = os.path.join(gold_folder, f"narc_{wl_naming[split]}.jsonl")
        pred_path = os.path.join(predicted_folder, f"{experiment}_{split}_predicted.jsonlines")
        
        for f in [gold_path, pred_path]:
            assert os.path.exists(f)
        gold_clusters = read_clusters(gold_path)
        pred_clusters = read_clusters(pred_path )

        assert len(gold_clusters) == len(pred_clusters) # Should be one for each document

        scorer = corefeval.Scorer()
        for gold_doc, pred_doc in zip(gold_clusters, pred_clusters):
            scorer.update(corefeval.Document(predicted = pred_doc, truth = gold_doc))
        
        conll_f1, metrics = scorer.detailed_score(experiment, split)
        # Feiler, har fire, ikke tre listenivåer: [[[[1, 3], [26, 27], [
        # corefeval.get_metrics(pred_clusters, gold_clusters)
        print(conll_f1)
        print(metrics)
