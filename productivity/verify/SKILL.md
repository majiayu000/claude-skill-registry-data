---
name: verify
owner: baseline
description: Contract document for the binding test verdict file at .claude/state/last_test_result. Format spec for callers (integrate, simplify, chore, the verify-tick worker) that inline the four mechanical operations. Not Skill-tool-invocable.
disable-model-invocation: true
---

# verify — contract document for the binding test verdict

This skill is not invocable. Its body is the canonical reference for the `.claude/state/last_test_result` statefile that the `verify_pass_guard` hook reads as the single source of truth.

Callers that previously did `Skill(verify)` (integrate, simplify, chore, the `verify-tick` worker invoked by harness after a `/tdd` decomposition) now inline the four mechanical operations described below. There is one statefile format; every caller writes the same bytes.

# Statefile format (`.claude/state/last_test_result`)

```
<PASS|FAIL>
<ISO-8601 UTC timestamp, e.g. 2026-05-12T18:30:00Z>
<exact command run, verbatim>
<exit code>
```

Exactly four lines plus a single trailing newline. No preamble, no blank lines, no JSON. The `verify_pass_guard` hook reads line 1 verbatim — anything that breaks the byte format breaks the gate.

# The four mechanical operations a caller performs

1. **Read the command.** Open `.claude/project.json`; extract `test.cmd`. If absent or empty, the verdict is `FAIL` with reason "project.json not configured — run /init-project"; skip step 2 and proceed to step 3 with exit code 1 and an empty command string.
2. **Run the command.** Execute via Bash from the project root. Capture stdout, stderr, and exit code. Do not retry. Do not pass `{file}` placeholders — verify always runs the full suite.
3. **Format the four lines.** Apply the verdict rules below to decide PASS vs FAIL. Build the four-line string in memory.
4. **Atomically write the statefile.** Write the four lines plus trailing newline to `.claude/state/last_test_result`. Prefer write-then-rename for atomicity when the writer needs guarantees; a direct overwrite is acceptable for non-concurrent callers (the four current callers are sequential).

# Verdict rules

- `PASS` iff **all** of: exit code 0 **and** at least one test executed **and** no test reported as failed/errored.
- `FAIL` otherwise. Specifically: non-zero exit, "0 tests collected", a panic/crash, a timeout (treat as FAIL), a killed process (FAIL), or output that contradicts the exit code (ambiguity is FAIL).
- If the same FAIL has stamped three or more consecutive times for the same slug, surface a recommendation that the caller invoke the `rca` skill. (The caller is responsible for noticing repeated failures; verify writes only the current verdict.)

# Inline report the caller emits

Callers emit a human-readable report alongside the statefile write (sent to stdout / surface, not to the statefile):

```
# Verify — <slug or task id>

## Verdict: PASS | FAIL

## Command
`<exact command>`

## Exit code
<N>

## Output tail (last 80 lines)
```
<raw>
```

## Reason (only if FAIL)
<one paragraph>
```

The report's role is human review; the statefile's role is the binding gate.

# verify_pass_guard interaction

`verify_pass_guard.sh` (PreToolUse on Write/Edit/MultiEdit) reads line 1 of `.claude/state/last_test_result`. When a caller attempts to write a PASS line to a verification artifact and line 1 of the statefile says FAIL, the guard blocks the write. Inlined callers MUST preserve the four-line byte format so the guard's parser keeps working.

# Constraints on inlined callers

- **Do not modify source or tests.** Inlined verify reads; it never writes outside `.claude/state/last_test_result`.
- **Do not retry the command.** One run, one verdict.
- **State-write discipline (binding — see `.claude/CONSTITUTION.md` §2 "State-write discipline").** `last_test_result` is **Tier 2 workflow state** — not a consent path. Prefer the **Write tool** for the four-line statefile (write-then-rename when atomicity is needed); if Bash is used, only a shell **builtin** redirect — never `tee` or `sed -i`. The byte format is what `verify_pass_guard` parses; the tool that writes it is the caller's choice within this rule.
- **Do not synthesize, summarize, or "clean up" test output.** Capture raw output for the report; the statefile records the verdict only.
- **A timeout is FAIL. A killed process is FAIL.**
- **The truth lives in the statefile.** The inline report is for the human; the hook trusts the four-line file.
