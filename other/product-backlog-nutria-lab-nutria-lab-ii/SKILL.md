---
name: product-backlog
description: "Trigger: user story, acceptance criteria, backlog refinement, epic, priority. Create testable NutrIA product work."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use to turn product requests into Linear issues.

# Hard Rules
- Each issue has a user outcome, non-goals, acceptance criteria and UX states.
- Keep clinical advice outside the product scope.
- Do not split work by frontend/backend alone; split by user value and verifiable increment.

# Execution Steps
1. Map request to NutrIA epic.
2. Write a concise story and measurable acceptance criteria.
3. Add failure, empty, loading and restricted-input cases.
4. Identify dependencies and QA evidence.

# Output Contract
Return a ready-to-review Linear issue draft, not an unapproved issue mutation.
