---
name: policy-runner
description: Run policy-as-code checks (e.g., OPA/Conftest) based on the policy_plan. Use in Flow 2 and Flow 4.
allowed-tools: Bash, Read
---

# Policy Runner Skill

You are a helper for running policy-as-code checks. If no policies are configured,
report that no policy checks are wired for this change.

## Behavior

1. If `policy_plan.md` exists, read it to discover which policies and paths to evaluate.

2. For each configured policy entry:
   - If an explicit command is listed (e.g., `conftest test <path>` or `opa eval ...`), run it.
   - Otherwise, if a policy file/rego path is provided, return a message that this policy is planned but not auto-executed.

3. Output artifacts:
   - Save raw runner output to `policy_runner_output.log`.
   - Write `policy_runner_summary.md` summarizing checks run, passed, failed, and planned-only policies.

4. Do not modify policy files or code.

