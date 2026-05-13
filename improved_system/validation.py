"""Validation for the improved research system."""

from __future__ import annotations

from typing import List

from .models import Submission, ValidationResult


class Validator:
    """Validates submissions before persistence."""

    def validate(self, submission: Submission) -> ValidationResult:
        errors: List[str] = []

        if not submission.author.strip():
            errors.append("Author is required")
        if not submission.title.strip():
            errors.append("Title is required")
        if not submission.content.strip():
            errors.append("Content is required")

        return ValidationResult(is_valid=not errors, errors=errors)
