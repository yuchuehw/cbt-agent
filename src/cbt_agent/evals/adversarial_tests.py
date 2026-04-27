from __future__ import annotations

import json
from pathlib import Path

from runtime.agent_loop import run_agent


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "evals" / "test_conversations.jsonl"


def run_eval() -> int:
    passed = 0
    total = 0
    failed = 0

    with DATA_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue

            case = json.loads(line)
            response = run_agent(case["user"], conversation_state={"history": []})
            total += 1
            case_failed = False

            if response.meta.get("mode") == case["expected_mode"]:
                pass
            else:
                case_failed = True
                print(
                    f"FAILED {case['id']}: expected mode {case['expected_mode']} "
                    f"but got {response.meta.get('mode')}"
                )

            lowered_response = response.text.lower()
            banned_terms = [item.lower() for item in case.get("must_not_contain", [])]
            if any(term in lowered_response for term in banned_terms):
                case_failed = True
                print(f"FAILED {case['id']}: response contains banned phrase")

            required_any = [item.lower() for item in case.get("must_contain_any", [])]
            if required_any and not any(term in lowered_response for term in required_any):
                case_failed = True
                print(f"FAILED {case['id']}: response missing required phrase set")

            mhealth_eval = response.meta.get("mhealth_eval", {})
            min_appropriateness = int(case.get("min_appropriateness", 0))
            if int(mhealth_eval.get("appropriateness_score", 0)) < min_appropriateness:
                case_failed = True
                print(f"FAILED {case['id']}: appropriateness below minimum")

            max_trust_flags = int(case.get("max_trust_flags", 99))
            trust_flags = mhealth_eval.get("trustworthiness_flags", [])
            if len(trust_flags) > max_trust_flags:
                case_failed = True
                print(f"FAILED {case['id']}: trustworthiness flags exceeded limit")

            max_safety_flags = int(case.get("max_safety_flags", 99))
            safety_flags = mhealth_eval.get("safety_flags", [])
            if len(safety_flags) > max_safety_flags:
                case_failed = True
                print(f"FAILED {case['id']}: safety flags exceeded limit")

            if case_failed:
                failed += 1
            else:
                passed += 1

    print(f"Eval result: {passed}/{total} passed, {failed} failed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(run_eval())

