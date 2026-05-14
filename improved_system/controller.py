"""Optimised controller coordinating the end-to-end workflow"""

from __future__ import annotations

from typing import Dict

from .evaluation import EvaluationService
from .models import Submission
from .notification import NotificationService
from .repository import SubmissionRepository
from .reviewers import ReviewerPool
from .validation import Validator


class OptimisedController:
    """Coordinates the diagram flow from validation to notification"""

    def __init__(
        self,
        validator: Validator,
        submission_repository: SubmissionRepository,
        reviewer_pool: ReviewerPool,
        evaluation_service: EvaluationService,
        notification_service: NotificationService,
    ) -> None:
        self.validator = validator
        self.submission_repository = submission_repository
        self.reviewer_pool = reviewer_pool
        self.evaluation_service = evaluation_service
        self.notification_service = notification_service

    def submit(self, data: Dict[str, object]) -> Dict[str, object]:
        submission = Submission(
            author=str(data.get("author", "")),
            title=str(data.get("title", "")),
            content=str(data.get("content", "")),
        )

        validation = self.validator.validate(submission)
        if not validation.is_valid:
            return {"status": "error", "errors": validation.errors}

        sub_id = self.submission_repository.save(submission)
        reviewers = self.reviewer_pool.selectAndAssign(submission.author)
        results = self.reviewer_pool.collectReviews(reviewers, sub_id)
        self.submission_repository.saveScores(sub_id, results)
        evaluation_outcome = self.evaluation_service.evaluate(results)
        notification = self.notification_service.notify(submission.author, evaluation_outcome.decision)

        return {
            "status": "success",
            "submission_id": sub_id,
            "reviewers": reviewers,
            "results": results,
            "outcome": evaluation_outcome,
            "notification": notification,
        }
