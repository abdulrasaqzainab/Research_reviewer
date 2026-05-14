"""Notification behavior for the improved system"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from .models import SubmissionStatus


class NotificationService:
    """Creates the final notification payload for the researcher"""

    def __init__(self) -> None:
        self.notifications: List[Dict[str, object]] = []

    def notify(self, author: str, decision: SubmissionStatus) -> Dict[str, object]:
        notification = {
            "author": author,
            "decision": decision.value,
            "message": self._message_for(decision),
            "timestamp": datetime.now(),
        }
        self.notifications.append(notification)
        return notification

    def _message_for(self, decision: SubmissionStatus) -> str:
        if decision == SubmissionStatus.ACCEPTED:
            return "Submission accepted."
        if decision == SubmissionStatus.REJECTED:
            return "Submission rejected."
        return "Revision needed."
