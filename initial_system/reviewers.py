"""Reviewer domain objects and assignment logic."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from .models import ReviewScore


class Reviewer:
    """Represents a reviewer in the system."""

    def __init__(self, reviewer_id: str):
        self.reviewer_id = reviewer_id
        self.assigned_reviews: List[str] = []
        self.submitted_scores: List[ReviewScore] = []

    def assign_review(self, submission_id: str) -> None:
        print(
            f"[R] Reviewer {self.reviewer_id}: Received review assignment for submission {submission_id}"
        )
        self.assigned_reviews.append(submission_id)

    def submit_score(
        self,
        submission_id: str,
        score: float,
        comments: str,
        evaluation_manager: "EvaluationManager",
    ) -> None:
        review_score = ReviewScore(
            reviewer_id=self.reviewer_id,
            submission_id=submission_id,
            score=score,
            comments=comments,
            submission_date=datetime.now(),
        )
        print(
            f"[R] Reviewer {self.reviewer_id}: Submitting score {score} to EvaluationManager"
        )
        evaluation_manager.submit_score(review_score)
        self.submitted_scores.append(review_score)


class ReviewerManager:
    """Manages reviewer assignment process."""

    def __init__(self):
        self.reviewers: Dict[str, Reviewer] = {}
        self.assignments: Dict[str, List[str]] = {}

    def get_or_create_reviewer(self, reviewer_id: str) -> Reviewer:
        if reviewer_id not in self.reviewers:
            self.reviewers[reviewer_id] = Reviewer(reviewer_id)
        return self.reviewers[reviewer_id]

    def assign_review(self, submission_id: str, filtered_reviewers: List[str]) -> None:
        print(
            f"[RM] ReviewerManager: Starting assignment process for submission {submission_id}"
        )
        self.assignments[submission_id] = []

        for reviewer_id in filtered_reviewers[:3]:
            self._assign_to_reviewer(submission_id, reviewer_id)

    def _assign_to_reviewer(self, submission_id: str, reviewer_id: str) -> None:
        print(f"[RM] ReviewerManager: Assigning review to Reviewer {reviewer_id}")
        reviewer = self.get_or_create_reviewer(reviewer_id)
        reviewer.assign_review(submission_id)
        self.assignments[submission_id].append(reviewer_id)
