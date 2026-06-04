from .model import Outcome
from .engine import Rule

HOMELAB_RULES = [
    # Git Destructive
    Rule(
        id="git-reset-hard",
        category="git_destructive",
        outcome=Outcome.DENY,
        reason="git reset --hard is dangerous and can lose uncommitted work. Use git stash first.",
        argv_prefix=("git", "reset", "--hard"),
    ),
    Rule(
        id="git-push-force",
        category="git_destructive",
        outcome=Outcome.CONFIRM,
        reason="Force pushing can overwrite remote history. Ensure you are on a feature branch.",
        argv_prefix=("git", "push", "--force"),
    ),
    Rule(
        id="git-push-force-with-lease",
        category="git_destructive",
        outcome=Outcome.CONFIRM,
        reason="Force pushing with lease is safer but still overwrites history.",
        argv_prefix=("git", "push", "--force-with-lease"),
    ),
    Rule(
        id="git-branch-delete-force",
        category="git_destructive",
        outcome=Outcome.CONFIRM,
        reason="Force deleting a branch can lose commits not merged elsewhere.",
        argv_prefix=("git", "branch", "-D"),
    ),

    # Filesystem Destructive
    Rule(
        id="rm-rf-root",
        category="filesystem_destructive",
        outcome=Outcome.DENY,
        reason="rm -rf / is strictly forbidden.",
        argv_pattern=r"^rm\s+.*-rf.*\s+/$",
    ),
    Rule(
        id="rm-rf-home",
        category="filesystem_destructive",
        outcome=Outcome.DENY,
        reason="rm -rf on home directory is forbidden.",
        argv_pattern=r"^rm\s+.*-rf.*\s+\$HOME|~|/home/deepwatrcreatur/?$",
    ),

    # Remote Execution & Privilege Escalation
    Rule(
        id="sudo-generic",
        category="privilege_escalation",
        outcome=Outcome.CONFIRM,
        reason="sudo grants root privileges.",
        argv_prefix=("sudo",),
    ),
    Rule(
        id="ssh-generic",
        category="remote_execution",
        outcome=Outcome.CONFIRM,
        reason="Executing commands on remote hosts requires confirmation.",
        argv_prefix=("ssh",),
    ),

    # Infra Mutation
    Rule(
        id="nixos-rebuild-switch",
        category="infra_mutation",
        outcome=Outcome.CONFIRM,
        reason="nixos-rebuild switch applies changes to the live system.",
        argv_pattern=r"nixos-rebuild\s+.*switch",
    ),
    Rule(
        id="nix-flake-update",
        category="infra_mutation",
        outcome=Outcome.CONFIRM,
        reason="Updating flake inputs can trigger broad system changes.",
        argv_prefix=("nix", "flake", "update"),
    ),

    # Safe Read-Only (Examples to show ALLOW)
    Rule(
        id="git-status",
        category="safe_read_only",
        outcome=Outcome.ALLOW,
        reason="git status is safe.",
        argv_prefix=("git", "status"),
    ),
    Rule(
        id="ls-generic",
        category="safe_read_only",
        outcome=Outcome.ALLOW,
        reason="ls is safe.",
        argv_prefix=("ls",),
    ),
    Rule(
        id="rg-generic",
        category="safe_read_only",
        outcome=Outcome.ALLOW,
        reason="ripgrep is safe.",
        argv_prefix=("rg",),
    ),
]
