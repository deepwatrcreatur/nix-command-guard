# 04 Shell Wrapper And Audit Log

Status: ready

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
