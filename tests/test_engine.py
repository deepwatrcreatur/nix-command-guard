from __future__ import annotations

import unittest

from nix_command_guard.engine import DecisionEngine, Rule
from nix_command_guard.model import Outcome


def build_engine() -> DecisionEngine:
    return DecisionEngine(
        [
            Rule(
                id="git-reset-hard",
                category="git_destructive",
                outcome=Outcome.DENY,
                reason="`git reset --hard` discards tracked work immediately",
                argv_prefix=("git", "reset", "--hard"),
            ),
            Rule(
                id="git-push-force",
                category="git_destructive",
                outcome=Outcome.CONFIRM,
                reason="Force-pushing rewrites remote history",
                argv_pattern=r"^git push(?: .*)? --force(?:-with-lease)?(?:\s|$)|^git push(?: .*)? --force-with-lease(?:\s|$)",
            ),
            Rule(
                id="rm-root",
                category="filesystem_destructive",
                outcome=Outcome.DENY,
                reason="Recursive deletion of root-like paths must never execute",
                argv_pattern=r"^rm(?:\s+-[A-Za-z]*[rR][A-Za-z]*|\s+-[A-Za-z]*[fF][A-Za-z]*|\s+--recursive|\s+--force)*\s+/\s*$",
            ),
            Rule(
                id="rm-recursive",
                category="filesystem_destructive",
                outcome=Outcome.CONFIRM,
                reason="Recursive removal needs an explicit safety gate",
                argv_pattern=r"^rm(?: .*)?-r(?:f)?(?:\s|$)|^rm(?: .*)?-rf(?:\s|$)",
            ),
            Rule(
                id="ssh-sudo-rebuild",
                category="infra_mutation",
                outcome=Outcome.CONFIRM,
                reason="Remote privileged rebuild mutates infrastructure state",
                argv_pattern=r"^ssh\s+\S+.*\bsudo\b.*\bnixos-rebuild\b.*\b(switch|boot|test)\b",
            ),
            Rule(
                id="ripgrep-read-only",
                category="safe_read_only",
                outcome=Outcome.ALLOW,
                reason="Read-only search command",
                argv_prefix=("rg",),
            ),
        ]
    )


class DecisionEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_engine()

    def test_denies_git_reset_hard(self) -> None:
        decision = self.engine.evaluate(["git", "reset", "--hard"])
        self.assertEqual(decision.outcome, Outcome.DENY)
        self.assertEqual(decision.category, "git_destructive")
        self.assertEqual(decision.matched_rule, "git-reset-hard")

    def test_confirms_force_push(self) -> None:
        decision = self.engine.evaluate(["git", "push", "--force", "origin", "main"])
        self.assertEqual(decision.outcome, Outcome.CONFIRM)
        self.assertTrue(decision.requires_confirmation)
        self.assertEqual(decision.category, "git_destructive")

    def test_denies_recursive_root_delete(self) -> None:
        decision = self.engine.evaluate(["rm", "-rf", "/"])
        self.assertEqual(decision.outcome, Outcome.DENY)
        self.assertEqual(decision.category, "filesystem_destructive")

    def test_confirms_other_recursive_delete(self) -> None:
        decision = self.engine.evaluate(["rm", "-rf", "/tmp/some-known-worktree"])
        self.assertEqual(decision.outcome, Outcome.CONFIRM)
        self.assertEqual(decision.category, "filesystem_destructive")

    def test_confirms_remote_rebuild(self) -> None:
        decision = self.engine.evaluate(
            ["ssh", "router", "sudo", "nixos-rebuild", "switch", "--flake", ".#router"]
        )
        self.assertEqual(decision.outcome, Outcome.CONFIRM)
        self.assertEqual(decision.category, "infra_mutation")

    def test_allows_read_only_search(self) -> None:
        decision = self.engine.evaluate(["rg", "pattern", "."])
        self.assertEqual(decision.outcome, Outcome.ALLOW)
        self.assertEqual(decision.category, "safe_read_only")

    def test_normalizes_executable_path(self) -> None:
        decision = self.engine.evaluate(["/usr/bin/git", "reset", "--hard"])
        self.assertEqual(decision.outcome, Outcome.DENY)
        self.assertEqual(decision.command, "git")

    def test_defaults_to_warn_when_no_rule_matches(self) -> None:
        decision = self.engine.evaluate(["echo", "hello"])
        self.assertEqual(decision.outcome, Outcome.WARN)
        self.assertEqual(decision.category, "unclassified")
        self.assertIsNone(decision.matched_rule)

    def test_returns_structured_output(self) -> None:
        record = self.engine.evaluate(["rg", "needle", "."]).as_dict()
        self.assertEqual(record["schema_version"], "command-guard/v1")
        self.assertEqual(record["command"], "rg")
        self.assertEqual(record["outcome"], "allow")
        self.assertEqual(record["matched_rule"], "ripgrep-read-only")
        self.assertFalse(record["requires_confirmation"])


if __name__ == "__main__":
    unittest.main()
