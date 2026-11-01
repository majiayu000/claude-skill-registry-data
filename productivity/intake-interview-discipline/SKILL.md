---
name: intake-interview-discipline
version: "0.5.0"
user-invocable: false
description: "Deep intake discipline for unattended long-run hosts: interview with interactive-workflow depth while the human is present (destination → fog tickets → one-per-turn resolution → approach comparison), freeze the chosen approach plus open assumptions into the run contract with a bounded pre-launch self-review, self-answer mid-run decisions with recorded assumptions (clean stop + ticket report when the frozen approach is falsified — never a silent pivot), and roll the decision/assumption ledger into human acceptance. Referenced by goal-driven hosts via frontmatter dependencies. Triggers — 「深谈入库」「入库深谈」「前置深谈」「无人值守深谈」「决策冻结」「冻结方向」「自答留痕」「票台账」「方向证伪」 / deep intake interview, freeze the approach, runtime self-answer ledger, falsified-approach clean stop. Do NOT use as a name alias for clarifying-question-discipline or decision-fog-discipline, or for interactive attended workflows (solve-workflow owns those pauses)."
dependencies:
  - clarifying-question-discipline
  - decision-fog-discipline
---

# Intake Interview Discipline

> Internal shared skill. Single source of truth for **interactive-grade question depth in unattended long-run hosts**: everything only the human can answer is asked up front while they are present; everything the run answers alone is recorded for their return. Composes `clarifying-question-discipline` (how to ask) and `decision-fog-discipline` (when understanding is clear enough); adds what unattended hosts lack — approach freeze, runtime self-answer rules, and the acceptance ledger.
>
> **Prerequisite check**: this skill declares frontmatter dependencies; verify each is available on load — if one is missing, abort and print the install command (`npx skills add FuDesign2008/open-skills -g --skill <name> --yes`). No silent fallback.

## Iron rules

1. **Fog-bounded depth, not round-bounded** — interview until no blocking fog remains (graduation per `decision-fog-discipline`), never a fixed questionnaire. A clear task graduates fast; a foggy one earns more rounds. The human's time is spent on **decisions only** — facts get investigated, not asked.
2. **The frozen approach is the run's compass** — once frozen into the contract, the approach MUST NOT be silently replaced mid-run. If run evidence falsifies it: **clean stop + ticket report** (§B). A visible stop is success discipline; a silent pivot is failure.
3. **Every runtime self-answer is an assumption until reviewed** — recorded in the ledger with rationale and impact-if-wrong; the human MAY overturn any entry at acceptance.

## A. Intake deep interview (human present)

**Presence tiers** — interview depth follows human availability, because a question is only cheap while someone can answer it:

- **Present (default)** — resolve open decisions as per-decision questions until fog graduates. Self-answers are reserved for explicitly low-impact items; anything whose impact-if-wrong is high (positioning that trusts an upstream MR, verification strategy, external contracts) gets asked, not defaulted. Open the intake output with a three-part base — restatement / key elements / open questions — so the human checks the AI's unfolded understanding before anything is frozen into a compact contract.
- **Declared or structural absence** (「无人值守」/ "I'm off", batch child runs, scheduled pulls, card-inherited intake) — the once-confirm + full-ledger mode applies unchanged: freeze what investigation and conservative defaults support, flag everything as assumptions, close the loop at ledger review when the human returns.
- **AI proxy (opt-in third source)** — when the host run's Stage-exit policy is `ai-proxy` (per `ai-proxy-discipline`), present-mode methodology runs with the proxy as answer source at the enumerated checkpoints, every answer ledger-marked `proxy-made`. Reserved-list items stay human-only at every touchpoint.

1. **Destination** — one short success picture (what "done" looks like).
2. **Fog map & tickets** — list open decisions as tickets per `decision-fog-discipline`; keep the list short; mark blocking vs deferrable.
3. **Resolve one ticket per turn** — `clarifying-question-discipline` (one question per turn, recommended answer required); facts are investigated, not asked.
4. **Approach comparison** — 2–5 approaches, one comparison table (core idea / files touched / pros / cons / complexity / recommendation); the human picks. Lean path with no fog: 1 approach + a risk note is enough.
5. **Freeze** — write into the host contract: chosen approach (one line + pointer to the table), resolved tickets, deferred tickets (with reason), initial assumptions, plus a **Decisions-I-made-for-you** section — every self-answered decision with its impact tier, so the approval event shows what was decided without the human. Mark each entry `factual` (branch baselines, dependency existence, target paths) or `preference`; unmarked defaults to factual, and hosts verify factual entries at their dispatch boundary. Consequence descriptions MUST be derived by walking the enqueue configuration → child default behavior path **as actually configured** — e.g. proxy off + child manual mode means stage exits will stop and ask the user, not "follow frozen decisions"; a mis-described consequence is worse than none. Before closing, re-check each self-answered item's impact-if-wrong and escalate any high-impact item to a question now: this is the last cheap moment to ask. Templates in [reference.md](reference.md).
6. **Bounded pre-launch self-review** — one checklist-level pass over the frozen contract: covers the destination? risks named? budget + constraints present? anything self-contradictory? Fix gaps and re-check once; a remaining blocking doubt goes back to the human **now** — they are still present; after launch there is no one to ask.

## B. Runtime self-answer (human absent)

When a decision arises mid-run, take the **first branch that closes it**:

| Priority | Situation | Action |
|---|---|---|
| 1 | The frozen contract answers it | Follow the contract; no ledger entry needed |
| 2 | Investigable fact | Investigate (read-only), decide, record assumption in the ledger |
| 3 | Reversible choice whose impact-if-wrong is explicitly **low**, no contract guidance | Pick the conservative default; record in the ledger |
| 4 | High impact-if-wrong, unanswerable by 1–2 | Escalate at the next human touchpoint (a present intake, a queue discovery boundary, an opted-in proxy checkpoint); with no touchpoint ahead, clean stop — never a silent default |
| 5 | Blocks progress AND unanswerable by 1–4, or evidence falsifies the frozen approach | **Clean stop**: halt this task at a safe point (no half-edits, budget respected), write a ticket report (what was falsified/blocked, evidence, options with trade-offs), set status per the host's vocabulary; never improvise a new direction |

Batch/queue hosts: a clean stop on one task never cancels the others (non-blocking failure).

## C. Acceptance ledger

- One ledger per run, carried in the host's contract artifact (task card / run contract / completion report); fields in [reference.md](reference.md).
- The host's completion report MUST surface for human review: unresolved tickets, low-confidence assumptions, and every ledger entry whose impact-if-wrong is high.
- Acceptance findings feed the next run's intake — interview quality compounds across runs.

## Integration guide (for referencing hosts)

1. Declare `intake-interview-discipline` in frontmatter `dependencies`; abort at startup if missing.
2. Keep exactly these touchpoints in the host body — do not restate this skill's prose:
   - **Intake stage**: one pointer line (deep interview with presence tiers + freeze + impact re-review + bounded pre-launch self-review per this skill)
   - **Contract fields**: point at [reference.md](reference.md) templates (frozen approach, tickets, assumptions, Decisions-I-made-for-you section)
   - **Run stage**: one line — self-answer per this skill (impact-gated ladder); falsified approach → clean stop, no silent pivot
   - **Report/acceptance stage**: one line — ledger surfaces unresolved + high-impact entries for human judgment
3. Attended hosts that pause at every gate by design (solve-workflow-style) do not need this skill — their humans are present. This skill exists for hosts whose value promise is that **nobody has to be present mid-run**.
4. Auto-mode intake with no human present at all: run §A in self-answer mode — investigate, propose defaults, freeze them **flagged as assumptions**; the "interview" then happens when the human returns, via ledger review.

## Forbidden

- Restating `clarifying-question-discipline` or `decision-fog-discipline` rules in host bodies (thin pointers only)
- Fixed question counts or questionnaire dumps ("ask exactly N questions")
- Silent mid-run approach changes; treating budget exhaustion as success
- Marking outcome-type standards as passed by ledger self-assessment (humans judge outcomes)
