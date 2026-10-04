---
name: auto-optimize
description: >-
  Host-agnostic Agent Skill: double-layer workflow for AI-assisted delivery—requirement
  specification, multi-prompt outer loop, on-disk inner iterations, phase gates,
  optional byte-level verify. For any IDE, CLI, or Skill-capable tool (e.g. OpenClaw).
  Read program.md and docs/verifiability.md before editing delivery artifacts unless waived.
---

# Double-layer auto-optimization (Skill entry)

This file is the **Skill package entry** (`SKILL.md`). Normative text lives under `docs/`. **Not tied to a specific IDE**—any host that loads this Skill can use it.

## Strict execution (hard constraints)

- The agent **must** follow **`program.md`**, **`docs/verifiability.md`**, **`docs/phase-01-spec.md`** through **`phase-04-output.md`**, and **`docs/execution.md`** in full; **must not** shorten the workflow to save tokens, time, or because it “feels enough”.
- **Each** `tracks/prompt-*/` inner loop **must** satisfy **`docs/phase-03-inner.md`**: **gates** (e.g. at least **r01**, **r02** per scheme) and **main termination** (**all items checked** in **`tracks/phase-01-acceptance.md`**; or **5** rounds max). Self-score “≥8” **must not** alone justify stopping (**`verifiability.md` R3**). **Forbidden**: claiming a track is “deliverable” and moving to phase 4 before the acceptance checklist passes.
- **Forbidden**: using “reduce workload” or other **reasons not in the Skill** to deviate; **only** when the user **explicitly waives in the current turn** may the full workflow be skipped.

## Quick start (agent)

1. Read **[program.md](program.md)** (shortest path) or the checklist below; **do not skip** **[docs/verifiability.md](docs/verifiability.md)** (R1–R5).
2. Open phases in order: **`docs/phase-01-spec.md`** → **`phase-02-prompts.md`** → **`phase-03-inner.md`** → **`phase-04-output.md`**; read **[docs/execution.md](docs/execution.md)** for cost/order reminders.
3. **Before** phase 1 gates pass, do not rewrite delivery code; phase 1 **must** write **`tracks/phase-01-acceptance.md`** (**R3**); phase 2 **must** write **`tracks/phase-02-consistency-check.md`** (check + scheme–dimension table); **`r01` for `prompt-b`/`prompt-c` must not** be a full-page copy of `prompt-a`; waivers **must** be explicit in the **current** user message.
4. Before claiming delivery matches the final track file, in a class-A environment actually run **`scripts/skill-verify.sh`** from the **repository root** (see [program.md](program.md)).

## Execution checklist

```text
- [ ] Read docs/verifiability.md (R1–R5)
- [ ] Phase 1: spec written, feature list non-empty; tracks/phase-01-acceptance.md exists with ≥1 item
- [ ] Phase 2: outer prompts + consistency check; tracks/phase-02-consistency-check.md written (with table)
- [ ] Phase 3: each tracks/prompt-*/ has at least r01.* and r02.*; non-a r01 is independently generated
- [ ] Phase 4: compare & output; at least one track fully checked before final delivery (R3; self-score reference only)
- [ ] Delivery claim: ran skill-verify.sh and recorded command + output (R2/R4)
```

## Resource index

| Resource | Path |
|----------|------|
| Shortest entry | [program.md](program.md) |
| R1–R5 authority | [docs/verifiability.md](docs/verifiability.md) |
| Phases 1–4 | [docs/phase-01-spec.md](docs/phase-01-spec.md) etc. |
| Execution | [docs/execution.md](docs/execution.md) |
| Layout & verify | [reference.md](reference.md) |
| Example | [examples.md](examples.md) |
| Human guide | [SKILL-GUIDE.md](SKILL-GUIDE.md) |
| Script | `scripts/skill-verify.sh` (run from repo root) |

## User waiver

Must be **written in the current task message**, e.g.:

`This task waives the Skill / skips phases`

(Synonyms allowed if equally explicit; the agent **must not** infer a waiver.)

## High-risk domains

Does not replace regulation, clinical procedures, or human review; model self-scores and scripts are not sole safety evidence.
