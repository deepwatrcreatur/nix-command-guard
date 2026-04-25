# 04 Shell Wrapper And Audit Log

Status: done

## Progress

- enhanced `src/nix_command_guard/cli.py` with human-readable colored output
- implemented append-only audit logging to `~/.cache/nix-command-guard/audit.jsonl`
- added `--json` and `--no-log` flags to the CLI
- implemented standard exit code contract (0 for allow/warn/confirm, 1 for deny)

## Goal

Wrap the decision engine in a shell-friendly CLI and store useful audit logs.

## Deliverables

- executable CLI
- JSON and human-readable output modes
- append-only audit log
- exit code contract for allow, warn, and block outcomes

## Notes

- do not couple this to one agent provider
- keep logging format easy to search later
