"""Researcher actor that initiates submissions"""

from __future__ import annotations

from typing import Dict, List

from .ui import UI


class Researcher:
    """Actor that initiates the submission through the UI."""

    def __init__(self, researcher_id: str, ui: UI) -> None:
        self.researcher_id = researcher_id
        self.ui = ui
        self.errors: List[List[str]] = []
        self.notifications: List[Dict[str, object]] = []

    def submitResearchOutput(self, data: Dict[str, object]) -> Dict[str, object]:
        payload = dict(data)
        payload.setdefault("author", self.researcher_id)
        return self.ui.submitResearchOutput(payload, self)

    def displayError(self, error: List[str]) -> None:
        self.errors.append(list(error))

    def receiveNotification(self, result: Dict[str, object]) -> None:
        self.notifications.append(dict(result))
