"""System initialization and demo entry point"""

from __future__ import annotations

from typing import Tuple

from .controller import SubmissionController
from .database import Database
from .evaluation import EvaluationManager
from .notification import NotificationService
from .researcher import Researcher
from .reviewers import ReviewerManager
from .validation import ValidationManager


def initialize_system() -> Tuple[SubmissionController, Researcher]:
    """Create all components and wire them together"""

    validation_manager = ValidationManager()
    database = Database()
    reviewer_manager = ReviewerManager()
    evaluation_manager = EvaluationManager()
    notification_service = NotificationService()

    submission_controller = SubmissionController(
        validation_manager=validation_manager,
        database=database,
        reviewer_manager=reviewer_manager,
        evaluation_manager=evaluation_manager,
        notification_service=notification_service,
    )

    researcher = Researcher(researcher_id="RES001", submission_controller=submission_controller)

    return submission_controller, researcher


def main() -> None:
    print("\n" + "=" * 70)
    print("RESEARCH OUTPUT SUBMISSION AND EVALUATION SYSTEM")
    print("=" * 70 + "\n")

    submission_controller, researcher = initialize_system()

    print("\n>>> EXAMPLE 1: Valid Submission with Evaluation\n")
    researcher.submit_research_output(
        title="Machine Learning Advances in NLP",
        content="This research explores novel approaches to natural language processing using transformer-based architectures...",
    )

    print("\n>>> EXAMPLE 2: Invalid Submission (Missing Title)\n")
    researcher.submit_research_output(title="", content="Some content here")


if __name__ == "__main__":
    main()
