---
name: dissect
description: >-
  Evidence-driven dissection of an existing service, written plan, or codebase
  area. Interrogates every entity (table, field, component, endpoint, module,
  boundary) against ground truth from multiple sources at once, red-teams each
  verdict devil's-advocate style, and arrives at the minimal-build optimization
  plan. Runs as a staged pipeline with human checkpoints and parallel read-only
  sub-agents so each investigation stays laser-focused. Optional --circuit skips
  intermediate checkpoint waits and asks at the final recommendation; --autopilot
  takes recommended choices and proceeds. Use when the user invokes /dissect, or
  asks to audit / optimize / challenge / "tear apart" an existing system, schema,
  or plan. If the session is in Cursor or Claude Plan Mode, update the existing
  plan in place — never rewrite it. Use inception to author a new plan.
user-invocable: true
disable-model-invocation: false
version: "2.6.0"
author: "Ali Farahat"
tags: ["dissect", "audit", "red-team", "minimal-build", "refactor", "ground-truth", "orchestration"]
when_to_use: |
  USE WHEN (backward-looking, "what is actually here and what should change?"):
  - User invokes /dissect <target> or asks to audit, dissect, optimize, or
    challenge an EXISTING service, schema, data model, or codebase area.
  - User hands you a WRITTEN PLAN or spec and wants it pressure-tested against the
    code/DB that already exists (intent vs reality).
  - A system feels bloated, over-engineered, or misnamed and you need an
    evidence-backed keep/fold/drop/defer decision per entity.
  - You suspect scope-creep, dead code, stubs masquerading as features, or tables/
    components living in the wrong domain.
  - Before a migration or refactor, to find the minimal set of changes that
    actually meets the requirement.
  - The session is in Cursor Plan Mode or Claude Plan Mode and the user wants
    the current plan dissected, fixed, and tuned (gaps filled, errors corrected)
    without replacing the document.

  DO NOT USE WHEN:
  - The thing does not exist yet and you need a detailed work-breakdown plan.
    That is `inception`. If you only need to pick among approaches, use
    `deep-deliberation`.
  - The task is a quick lookup or a one-line fix with an obvious answer.
  - You only have intent (a plan) with no code/DB/runtime to verify against AND no
    way to get ground truth — dissect's power comes from live evidence; flag the gap.
---

# Dissect

> **Leading words:** dissect, ground truth, entity-level, minimal-build,
> red-team, evidence-backed, stub detection, naming audit, fold test,
> phase separation, patch in place, circuit, autopilot, plain question.

Systematically interrogate and optimize an existing service, written plan, or
system. The goal is not to rubber-stamp the current design — it is to arrive at
the **minimal-build plan** that correctly meets the requirements, by challenging
every assumption with live evidence and an adversarial review panel.

**Trigger:** `/dissect [--circuit|--autopilot] <target>` where `<target>` is a
service name, plan file path, codebase area, or free-form description. If
omitted, ask. Pace flags are optional; default is interactive (stop at every
checkpoint).

`dissect` is the backward-looking counterpart to `deep-deliberation`. They share
DNA — parallel read-only sub-agents, devil's-advocate red-teaming, human
checkpoints, evidence over intent, and the same `--circuit` / `--autopilot`
grammar — but point in opposite directions: deliberation designs what to build;
dissect audits what already exists.

---

## User Input

```text
$ARGUMENTS
```

Parse a pace flag from arguments **before** treating the rest as `<target>`:
`--circuit`, `--autopilot`, `--auto` (alias of `--autopilot`). Strip the flag
from the target string. If both circuit and autopilot appear, autopilot wins.

---

## Pace modes (optional)

Default is **interactive**: stop and wait at every checkpoint.

The user must opt in **this invocation** — a flag above, or an explicit phrase
(`circuit`, `autopilot`, `take recommended`, `circuit the rest`,
`autopilot the rest`). Do not infer from urgency, "just audit this", or a
desire to move fast. Mid-run, the same phrases switch mode from the current
checkpoint. `stop circuit` / `stop autopilot` drops back to interactive.

| Mode | Intermediate checkpoints (1–2) | Final checkpoint (3) |
|---|---|---|
| `interactive` | Stop and wait | Stop and wait. Do not proceed until they ask |
| `--circuit` | Auto-accept the recommended choice; log and continue | Stop. Ask whether to go ahead with the final recommendation |
| `--autopilot` | Auto-accept; log and continue | Auto-accept. Treat the recommendation as the way to proceed |

**Skip the wait, not the work.** Stages, evidence, red-team, and the naming
audit still run. Emit a compact `PACE_LOG` of every auto-accepted choice.

**Cannot proceed:** if there is no unique recommendation (tie, empty shortlist,
pipeline wants to go backward), stop and ask even on autopilot.

**Proceed** (autopilot, or circuit after the user says go ahead):

- Plan Mode / existing plan file: apply the surgical patch map. Do not
  implement code unless they also asked to implement.
- Otherwise: start executing the recommended ToT / execution branch.

Discrepancies still surface (principle 9). Circuit holds them for the final
ask. Autopilot logs the recommended resolution in `PACE_LOG` and the report;
never drop them.

**Interactive final footer.** On Checkpoint 3 only, when this run is
interactive, append the block below **verbatim as the last thing in the
message** (after the Checkpoint 3 ask). Omit it under `--circuit` /
`--autopilot`. Do not paraphrase. Do not place it earlier.

```markdown
⚡ **Skip the waits next time**

This run was **interactive** — a stop at every checkpoint. Same skill, two other paces:

- `--circuit` — take the recommended choices through the middle checkpoints, then stop at the final recommendation and ask before proceeding.
- `--autopilot` — take every recommended choice, including the last, and proceed without waiting.

`/dissect --circuit <target>` · `/dissect --autopilot <target>`
```

---

## User questions (plain question)

The report may be technical. The **ask** must not be.

Same turn as the checkpoint message: host structured question tool
(Cursor `AskQuestion`, Claude Code `AskUserQuestion`, OpenCode equivalent).
No tool → numbered list. Do not replace the report. Then stop.

Prompt: one sentence, product language. Labels ≤40 chars. First ends
`(Recommended)`. Last is always `Say this in plain English` (meta: do not
advance; rephrase + one example of what each real option means here; re-ask).
Second pick: a simpler analogy. Free-text overrides. Per-option
descriptions: one plain sentence if the host supports them. Any ask to
the human (including cannot-proceed) follows this contract.

---

## Core principles (never waive)

1. **Ground truth beats intent.** What the code actually does overrides what the
   plan says it should do. Always verify live.
2. **Row counts are a liveness signal only.** A 0-row table can be load-bearing;
   a populated table can be redundant. Never use row count as a keep/drop reason.
3. **Name what it IS, not what it was named.** Entities are frequently misnamed.
   Read a few actual records before drawing conclusions. A table called
   `contact_preference` might store food allergies and golf equipment.
4. **Own vs read.** "Entities this service reads" ≠ "entities this service owns."
   Reading a table does not mean you should count it in the domain.
5. **Stubs are not live.** A function that `throws new Error('not implemented')`,
   a cron that no-ops, or a consumer that re-queues to the DLQ is not a running
   feature. Check before counting it as active behavior.
6. **Minimal build.** Every proposed change must trace to a requirement. Do not
   design for hypothetical future use. Three similar things beat a premature
   abstraction.
7. **Naming audit is phase zero.** Naming confusion causes the most incorrect
   verdicts. Run it before any verdict.
8. **Sub-agents return evidence, the orchestrator returns verdicts.** A sub-agent
   that declares "VERDICT: DROP" unprompted is overstepping. Synthesis happens in
   the main context where all evidence is held together.
9. **Escalate discrepancies, don't resolve them silently.** If code says X and the
   plan says Y, surface both. Interactive: wait at the checkpoint. `--circuit`:
   hold them for the final ask. `--autopilot`: log the recommended resolution
   in `PACE_LOG` and the report; never drop them.
10. **Patch in place — never rewrite the live plan.** If the session is in Cursor
    Plan Mode or Claude Plan Mode, or the target is an existing plan document,
    the source plan is the document of record. Dissect it, then surgically
    update it (fix, tune, fill gaps). Never full-file `Write` it. Never create a
    second plan that replaces it. Unaddressed sections stay verbatim. Read
    [references/plan_preservation.md](references/plan_preservation.md) before
    any write. Override only if the human explicitly asks to rewrite from scratch.

---

## Pipeline overview

```
USER input (service / plan / codebase area)
   ↓
[Stage 0] Intake + Naming Audit                 (1 explore sub-agent)
   🛑 CHECKPOINT 1 — human confirms names + scope boundary
   ↓
[Stage 1] Multi-source Ground Truth             (3 explore sub-agents, parallel)
[Stage 2] Entity-level Devil's Advocate         (1 explore sub-agent per cluster)
   🛑 CHECKPOINT 2 — human reviews per-entity verdicts
   ↓
[Stage 3] Cross-cutting + Adversarial Red-Team  (system challenge + ToT branches)
[Stage 4] Synthesis + Minimal-Build Plan        (orchestrator, main context)
   🛑 CHECKPOINT 3 — human picks the execution branch
```

Copy this checklist and track progress out loud:

```
Progress:
- [ ] Stage 0: Naming audit
- [ ] CHECKPOINT 1 — names + scope confirmed
- [ ] Stage 1: Multi-source ground truth (DB + code + plan, parallel)
- [ ] Stage 2: Entity-level devil's advocate (one agent per cluster)
- [ ] CHECKPOINT 2 — entity verdicts reviewed
- [ ] Stage 3: Cross-cutting challenges + ToT refactor branches + red-team
- [ ] Stage 4: Synthesis → minimal-build plan
- [ ] CHECKPOINT 3 — execution branch chosen
```

> **Right-size the pipeline.** This is heavy. For a small target (a handful of
> entities, one file) collapse Stages 0–2 into a single pass and skip the parallel
> fan-out — but never skip the naming audit. Checkpoint 1 **wait** is skippable
> only under `--circuit` / `--autopilot`.

---

## Stage 0 — Intake + Naming Audit

Surface naming confusion that could corrupt every later verdict, before any
analysis. Dispatch one read-only (`explore`) sub-agent:

```
Prompt: Naming audit for <target>.

For every entity (table, field, service, component, endpoint) in scope:
  1. Does the name accurately describe what it actually holds/does?
  2. Is there another entity with a similar name it could be confused with?
  3. Read 2–3 actual records (or the code body) and compare to the name.
     Flag any mismatch.

Return a table only (no verdicts):
  Entity | What name implies | What it actually contains | Mismatch?
```

If the session is already in **Cursor Plan Mode** or **Claude Plan Mode** and
the user did not name a different target, the target **is the current plan
document**. Record its path. Read
[references/plan_preservation.md](references/plan_preservation.md) now — before
any write.

### 🛑 Checkpoint 1
Lead with one sentence a product owner could repeat (what you found, what's
in vs out of scope). Then the naming table and proposed scope boundary (what
this target owns vs merely reads).

Interactive: structured question per **User questions**, then stop.

```text
prompt: Some names don't match what they actually store. Use the corrected names for the rest of this review?
options:
- Yes, use the corrected names (Recommended)
- Keep the original names
- Change what we're reviewing first
- Say this in plain English
```

`--circuit` / `--autopilot`: log the proposed names and scope as auto-accepted
(`PACE_LOG`) and continue. A mismatch here changes the verdicts in every later
stage.

---

## Stage 1 — Multi-source Ground Truth

Gather evidence from **all three** sources simultaneously via parallel read-only
sub-agents. Each source catches what the others miss.

| Source | What it catches |
|---|---|
| **Live DB / runtime** | Actual schema, real data, column comments, row shapes |
| **App code** | What actually reads/writes each entity; stubs vs live paths |
| **Plan / spec / migrations** | Intent; evolution history; documented decisions |

Launch three `explore` sub-agents in parallel (one message, three `Task` calls):

**A — Live introspection:** every in-scope entity (name, fields, types,
descriptions), 2 sample records each, row counts (liveness only), and FK/ownership
relationships.

**B — Code evidence:** every file that reads/writes each entity (file:line);
whether each reader/writer is live or a stub; the module that OWNS each entity vs
those that merely READ it; any code using the wrong entity for its purpose.

**C — Plan / spec / migration evidence:** the original design doc, migration
history (before/after), documented decisions, what was explicitly deferred or
descoped, and what the plan SAYS is live vs what code/DB show.

Synthesize the three outputs. Note every discrepancy between sources — that is
where the real problems live.

---

## Stage 2 — Entity-level Devil's Advocate

For each entity **cluster** (group related entities), dispatch one focused
`explore` sub-agent that challenges every verdict. **One cluster = one agent.**
Never batch unrelated clusters — context pollution corrupts both verdicts.

Standard question set (apply to every entity):

```
For entity <X>:
1. PURPOSE   — Plain terms: what does it do? What breaks if it vanished tomorrow?
2. OWNERSHIP — Does <service> own it, or merely read it from another domain?
3. NAME      — Does the name match the data? (Reference Stage 0.)
4. EVIDENCE  — Live code that reads AND writes it? file:line each. Writers but no
               readers (or vice-versa) → flag. Read by a service that shouldn't
               own it → flag.
5. FOLD TEST — Can it be absorbed into a parent? (See fold tests below.)
6. PII/BOUNDARY — Personal data? Which DB/domain should it live in? Match current?
7. STUB CHECK — Is the using code live, or a stub/throw/no-op?
8. VERDICT   — Propose from the dynamic taxonomy below, justified with evidence.
               Never justify with row count.
```

### 🛑 Checkpoint 2
Lead with one sentence a product owner could repeat. Then the per-entity
verdicts table (Entity | Proposed verdict | Evidence).

Interactive: structured question per **User questions**, then stop.

```text
prompt: For each piece I recommend keep it, combine it, remove it, or move it. Look right?
options:
- Looks right, keep going (Recommended)
- I want to change some of those
- Look closer at one of them
- Say this in plain English
```

`--circuit` / `--autopilot`: log the proposed verdicts as auto-accepted and
continue.

---

## Dynamic verdict taxonomy

`KEEP / FOLD / DROP` is too rigid — it only fits relational tables. A
dissection target may be a written plan, a runtime flow, or a coupled module,
so verdicts are **action-oriented and target-aware**. The full taxonomy
(KEEP, FOLD, DROP, DEFER, ON-DEMAND, EXTRACT, RE-HOME, REFACTOR,
OUT-OF-SCOPE) with meanings, plan-vs-code typicals, and the distinctions
that matter (RE-HOME vs EXTRACT, DEFER vs DROP, ON-DEMAND vs KEEP) lives in
[references/verdict_taxonomy.md](references/verdict_taxonomy.md).

Each verdict must cite evidence (file:line or live DB), never row count.
Pick the most precise verdict from the taxonomy.

---

## Stage 3 — Cross-cutting challenges + adversarial red-team

After entity verdicts, challenge the **system-level design**, then red-team the
emerging plan from independent adversarial angles. This is where dissect borrows
deep-deliberation's Tree-of-Thought and red-team machinery.

### 3a. System-level questions (one `explore` sub-agent)
1. **Send/process model** — Is there pre-staging/pre-rendering/pre-computation
   that could be deferred to the moment it's needed? What's the throughput ceiling?
2. **Feedback loops** — When something fails (bounce, rejection, error), is the
   signal captured and acted on, or is the feedback path a stub?
3. **Ownership boundaries** — Where does this service read/write data that belongs
   to another? Any misuse of another domain's tables?
4. **Naming & taxonomy** — Are concepts that share a name actually different
   things (kind vs channel vs group)? Conflation causes the worst bugs.
5. **Live vs designed** — For each major feature, is it actually running or a
   stub/planned/throw? List what is NOT live that the plan implies is live.

### 3b. Tree-of-Thought refactor branches (orchestrator)
Do not assume a single target state. Generate **2–4 distinct end-states** for the
optimization, each with idea, pros/cons, main risk, and rough effort (S/M/L).
Example axis for a storage-heavy target:
- *Branch A — ON-DEMAND:* compute at read, zero new storage.
- *Branch B — FOLD/JSONB:* absorb into parent, flexible, fewer joins.
- *Branch C — hard relational consolidation:* columns + strict keys.
Prune dominated branches and say why. Recommend one + a runner-up.

### 3c. Adversarial red-team panel (parallel `explore` sub-agents)
Launch independent personas in parallel; each attacks first, then concedes what
survives, and returns evidence — not a final verdict. Minimum panel:
- **Zero-Utility Hawk** — argues to DROP or FOLD every entity; forces each KEEP to
  earn its place against live evidence.
- **Migration-Risk Hawk** — red-teams the proposed plan itself: does the migration
  create more downtime/risk than leaving the mess in place?
- **Boundary Hawk** — hunts ownership/PII violations and wrong-domain reads.
- **Stub Hunter** — proves which "features" are actually live vs throws/no-ops/DLQ.

(Reuse the deep-deliberation persona prompt shape: identity → relevant file paths
→ approach under review → attack, then concede, then evidence.)

### 3d. Lead judgment (orchestrator)

After the panel returns, you are the lead. Filter findings before they enter
Stage 4. Do not auto-apply.

| Bucket | Meaning |
|---|---|
| **Act On** | Consensus or a lone finding with a `file:line` that would ship a real defect |
| **Consider** | Plausible, not proven; mention in the report |
| **Noted** | Style or preference; do not churn the plan |
| **Dismissed** | Nit, hypothetical, or "I would have done it differently" with no failure |

Nitpick gravity: a rename is not a defect. Hypothetical vs actual: "could theoretically" without a path is Dismissed. Preserve material disagreements; never silently average them away.

---

## Stage 4 — Synthesis + minimal-build plan

Done in the main context (synthesis needs all evidence held together). Output:

**0. Naming corrections** — every mismatch found, with corrected names (apply
throughout).
**1. Scope boundary corrections** — entities wrongly counted in this domain; the
real owner of each; any live code that incorrectly crosses the boundary.
**2. Entity verdicts** — one table: Entity | Verdict | Rationale (file:line / live
evidence) | Lands (if FOLD/RE-HOME). No row-count justifications.
**3. System-level changes** — for each cross-cutting issue, in this format:
- **Decision:** [what]
- **Why:** [evidence-backed reason]
- **Other options:** [alternatives + why rejected]
**4. Bug / misuse log** — places where code uses the wrong entity or wires an
entity to the wrong system. Correctness issues, distinct from optimization.
**5. Execution order** — the minimal-build sequence: highest-value/most-independent
first, what depends on what, what to defer.
**6. Deferred / out of scope** — what is intentionally NOT changing, each with a
reason.

The six sections above are the **dissection report** (chat). They are not a
replacement body for an existing plan file.

### Plan Mode / existing plan document

If the session is in Cursor or Claude Plan Mode, or the target is an existing
plan file: do **not** emit a new plan. Follow
[references/plan_preservation.md](references/plan_preservation.md). Build a
patch map (`KEEP` / `PATCH` / `APPEND` / `FLAG`), apply surgical edits after
Checkpoint 3, and preserve every unaddressed section. `APPEND` is how newly
identified gaps land in the plan — they are added, not used as a reason to
rewrite.

### 🛑 Checkpoint 3
Lead with one sentence a product owner could repeat. Then the technical
detail (recommended ToT branch and ranked alternatives). If a live plan is
being patched, also present the patch map.

Interactive / `--circuit`: structured question per **User questions**, then
stop. Name the recommended branch in the prompt in product language, not
taxonomy.

```text
prompt: I recommend we do “[short name]”: [one-line why]. Go with that?
options:
- Yes, do that (Recommended)
- Do the other option instead
- Don't start yet
- Say this in plain English
```

- **Interactive:** do not start implementing unless they ask. Do not touch
  the plan file until they confirm. End the message with the interactive
  final footer (Pace modes) — last block, verbatim.
- **`--circuit`:** if they say no, stay at this checkpoint.
- **`--autopilot`**, or **circuit after they say go ahead:** proceed as defined
  under Pace modes.

---

## Fold tests (reference)

The full fold-test table (cardinality → fold type → blocker, plus the
independent-relational-access check and the PII/DB-boundary rule) lives in
[references/fold_tests.md](references/fold_tests.md).

Quick reference:
- 1:1 with parent → columns on parent (just do it).
- 1:N bounded (≤~10) → JSONB on parent, **unless** independent relational
  access is needed.
- 1:N unbounded/queried, N:M → keep as table.
- Never fold across a PII/DB boundary.

---

## Sub-agent dispatch rules

- **Parallel for the Stage 1 triple** (DB + code + plan) — independent, run at once.
- **One cluster per Stage 2 agent** — never mix unrelated clusters.
- **Read-only only.** All dissection agents use `subagent_type: "explore"`. No
  write access. Do NOT pass a `model` — sub-agents inherit the parent model.
- **Agents return raw evidence, not verdicts.** Synthesis is the orchestrator's
  job. Escalate discrepancies to the checkpoint (or `PACE_LOG` / final ask
  under pace modes); never drop them.

---

## Key lessons (baked in)

- **Read the actual data first.** A table named `managed_preference` might contain
  "Favorite Drink → Moscow Mule." You would never know without reading it.
- **Channel ≠ kind ≠ group.** Multiple orthogonal taxonomies get conflated; that
  produces wrong verdicts. Keep them distinct.
- **"Built for" vs "used for."** A table built for one purpose can be misused for
  another. If design intent and actual use diverge, that's a bug, not a design.
- **The eligibility/read pipeline is not authoritative.** What a pipeline reads
  doesn't define the correct data model — it may be reading the wrong thing.
- **Stubs inflate the system.** A cron that throws, a consumer that re-queues, a
  client that returns `permanent_failure` for all inputs — none are live.
- **Plan and code diverge.** The plan is intent; the code is reality. Ground the
  optimization in reality.

---

## Output format notes

- Every verdict cites evidence. No bare assertions.
- Every FOLD/RE-HOME states the target it lands in and which fold test applies.
- Every OUT-OF-SCOPE names the correct domain owner.
- Every DROP names the reason (no code path / derivable / moved / legacy).
- Every DEFER/ON-DEMAND names the requirement that justifies the seam (or its
  absence).
- Row count appears only as liveness context, never as a reason.
- Lead with plain-terms summaries, then technical detail. Write both. The
  structured question at each checkpoint is a **plain question** (User
  questions); jargon stays in the report, not in the prompt or labels.
- Interactive Checkpoint 3: end with the pace-mode footer from Pace modes
  (verbatim, last block). Omit under `--circuit` / `--autopilot`.

## References

| File | Use it for |
|---|---|
| [references/verdict_taxonomy.md](references/verdict_taxonomy.md) | Full dynamic verdict taxonomy (KEEP/FOLD/DROP/DEFER/ON-DEMAND/EXTRACT/RE-HOME/REFACTOR/OUT-OF-SCOPE) with meanings, plan-vs-code typicals, distinctions, output format |
| [references/fold_tests.md](references/fold_tests.md) | Fold-test table (cardinality → fold type → blocker), independent-relational-access check, PII/DB-boundary rule |
| [references/plan_preservation.md](references/plan_preservation.md) | Plan Mode / existing plan file: patch in place, never rewrite. Detection, forbidden actions, patch map, host notes, worked example |
