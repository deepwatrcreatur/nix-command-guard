# Agent Prompts

## Prompt 1

Design the policy model and risk categories.

Requirements:
- map commands into deny, warn, confirm, and allow outcomes
- make policy data-driven
- include rationale fields so agents can explain decisions

## Prompt 2

Build the parser and decision engine.

Requirements:
- parse argv rather than raw shell strings where possible
- support prefix-based and pattern-based rules
- return structured decision output

## Prompt 3

Create the homelab policy pack.

Requirements:
- cover destructive git commands
- cover dangerous filesystem operations
- cover remote execution and infra-impacting commands
- keep exceptions explicit and reviewable
