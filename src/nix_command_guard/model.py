from __future__ import annotations

from enum import StrEnum


class Outcome(StrEnum):
    ALLOW = "allow"
    WARN = "warn"
    CONFIRM = "confirm"
    DENY = "deny"

    @property
    def requires_confirmation(self) -> bool:
        return self is Outcome.CONFIRM
