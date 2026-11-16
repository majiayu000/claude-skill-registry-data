---
name: skill-evaluation
description: Evaluate whether a skill triggers correctly, follows its workflow, and produces useful evidence. Use when validating a new or changed skill before publication.
---

# Skill Evaluation

Evaluate the behavior, not just whether the Markdown parses.

1. Define the intended user task, expected trigger, expected output, and prohibited actions.
2. Create positive cases that should activate the skill and negative/near-miss cases that should not.
3. Run the same task with and without the skill when a suitable evaluation harness is available; compare correctness, omissions, unnecessary steps, and token/context overhead.
4. Check whether the instructions are actionable, internally consistent, tool-aware, and appropriately bounded.
5. Verify every bundled script in a safe test fixture. Inspect network calls, shell commands, permissions, file writes, and failure paths.
6. Check for semantic overlap with other skills and ambiguous routing descriptions.
7. Record model, harness, prompt cases, tool availability, results, and limitations so the evaluation can be reproduced.

Use a small human-reviewed rubric when an automated evaluator is unavailable. Do not treat one successful run as a benchmark. Report observed results separately from expected behavior and do not claim broad reliability without repeated evaluation.
