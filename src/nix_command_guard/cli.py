import argparse
import datetime
import json
import os
import sys
from pathlib import Path

from .engine import DecisionEngine, DecisionRecord
from .homelab import HOMELAB_RULES


def log_decision(decision: DecisionRecord) -> None:
    log_dir = Path("~/.cache/nix-command-guard").expanduser()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "audit.jsonl"
    
    entry = decision.as_dict()
    entry["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def print_human(decision: DecisionRecord) -> None:
    color = ""
    reset = "\033[0m"
    if decision.outcome == "deny":
        color = "\033[31m" # Red
    elif decision.outcome == "confirm":
        color = "\033[33m" # Yellow
    elif decision.outcome == "warn":
        color = "\033[33m" # Yellow
    elif decision.outcome == "allow":
        color = "\033[32m" # Green

    print(f"{color}Decision: {decision.outcome.upper()}{reset}")
    print(f"Category: {decision.category}")
    print(f"Reason:   {decision.reason}")
    if decision.matched_rule:
        print(f"Rule:     {decision.matched_rule}")


def main() -> int:
    parser = argparse.ArgumentParser(prog="nix-command-guard")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable text")
    parser.add_argument("--no-log", action="store_true", help="Disable audit logging")
    parser.add_argument("argv", nargs="+", help="The command line to evaluate")
    args = parser.parse_args()

    engine = DecisionEngine(HOMELAB_RULES)
    decision = engine.evaluate(args.argv)

    if not args.no_log:
        try:
            log_decision(decision)
        except Exception as exc:
            print(f"Warning: Failed to write audit log: {exc}", file=sys.stderr)

    if args.json:
        print(json.dumps(decision.as_dict(), indent=2))
    else:
        print_human(decision)

    if decision.outcome == "deny":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
