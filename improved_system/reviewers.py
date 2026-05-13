"""Reviewer selection and review collection."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .models import ReviewResult


class ReviewerPool:
    """Selects reviewers and collects review results."""

    def __init__(self) -> None:
        self.available_reviewers: List[str] = [
            "Reviewer001",
            "Reviewer002",
            "Reviewer003",
            "Reviewer004",
            "Reviewer005",
        ]
        self.review_assignments: Dict[str, List[str]] = {}

    def selectAndAssign(self, author: str) -> List[str]:
        reviewers = [reviewer_id for reviewer_id in self.available_reviewers if reviewer_id != author][:3]
        self.review_assignments[author] = list(reviewers)
        return reviewers

    def collectReviews(self, reviewers: List[str], sub_id: str) -> List[ReviewResult]:
        results: List[ReviewResult] = []

        for reviewer_id in reviewers:
            score, comments = self._generate_review(reviewer_id)
            results.append(
                ReviewResult(
                    reviewer_id=reviewer_id,
                    submission_id=sub_id,
                    score=score,
                    comments=comments,
                )
            )

        return results

    def _generate_review(self, reviewer_id: str) -> Tuple[float, str]:
        template_scores = {
            "Reviewer001": (8.2, "Strong contribution and clear analysis."),
            "Reviewer002": (7.9, "Well structured and technically sound."),
            "Reviewer003": (8.1, "Good evidence and coherent conclusions."),
            "Reviewer004": (7.6, "Solid work with minor improvements needed."),
            "Reviewer005": (8.0, "Quality research with consistent findings."),
        }
        return template_scores.get(reviewer_id, (7.5, "Review completed."))
