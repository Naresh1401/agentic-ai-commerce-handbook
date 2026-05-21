from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evals.contracts import DEFAULT_CASES, DEFAULT_POLICIES, GuardrailEvaluator


def main() -> None:
    evaluator = GuardrailEvaluator(DEFAULT_POLICIES)
    results = [evaluator.evaluate(case) for case in DEFAULT_CASES]
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        reasons = "; ".join(result.reasons) if result.reasons else "ok"
        print(f"{status} {result.case_name}: {reasons}")
    failed = [result for result in results if not result.passed]
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
