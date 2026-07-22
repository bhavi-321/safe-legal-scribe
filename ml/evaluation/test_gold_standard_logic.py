import numpy as np

from test_gold_standard import evaluate_at_threshold


def test_evaluate_at_threshold_uses_own_category_only():
    examples = [
        {"id": "a_risky", "category": "A", "label": 1},
        {"id": "a_safe", "category": "A", "label": 0},
        {"id": "b_safe", "category": "B", "label": 0},
    ]
    categories = ["A", "B"]
    sims = np.array([
        [0.60, 0.10],  # risky in A gets flagged via A
        [0.40, 0.95],  # safe in A is NOT flagged (B score must be ignored)
        [0.70, 0.30],  # safe in B is NOT flagged (B score below threshold)
    ])

    result = evaluate_at_threshold(examples, sims, categories, threshold=0.50)

    assert result["tp"] == 1
    assert result["fp"] == 0
    assert result["tn"] == 2
    assert result["fn"] == 0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
