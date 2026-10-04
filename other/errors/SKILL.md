---
description: Imported skill errors from agentskills
name: errors
signature: 5780d314db735400c3959d20ed19a8c59445786d35a1a1b7cf368f01576d91f4
source: /a0/tmp/skills_research/agentskills/skills-ref/src/skills_ref/errors.py
---

"""Skill-related exceptions."""


class SkillError(Exception):
    """Base exception for all skill-related errors."""

    pass


class ParseError(SkillError):
    """Raised when SKILL.md parsing fails."""

    pass


class ValidationError(SkillError):
    """Raised when skill properties are invalid.

    Attributes:
        errors: List of validation error messages (may contain just one)
    """

    def __init__(self, message: str, errors: list[str] | None = None):
        super().__init__(message)
        self.errors = errors if errors is not None else [message]
