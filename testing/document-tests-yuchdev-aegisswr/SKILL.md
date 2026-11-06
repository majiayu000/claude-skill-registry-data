---
name: document-tests
description: User-invoked as /document-tests [path]. Documents every automated test under path (default tests/) - classifies each as Unit, Mock, Integration, or E2E and inserts a standardized Scenario/Boundaries/On-failure docstring via the document_tests.py codemod, then delegates flagged/ambiguous cases to the test-documenter agent. Use to bring an undocumented or partially-documented test suite up to a consistent standard.
allowed-tools: Read, Grep, Glob, Bash, Agent
invocation: /document-tests [path]
# Ported from Claude (.claude/skills/document-tests/SKILL.md) on 2026-07-03
---

# Document Tests

Document every `test_*` function under `$ARGUMENTS` (default `tests/`) with a
standardized classification + Scenario/Boundaries/On-failure docstring.

**When resolving `Ambiguous classification` items** (step 2 below), use
`.github/copilot/skills/document-tests/references/classification-guide.md` — it
gives the semantic Unit/Mock/Integration/E2E definitions the script cannot infer,
the resolution rules of thumb, and the exact docstring format.

## Steps

1. **Preview**: `python scripts/document_tests.py $ARGUMENTS --check`
   Read the summary: total tests, classification counts, any `Skipped (custom
   docstring present)` and `Ambiguous classification` lists.
2. **Decide whether the agent is needed**:
   - If there are zero `Skipped` and zero `Ambiguous` entries, the change is
     purely mechanical - apply directly: `python scripts/document_tests.py $ARGUMENTS`.
   - Otherwise, spawn the **`test-documenter`** agent with the target path and
     the preview output. It applies the script, then hand-resolves every
     `Ambiguous` item by reading the test body, and leaves every `Skipped`
     (custom docstring) item untouched unless the user asked to standardize
     that specific file.
3. **Verify no regressions**: `uv run pytest $ARGUMENTS --collect-only -q`
4. Report the summary the agent (or the direct script run) produced.

## Output

```
## Test Documentation - <path>
Scanned: N files, M tests
[Unit] a  [Mock] b  [Integration] c  [E2E] d
Documented: X new/updated
Skipped (custom docstring, left as-is): <list, or none>
Ambiguous - resolved: <file::test -> classification>
Verification: pytest <path> --collect-only -> <pass/fail>
```

## Completion checklist

- [ ] `--check` preview run before any apply
- [ ] Every `Skipped (custom docstring present)` item left untouched unless explicitly asked to `--force`
- [ ] Every `Ambiguous classification` item resolved by reading the actual test body
- [ ] `pytest <path> --collect-only -q` run after apply and passed
- [ ] Diff is docstrings only - no test logic changed
