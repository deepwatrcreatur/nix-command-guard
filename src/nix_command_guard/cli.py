import argparse
import json
import sys

from .engine import DecisionEngine
from .homelab import HOMELAB_RULES


def main() -> int:
    parser = argparse.ArgumentParser(prog="nix-command-guard")
    parser.add_argument("argv", nargs="+", help="The command line to evaluate")
    args = parser.parse_args()

    engine = DecisionEngine(HOMELAB_RULES)
    decision = engine.evaluate(args.argv)

    print(json.dumps(decision.as_dict(), indent=2))

    if decision.outcome == "deny":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
