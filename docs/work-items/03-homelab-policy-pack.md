# 03 Homelab Policy Pack

Status: done

## Progress

- implemented `src/nix_command_guard/homelab.py` with 13 initial rules
- added `git_destructive`, `filesystem_destructive`, `privilege_escalation`, `remote_execution`, `infra_mutation`, and `safe_read_only` rule families
- added `src/nix_command_guard/cli.py` for testing and evaluation

## Goal

Provide a policy pack tuned to the kinds of commands used in your Nix and homelab repos.

## Deliverables

- conservative defaults for destructive git operations
- protections for broad `rm` and path-sensitive deletes
- rules for `sudo`, `ssh`, `nixos-rebuild`, and related host-impacting commands
- policy examples for temporary exceptions

## Notes

- assume a mixed local-plus-remote admin environment
- err on the side of confirm over allow
