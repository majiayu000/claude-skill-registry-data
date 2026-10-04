---
name: mandate-conversion
description: "No-loss protocol for changing an existing mandate's output contract. Use when changing what an agent or mandate emits or how it is typed: binding a kind, declaring output_kind, kind-backfill batches, provision reconciliation, or any make-this-contract-honest sweep. NOT for creating a new agent (use create-agent)."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/mandate-conversion/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# mandate-conversion — change the contract, lose nothing

## THE LAW (Arman, 2026-08-25)

> "If one piece of data stops being passed the way it needs to be or one little thing is
> lost, then the application degrades silently! That's not an option!!!!"

A conversion is not "done" when the mandate declares a kind and the tests are green. It is
done when you can **show the payload before and after and prove nothing a consumer reads
disappeared**. Silent degradation is the only unacceptable outcome — worse than not doing
the work at all, because a broken thing that still returns 200 gets discovered by a customer.

**Evidence or it did not happen.** Every claim in your report is a diff, a count, or a
`file:line`. Prose is a rejected report — the same rule
[agent-provision](/skills/agent-provision/SKILL.md) applies to Briefs, for the same reason:
reflection has no failure state, so it always succeeds.

**Sibling skills.** Creating a new agent → [create-agent](/skills/create-agent/SKILL.md).
Designing what a call site offers (the Brief, answerability) →
[agent-provision](/skills/agent-provision/SKILL.md). This skill owns changing an existing
contract — a registered kind or honest text — without losing a field anyone downstream reads.

## 🚨 THE KIND-NARROWING TRAP — the thing that already bit us

**Measured 2026-08-25, live, on work this campaign shipped:** the Study Quiz agent's own
schema requires a per-question `trust` object (its grounding evidence — chunk ids, excerpts,
confidence). The registered `quiz_set` kind has **no room for it**. `ai.agent.produce` binds
the KIND's schema to the provider, and the kind's schema sits ABOVE the agent's. Result: the
agent produced citations, the kind stripped them, **nothing errored**, and the artifact
looked perfect. Filed as feedback `499a460f`.

**The generalization, and it is the whole reason this skill exists:**

> A kind is frequently a NARROWER contract than the agent that fills it. Binding a kind is
> therefore a potential DATA-DELETION event, and it is invisible unless you diff.

So: **never bind a kind to an agent without diffing the agent's own schema against the
kind's schema, field by field, including nested objects.** If the agent emits a field the
kind cannot hold, you have exactly three honest moves — widen the kind, keep the mandate on
`required_output_keys` until the kind can hold it, or (only with evidence nobody reads the
field) drop it deliberately and say so in writing. Silently letting the binding eat it is
the one forbidden move.

Related live instances of the same disease class, for calibration:
- `flashcard_set.cards` was a bare array — the item kind existed but was inactive, so every
  card's declared shape was unenforced.
- `research.coverage_audit` / `source_authority` agents emitted `__kind` values that were
  never registered anywhere — "phantom kinds", stamping a type that did not exist.
- `education.summarize` / `notes_generate` answer `{…, trust}`; `study_notes` has **no**
  `trust` field. Binding them to it would delete every citation in the education product.

## The protocol

Run these in order. Steps 1–3 happen BEFORE you change anything.

### 1. Capture the truth — a real payload, from a real run

Run the mandate's live agent on realistic input and **save the complete raw output**. Not a
summary of it. This artifact is your baseline; every later claim is measured against it.

- Variable-driven agent → `agent_run` with real variables.
- Conversational agent → `agent_run` with `user_message`.
- If it only runs inside a workflow/pipeline, run that and capture the node's output.
- **A conversion whose baseline you could not capture is a conversion you may not perform.**
  Say so and stop; that is a finding, not a blocker to route around.

### 2. The consumer census — every reader of every field

Enumerate, with `file:line`, **every** consumer in **both** repos (server and client, plus
any package or workflow node):

| Field in the payload | Who reads it | Where it lands |
|---|---|---|
| `questions[].trust` | `features/…/x.ts:NN` | `assessment_item.trust` |

Rules that make this census real rather than performed:
- Grep the field NAME, not just the mandate key — parsers read keys, not mandates.
- Include the **persistence** target: a field written to a column is read by everything that
  ever selects that column.
- Include **replay/history** surfaces: stored artifacts are re-rendered later; a field that
  vanishes today still exists in old rows and its renderer must not break.
- A field with **zero** consumers is your best find — record the evidence, and it becomes a
  legitimate candidate for deliberate removal. 🚨 **BUT a zero-consumer claim is the one
  census result that can license DELETION, so it is never accepted from a single pass**
  (adversarial finding, 2026-08-26): batch 2 claimed `commentary`/`wrap_rating` had "zero
  consumers, grepped both repos" while both were load-bearing — one WAS the agent's spoken
  turn, the other governed stage advancement. Before any zero-consumer claim may justify a
  removal: (a) grep the field name in BOTH repos including bracket/dict access patterns
  (`structured["field"]`, `.get("field")`, destructuring), (b) read the actual consumer
  module end to end rather than trusting grep absence, and (c) the claim must survive the
  batch's adversarial verification before anyone acts on it. Until then it is a candidate,
  never a license.

### 3. The narrowing diff — agent schema vs target kind

Field-by-field, including nested objects and array items:

| Agent emits | Kind holds | Verdict |
|---|---|---|
| `questions[].trust` | — | ❌ WOULD BE STRIPPED |

Any ❌ stops the conversion until you choose a door and write down which:
**widen the kind** · **keep `required_output_keys` and defer the kind** · **drop it
deliberately**, with the zero-consumer evidence from step 2.

### 4. Make the change — all layers, together

A half-converted contract is worse than an unconverted one. In the same change:
the **mandate** (`output_kind`, `required_output_keys`, `accepts_user_input`), the
**provision** (offered values reconciled to what the call site really sends — see
[agent-provision](/skills/agent-provision/SKILL.md)), the **agent** (its prompt must state
the exact output shape it is now bound to; a prompt that describes a different shape than
the schema is the drift this campaign keeps finding), and the **consumers** if a reader must
change.

**Report hygiene (adversarial findings, 2026-08-26):** run ids are `chat.agent_run` /
workflow run ids — never present an agent VERSION id as a run id. And never write a kind's
activation state into a code comment from a stale check: the Kind Architect completes
server-side after client timeouts (proven twice), so re-verify by SQL immediately before
writing any "inactive"/"active" claim into code or the register.

### 5. Prove it — the after-capture and the diff

Re-run **the same input** from step 1. Then produce, in the report:

1. **The field diff**: before-fields vs after-fields. Every removal explained or reverted.
2. **The consumer check**: for each row of the step-2 census, does that read still resolve?
3. **A content read.** `success: true` is not evidence. Read the output and judge it against
   the job. If quality dropped, that is a finding — report it, do not bury it.
4. **The gate results**: `output_kind_ok`, schema validation, the test suites.

### 6. Batch discipline

**10–15 mandates per agent, maximum** (Arman, 2026-08-25). One cluster per batch where
possible — mandates that share a provision or a kind fail together and must be reasoned
about together. Never split one kind's consumers across two batches: whoever widens a kind
owns every mandate bound to it in that same batch.

## The report format — nothing else is accepted

Per mandate:

```
mandate: education.quiz_generate_from_source
baseline run: <run id / captured payload location>
census: 6 consumers (file:line each), 1 field with zero readers (`difficulty`)
narrowing diff: 1 ❌ — questions[].trust has no home in quiz_set
  → door taken: WIDEN the kind (kind updated to vN, edge added)
after-run: <run id>  | field diff: 0 removals
consumers re-checked: 6/6 resolve
content read: "distractors are real misconceptions; one question thin on section 4"
gates: output_kind_ok true · 14 tests green
```

## Hard rules

- ❌ Never bind a kind without the narrowing diff. This is the trap that already fired.
- ❌ Never report a conversion from `success: true`. Read the content.
- ❌ Never fabricate a kind client-side to "wrap" an agent's output (`study_summary` was
  invented in the browser around an agent payload of a different shape — a fake type over
  real data is worse than no type).
- ❌ Never let a mandate declare a kind that is not registered and active — phantom kinds
  stamp a type nothing can resolve.
- ❌ Never mint a kind to make a conversion fit. Kinds go through
  [data-to-kinds](/skills/data-to-kinds/SKILL.md); no agent mints one.
- ✅ A field with zero consumers, proven, may be dropped — say so explicitly.
- ✅ "This one cannot be converted honestly yet" is a successful outcome when the evidence
  says so. Blocked-with-evidence beats converted-and-lying.
