"""Evaluation logic for collected review results."""

from __future__ import annotations

from statistics import mean, pstdev
from typing import List

from .decision import DecisionTable
from .models import EvaluationOutcome, ReviewResult


class EvaluationService:
    """Evaluates collected review results and returns the outcome."""

    def __init__(self, decision_table: DecisionTable) -> None:
        self.decision_table = decision_table

    def evaluate(self, results: List[ReviewResult]) -> EvaluationOutcome:
        scores = [result.score for result in results]

        if not scores:
            average = 0.0
            standard_deviation = 0.0
            consensus = False
        else:
            average = mean(scores)
            standard_deviation = pstdev(scores) if len(scores) > 1 else 0.0
            consensus = standard_deviation <= 1.0

        decision = self.decision_table.evaluate(average, consensus)
        return EvaluationOutcome(
            average=average,
            consensus=consensus,
            decision=decision,
            reviewer_count=len(scores),
            standard_deviation=standard_deviation,
        )
