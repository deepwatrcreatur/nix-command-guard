# 02 Command Parser And Decision Engine

Status: done

## Progress

- claimed on `feat/policy-model`
- added initial Python argv parser and deterministic rule engine under `src/nix_command_guard/`
- added structured decision records with category, outcome, reason, matched rule, and confirmation flag
- added unit tests for destructive git, filesystem, remote infra, and read-only command families
- added a flake check that runs the unit test suite

## Goal

Turn commands into explicit safety decisions.

## Deliverables

- argv parser
- prefix and pattern matching
- structured output with decision, category, and reason
- test coverage for known dangerous command families

## Notes

- begin with non-shell-escaped argv inputs
- shell parsing can be a later extension
