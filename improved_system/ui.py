"""UI participant"""

from __future__ import annotations

from typing import Dict, List, Optional

from .controller import OptimisedController


class UI:
    """Represents the user interface"""

    def __init__(self, controller: OptimisedController) -> None:
        self.controller = controller
        self.last_error: Optional[List[str]] = None
        self.last_result: Optional[Dict[str, object]] = None

    def submitResearchOutput(self, data: Dict[str, object], researcher: "Researcher") -> Dict[str, object]:
        result = self.controller.submit(data)
        if result["status"] == "error":
            self.displayError(result["errors"], researcher)
        else:
            self.sendNotification(result, researcher)
        return result

    def displayError(self, error: List[str], researcher: "Researcher") -> None:
        self.last_error = list(error)
        researcher.displayError(error)

    def sendNotification(self, result: Dict[str, object], researcher: "Researcher") -> None:
        notification = dict(result.get("notification", result))
        self.last_result = notification
        researcher.receiveNotification(notification)
