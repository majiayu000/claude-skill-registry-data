---
name: Clarification Protocol
description: Reusable contract for surfacing multiple-choice clarifying questions (with a recommended option) at phase intake and whenever in-phase ambiguity exceeds threshold. Defines question shape, threshold scoring, capture format, and bypass. Phase-specific question banks live in the calling agent. Surface-and-pause is mandatory; the agent never self-resolves Recommended options.
version: 1.2.1
author: Mattermost Design Team
tags: [governance, intake, ambiguity, decision-aid, all-phases, complexity-tier]
allowed-tools: Read, Grep, Glob
---

# Clarification Protocol

## Purpose

The contract every phase agent follows when it needs a decision from the user. Defines:
- **When** to surface questions (intake + ambiguity threshold + loopback)
- **How** to shape them (multiple-choice with exactly one Recommended option)
- **Where** to capture answers (spec state) so they are auditable and never re-asked

Phase-specific question content lives in each phase agent's SKILL.md. This skill carries only the contract.

---

## When to Invoke (Three Triggers)

### Trigger A — Phase Intake (mandatory)

Every phase agent runs the protocol as **Step 0**, before any artifact-producing skill. The agent **surfaces its phase-specific intake questions (defined in the agent's own SKILL.md) to the user and pauses**. The agent does not produce, draft, or progress any artifact until the user has replied.

**Scope-bearing intake (Phase 1 + Phase 3).** Two intake rounds carry scope-discipline duties beyond the normal capture:

- **Phase 1 (discovery) intake MUST resolve the scope-lock inputs** so the orchestrator can lock `scope_lock` before accepting the Problem Statement (gate item 1.12): the **complexity tier**, the **in/out-of-scope boundary**, the **surface count** (how many UI surfaces the feature touches), and the **comparator count** (competitor platforms for Phase 2 / solution approaches for Phase 4 — Tier 1/2 ≥ 3, Tier 3 ≥ 2). If the brain dump does not make these inferable with high confidence, the discovery-agent includes a question for each missing one (within the tier's ceiling). These are load-bearing — a missing surface/comparator count is a critical signal (+2) under the heuristics below.
- **Phase 3 (PRD) intake opens with a scope re-confirm**, not a question round: the orchestrator re-presents the locked scope and the user confirms (`y`) or describes a change. A described change is captured as a deliberate `scope_change` (recorded in `scope_lock.changes[]`), never a silent rerun. Only after re-confirm does the normal Phase 3 question round run. See the orchestrator's SCOPE-LOCK section.

**Surface-and-pause is non-negotiable.** The agent **MUST NOT** "auto-apply" the Recommended options on the user's behalf, "fast-forward" past the round, or treat the round as internal scaffolding. The Recommended option exists only as a decision aid for the user; only the user can adopt it, either explicitly per-question or via `accept recommendations` (which records a `bulk_accept_recommended` audit event). Producing an artifact without a user response in the audit log is a **protocol violation**, not a shortcut.

The spec-orchestrator enforces this: a gate artifact is **invalid** unless `context.clarifications[]` shows that every intake question was resolved with `chosen_via: "user_response"` or `chosen_via: "accept_recommendations_bulk"`. Any other value (e.g., `chosen_via: "agent_default"`, `chosen_via: "auto"`, or missing field) is rejected and the artifact is returned for revision.

### Trigger B — In-Phase Ambiguity (conditional)

During work, each agent tracks an ambiguity score (rules below). **Score ≥ 2 → pause and run a clarification round** before continuing.

### Trigger C — Loopback (focused)

When a downstream phase blocks back to an earlier one, the responsible agent re-asks only the **delta** between the prior decision set and the new state. Already-resolved clarifications in `context.clarifications[]` are never re-asked.

---

## Round Limits

- **Ask the minimum number of questions needed — not the maximum.** A round contains only questions whose answers (a) cannot be inferred with high confidence from the spec state, brain dump, or prior artifacts, AND (b) actually change a downstream artifact. A clean brain dump may produce a **1–3 question round**. The ceiling exists to prevent fatigue, not as a target.
- **The per-round question ceiling scales with `meta.complexity_tier`** (the caller injects the tier; if absent, treat as Tier 2). The ceiling is a guardrail, not a target — always prefer fewer:

  | Tier | Per-round ceiling | Posture |
  |---|---|---|
  | **Tier 1 — Full Spec** | up to **10** | Full question bank in play; novel/complex feature warrants broad intake. |
  | **Tier 2 — Standard Spec** | up to **6** | Standard feature; ask only the load-bearing decisions. |
  | **Tier 3 — Incremental Spec** | **a focused few (≤ 4)** | Parent spec already carries most context; ask only the *delta* the addendum introduces. |

  Reaching the ceiling for the active tier is a signal the phase or input is mis-scoped — prefer fewer.
- **Surface-and-pause is mandatory at every tier.** Tier only scales the question *count*. Tier 3 does **not** mean "skip intake" — it means a shorter round. A Tier-3 phase still surfaces its (smaller) round and pauses for the user, and still captures answers via the v1.2 two-stage format (`chosen_via` + `user_message_ref`). There is no tier at which the agent self-resolves Recommended options.
- **Before surfacing, prove each question earns its slot.** For every candidate question, the agent must be able to name (a) what spec-state field is empty/ambiguous, and (b) which downstream artifact changes based on the answer. If either is missing, drop the question. (For Tier 3, also drop anything the parent spec already answers — see Trigger C.)
- **Up to 3 rounds per phase** (all tiers). If a fourth round is needed, the agent **escalates**: the phase is likely mis-scoped. Surface a recommendation to re-run an earlier phase (typically Discovery) or revise the input artifact before continuing.
- If the agent generates more candidate questions than the active tier's ceiling, rank by stakes (critical signals first, then minor) and defer the rest to a later round if still relevant.

---

## Ambiguity Heuristics (Threshold Logic)

Each agent maintains an internal score during phase work. **+2 per critical signal, +1 per minor signal.**

### Critical signals (+2 each)

1. Load-bearing field is missing or empty in an input artifact or spec state (e.g., no user roles named, no success metric).
2. Multiple plausible interpretations diverge in artifact-shaping ways (e.g., reading the brain dump one way changes Phase 4's approaches).
3. The decision commits ≥ 2 downstream phases to a hard-to-reverse path.
4. Approved artifacts contradict each other on a load-bearing point.
5. About to add `[VERIFY WITH PM]` on a load-bearing requirement (not a cosmetic detail).
6. Compliance interpretation requires judgment — the same control has 2+ valid UX implications.
7. Untrusted external source is the only evidence for a high-impact claim.

### Minor signals (+1 each)

1. Ambiguous quantifiers ("many", "fast", "some") on load-bearing parameters.
2. A user role is referenced generically ("users") without title or scope.
3. Out-of-scope boundary is implied but not stated.
4. Mobile/desktop parity is not explicit.
5. A Compass design system gap is implied.
6. A scope-vs-time tradeoff is implicit.

### Threshold actions

| Score | Action |
|-------|--------|
| 0–1   | Proceed. Note any minor signals in `audit_trail.ambiguity_notes`. |
| ≥ 2   | **Stop.** Run a clarification round. Do not produce the gate artifact until resolved. |
| ≥ 4 (or 3rd round needed) | **Escalate.** Recommend re-running Discovery or revising the input artifact. |

---

## Question Format (Mandatory)

Every question follows this exact shape:

```markdown
### Question N — [3–6 word topic]

**Why this matters:** [1 sentence on what downstream artifact or decision changes based on the answer.]

**Options:**
- **A.** [Option label] — [1-line tradeoff]
- **B.** [Option label] — [1-line tradeoff] ✅ **Recommended**
- **C.** [Option label] — [1-line tradeoff]
- **D.** Other — let me describe it

**Recommendation rationale:** [1–2 sentences grounded in a concrete reason — see below.]
```

### Rules for question construction

1. **Exactly one option marked Recommended.** Never zero, never two.
2. **Always include "Other — let me describe it"** as the final option, even when A–C feel exhaustive. The user is the authority on their domain.
3. **2–5 options total** (including "Other"). Fewer than 2 isn't a question; more than 5 is decision fatigue.
4. **Options must be conceptually distinct**, not cosmetic variants.
5. **Tradeoffs, not adjectives.** "Inline editing — faster but spillage risk on classified data" beats "Inline editing — modern and clean."
6. **No leading questions.** Phrasing must not bias toward the recommended option beyond the explicit rationale.
7. **One decision per question.** Never bundle two choices.
8. **Numbered, batched, one message.** Never drip-feed.
9. **No question whose answer is already in spec state.** Read first.

### Recommendation rationale — grounding requirement

The rationale must point to something **concrete and defensible**. Acceptable grounding includes any of:

- A prior approved artifact in spec state ("Problem Statement names IL5 environments only — broader scope contradicts it")
- A design principle from P1–P6 ("P3 cognitive load floor — the simpler default keeps the operator's OODA loop tight")
- A Compass DS convention ("Compass Patterns uses the right-hand panel for secondary actions — a modal diverges")
- A concrete user impact ("Admins using a CSV workaround today will recognize the table view immediately")
- A known operational or technical constraint ("Air-gapped IL6 environments can't load external fonts")
- A compliance constraint (cite the framework, not necessarily the control ID — "DoD ZT requires least privilege; the narrower scope matches")

**Not acceptable** (treat as a protocol violation):
- "Industry best practice" with no source
- "Modern and clean" or other adjective-driven flair
- Restating the option as its own rationale
- A vague "this is better" with no reason

If no grounding exists, say so explicitly: **"Recommendation is a best-guess in absence of clearer evidence — override if domain knowledge says otherwise."**

---

## Output Format (When Agent Surfaces a Round)

```markdown
## [Phase N] Clarification — [Intake | Ambiguity Pause | Loopback]  ·  Round N of 3

**BLUF:** [1 sentence on why this round is happening and what is blocked until it resolves.]

**Ambiguity score:** [N — list triggered signals if Trigger B; omit for intake]

### Question 1 — [Topic]
**Why this matters:** ...
**Options:**
- **A.** ...
- **B.** ... ✅ **Recommended**
- **C.** ...
- **D.** Other — let me describe it
**Recommendation rationale:** ...

### Question 2 — [Topic]
...

---

**To answer:** Reply with `1: B, 2: A, 3: other (your description)` — or `accept recommendations` to take all defaults.
```

---

## Capture Format (Spec State)

After the user answers, the agent writes each resolved clarification to `context.clarifications[]`:

```json
{
  "id": "clar-2026-05-11-001",
  "phase": 3,
  "round": 1,
  "trigger": "intake | ambiguity | loopback",
  "topic": "Permission model scope",
  "why_it_matters": "Determines Phase 5 flow count and Phase 7 permissions table.",
  "options": [
    { "key": "A", "label": "Single role per user", "tradeoff": "...", "recommended": false },
    { "key": "B", "label": "Multi-role with inheritance", "tradeoff": "...", "recommended": true },
    { "key": "C", "label": "ABAC attribute-based", "tradeoff": "...", "recommended": false },
    { "key": "D", "label": "Other", "tradeoff": "user-supplied", "recommended": false }
  ],
  "recommendation_rationale": "...",
  "chosen": "B",
  "chosen_at": "2026-05-11T14:23:00Z",
  "chosen_via": "user_response | accept_recommendations_bulk",
  "user_message_ref": "(short quote or message-id of the user reply that produced this resolution — required when chosen_via = user_response or accept_recommendations_bulk)",
  "user_note": "(optional free-text from user)"
}
```

**`chosen_via` is restricted to two values: `user_response` or `accept_recommendations_bulk`.** Any other value (e.g., `agent_default`, `auto`, `recommended`, `inferred`) is a protocol violation — the orchestrator will reject the artifact and require the round to be re-surfaced to the user.

Append a per-clarification audit entry using the closed event vocabulary in `spec-state-object.json::$conventions.audit_event_vocabulary` and a **real ISO-8601 timestamp**: `{ timestamp: <real ISO>, event: "clarification_resolved", phase: N, actor: "<agent-name>", details: { clarification_id: "clar-...", chosen: "B", chosen_via: "user_response", user_message_ref: "..." } }`.

For each phase, also update `gates.phase_N.intake_clarifications` with the round summary (count asked, count resolved, bulk-accept used).

---

## Bypass Mechanism

The user can short-circuit a round with a single message:

| User says | Action |
|---|---|
| `accept recommendations` / `use defaults` / `all defaults` | Set every unanswered question to its recommended option |
| `B for 1, default for the rest` | Honor explicit choices, recommended for the rest |
| `spec accept-recommendations` (orchestrator command) | Same as "accept recommendations" |

When the agent applies bulk-accept:
1. Set `chosen` per question to the recommended option.
2. Record `chosen_via: "accept_recommendations_bulk"` per clarification.
3. Append a **single** typed audit entry (real ISO timestamp): `{ timestamp: <real ISO>, event: "bulk_accept_recommended", phase: N, actor: "human", details: { count: N, user_message_ref: "..." } }`.
4. Proceed to artifact production.

If the user's reply is ambiguous (e.g., "yeah ok"), the agent must echo back its parse before recording: *"Reading that as 'accept recommendations' — confirm?"*

---

## Hard Rules

1. **No silent assumptions.** If you find yourself "assuming" anything load-bearing, that's a clarification trigger.
2. **Surface and pause — never self-resolve.** When a round is surfaced, the agent stops working and waits for a user reply. The agent does **not** apply Recommended options on the user's behalf, does **not** record `chosen` without a user message, and does **not** treat its own confidence as a substitute for the user's decision. The only valid resolutions are an explicit per-question reply or `accept recommendations` from the user.
3. **No artifact production during a clarification round.** Surface questions, wait. Do not pre-draft.
4. **Minimum-necessary questions, not maximum.** Drop any question whose answer is inferable from spec state, or whose answer would not change a downstream artifact. The per-tier ceiling (Tier 1 = 10, Tier 2 = 6, Tier 3 = ≤4) is a guardrail, not a target — a round of 1–3 questions is normal and preferred when the input is well-formed.
5. **Recommendations come from evidence.** Vague "best practice" is a protocol violation.
6. **No customer names** in question text, options, or rationale.
7. **Read spec state first.** Never ask what is already recorded.
8. **One question = one decision.** No bundled choices.
9. **BLUF every round.** Open with one sentence on what's blocked.
10. **"Keep moving" applies to gates, not intake.** Project guidance to keep momentum at *gate-approval* stages does **not** authorize skipping or self-resolving an intake round. Intake is a hard stop until the user replies; the orchestrator enforces this.

---

## Anti-Patterns (Do Not Do These)

| Anti-pattern | Correct behavior |
|---|---|
| Surfacing the round and then continuing internally with the Recommended options | Surface and **stop**. Wait for the user's reply. Recording `chosen` without a user message is a protocol violation. |
| Framing the round as "applied defaults; user may override" in the return payload | The round is **either pending or user-resolved** — there is no provisional state. If the user has not answered, `ready_to_proceed` must be `false`. |
| Padding the round to the tier ceiling because it's allowed | Ask only what is genuinely undecided. The tier ceiling (10/6/≤4) is a guardrail, not a target. |
| Reading "Tier 3" as "skip intake" | Tier 3 scales the round *down* (≤4 questions), it does not remove it. Surface the focused round and pause. |
| Asking a question whose answer is already in spec state or the brain dump | Read first. If the answer is inferable with high confidence, drop the question — do not "confirm for safety". |
| Treating Step 0 as internal scaffolding for the agent's own planning | Step 0 is a user-facing pause, not an internal one. The user is the resolver, not the agent. |
| Dripping questions one per turn | Batch the round in one message (numbered 1..N). |
| 0 or 2 Recommended options | Exactly one Recommended per question |
| "Recommendation: best practice" | Cite a prior artifact, principle, DS convention, user impact, or constraint |
| Drafting "to save time" while waiting | No artifact production during a round |
| Re-asking a resolved clarification on loopback | Read `context.clarifications[]`; only ask deltas |
| 4th round in one phase | Escalate instead — phase is mis-scoped |

---

## Integration (Who Calls This)

| Caller | When | Question bank source |
|---|---|---|
| spec-orchestrator | Validates that intake round happened before each phase delegation | n/a (enforcer only) |
| discovery-agent | Step 0 + on ambiguity ≥ 2 | discovery-agent SKILL.md |
| research-agent | Step 0 + on ambiguity ≥ 2 | research-agent SKILL.md |
| prd-agent | Step 0 + on ambiguity ≥ 2 | prd-agent SKILL.md |
| ideation-agent | Step 0 + on ambiguity ≥ 2 | ideation-agent SKILL.md |
| flow-agent | Step 0 + on ambiguity ≥ 2 | flow-agent SKILL.md |
| prototype-agent | Step 0 + on ambiguity ≥ 2 | prototype-agent SKILL.md |
| spec-writer-agent | Step 0 + on ambiguity ≥ 2 | spec-writer-agent SKILL.md |

Skills (atomic, non-agent) never ask questions directly. If a skill detects ambiguity, it surfaces back to its parent agent, which then runs this protocol.

---

## Output Format (Final to Orchestrator after a Round)

```json
{
  "phase": N,
  "round": 1,
  "trigger": "intake | ambiguity | loopback",
  "questions_asked": N,
  "questions_resolved": N,
  "clarifications": [ /* per the capture format above */ ],
  "bulk_accept_used": true | false,
  "ready_to_proceed": true | false,
  "escalation_needed": true | false
}
```

If `ready_to_proceed: false`, the orchestrator blocks the phase and waits.
If `escalation_needed: true` (3rd round exhausted or score ≥ 4), the orchestrator surfaces an escalation message and recommends a re-run of an earlier phase.

---

## Version History

- **1.2.1** (2026-07-01): Scope-discipline addendum (no change to the two-stage capture contract). Trigger A now names the **scope-bearing intake** duties: Phase 1 intake must resolve the scope-lock inputs (tier, in/out scope, surface count, comparator count) so the orchestrator can lock `scope_lock` before the Problem Statement gate (item 1.12), and Phase 3 intake opens with a scope re-confirm (item 3.16) that records any change as a deliberate `scope_change`. A missing surface/comparator count counts as a critical (+2) ambiguity signal. The "v1.2 two-stage check" referenced elsewhere is unchanged.
- **1.2.0** (2026-07-01): Wired the per-round question ceiling to `meta.complexity_tier` so Tier-3 incremental work isn't crushed by Tier-1 intake overhead. Changes: (1) tiered ceiling — Tier 1 up to 10, Tier 2 up to 6, Tier 3 a focused few (≤ 4); (2) explicit "surface-and-pause is mandatory at every tier — only the count scales, never the pause" rule, with the two-stage capture (`chosen_via` + `user_message_ref`) unchanged for all tiers; (3) Tier-3 rounds drop anything the parent spec already answers (ties to Trigger C loopback); (4) new anti-pattern: "Tier 3" never means "skip intake." The "v1.2 two-stage check" the orchestrator and gate-checklists already cite refers to this capture format (round-exists + per-item evidence), now formalized as version 1.2.0.
- **1.1.0** (2026-05-12): Tightened the contract after a retro caught the agent self-applying Recommended defaults at Phase 1 intake and skipping Phase 2 intake entirely. Changes: (1) explicit surface-and-pause language in Trigger A and Hard Rules; (2) `chosen_via` restricted to `user_response` or `accept_recommendations_bulk`, with `user_message_ref` required as proof; (3) "minimum necessary, not maximum" rule for question count — the 10-question limit is a ceiling, not a target; (4) new anti-patterns covering provisional/"applied defaults" framings and padding to ceiling; (5) "keep moving" guidance scoped to gates, not intake.
- **1.0.0** (2026-05-11): Initial release. Up to 10 questions/round, up to 3 rounds/phase, ambiguity threshold ≥ 2, grounded-rationale requirement (concrete reason, not citation-strict).
