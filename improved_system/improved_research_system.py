"""Research output submission system aligned with the UML sequence diagram.

This module is the backwards-compatible import surface:

    import improved_system.improved_research_system as improved_research_system

The implementation is split into smaller modules under `improved_system/`.
"""

from .actor import Researcher
from .controller import OptimisedController
from .decision import DecisionTable
from .evaluation import EvaluationService
from .models import (
    EvaluationOutcome,
    ReviewResult,
    Submission,
    SubmissionStatus,
    ValidationResult,
)
from .notification import NotificationService
from .repository import SubmissionRepository
from .reviewers import ReviewerPool
from .ui import UI
from .validation import Validator
from .wiring import initialize_system, main

__all__ = [
    "SubmissionStatus",
    "Submission",
    "ReviewResult",
    "ValidationResult",
    "EvaluationOutcome",
    "Validator",
    "SubmissionRepository",
    "ReviewerPool",
    "DecisionTable",
    "EvaluationService",
    "NotificationService",
    "OptimisedController",
    "UI",
    "Researcher",
    "initialize_system",
    "main",
]


if __name__ == "__main__":
    main()