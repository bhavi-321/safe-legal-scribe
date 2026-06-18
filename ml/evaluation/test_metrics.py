"""
test_metrics.py

Unit tests for metrics.py. No network, no ML libraries -- just checks the
math is right. Run with: pytest test_metrics.py -v
"""

import math
import pytest

from metrics import (
    confusion_counts,
    precision_recall_f1,
    accuracy_score,
    false_positive_rate,
    false_negative_rate,
    dcg_at_k,
    ndcg_at_k,
    reciprocal_rank,
    mean_reciprocal_rank,
)


def test_confusion_counts_basic():
    y_true = [1, 1, 0, 0, 1, 0]
    y_pred = [1, 0, 0, 1, 1, 0]
    tp, fp, tn, fn = confusion_counts(y_true, y_pred)
    assert (tp, fp, tn, fn) == (2, 1, 2, 1)


def test_confusion_counts_length_mismatch():
    with pytest.raises(ValueError):
        confusion_counts([1, 0], [1])


def test_precision_recall_f1_normal_case():
    # tp=2, fp=1, fn=1 -> precision=2/3, recall=2/3, f1=2/3
    result = precision_recall_f1(tp=2, fp=1, fn=1)
    assert math.isclose(result["precision"], 2 / 3, rel_tol=1e-9)
    assert math.isclose(result["recall"], 2 / 3, rel_tol=1e-9)
    assert math.isclose(result["f1"], 2 / 3, rel_tol=1e-9)


def test_precision_recall_f1_perfect():
    result = precision_recall_f1(tp=10, fp=0, fn=0)
    assert result == {"precision": 1.0, "recall": 1.0, "f1": 1.0}


def test_precision_recall_f1_no_positives_predicted():
    # tp=0, fp=0 -> precision undefined, defined here as 0.0 by convention
    result = precision_recall_f1(tp=0, fp=0, fn=5)
    assert result["precision"] == 0.0
    assert result["recall"] == 0.0
    assert result["f1"] == 0.0


def test_accuracy_score():
    assert accuracy_score(tp=3, tn=4, fp=1, fn=2) == pytest.approx(7 / 10)
    assert accuracy_score(tp=0, tn=0, fp=0, fn=0) == 0.0


def test_false_positive_rate():
    assert false_positive_rate(fp=1, tn=9) == pytest.approx(0.1)
    assert false_positive_rate(fp=0, tn=0) == 0.0


def test_false_negative_rate():
    assert false_negative_rate(fn=2, tp=8) == pytest.approx(0.2)
    assert false_negative_rate(fn=0, tp=0) == 0.0


def test_dcg_at_k_ideal_ordering():
    # Best possible ordering: all relevant items first.
    relevances = [1, 1, 1, 0, 0]
    expected = 1 / math.log2(2) + 1 / math.log2(3) + 1 / math.log2(4)
    assert dcg_at_k(relevances, k=5) == pytest.approx(expected)


def test_dcg_at_k_respects_k():
    relevances = [1, 1, 1, 1]
    # Only first 2 should count
    expected = 1 / math.log2(2) + 1 / math.log2(3)
    assert dcg_at_k(relevances, k=2) == pytest.approx(expected)


def test_ndcg_at_k_perfect_ranking_is_one():
    relevances = [1, 1, 0, 0, 0]
    assert ndcg_at_k(relevances, k=5) == pytest.approx(1.0)


def test_ndcg_at_k_worst_ranking_is_low():
    # All relevant items pushed to the bottom -> ndcg should be < a good ranking
    worst = [0, 0, 0, 1, 1]
    best = [1, 1, 0, 0, 0]
    assert ndcg_at_k(worst, k=5) < ndcg_at_k(best, k=5)


def test_ndcg_at_k_no_relevant_items_is_zero():
    assert ndcg_at_k([0, 0, 0], k=3) == 0.0


def test_reciprocal_rank_first_position():
    assert reciprocal_rank([1, 0, 0]) == 1.0


def test_reciprocal_rank_third_position():
    assert reciprocal_rank([0, 0, 1]) == pytest.approx(1 / 3)


def test_reciprocal_rank_no_relevant_items():
    assert reciprocal_rank([0, 0, 0]) == 0.0


def test_mean_reciprocal_rank():
    lists = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
    # RRs: 1.0, 0.5, 0.0 -> mean = 0.5
    assert mean_reciprocal_rank(lists) == pytest.approx(0.5)


def test_mean_reciprocal_rank_empty():
    assert mean_reciprocal_rank([]) == 0.0
