---
name: adr-check
description: Run ADR conformance checks, explain failures, and identify required ADR/doc updates for the current change.
---

# ADR Check

Use this skill when the change touches architecture, workflows, hooks, shared contracts, or guardrail files.

## Steps

1. Identify changed files:

```bash
git diff --name-only HEAD
```

2. Run the fast ADR guard on changed files:

```bash
python3 scripts/adr_guard/adr_guard.py --changed --level fast
```

3. If the fast guard fails:
   - Report the exact rule ids and files.
   - Fix the code or docs.
   - Re-run the guard.

4. If guardrail files changed, verify that one of these changed too:
   - `docs/adr/**`
   - `shifter/shifter_platform/documentation/docs/technical/dev/adr-enforcement.md`
   - technical index pages linking to ADR enforcement docs

5. If a temporary waiver is genuinely required:
   - add it to `docs/adr/exceptions.yaml`
   - include `rule_id`, `owner`, `reason`, and `expires_on`
   - keep the waiver as narrow as possible with `checks` and `paths`

6. Before completion, run the CI profile:

```bash
python3 scripts/adr_guard/adr_guard.py --all --level ci
```

## Output

Report:

- checks run
- violations found or “ADR guard clean”
- ADR/doc files updated
- any exception added and its expiry
