"""Evaluation coordination: collecting scores and triggering decision logic"""

from __future__ import annotations

from typing import Dict, List

from .models import ReviewScore


class EvaluationManager:
    """Manages the evaluation and scoring process for submissions"""

    def __init__(self):
        self.submission_scores: Dict[str, List[ReviewScore]] = {}
        self.evaluation_results: Dict[str, Dict] = {}

    def start_evaluation(self, submission_id: str) -> None:
        print(f"[EM] EvaluationManager: Starting evaluation for submission {submission_id}")
        self.submission_scores[submission_id] = []

    def submit_score(self, review_score: ReviewScore) -> None:
        submission_id = review_score.submission_id
        print(
            f"[EM] EvaluationManager: Received score from {review_score.reviewer_id} for submission {submission_id}"
        )

        if submission_id not in self.submission_scores:
            self.submission_scores[submission_id] = []
        self.submission_scores[submission_id].append(review_score)

    def finalize_evaluation(self, submission_id: str, notification_service: "NotificationService") -> None:
        print(f"[EM] EvaluationManager: Finalizing evaluation for submission {submission_id}")
        notification_service.calculate_average(
            submission_id, self.submission_scores.get(submission_id, [])
        )
        notification_service.check_consensus(
            submission_id, self.submission_scores.get(submission_id, [])
        )
        notification_service.apply_rules(
            submission_id, self.submission_scores.get(submission_id, [])
        )
