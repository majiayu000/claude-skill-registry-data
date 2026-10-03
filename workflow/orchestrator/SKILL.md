---
skill_id: orchestrator
name: Orchestrator — Autonomous Workflow Standard (mxm-orchestrator)
description: "Author and run unattended autonomous workflows — \"workflow\", \"unattended\", \"run on a schedule\", \"automate this overnight\", \"set up an autonomous\", \"dry-run\". Mandatory budget guards, a separate verification gate, idempotency, and dry-run on by default."
version: 1.0.0
category: operational
office: coo
lead_agent: planner
governs: documents/ADRs/ADR-022-autonomous-workflow-standard.md
triggers:
  - "workflow"
  - "unattended"
  - "run on a schedule"
  - "automate this overnight"
  - "every day run"
  - "every hour run"
  - "set up an autonomous"
  - "dry-run"
  - "mxm-workflow"
collaborates_with:
  - planner               # owns orchestration; extends the `loops` skill
  - reviewer              # the independent verify() gate
  - tester                # test-as-verification workflows
  - security-analyst      # CSO auto-loop on any regulated/PII/data workflow
  - handoff-coordinator   # dead-letter + escalation → review queue
  - executive-router      # routes a workflow to its owning office
references:
  engine: orchestrator/engine.mjs
  acceptance_test: orchestrator/acceptance-test.mjs
  readme: orchestrator/README.md
  adr_workflow_standard: documents/ADRs/ADR-022-autonomous-workflow-standard.md
  adr_executable_contracts: documents/ADRs/ADR-002-documents-as-executable-contracts.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
  adr_office_dispatch: documents/ADRs/ADR-017-office-as-dispatch-boundary.md
  sibling_loops: .claude/skills/loops/SKILL.md
  sibling_scheduler: .claude/skills/usage-aware-scheduler/SKILL.md
confidence_default: 🟢 HIGH
---

# Orchestrator — Autonomous Workflow Standard (`mxm-orchestrator`)

> The governed home of **unattended** automation. A **workflow** is a process a trigger fires **without a human present** (schedule, file drop, webhook, queue event) — so budgets, a separate verification gate, and dry-run are **mandatory**, precisely because nobody is in the chair to stop a runaway. Governed by ADR-022.

> **Loops vs. Workflows — the one distinction that matters.** The `loops` skill governs **interactive, operator-present** iteration and is deliberately permissive about budgets ("don't invent a budget the operator didn't give"). This skill governs the **unattended** case and inverts that rule: every workflow carries hard budget guards. They compose — `mxm-orchestrator` extends `loops` and reuses its terminal-state vocabulary — but they are distinct contracts. If a human is watching → `loops`. If a trigger fires it unattended → a workflow.

---

## What this skill protects (the moat)

A scheduled run that over-spends, double-sends, or fails silently is the most expensive failure class in autonomous agents — and the one Maxim was least bounded against before ADR-022. This skill makes "Maxim ran something while you slept" a **safe** sentence: every unattended run is **bounded** (BudgetGuard hard-kill), **verified** (a separate gate before anything ships), **idempotent** (no double-anything), **dry-run by default**, and **fully logged** (one structured record per step). That is governed autonomy — the engineering substrate of the PaaS thesis.

Frameworks embodied (cited per ADR-007): **Feedback Control** (bounded observe→act→verify loop) · **Separation of Duties** (maker ≠ checker; `run()` never approves its own `output`) · **Fail-safe Defaults** (`dry_run` ON until go-live) · **Defense in Depth** (budget ∧ verify ∧ dry-run ∧ idempotency, independent layers) · **Exactly-Once / Idempotency** (re-fire is a no-op).

---

## The three layers (non-negotiable, ADR-022 §2)

Every workflow is exactly: **Trigger → Capable Agent(s) → Verification**. The verification layer is a *separate* gate (second-agent checker, rule validator, test suite, or human-review queue). **No unattended output reaches a human or goes live without passing verification.** A workflow with no `verify()` is rejected at registration time — the checker is written before the maker (ADR-002 Executable Contract).

---

## The `Workflow` contract

Author a workflow as a module exporting an object (or a factory returning one):

```js
{
  id,                          // stable, unique — the registry key
  trigger() => 'schedule'|'file'|'webhook'|'queue'|'manual',
  idempotency_key(context) => string|null,   // re-fire dedup key
  budget: { max_tokens, max_tool_calls, max_runtime_s, max_cost_usd },
  dry_run: true,               // DEFAULT ON until operator approves go-live
  async run(ctx) => output,    // the maker. ctx.charge('tokens'|'tool_calls'|'cost_usd', n) + ctx.tick()
  verify(output, ctx) => 'pass'|'fail'|'escalate',   // the SEPARATE gate (required)
  async commit(output, ctx) => sideEffect,           // the ONLY place a side-effect happens
}
```

The orchestrator runs `trigger → run → verify → (commit)` and enforces every guard. `commit()` fires **only** when `dry_run === false` **and** `verify()` returned `pass`. A `BudgetGuard` breach anywhere throws before `commit`, so a runaway never reaches the outside world.

**Terminal states** (reused from `loops`): `success` · `clean-no-op` (return `{noop:true}`) · `blocked` · `approval-required` (`verify` → `escalate`) · `exhausted` (budget breach) · `stagnated` · `failed`. **Never report `failed`/`exhausted`/`blocked` as `success`** (the `loops` cardinal rule).

---

## Mandatory per-run guards (ADR-022 §3)

| Guard | What it does | Where |
|---|---|---|
| **BudgetGuard** | `max_tokens / max_tool_calls / max_runtime_s / max_cost_usd` → **hard-kill** on breach → `exhausted` + dead-letter | `engine.mjs` |
| **StateStore** | run/step state + idempotency markers; a seen key → clean-no-op | `.mxm-skills/workflows/{runs,idempotency}/` |
| **Unified RunLog** | one JSON record per step | `.mxm-skills/runlog.jsonl` |
| **Dead-letter** | failed/exhausted runs land here with full context → review queue | `.mxm-skills/workflows/dead-letter/` |
| **Dry-run default ON** | no sends/trades/publishes/destructive writes unattended until go-live | per-workflow `dry_run` |

BudgetGuard **composes with** the `usage-aware-scheduler`: the scheduler throttles *when* work runs (OAuth usage %); BudgetGuard bounds *how much* a single run may consume. Both apply.

---

## The behavioral + governance overlay (on top, non-negotiable)

Every workflow inherits the Maxim overlay: **confidence tag** on each step + terminal state (ADR-010) · **framework citation** for the pattern it embodies (ADR-007) · **CSO auto-loop** — any regulated/PII/data workflow routes `security-analyst` into the verify gate; no secrets/PII into logs · **no-fabrication** — every rate carries its sample size.

---

## Authoring contract — the 10-section template (ADR-022 §3)

A workflow is registrable only with all ten, **verification first**: (1) "wrong output" definition · (2) trigger spec + idempotency key · (3) agent design (router/maker/checker tiers) · (4) budget guards (concrete numbers) · (5) verification logic (pass/fail/escalate thresholds) · (6) state + logging schema · (7) error & recovery (retry/backoff/dead-letter) · (8) runnable code (registered, `--dry-run` ON) · (9) deployment (trigger, secrets — request only) · (10) safety guardrails (what it must never do unattended). `/mxm-workflow new` scaffolds the skeleton.

---

## Activation & dispatch

| Trigger | Behavior |
|---|---|
| "automate X overnight" / "every day run Y" / "set up an autonomous Z" | `planner` scaffolds a workflow against this contract, routes per-run work to the owning office (ADR-017), registers it **dry-run ON** |
| A regulated/PII/data workflow | **CSO auto-loop fires** — `security-analyst` gates the verify step |
| Any workflow before go-live | runs in **dry-run**; operator reviews the dry-run RunLog, then explicitly approves `dry_run:false` |

Run directly: `node orchestrator/engine.mjs` is the library; `node orchestrator/acceptance-test.mjs` proves the guards. Surface command: **`/mxm-workflow`** (new · list · run · dry-run · go-live · logs).

---

## Acceptance test (prove the orchestrator before trusting it)

`orchestrator/acceptance-test.mjs` runs a no-op workflow that breaches each guard and asserts: clean hard-stop (`exhausted`) + dead-letter + log + **nothing external** on every breach; the happy path commits; dry-run skips the side-effect; an idempotent re-fire is a clean-no-op with no double-commit. **Status: 29/29 PASS (2026-06-26).** Re-run after any `engine.mjs` change — this is the gate (ADR-002 Executable Contract).

---

## References

- ADR-022 (Autonomous Workflow Standard) · ADR-002 (executable contracts) · ADR-007 (framework citation) · ADR-010 (confidence) · ADR-017 (office dispatch).
- Engine + test + docs: `orchestrator/engine.mjs` · `orchestrator/acceptance-test.mjs` · `orchestrator/README.md`.
- Siblings: `loops` (interactive iteration) · `usage-aware-scheduler` (throttle) · `handoff-coordinator` (escalation) · Proactive Watch (the standing read-only workflow exemplar).
