---
name: document-tests
description: User-invoked as /document-tests [path]. Documents every automated test under path (default tests/) - classifies each as Unit, Mock, Integration, or E2E and inserts a standardized Scenario/Boundaries/On-failure docstring via the document_tests.py codemod, then delegates flagged/ambiguous cases to the test-documenter agent. Use to bring an undocumented or partially-documented test suite up to a consistent standard.
allowed-tools: Read, Grep, Glob, Bash, Agent
invocation: /document-tests [path]
---

# Document Tests

Document every `test_*` function under `$ARGUMENTS` (default `tests/`) with a
standardized classification + Scenario/Boundaries/On-failure docstring.

**When resolving `Ambiguous classification` items** (step 2 below), use
[references/classification-guide.md](references/classification-guide.md) — it
gives the semantic Unit/Mock/Integration/E2E definitions the script cannot infer,
the resolution rules of thumb, and the exact docstring format (with a good/bad
example) the codemod emits.

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
   - a broken insertion shows up as a collection error, not a passing/failing
     test, so this check is cheap and catches it immediately.
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

If `--collect-only` fails, stop and hand the failure to `python-expert` before
re-running this skill - do not re-apply the codemod over a file that's already
broken. If the user wants hand-written docstrings standardized too, re-run
with the `test-documenter` agent and explicit permission to `--force` the
specific files named.

## Completion checklist

- [ ] `--check` preview run before any apply - counts, `Skipped`, and `Ambiguous` lists reviewed
- [ ] Every `Skipped (custom docstring present)` item left untouched, unless the user explicitly asked to `--force` that specific file
- [ ] Every `Ambiguous classification` item resolved by reading the actual test body - not left at the script's best-effort guess
- [ ] `pytest <path> --collect-only -q` run after apply and passed (no collection errors)
- [ ] Diff is docstrings only - no test logic, fixtures, assertions, or imports changed
- [ ] Classification counts, skipped list, and ambiguous resolutions all included in the final report
