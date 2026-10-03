---
skill_id: loops
name: Loops — Bounded Agent Loop Orchestration
description: "Run a bounded, governed iteration — \"loop\", \"iterate until\", \"keep going until\", \"sweep\", \"ratchet\", \"until it passes\", \"coverage to 100\". Turns an open-ended autonomous run into a finite loop with checkpoints and explicit stopping conditions."
version: 1.0.0
category: operational
office: coo
lead_agent: planner
triggers:
  - "loop"
  - "iterate until"
  - "keep going until"
  - "run the X loop"
  - "sweep"
  - "ratchet"
  - "until it passes"
  - "fresh-clone"
  - "production error sweep"
  - "coverage to 100"
  - "champion challenger"
collaborates_with:
  - executive-router      # routes a loop to its owning office
  - planner               # owns loop orchestration + stopping conditions
  - reviewer              # independent verification pass (generation != approval)
  - tester                # coverage / quality-streak / test-speed loops
  - security-analyst      # CSO auto-loop on any regulated/PII/data loop
  - sre-analyst           # production error sweep / baseline loops
references:
  prior_art_loop_library: "Forward-Future/loop-library (31 loops, explicit stopping conditions)"
  prior_art_autonomy_loop: "inferencegod/autonomy-loop (deterministic fail-closed verification gates)"
  adr_executable_contracts: documents/ADRs/ADR-002-documents-as-executable-contracts.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
  adr_office_dispatch: documents/ADRs/ADR-017-office-as-dispatch-boundary.md
confidence_default: 🟢 HIGH
---

# Loops — Bounded Agent Loop Orchestration

> A **loop** is a bounded feedback process (observe → choose → act → verify → record → repeat-or-stop) run over Maxim's existing offices/agents, with an **explicit stopping condition** and a **named terminal state**. This skill is the loop layer ON TOP of the office/command dispatch — it does not replace any command.
> Prior art: loop-library (the 31-loop catalog) and autonomy-loop (deterministic verification gates), both cited per ADR-007. Maxim adds the behavioral overlay: confidence tagging, framework citation, CSO auto-loop on regulated loops, and the no-fabrication rule.

---

## Skill Purpose

Turn "do X repeatedly until it's right" from an open-ended autonomous run into a **governed, finite loop** with checkpoints and a defined stop. Maxim already owns the verbs (`/mxm-build`, `/mxm-fix`, `/mxm-review`, `/mxm-test`, `/mxm-ship`) and the offices; a loop orchestrates those against a stopping condition. The moat this skill protects: **a Maxim loop never reports an error, a stall, or an exhausted budget as success** — the confidence-tagging ethos (ADR-010) applied to iteration.

---

## The Bounded-Loop Discipline (non-negotiable)

Every loop MUST declare, up front:

1. **Trigger** — what starts it (a command, a schedule, a backlog, a symptom).
2. **Stopping condition** — a *rubric, threshold, benchmark, reviewer decision, or finite scenario set* — never "until it looks good." If the operator gave no limit, use a **no-progress stop**; do NOT invent time/iteration/cost budgets.
3. **Checkpoint** — what is verified each iteration before continuing.
4. **Terminal state** — name it on exit: `success` · `clean no-op` (nothing to do) · `blocked` (dependency/permission) · `approval-required` (human gate) · `exhausted` (budget hit) · `stagnated` (no progress N rounds).

**Hard rule:** never report `error`, `blocked`, `exhausted`, or `stagnated` as `success`. Tag the exit state honestly (ADR-010). A loop that both produces and verifies its own work MUST run an **independent verification** pass (a separate `reviewer` invocation) — generation ≠ approval.

---

## Activation & Dispatch

| Trigger | Behavior |
|---|---|
| "run the `<name>` loop" / "iterate until X" | `planner` composes the loop, routes the per-iteration work to the owning office (ADR-017), enforces the stopping condition + checkpoints |
| A regulated/PII/data loop (e.g. production data cleanup) | **CSO auto-loop fires** — `security-analyst` gates every iteration; no PII copied into logs |
| A produce-and-verify loop | `reviewer` runs the independent verification pass each round |

```
"iterate until coverage is 100%"  →  loops skill
   → planner composes: tester (act) + coverage checkpoint + reviewer (verify)
   → ratchet floor each round; stop at 100% (success) or no-progress (stagnated)
   → confidence tag + framework citation on exit
```

No command is required — this skill is invoked by intent, by `/mxm-superpowers`, or by an office command that recognizes a loop-shaped task.

---

## The Loop Catalog (31 loops → Maxim surfaces)

Each loop orchestrates an existing Maxim office/agent. Status: ✅ already a Maxim command · 🔁 loop over an existing surface · ⭐ native gap-loop (defined below).

**Engineering:** 001 docs-sweep 🔁(`proactive-watch`+`reviewer`) · 002 architecture-satisfaction 🔁(build→review→test) · 003 perf-to-threshold ⭐ · 004 production-error-sweep ⭐ · 005 coverage-to-100 ⭐ · 007 logging-coverage ⭐ · 008 nightly-changelog 🔁(`changelog-writer`) · 011 test-suite-speed ⭐ · 016 ticket-to-PR-ready 🔁(`/mxm-fix`) · 019 adversarial-review 🔁(`reviewer`+`pre-release-audit`) · 020 scheduled-work-verification ⭐ · 027 builder-reviewer 🔁(`/mxm-superpowers`; see autonomy-loop) · 028 completion-contract 🔁(Coverage Matrix) · 031 recent-feedback-sweep ⭐

**Evaluation:** 009 quality-streak ⭐ · 010 full-product-eval 🔁(`/mxm-health`) · 023 champion-challenger ⭐ · 024 devils-advocate 🔁(`reviewer`/`threat-modeler`) · 029 versioned-experiment 🔁(`experiment-tracker`)

**Operations:** 012 repo-cleanup 🔁(`/mxm-organize`) · 013 stale-safe-batch-release 🔁(`/mxm-ship`) · 014 production-data-cleanup ⭐(CSO-gated) · 015 post-release-baseline ⭐ · 017 customer-deployment 🔁(`customer-success-manager`) · 025 fresh-clone ⭐ · 030 repo-maintainer-heartbeat 🔁(`/mxm-portfolio`+`/mxm-tasks`)

**Content:** 006 SEO/GEO ✅(`/mxm-seo`) · 018 product-podcast ✅(NotebookLM)

**Design:** 021 3D-render-benchmark (skipped — niche) · 022 frontend-reconstruction 🔁(`ui-styling`) · 026 thumbnail-iterate 🔁(`banner-design`)

---

## Native Gap-Loops (⭐ — Maxim has no equivalent; defined here)

Ordered by priority. Each names its stop.

### fresh-clone (025) — ⭐ top priority
In a disposable environment, follow ONLY `documents/guides/GETTING_STARTED.md` / README — no insider knowledge — until install + first-run works clean. **Stop:** clean install (success) OR a precise documented blocker (blocked). *Targets Maxim's worst historical failure class: BUG-001..005 were all fresh-clone install failures (DEBUGGING_PLAYBOOK §1). This loop would have caught all five.*

### recent-feedback-sweep (031) — ⭐
Collect recent operator corrections (`.mxm-operator-profile/` rejected patterns + `.mxm-skills/agents-skill-gaps.log`) → audit the whole project for the same pattern → fix each → record in the pattern registry. **Stop:** no new instances of the pattern (success) or no-progress (stagnated). *Maps onto Maxim's pattern-registry discipline (BUG_TRACKER Recurring-Pattern Registry).*

### coverage-ratchet (005) — ⭐
Drive test coverage to a floor that can only ratchet UP (line AND branch, independently). A corrupt/missing baseline is an honest error, never a silent re-seed lower. **Stop:** floor met (success) or no viable test to add (exhausted). *Ports the autonomy-loop `coverage-ratchet` logic.*

### production-error-sweep (004) — ⭐ (CSO-gated)
Group prod-log symptoms → separate actionable from noise → root-cause + smallest fix + verify, one PR each. **Stop:** clean if no actionable errors (clean no-op) or all fixed (success). `security-analyst` gates: never copy credentials/PII into logs or output.

### champion-challenger (023) — ⭐ strategic
Promote a prompt/policy/framework change only if it beats the incumbent on a **frozen holdout set** without weakening a must-pass check. Keep the incumbent on uncertainty. **Stop:** target met / budget / no-progress. *On-ramp to the PaaS data flywheel — the only loop that makes Maxim self-improving rather than static.*

### perf-to-threshold (003) · logging-coverage (007) · quality-streak (009) · test-suite-speed (011) · data-cleanup (014, CSO-gated) · post-release-baseline (015)
Defined in `references/loop-catalog.md` (each: trigger · stop · checkpoint · owning agent).

---

## Behavioral Overlay (applied to every loop)

- **Confidence tag** on every iteration's output and on the terminal state (ADR-010).
- **Framework citation** — name the behavioral/CS principle the loop embodies (ADR-007): bounded loop (feedback control), independent verification (separation of duties), champion-challenger (Goodhart-resistance + holdout).
- **CSO auto-loop** — any loop touching PII / regulated data / production data routes `security-analyst` into every iteration; cannot be bypassed.
- **No-fabrication** — any rate/metric a loop reports carries its sample size (e.g. "12/30 passing"), never a bare claim. (autonomy-loop's honesty rule.)

---

## References

- loop-library — `Forward-Future/loop-library` (31-loop catalog; the stopping-condition discipline). Prior art, cited per ADR-007.
- autonomy-loop — `inferencegod/autonomy-loop` (deterministic fail-closed gates: coverage-ratchet, mutation-as-gate, money-path floor). Reference for the verification loops.
- ADR-002 (executable contracts) · ADR-007 (framework citation) · ADR-010 (confidence) · ADR-017 (office dispatch).
- Full adoption rationale + the 31-loop mapping: `documents/architecture/MAXIM_LOOP_ADOPTION_PLAN.md`.
