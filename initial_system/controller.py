"""Submission controller orchestrating the baseline workflow."""

from __future__ import annotations

from datetime import datetime
from typing import Dict

from .database import Database
from .evaluation import EvaluationManager
from .models import ResearchOutput
from .notification import NotificationService
from .reviewers import ReviewerManager
from .validation import ValidationManager


class SubmissionController:
    """Main controller for research output submissions."""

    def __init__(
        self,
        validation_manager: ValidationManager,
        database: Database,
        reviewer_manager: ReviewerManager,
        evaluation_manager: EvaluationManager,
        notification_service: NotificationService,
    ):
        self.validation_manager = validation_manager
        self.database = database
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager
        self.notification_service = notification_service

    def validate_format(self, data: Dict) -> bool:
        print("[SC] SubmissionController: Validating format of submission data")

        required_fields = ["researcher_id", "title", "content"]
        is_valid = all(field in data and data[field] for field in required_fields)

        if is_valid:
            print("[SC] SubmissionController: Format validation passed")
        else:
            print("[SC] SubmissionController: Format validation failed")

        return is_valid

    def submit_research_output(self, researcher_id: str, title: str, content: str) -> bool:
        print("\n" + "=" * 70)
        print(f"[SC] SubmissionController: Received submission from Researcher {researcher_id}")
        print("=" * 70 + "\n")

        submission_data = {"researcher_id": researcher_id, "title": title, "content": content}

        if not self.validate_format(submission_data):
            print("[SC] SubmissionController: Returning error to Researcher")
            error_message = "Invalid submission format"
            self.validation_manager.validation_error("UNKNOWN", error_message)
            print(f"[SC] SubmissionController -> Researcher: ERROR - {error_message}\n")
            return False

        submission_id = f"SUB_{researcher_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        research_output = ResearchOutput(
            id=submission_id,
            researcher_id=researcher_id,
            title=title,
            content=content,
            submission_date=datetime.now(),
        )

        self.database.save_submission(research_output)

        print("\n[SC] SubmissionController: Starting reviewer assignment loop")
        self._assign_reviewers(submission_id, researcher_id)

        print("\n[SC] SubmissionController: Starting evaluation")
        self.evaluation_manager.start_evaluation(submission_id)

        print("\n[SC] SubmissionController: Waiting for reviewer scores")
        self._collect_reviewer_scores(submission_id)

        print("\n[SC] SubmissionController: Finalizing evaluation")
        self.evaluation_manager.finalize_evaluation(submission_id, self.notification_service)

        decision = self.notification_service.evaluation_results.get(submission_id, {}).get(
            "decision", "REJECTED"
        )

        print(f"\n[SC] SubmissionController: Processing decision: {decision}")
        if decision == "REJECTED":
            self.notification_service.notify_rejection(submission_id, self.validation_manager)
        elif decision == "REVISION_NEEDED":
            self.notification_service.notify_revision(submission_id, self.validation_manager)

        self.validation_manager.send_notification()
        self.notification_service.send_notification(researcher_id, submission_id, decision)

        print(f"\n[SC] SubmissionController -> Researcher: {decision}\n")
        print("=" * 70 + "\n")

        return True

    def _assign_reviewers(self, submission_id: str, researcher_id: str) -> None:
        filtered_reviewers = self.database.get_filtered_reviewers(researcher_id)
        self.reviewer_manager.assign_review(submission_id, filtered_reviewers)

        for reviewer_id in filtered_reviewers[:3]:
            self.database.increment_reviewer_workload(reviewer_id)

    def _collect_reviewer_scores(self, submission_id: str) -> None:
        if submission_id in self.reviewer_manager.assignments:
            reviewer_ids = self.reviewer_manager.assignments[submission_id]

            for reviewer_id in reviewer_ids:
                reviewer = self.reviewer_manager.reviewers[reviewer_id]
                score = self._generate_sample_score()
                reviewer.submit_score(
                    submission_id,
                    score,
                    f"Comments from {reviewer_id}",
                    self.evaluation_manager,
                )

    def _generate_sample_score(self) -> float:
        import random

        return random.uniform(3.0, 9.0)
