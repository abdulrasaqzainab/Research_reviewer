"""Domain models """

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SubmissionStatus(Enum):
    """Status of a research submission"""

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REVISION_NEEDED = "REVISION_NEEDED"


class ReviewStatus(Enum):
    """Status of a review assignment"""

    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


@dataclass
class ResearchOutput:
    """Data structure for research output submission"""

    id: str
    researcher_id: str
    title: str
    content: str
    submission_date: datetime
    status: SubmissionStatus = SubmissionStatus.PENDING


@dataclass
class ReviewScore:
    """Data structure for a reviewer's score"""

    reviewer_id: str
    submission_id: str
    score: float
    comments: str
    submission_date: datetime
