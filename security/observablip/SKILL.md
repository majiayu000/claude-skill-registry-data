---
name: observablip
description: Audits source code for observability gaps — missing telemetry, poor observability practices, and code structure that resists instrumentation — then emits a ranked, bounded finding list. Invoke when the user says "observablip this", "observablip `pkg/foo`", "audit observability", "review telemetry", "find missing spans", "audit o11y on this PR", "review my logging", or "is this instrumented well enough?". Read-only; never edits files.
license: MIT
compatibility: Designed for Claude Code (or similar agentskills.io-compatible clients).
---

# observablip

Audits source files for observability gaps across three dimensions —
missing telemetry, poor practices, and code structure that resists
instrumentation. Output is a ranked, bounded finding list. Never edit
files in the target codebase.

## Install

```bash
npx skills add xornivore/skills@observablip --agent claude-code -y
```

## When to use

Invoke when the user:

- Uses an explicit invocation phrase: "observablip this",
  "observablip `pkg/foo`", "audit o11y on this PR".
- Asks for an observability or telemetry review: "audit observability",
  "review telemetry", "find missing spans", "review my logging".
- Asks a diagnostic question: "is this instrumented well enough?"

Do not invoke for:

- Requests to write or apply telemetry — observablip is read-only.
- Security review, performance review, correctness review, or test
  coverage review.
- Vendor selection ("should I use Datadog or Honeycomb?").
- Audits from runtime data (traces, logs, metrics dumps). observablip
  reads source files only.

## Hard rules

1. **Read-only.** Never edit files in the target codebase. Never
   execute target code. Never run shell commands inside the target.
   **Audit:** no `Edit` / `Write` / `Bash` tool calls touching paths
   inside the target during a run.

2. **No author attribution.** Findings name behaviors, not authors.
   Never use `git blame` to attribute. Never include usernames, emails,
   or handles in findings. **Audit:** `grep -E '@[a-zA-Z0-9_-]+|<[^>]+@[^>]+>'`
   over emitted findings returns nothing.

3. **No verbatim secrets/PII.** A finding referencing a log call with
   sensitive data describes the shape (`a log call passes a raw email
   field`) and never quotes the line verbatim. **Audit:** findings must
   not contain string literals matching the regex set in
   [poor-practices](./references/poor-practices.md) (basic email, JWT,
   bearer-token shapes).

4. **Bounded output.** Default cap 20 findings; overflow surfaces with
   a count and a "narrow the target" prompt. Never silently truncate.
   **Audit:** if `len(findings) > --max`, emitted output contains the
   string `narrow the target`.

5. **Skipped files are explained.** Every excluded file is counted in
   the footer aggregate under one of the fixed reason words from
   [precheck](./references/precheck.md). Never silently exclude.
   **Audit:** `scanned` + `skipped` in the footer equals the resolved
   file count from step 4.1.

6. **No library prescription unless detected.** If the codebase imports
   OTel / slog / zap / structlog, suggestions use that vocabulary.
   Otherwise stay neutral ("a span", "a structured log") — never push
   a specific library. **Audit:** for each finding, the suggestion's
   library tokens (`otel`, `slog`, `zap`, `structlog`, etc.) must
   appear somewhere in the file set's imports — or the suggestion uses
   neutral vocabulary only.

## Reference index

The action-checklist steps below (1–5) correspond to spec sections 4.1–4.5. Reference files refer to step numbers in the 4.x form; treat checklist step N as spec step 4.N.

Read each reference only at the action step that loads it. Each
reference ends with an `## Action checklist` — load and jump there.

- [precheck](./references/precheck.md) — observable-surface-area
  criteria and skip categories. Load at step 4.2 (per-file precheck).
- [missing-telemetry](./references/missing-telemetry.md) — rubric
  dimension 1. Load at step 4.3 dim 1.
- [poor-practices](./references/poor-practices.md) — rubric dimension
  2 and secret/PII regex set. Load at step 4.3 dim 2.
- [structure-for-telemetry](./references/structure-for-telemetry.md)
  — rubric dimension 3. Load at step 4.3 dim 3.
- [false-positive-review](./references/false-positive-review.md) — FP
  pass rubric. Load at step 4.4.
- [output-schema](./references/output-schema.md) — finding fields,
  ranking, and footer format. Load at step 4.5 (rank and emit).

The per-finding render template lives at `assets/finding-template.md`,
loaded at the emit substep of step 4.5.

## Top-level action checklist (when invoked)

1. **Resolve target.** Expand the path/glob (or `--diff` rev range)
   to a concrete file set. If the count exceeds 200, halt with a
   "narrow the target" prompt — never partially scan.

2. **Per-file precheck.** Load [precheck](./references/precheck.md).
   For each file, apply the pass criteria; assign a skip reason from
   the fixed set if it fails. Record the rejection log for the footer.

3. **Apply rubric.** For each surviving file:

   1. Load [missing-telemetry](./references/missing-telemetry.md);
      produce candidate findings for dimension 1.
   2. Load [poor-practices](./references/poor-practices.md); produce
      candidates for dimension 2. Apply the secret/PII redaction rule
      before queueing each candidate.
   3. Load [structure-for-telemetry](./references/structure-for-telemetry.md);
      produce candidates for dimension 3.

4. **False-positive review.** Load
   [false-positive-review](./references/false-positive-review.md). Run
   every candidate through checks 1–4 in order; drop on first match;
   increment `n_fp_dropped`.

5. **Rank and emit.** Load [output-schema](./references/output-schema.md).
   Rank surviving findings; render each through
   `assets/finding-template.md`; emit the footer block. If candidate
   count exceeds `--max`, render only the top `--max` and append the
   overflow note.
