"""Persistence layer for submissions and review scores (in-memory)."""

from __future__ import annotations

from typing import Dict, List

from .models import ReviewResult, Submission


class SubmissionRepository:
    """Stores submissions and review scores."""

    def __init__(self) -> None:
        self.submissions: Dict[str, Submission] = {}
        self.review_scores: Dict[str, List[ReviewResult]] = {}
        self._next_id = 1

    def save(self, submission: Submission) -> str:
        submission_id = submission.submission_id or self._generate_submission_id()
        submission.submission_id = submission_id
        self.submissions[submission_id] = submission
        self.review_scores.setdefault(submission_id, [])
        return submission_id

    def saveScores(self, submission_id: str, results: List[ReviewResult]) -> None:
        self.review_scores.setdefault(submission_id, []).extend(results)

    def _generate_submission_id(self) -> str:
        submission_id = f"SUB_{self._next_id:04d}"
        self._next_id += 1
        return submission_id
