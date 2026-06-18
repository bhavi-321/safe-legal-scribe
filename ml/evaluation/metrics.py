"""
metrics.py

Pure, dependency-light metric functions used by test_gold_standard.py.

Deliberately has zero ML/network imports (no sentence-transformers, no
sklearn) so it can be unit tested in complete isolation -- see
test_metrics.py. The evaluation harness is the only thing that needs a
model; the math itself doesn't.
"""

import math
from typing import Sequence


def confusion_counts(y_true: Sequence[int], y_pred: Sequence[int]):
    """
    Returns (tp, fp, tn, fn) given parallel lists of binary 0/1 labels.

    1 = "is a risky clause" / "model flagged this as risky"
    0 = "is a safe clause"  / "model did not flag this"
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be the same length")

    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            tp += 1
        elif t == 0 and p == 1:
            fp += 1
        elif t == 0 and p == 0:
            tn += 1
        elif t == 1 and p == 0:
            fn += 1
        else:
            raise ValueError(f"Labels must be 0 or 1, got y_true={t}, y_pred={p}")
    return tp, fp, tn, fn


def precision_recall_f1(tp: int, fp: int, fn: int) -> dict:
    """Standard precision / recall / F1 from confusion-matrix counts."""
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def accuracy_score(tp: int, tn: int, fp: int, fn: int) -> float:
    total = tp + tn + fp + fn
    return (tp + tn) / total if total else 0.0


def false_positive_rate(fp: int, tn: int) -> float:
    """Of all actually-safe clauses, what fraction got (wrongly) flagged?"""
    return fp / (fp + tn) if (fp + tn) else 0.0


def false_negative_rate(fn: int, tp: int) -> float:
    """Of all actually-risky clauses, what fraction did we miss?"""
    return fn / (fn + tp) if (fn + tp) else 0.0


def dcg_at_k(relevances: Sequence[int], k: int) -> float:
    """Discounted cumulative gain over a ranked list of 0/1 relevances."""
    return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(relevances[:k]))


def ndcg_at_k(relevances: Sequence[int], k: int) -> float:
    """
    Normalized DCG@k. 1.0 = the k most relevant items were ranked first
    (best possible ordering); 0.0 = nothing relevant appeared in the top k.
    """
    dcg = dcg_at_k(relevances, k)
    ideal = sorted(relevances, reverse=True)
    idcg = dcg_at_k(ideal, k)
    return dcg / idcg if idcg else 0.0


def reciprocal_rank(relevances: Sequence[int]) -> float:
    """1 / (rank of first relevant item), or 0.0 if none are relevant."""
    for idx, rel in enumerate(relevances):
        if rel:
            return 1.0 / (idx + 1)
    return 0.0


def mean_reciprocal_rank(list_of_relevance_lists: Sequence[Sequence[int]]) -> float:
    rrs = [reciprocal_rank(r) for r in list_of_relevance_lists]
    return sum(rrs) / len(rrs) if rrs else 0.0
