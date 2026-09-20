"""
Demo CI failure scenarios for dependency remediation orchestrator presentation.

This test provides controlled failure scenarios to demonstrate:
1. Bounded repair success (Devin fixes the issue on retry)
2. Escalation to human (Devin cannot fix)
"""
import os


def test_demo_ci_failure_markers():
    """
    Demo test that fails based on temporary markers in README.md
    
    Scenarios:
    - TEMP_FAILURE_FIRST: Fails first attempt, Devin should remove marker
    - TEMP_FAILURE_ALWAYS: Always fails, requires human intervention
    """
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    with open(readme_path, "r") as f:
        content = f.read()
    
    if "TEMP_FAILURE_FIRST" in content:
        raise AssertionError(
            "First attempt failure - Devin should remove TEMP_FAILURE_FIRST marker "
            "on bounded repair attempt. This demonstrates the bounded retry logic."
        )
    
    if "TEMP_FAILURE_ALWAYS" in content:
        raise AssertionError(
            "Permanent failure - requires human intervention. "
            "This demonstrates escalation to 'needs_human' state when "
            "bounded repair attempts are exhausted."
        )


if __name__ == "__main__":
    test_demo_ci_failure_markers()
