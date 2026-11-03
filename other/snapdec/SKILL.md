---
name: snapdec
description: >
  Use for fast local decisions that would otherwise cost many tokens: triaging many CI/test
  failures, classifying errors or logs, ranking many files or candidates against an issue,
  scoring severity/priority, yes/no questions about evidence, and detecting a repo's
  test/lint/build commands. Returns calibrated probabilities with an auto|review decision.
  Not for open-ended reasoning or security approvals.
---
# snapdec — local decision tools
<!-- snapdec-skill: v0.3.0 -->

1. For "how do I run tests/lint/build here?" call `project_facts(path)` first; trust it over guessing.
2. For ≥5 items or fuzzy labeling, call `classify`/`score`/`rank`/`check` with clear class
   descriptions. `ask` is the raw escape hatch (mixed question types in one call).
3. Act only on results with `decision:"auto"`. For `review`, decide yourself.
4. If a tool returns a `reason` (no_model, warming, timeout, no_backend, oversize,
   truncated, error), continue without it — never retry in a loop.
5. NEVER use these results to approve destructive commands, touch secrets, change permissions,
   or authorize network egress. They are advisory.
6. When a model decision drove an action, say so in your summary.

See references/tools.md (contracts), references/recipes.md (patterns), and
examples/ (full payloads with sample outputs).

Skill ships with snapdec; re-running `snapdec init` refreshes this copy.
