"""Validation-related behavior"""

from __future__ import annotations

from typing import List, Tuple


class ValidationManager:
    """Manages validation of research submissions"""

    def __init__(self):
        self.validation_errors: List[Tuple[str, str]] = []

    def validation_error(self, submission_id: str, error_message: str) -> None:
        print(f"[VM] ValidationManager: Recording validation error for submission {submission_id}")
        self.validation_errors.append((submission_id, error_message))

    def notify_rejection(self, submission_id: str, reason: str) -> None:
        print(
            f"[VM] ValidationManager: Notifying rejection for submission {submission_id}. Reason: {reason}"
        )

    def notify_revision(self, submission_id: str, feedback: str) -> None:
        print(
            f"[VM] ValidationManager: Notifying revision needed for submission {submission_id}. Feedback: {feedback}"
        )

    def send_notification(self) -> None:
        print("[VM] ValidationManager: Sending notification via NotificationService")
