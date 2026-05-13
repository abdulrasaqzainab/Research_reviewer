"""Decision table encapsulation."""

from __future__ import annotations

from .models import SubmissionStatus


class DecisionTable:
    """Encapsulates the decision rules used by the evaluation service."""

    def evaluate(self, average: float, consensus: bool) -> SubmissionStatus:
        if average >= 7.5 and consensus:
            return SubmissionStatus.ACCEPTED
        if average < 5.0:
            return SubmissionStatus.REJECTED
        return SubmissionStatus.REVISION_NEEDED
