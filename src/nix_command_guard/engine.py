from __future__ import annotations

from dataclasses import dataclass
import os
import re
from typing import Iterable

from .model import Outcome

SCHEMA_VERSION = "command-guard/v1"


def _normalize_executable(token: str) -> str:
    return os.path.basename(token) if token else token


def normalize_argv(argv: Iterable[str]) -> tuple[str, ...]:
    items = tuple(argv)
    if not items:
        raise ValueError("argv must contain at least one token")
    return (_normalize_executable(items[0]), *items[1:])


@dataclass(frozen=True)
class Rule:
    id: str
    category: str
    outcome: Outcome
    reason: str
    argv_prefix: tuple[str, ...] | None = None
    argv_pattern: str | None = None

    def matches(self, argv: tuple[str, ...]) -> bool:
        if self.argv_prefix is None and self.argv_pattern is None:
            return False

        if self.argv_prefix is not None:
            prefix = normalize_argv(self.argv_prefix)
            if len(argv) < len(prefix) or argv[: len(prefix)] != prefix:
                return False

        if self.argv_pattern is not None:
            if re.search(self.argv_pattern, " ".join(argv)) is None:
                return False

        return True


@dataclass(frozen=True)
class DecisionRecord:
    command: str
    argv: tuple[str, ...]
    category: str
    outcome: Outcome
    reason: str
    matched_rule: str | None
    schema_version: str = SCHEMA_VERSION

    @property
    def requires_confirmation(self) -> bool:
        return self.outcome.requires_confirmation

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "command": self.command,
            "argv": list(self.argv),
            "category": self.category,
            "outcome": self.outcome.value,
            "reason": self.reason,
            "matched_rule": self.matched_rule,
            "requires_confirmation": self.requires_confirmation,
        }


class DecisionEngine:
    def __init__(
        self,
        rules: Iterable[Rule],
        *,
        default_outcome: Outcome = Outcome.WARN,
        default_category: str = "unclassified",
        default_reason: str = "No matching safety rule",
    ) -> None:
        self.rules = tuple(rules)
        self.default_outcome = default_outcome
        self.default_category = default_category
        self.default_reason = default_reason

    def evaluate(self, argv: Iterable[str]) -> DecisionRecord:
        normalized_argv = normalize_argv(argv)

        for rule in self.rules:
            if rule.matches(normalized_argv):
                return DecisionRecord(
                    command=normalized_argv[0],
                    argv=normalized_argv,
                    category=rule.category,
                    outcome=rule.outcome,
                    reason=rule.reason,
                    matched_rule=rule.id,
                )

        return DecisionRecord(
            command=normalized_argv[0],
            argv=normalized_argv,
            category=self.default_category,
            outcome=self.default_outcome,
            reason=self.default_reason,
            matched_rule=None,
        )


def evaluate_argv(argv: Iterable[str], rules: Iterable[Rule]) -> DecisionRecord:
    return DecisionEngine(rules).evaluate(argv)
