"""In-memory persistence and reviewer filtering."""

from __future__ import annotations

from typing import Dict, List

from .models import ResearchOutput, ReviewScore


class Database:
    """Manages all data persistence operations."""

    def __init__(self):
        self.submissions: Dict[str, ResearchOutput] = {}
        self.scores: Dict[str, List[ReviewScore]] = {}
        self.available_reviewers: List[str] = [
            "Reviewer001",
            "Reviewer002",
            "Reviewer003",
            "Reviewer004",
            "Reviewer005",
        ]
        self.reviewer_conflicts: Dict[str, List[str]] = {}
        self.reviewer_workload: Dict[str, int] = {r: 0 for r in self.available_reviewers}

    def save_submission(self, research_output: ResearchOutput) -> bool:
        print(f"[DB] Database: Saving submission {research_output.id}")
        self.submissions[research_output.id] = research_output
        self.scores[research_output.id] = []
        print(
            f"[DB] Database: Confirmation - submission {research_output.id} saved successfully"
        )
        return True

    def get_available_reviewers(self) -> List[str]:
        print("[DB] Database: Getting available reviewers")
        return self.available_reviewers.copy()

    def filter_conflicts(self, researcher_id: str, available_reviewers: List[str]) -> List[str]:
        print(f"[DB] Database: Filtering conflicts for researcher {researcher_id}")
        conflicted = self.reviewer_conflicts.get(researcher_id, [])
        return [r for r in available_reviewers if r not in conflicted]

    def check_workload(self, reviewers: List[str]) -> List[str]:
        print("[DB] Database: Checking workload for reviewers")
        max_workload = 5
        return [r for r in reviewers if self.reviewer_workload.get(r, 0) < max_workload]

    def get_filtered_reviewers(self, researcher_id: str) -> List[str]:
        available = self.get_available_reviewers()
        after_conflict = self.filter_conflicts(researcher_id, available)
        final_list = self.check_workload(after_conflict)
        print(
            f"[DB] Database: Returning {len(final_list)} filtered reviewers to ReviewerManager"
        )
        return final_list

    def increment_reviewer_workload(self, reviewer_id: str) -> None:
        if reviewer_id in self.reviewer_workload:
            self.reviewer_workload[reviewer_id] += 1

    def save_review_score(self, submission_id: str, score: ReviewScore) -> None:
        if submission_id in self.scores:
            self.scores[submission_id].append(score)
