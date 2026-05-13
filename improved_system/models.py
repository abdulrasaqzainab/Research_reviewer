"""Domain models for the improved research system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class SubmissionStatus(Enum):
    """Final decision values returned by the decision table."""

    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REVISION_NEEDED = "REVISION_NEEDED"


@dataclass
class Submission:
    """Submission payload passed through the workflow."""

    author: str
    title: str
    content: str
    submission_id: Optional[str] = None
    submitted_at: datetime = field(default_factory=datetime.now)


@dataclass
class ReviewResult:
    """Single review result collected from the reviewer pool."""

    reviewer_id: str
    submission_id: str
    score: float
    comments: str
    reviewed_at: datetime = field(default_factory=datetime.now)


@dataclass
class ValidationResult:
    """Validation outcome returned by the validator."""

    is_valid: bool
    errors: List[str]


@dataclass
class EvaluationOutcome:
    """Final evaluation outcome returned to the controller."""

    average: float
    consensus: bool
    decision: SubmissionStatus
    reviewer_count: int
    standard_deviation: float
