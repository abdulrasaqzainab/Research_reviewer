"""System initialization and demo entry point for the improved system."""

from __future__ import annotations

from typing import Dict
from typing import Tuple

from .actor import Researcher
from .controller import OptimisedController
from .decision import DecisionTable
from .evaluation import EvaluationService
from .notification import NotificationService
from .repository import SubmissionRepository
from .reviewers import ReviewerPool
from .ui import UI
from .validation import Validator


def _truncate(text: str, max_len: int = 60) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _print_banner() -> None:
    print("\n" + "=" * 70)
    print("RESEARCH OUTPUT SUBMISSION AND EVALUATION SYSTEM")
    print("=" * 70 + "\n")


def _print_controller_header(researcher_id: str) -> None:
    print("\n" + "=" * 70)
    print(f"[SC] SubmissionController: Received submission from Researcher {researcher_id}")
    print("=" * 70 + "\n")


def _print_invalid_submission_flow(researcher_id: str) -> None:
    print("[SC] SubmissionController: Validating format of submission data")
    print("[SC] SubmissionController: Format validation failed")
    print("[SC] SubmissionController: Returning error to Researcher")
    print("[VM] ValidationManager: Recording validation error for submission UNKNOWN")
    print("[SC] SubmissionController -> Researcher: ERROR - Invalid submission format")


def _print_valid_submission_flow(researcher_id: str, result: Dict[str, object]) -> None:
    submission_id = str(result.get("submission_id", "UNKNOWN"))
    reviewers = list(result.get("reviewers", []))
    results = list(result.get("results", []))
    outcome = result.get("outcome")
    notification = result.get("notification")

    print("[SC] SubmissionController: Validating format of submission data")
    print("[SC] SubmissionController: Format validation passed")

    print(f"[DB] Database: Saving submission {submission_id}")
    print(f"[DB] Database: Confirmation - submission {submission_id} saved successfully")

    print("\n[SC] SubmissionController: Starting reviewer assignment loop")
    print("[DB] Database: Getting available reviewers")
    print(f"[DB] Database: Filtering conflicts for researcher {researcher_id}")
    print("[DB] Database: Checking workload for reviewers")
    print(f"[DB] Database: Returning {len(reviewers)} filtered reviewers to ReviewerManager")
    print(f"[RM] ReviewerManager: Starting assignment process for submission {submission_id}")
    for reviewer_id in reviewers:
        print(f"[RM] ReviewerManager: Assigning review to Reviewer {reviewer_id}")
        print(f"[R] Reviewer {reviewer_id}: Received review assignment for submission {submission_id}")

    print("\n[SC] SubmissionController: Starting evaluation")
    print(f"[EM] EvaluationManager: Starting evaluation for submission {submission_id}")

    print("\n[SC] SubmissionController: Waiting for reviewer scores")
    for review_result in results:
        reviewer_id = getattr(review_result, "reviewer_id", "UNKNOWN")
        score = getattr(review_result, "score", 0.0)
        print(f"[R] Reviewer {reviewer_id}: Submitting score {score} to EvaluationManager")
        print(f"[EM] EvaluationManager: Received score from {reviewer_id} for submission {submission_id}")

    print("\n[SC] SubmissionController: Finalizing evaluation")
    print(f"[EM] EvaluationManager: Finalizing evaluation for submission {submission_id}")

    average = getattr(outcome, "average", 0.0)
    consensus = getattr(outcome, "consensus", False)
    standard_deviation = getattr(outcome, "standard_deviation", 0.0)
    decision = getattr(outcome, "decision", None)
    decision_value = getattr(decision, "value", str(decision) if decision is not None else "UNKNOWN")

    print(f"[NS] NotificationService: Calculated average score {average:.2f} for submission {submission_id}")
    print(
        f"[NS] NotificationService: Consensus check for submission {submission_id}: {bool(consensus)} (std_dev: {standard_deviation:.2f})"
    )
    print(f"[NS] NotificationService: Applied rules for submission {submission_id}: decision = {decision_value}")

    print(f"\n[SC] SubmissionController: Processing decision: {decision_value}")
    print("[VM] ValidationManager: Sending notification via NotificationService")
    print(f"[NS] NotificationService: Sending notification to Researcher {researcher_id}: {decision_value}")
    print(f"\n[SC] SubmissionController -> Researcher: {decision_value}")
    _ = notification  # included for completeness; already printed above


def initialize_system() -> Tuple[Researcher, UI, OptimisedController]:
    """Build the exact UML-matching object graph."""

    validator = Validator()
    submission_repository = SubmissionRepository()
    reviewer_pool = ReviewerPool()
    decision_table = DecisionTable()
    evaluation_service = EvaluationService(decision_table)
    notification_service = NotificationService()
    controller = OptimisedController(
        validator=validator,
        submission_repository=submission_repository,
        reviewer_pool=reviewer_pool,
        evaluation_service=evaluation_service,
        notification_service=notification_service,
    )
    ui = UI(controller)
    researcher = Researcher("RES001", ui)
    return researcher, ui, controller


def main() -> None:
    researcher, _, _ = initialize_system()

    _print_banner()

    valid_submission = {
        "title": "Machine Learning Advances in NLP",
        "content": "This research explores novel approaches to natural language processing.",
    }
    invalid_submission = {"title": "", "content": "Some content here"}

    print("\n>>> EXAMPLE 1: Valid Submission with Evaluation\n")
    print(f"[Researcher] {researcher.researcher_id}: Submitting research output")
    print(f"    Title: {valid_submission['title']}")
    print(f"    Content: {_truncate(valid_submission['content'])}\n")
    _print_controller_header(researcher.researcher_id)
    result_1 = researcher.submitResearchOutput(valid_submission)
    if result_1.get("status") == "success":
        _print_valid_submission_flow(researcher.researcher_id, result_1)
    else:
        _print_invalid_submission_flow(researcher.researcher_id)

    print("\n" + "=" * 70 + "\n")

    print("\n>>> EXAMPLE 2: Invalid Submission (Missing Title)\n")
    print(f"[Researcher] {researcher.researcher_id}: Submitting research output")
    print("    Title: ")
    print(f"    Content: {_truncate(invalid_submission['content'])}...\n")
    _print_controller_header(researcher.researcher_id)
    result_2 = researcher.submitResearchOutput(invalid_submission)
    if result_2.get("status") == "success":
        _print_valid_submission_flow(researcher.researcher_id, result_2)
    else:
        _print_invalid_submission_flow(researcher.researcher_id)


if __name__ == "__main__":
    main()
