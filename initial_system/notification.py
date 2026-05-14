"""Notification + decision rules"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from .models import ReviewScore
from .validation import ValidationManager


class NotificationService:
    """Handles notification logic and final evaluation decision making"""

    def __init__(self):
        self.notifications: List[Dict] = []
        self.evaluation_results: Dict[str, Dict] = {}

    def calculate_average(self, submission_id: str, scores: List[ReviewScore]) -> float:
        if not scores:
            return 0.0

        average = sum(s.score for s in scores) / len(scores)
        print(
            f"[NS] NotificationService: Calculated average score {average:.2f} for submission {submission_id}"
        )

        self.evaluation_results.setdefault(submission_id, {})["average_score"] = average
        return average

    def check_consensus(self, submission_id: str, scores: List[ReviewScore]) -> bool:
        if not scores:
            return False

        average = sum(s.score for s in scores) / len(scores)
        variance = sum((s.score - average) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5

        consensus = std_dev < 1.0
        print(
            f"[NS] NotificationService: Consensus check for submission {submission_id}: {consensus} (std_dev: {std_dev:.2f})"
        )

        self.evaluation_results.setdefault(submission_id, {})["consensus"] = consensus
        return consensus

    def apply_rules(self, submission_id: str, scores: List[ReviewScore]) -> str:
        if not scores:
            decision = "REJECTED"
        else:
            average = self.evaluation_results.get(submission_id, {}).get("average_score", 0)
            consensus = self.evaluation_results.get(submission_id, {}).get("consensus", False)

            if average >= 7.5 and consensus:
                decision = "ACCEPTED"
            elif average < 5.0:
                decision = "REJECTED"
            else:
                decision = "REVISION_NEEDED"

        print(
            f"[NS] NotificationService: Applied rules for submission {submission_id}: decision = {decision}"
        )
        self.evaluation_results.setdefault(submission_id, {})["decision"] = decision
        return decision

    def notify_rejection(self, submission_id: str, validation_manager: ValidationManager) -> None:
        print(f"[NS] NotificationService: Notifying rejection for submission {submission_id}")
        validation_manager.notify_rejection(submission_id, "Evaluation resulted in rejection")

    def notify_revision(self, submission_id: str, validation_manager: ValidationManager) -> None:
        print(
            f"[NS] NotificationService: Notifying revision needed for submission {submission_id}"
        )
        validation_manager.notify_revision(submission_id, "Evaluation resulted in revision needed")

    def send_notification(self, researcher_id: str, submission_id: str, decision: str) -> None:
        notification = {
            "researcher_id": researcher_id,
            "submission_id": submission_id,
            "decision": decision,
            "timestamp": datetime.now(),
        }
        self.notifications.append(notification)
        print(
            f"[NS] NotificationService: Sending notification to Researcher {researcher_id}: {decision}"
        )
