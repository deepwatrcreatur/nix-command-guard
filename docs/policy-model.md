# Policy Model

## Core Outcome Types

- `allow`: command can execute without user confirmation
- `warn`: command is allowed but should surface risk context
- `confirm`: command requires an explicit user confirmation gate
- `deny`: command must not execute

## Decision Record

Each evaluation should return:

- `schema_version`
- `command`
- `argv`
- `category`
- `outcome`
- `reason`
- `matched_rule`
- `requires_confirmation`

## Initial Risk Categories

- `git_destructive`
- `filesystem_destructive`
- `remote_execution`
- `privilege_escalation`
- `infra_mutation`
- `network_data_exfiltration`
- `safe_read_only`

## Example Defaults

- `git reset --hard` -> `deny`
- `git push --force` -> `confirm`
- `rm -rf /tmp/some-known-worktree` -> `confirm`
- `rm -rf /` -> `deny`
- `ssh host sudo nixos-rebuild switch` -> `confirm`
- `rg pattern .` -> `allow`
