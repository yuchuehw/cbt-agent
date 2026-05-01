#!/usr/bin/env python3
"""
Import verification script - Tests all imports to ensure they work correctly.
Run this to verify the project structure is correct before running main.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("CBT-Agent Import Verification")
print("=" * 60)

tests = []

# Test 1: Agent imports
try:
    from cbt_agent.agents.cbt_agent import CbtAgent
    tests.append(("✅", "CbtAgent", "from cbt_agent.agents.cbt_agent"))
except ImportError as e:
    tests.append(("❌", "CbtAgent", str(e)))

# Test 2: Policy engine
try:
    from cbt_agent.guardrails.policy_engine import load_policy
    tests.append(("✅", "load_policy", "from cbt_agent.guardrails.policy_engine"))
except ImportError as e:
    tests.append(("❌", "load_policy", str(e)))

# Test 3: Input router
try:
    from cbt_agent.runtime.input_router import parse_input
    tests.append(("✅", "parse_input", "from cbt_agent.runtime.input_router"))
except ImportError as e:
    tests.append(("❌", "parse_input", str(e)))

# Test 4: Tool router
try:
    from cbt_agent.runtime.tool_router import route_tool_call
    tests.append(("✅", "route_tool_call", "from cbt_agent.runtime.tool_router"))
except ImportError as e:
    tests.append(("❌", "route_tool_call", str(e)))

# Test 5: Agent loop
try:
    from cbt_agent.runtime.agent_loop import run_agent
    tests.append(("✅", "run_agent", "from cbt_agent.runtime.agent_loop"))
except ImportError as e:
    tests.append(("❌", "run_agent", str(e)))

# Test 6: Message schemas
try:
    from cbt_agent.runtime.message_schemas import AgentResponse
    tests.append(("✅", "AgentResponse", "from cbt_agent.runtime.message_schemas"))
except ImportError as e:
    tests.append(("❌", "AgentResponse", str(e)))

# Test 7: Memory system
try:
    from cbt_agent.memory import MemoryManager
    tests.append(("✅", "MemoryManager", "from cbt_agent.memory"))
except ImportError as e:
    tests.append(("❌", "MemoryManager", str(e)))

# Test 8: Crisis detector
try:
    from cbt_agent.guardrails.crisis_detector import detect_crisis
    tests.append(("✅", "detect_crisis", "from cbt_agent.guardrails.crisis_detector"))
except ImportError as e:
    tests.append(("❌", "detect_crisis", str(e)))

# Test 9: Validators
try:
    from cbt_agent.guardrails.validators import validate
    tests.append(("✅", "validate", "from cbt_agent.guardrails.validators"))
except ImportError as e:
    tests.append(("❌", "validate", str(e)))

# Test 10: Safety tools
try:
    from cbt_agent.tools.safety_tools import build_crisis_response
    tests.append(("✅", "build_crisis_response", "from cbt_agent.tools.safety_tools"))
except ImportError as e:
    tests.append(("❌", "build_crisis_response", str(e)))

# Test 11: Therapist tools
try:
    from cbt_agent.tools.therapist_tools import suggest_cbt_exercise
    tests.append(("✅", "suggest_cbt_exercise", "from cbt_agent.tools.therapist_tools"))
except ImportError as e:
    tests.append(("❌", "suggest_cbt_exercise", str(e)))

# Print results
print("\nImport Test Results:\n")
for status, name, path in tests:
    print(f"{status} {name:25} {path}")

# Summary
passed = sum(1 for status, _, _ in tests if status == "✅")
total = len(tests)

print("\n" + "=" * 60)
print(f"Result: {passed}/{total} imports successful")
print("=" * 60)

if passed == total:
    print("\n✅ All imports working! Ready to run: python main.py")
    sys.exit(0)
else:
    print(f"\n❌ {total - passed} import(s) failed. See errors above.")
    sys.exit(1)

