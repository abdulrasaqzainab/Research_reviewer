"""Research Output Submission and Evaluation System (baseline).

This file remains as the *public import surface* for backwards compatibility:

    from initial_system.research_system import SubmissionController, Database, ...

Internally, the implementation is split into focused modules under `initial_system/`
to keep the codebase maintainable.
"""

from .controller import SubmissionController
from .database import Database
from .evaluation import EvaluationManager
from .models import ResearchOutput, ReviewScore, ReviewStatus, SubmissionStatus
from .notification import NotificationService
from .researcher import Researcher
from .reviewers import Reviewer, ReviewerManager
from .validation import ValidationManager
from .wiring import initialize_system, main

__all__ = [
    "Researcher",
    "SubmissionController",
    "ValidationManager",
    "Database",
    "ReviewerManager",
    "Reviewer",
    "EvaluationManager",
    "NotificationService",
    "ResearchOutput",
    "ReviewScore",
    "SubmissionStatus",
    "ReviewStatus",
    "initialize_system",
    "main",
]


if __name__ == "__main__":
    main()
