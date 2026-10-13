---
name: auditing-logic
description: >
  Audits code for logical errors before they become bugs — control flow gaps,
  data contract violations, schema/type drift, business logic inconsistencies,
  and silent failure paths. Produces a severity-rated issue list with a one-line
  diagnosis and one-line fix per finding. Use this skill whenever code is pasted
  with a review request, or when the user says "audit this", "check the logic",
  "does this make sense", "any issues with this", "logic audit", "what's wrong
  here", "review this function", "is this correct", or hands you any code file
  and wants a critical eye. Even if the user does not say "logic" — if code is
  present and they want feedback, use this skill. Also triggers on: "find the
  bug", "something feels off", "is this right", "sanity check this", "does this
  hold", "validate my logic", "code review", "PR review", "review this PR".
metadata:
  version: "1.1.0"
---

# Auditing Logic

Audits code for five classes of logical defect. Does NOT review style, naming,
formatting, or architecture. Stays focused on: does this do what the developer
thinks it does?

---

## Scope Gate

Before running passes, assess scope:

| Scope | Guidance |
|-------|----------|
| ≤ 3 files / ≤ 300 LOC | Full five-pass audit on all code |
| 4–10 files / 300–1000 LOC | Full audit; group findings by file; emit cross-file section last |
| > 10 files / > 1000 LOC | Ask: "This is a large surface — which file or subsystem is highest priority?" Audit that first, then ask whether to continue. |

If scope is ambiguous (no file count given), proceed and note at the top:
`Auditing provided excerpt only — findings may not reflect full codebase state.`

---

## REQUIRED OUTPUT SCHEMA

Every audit response must contain these sections in this order.

**FINDINGS**
One bullet per finding:

- `[CRITICAL|HIGH|MEDIUM|LOW]` `file:line` — one-line diagnosis. **Fix:** one-line action (imperative verb first).

Never group findings. Every finding gets an individual severity label.

**SUMMARY**

- Severity counts: X critical, X high, X medium, X low
- Most dangerous finding: [one sentence]
- Fix effort: quick (<1hr) / medium (1–4hr) / involved (>4hr)

**SELF-REVIEW**
State what the self-review pass caught, or: "Self-review: no additional findings." Do not skip this section.

---

## Audit Passes

Run all five passes on every audit. Skip a pass only if it provably does not
apply. State skipped passes once.

### Pass 1 — Control Flow
- Branches that can never be reached
- Missing `else`/`default` in exhaustive-looking conditionals
- Async functions with unhandled rejection paths
- Early returns that leave callers with `undefined`/`None` when they expect a value
- Loops that can execute zero times when the caller assumes at least one
- Guard clauses that check the wrong condition (inverted logic)

### Pass 2 — Data Contracts
- Function return type vs what callers actually receive
- Optional chaining (`?.`) or None-safe access masking a null that should be an error
- Type assertions (`as X` / `cast()`) papering over a narrowing gap
- Inputs that pass validation but produce invalid downstream state
- Discriminated union / `Literal` type exhaustiveness — is every variant handled?
- Parameters accepted but never used (silent contract lie)
- Missing null/None checks before property access on values that can be absent

### Pass 3 — Schema / Type Drift

**Apply the relevant sub-pass for the language in scope. Skip and state why if none apply.**

**TypeScript / Zod:**
- Zod schema shape that doesn't match its corresponding TypeScript type
- `.strict()` schemas paired with types that allow extra keys (or vice versa)
- Schema `.default()` values that conflict with the interface default
- `z.infer<>` used downstream as authoritative when the schema is narrower than the type
- Runtime validation that passes for values the type system would reject (or vice versa)

**Python / Pydantic:**
- Model field types that diverge from actual usage (e.g., `Optional` field accessed without a guard)
- `model_validate()` called on data that hasn't been sanitized to match field constraints
- `Field(default=...)` values that conflict with caller assumptions
- `model_config` settings (e.g., `extra='ignore'`) silently dropping fields callers expect to survive
- `@validator` / `@field_validator` that passes but downstream code assumes stricter invariants

**Other languages / no schema library:**
Skip and emit: `Pass 3 skipped — no runtime schema/validation library detected.`

### Pass 4 — Business Logic Consistency
- Constants that reference each other but aren't derived — can silently drift
- Constraint sets that should be subsets/supersets of each other but aren't enforced
- State/phase transitions validated in one place but assumed valid elsewhere
- Lookup tables where the key space isn't guaranteed to match the type
- Lists where the same entity appears in logically conflicting positions

### Pass 5 — Silent Failures
- Errors caught and swallowed (`catch {}` / bare `except:` / `except Exception: pass`)
- Logging as the only signal — caller gets no indication something failed
- Functions that return a success shape containing partial/stale data
- Mutation of shared state inside what appears to be a pure function
- Missing teardown in resource acquisition paths (file handles, connections, locks)

---

## Context Escalation

When a finding depends on behavior you cannot see:

- **Flag and continue** (LOW or MEDIUM) if the gap is speculative:
  `Requires visibility into [X] to confirm.`
- **Ask the user** if the gap is structural and would change severity:
  `I need to see [X] to determine if this is HIGH or CRITICAL — can you paste it?`

Ask once per audit, max. If multiple findings need external context, batch:
`To fully assess N findings, I need: [list].`

---

## Output Format

Emit a severity-rated issue list. Never pad with "this looks good" between
findings. If a pass is clean, state it once and move on.

### Clean Pass (inline)
```
Pass N — Label: No findings.
```

### Severity Ratings

| Level    | Meaning |
|----------|---------|
| CRITICAL | Will produce wrong behavior at runtime; data loss or incorrect state likely |
| HIGH     | Logic gap that surfaces under realistic inputs |
| MEDIUM   | Inconsistency that becomes a bug as the codebase grows |
| LOW      | Latent fragility — won't bite now but creates risk |

### Per-Issue Format

```
[SEVERITY] Pass N — Label
Location: file.ts → functionName() (line N if available)
Diagnosis: One sentence — what is wrong and why.
Fix: One sentence or minimal code snippet showing the correction.
```

### Cross-File Root Cause Format

When the same root cause produces findings in multiple files, log once at the
root location. Do not duplicate per-file:

```
[SEVERITY] Pass N — Label  ⬡ ROOT CAUSE
Root: file-a.ts → sourceOfTruth()
Surfaces in:
  - file-b.ts → consumerA() — one-line description of how it manifests here
  - file-c.ts → consumerB() — one-line description of how it manifests here
Diagnosis: One sentence describing the shared underlying defect.
Fix: One sentence fixing the root. Surface findings resolve automatically.
```

**Use this pattern when:**
- Two or more findings share the exact same fix
- Fixing one location eliminates the others automatically
- The root is a shared constant, derived value, or data source

**Do NOT use when:**
- Findings are related in theme but require independent fixes
- Files have different owners or change at different rates

### Summary Block (end of audit)

```
AUDIT SUMMARY
─────────────
Critical: N  High: N  Medium: N  Low: N
Total: N issues across N passes
Root cause clusters: N  (N surface findings consolidated)   ← omit if none
Passes skipped: [list] — [reason]                           ← omit if none
```

### Clean Audit (zero findings across all passes)

```
AUDIT SUMMARY
─────────────
No logical defects found across all applicable passes.
Passes run: 1, 2, 3 (variant), 4, 5
Passes skipped: [list] — [reason]

[Note any caveats — e.g., "External function behavior assumed correct where
implementation was not provided."]
```

---

## Adversarial Check (run before finalizing)

Before emitting the summary, ask yourself:
1. Did I miss any implicit assumption the developer is relying on?
2. Is there a happy-path test that passes but an edge-case input that breaks the logic?
3. Did I flag any style issues instead of logic issues? Remove them.
4. Are any findings actually the same root cause? Consolidate before emitting.
5. Did I duplicate a finding across passes (e.g., null check in both Pass 2 and Pass 5)? Remove the duplicate — keep the finding in the pass where it most precisely belongs.

---

## Constraints

- Do not suggest refactors, renames, or architectural changes — only logic defects.
- If a finding requires external context, apply Context Escalation rules above.
- If the user provides a file path without content, ask for the code.
- For multi-file audits: group findings by file with a per-file sub-header, then
  emit cross-file root causes as a separate section after all per-file findings.

---

## Example Findings

**Single-file finding:**
```
[HIGH] Pass 2 — Unused parameter silently degrades contract
Location: raci-chart.ts → validatePhaseTransition()
Diagnosis: _targetPhase is accepted but never used — the function validates
  current-phase deliverables regardless of destination, so Build→Discovery
  passes if Build deliverables are complete.
Fix: Derive required deliverables from targetPhase entry criteria, or remove
  the parameter and document that only source-phase completion is checked.
```

**Cross-file root cause:**
```
[HIGH] Pass 4 — allowedPhases manually curated; drifts from RACI chart  ⬡ ROOT CAUSE
Root: role-matrix.ts → ROLE_CONSTRAINTS
Surfaces in:
  - role-tools.ts → ff_invoke_persona() — phase gate passes but RACI returns null
  - raci-tools.ts → ff_get_raci_position() — position lookup disagrees with gate result
Diagnosis: allowedPhases is hardcoded independently of RACI_CHART — the two
  sources can contradict each other silently as roles are modified.
Fix: Derive allowedPhases at startup from RACI_CHART so any phase where the
  role appears in R/A/C/I is automatically allowed.
```

**Clean audit:**
```
AUDIT SUMMARY
─────────────
No logical defects found across all applicable passes.
Passes run: 1, 2, 4, 5
Passes skipped: 3 — no runtime schema/validation library detected in provided code.
```
