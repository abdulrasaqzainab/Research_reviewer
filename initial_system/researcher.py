"""Researcher actor entry point"""

from __future__ import annotations

from datetime import datetime
from typing import List

from .controller import SubmissionController


class Researcher:
    """Represents a researcher who submits research outputs"""

    def __init__(self, researcher_id: str, submission_controller: SubmissionController):
        self.researcher_id = researcher_id
        self.submission_controller = submission_controller
        self.submissions: List[str] = []

    def submit_research_output(self, title: str, content: str) -> bool:
        print(f"[Researcher] {self.researcher_id}: Submitting research output")
        print(f"    Title: {title}")
        print(f"    Content: {content[:50]}...\n")

        success = self.submission_controller.submit_research_output(
            self.researcher_id, title, content
        )

        if success:
            submission_id = f"SUB_{self.researcher_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.submissions.append(submission_id)

        return success
