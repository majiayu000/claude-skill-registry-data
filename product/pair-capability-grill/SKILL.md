---
name: pair-capability-grill
description: "Interviews one question at a time, always with a recommendation, after exploring the KB/codebase first; sync mode drives systematic AI-human alignment on a story until shared understanding is confirmed. Invoke directly to interview on any topic ('grill me on the requirements'). Composed by /pair-process-refine-story and a future /brainstorm (planned — #230). Write-free — returns the synthesis, never writes adoption or issues."
version: 0.4.1
author: Foomakers
---

# /pair-capability-grill — Interview Engine

Ask one question at a time, always with a recommended answer, after exploring the KB/codebase for anything already answerable. `interview` mode explores a free topic; `sync` mode systematically aligns AI and human on every aspect of a story. Never writes — returns the synthesis to the caller.

## Core Rules

- **Never answer for the human.** The recommendation attached to each question is a proposal, not a stand-in for consent. If no reply has been given, the turn ends and the session waits for real input — treating a missing reply as acceptance, or drafting what the human "would probably say," breaks the interview. Grill is HITL by design.
- **One question per turn.** Ask exactly one question at a time; never batch multiple questions.
- **Write-free.** Never write adoption files or PM tool issues in any mode; the only file grill ever writes is the optional `.pair/working/` handoff, on request or interruption.

## Arguments

| Argument   | Required   | Description                                                                                                                    |
| ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `$mode`    | No         | `interview` (default) or `sync`.                                                                                                 |
| `$topic`   | No         | Freeform subject to explore in `interview` mode. If omitted, the opening question asks for it.                                  |
| `$story`   | Conditional| Target story identifier. Required for `sync` mode unless the composing skill already supplies a loaded story via `$context`.    |
| `$context` | No         | Caller-supplied context bundle (e.g. brainstorm's seed text, refine-story's current story body) so grill skips re-fetching it.   |
| `$aspects` | No         | Comma-separated subset of the [Sync Coverage Checklist](#sync-coverage-checklist) to focus on (e.g. `risks,dependencies`). `sync` only. If omitted, all six aspects are covered.|

## Modes

### Interview Mode (default)

Freeform exploration of `$topic`. No fixed checklist — the question queue grows from what Step 1's exploration leaves open and from what answers reveal. Used standalone or composed by `/brainstorm` (phase 1, planned — #230) to produce a raw requirements blob.

### Sync Mode

Systematic AI↔human alignment on a specific story, covering all six aspects of the [Sync Coverage Checklist](#sync-coverage-checklist) (goal, AC, edge cases, dependencies, design, risks). Ends only at explicit shared-understanding confirmation. Used standalone (e.g. "sync me on #42") or composed by `/pair-process-refine-story` phase 0.

## Algorithm

### Step 0: Detect Mode and Target

1. **Check**: Is `$mode` provided?
2. **Skip**: If provided, use it.
3. **Act**: Default to `interview` when omitted.
4. **Act**: If `$mode: sync`, resolve the target story:
   - Use `$story` if provided.
   - Else use a story already loaded by the composing skill via `$context`.
   - Else **HALT**: "sync mode needs a target story — provide `$story` or invoke via `/pair-process-refine-story`."
5. **Verify**: Mode is `interview` or `sync`; for `sync`, a target story is resolved.

### Step 1: Explore Before Asking

1. **Act**: Before drafting any question, gather what is already knowable:
   - `interview`: read the [PRD](../../../.pair/adoption/product/PRD.md), related epics/issues (per [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md)), and grep the codebase for the topic's terms.
   - `sync`: read the target story's current body (sections already populated), [architecture.md](../../../.pair/adoption/tech/architecture.md), [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md), [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md), prior decisions in decision-log/adr, and the codebase for the touched components.
2. **Act**: For every fact resolvable this way, mark it **explored** with its source. It is never asked — anything answerable by exploring KB/codebase is explored instead of asked.
3. **Verify**: An explored/unresolved map exists before the first question is asked.

### Step 2: Build the Question Queue

1. **Check**: `interview` or `sync`?
2. **Act (interview)**: Decompose `$topic` into the open sub-questions left after Step 1. If `$topic` is omitted, the opening question of the queue is simply "what's the topic?". The queue has no fixed size — it grows as answers reveal new sub-questions.
3. **Act (sync)**: Take the [Sync Coverage Checklist](#sync-coverage-checklist), restricted to `$aspects` if given. Drop any aspect fully resolved in Step 1; queue the remaining aspects in checklist order (already risk-ordered).
4. **Verify**: Queue built — topic-driven (interview) or checklist-driven (sync).

### Step 3: Ask One Question at a Time

1. **Act**: Pop the next queue item. Ask exactly one question, always with a recommended answer derived from Step 1's findings, project precedent, or best judgment:

   > [Question]?
   > **Recommendation**: [proposed answer] — [why].

2. **Act**: Read the human's reply:
   - **Accepts the recommendation** → record it as the answer.
   - **Gives a different answer** → record that instead.
   - **"Don't know"** → the recommendation becomes the **provisional answer**, flagged as an assumption in the synthesis.
   - **Raises a new sub-question** → insert it into the queue before continuing.
3. **Never answer on the human's behalf.** The recommendation is a proposal, not a stand-in for consent — if no reply has been given yet, the turn ends and the session waits for real input. Treating a missing reply as acceptance, or drafting what the human "would probably say," breaks the interview: grill is HITL by design.
4. **Verify**: Exactly one answer recorded per question. Never batch multiple questions in a single turn.

### Step 4: Repeat Until Explicit Shared Understanding

1. **Check**: Is the queue empty?
2. **Skip**: If not empty, return to Step 3.
3. **Act**: When the queue empties, ask directly:

   > Do we have shared understanding here? (yes / no — anything to add?)

4. **Verify**: Only an explicit **yes** ends the session. A **no**, or any new concern raised, adds items to the queue and returns to Step 3. The session never auto-exits on an empty queue alone.

### Step 5: Assemble the Synthesis

1. **Act**: Compile recorded answers, explored facts (with source), and flagged assumptions:
   - `interview` → raw requirements blob (topic, findings per sub-question, open items, assumptions).
   - `sync` → alignment synthesis mapped to the six [Sync Coverage Checklist](#sync-coverage-checklist) aspects, ready to drop into the matching [user-story-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/user-story-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)) sections.
2. **Verify**: Synthesis accounts for every answered/explored/assumed item — nothing silently dropped.

### Step 6: Return — Never Write

1. **Act**: Return the synthesis to the caller (composed invocation) or print it in conversation (standalone). **Never** write to adoption files or PM tool issues in either mode — that stays with the composer (`/brainstorm`, `/pair-process-refine-story`) or the human.
2. **Act (standalone, or session interrupted before Step 4's explicit yes)**: Offer an optional handoff file:

   > Save this as a handoff file in `.pair/working/`? (y/n)

   If yes, create `.pair/working/` if it doesn't exist and write `grill-<mode>-<slug>-<YYYYMMDD-HHMM>.md` with the synthesis-so-far plus per-aspect/per-topic coverage state (covered / explored / open).
3. **Verify**: No adoption or PM tool write occurred, regardless of mode or handoff.

## Sync Coverage Checklist

Ordered by risk of omission, except Goal always first — it anchors every other aspect; the remaining five follow the story template's functional-first, technical-last order.

| # | Aspect       | Story Template Section(s)                                                          | Explore First                                                     | Sample Probe                                             |
| - | ------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------- |
| 1 | Goal         | Story Statement                                                                       | PRD, parent epic body                                               | "As a [persona], I want [outcome], so that [benefit] — confirm or adjust?" |
| 2 | AC           | Acceptance Criteria → Functional Requirements (Given-When-Then), Business Rules      | Story's existing AC draft, similar refined stories                 | One Given-When-Then scenario at a time                    |
| 3 | Edge Cases   | Edge Cases and Error Handling                                                         | Codebase error-handling patterns, existing edge cases on the story | "What happens when [input/dependency] fails?"              |
| 4 | Dependencies | Dependencies and Coordination                                                         | PM tool backlog graph, epic breakdown                               | "Does this depend on, or block, another story?"            |
| 5 | Design       | Technical Analysis → Implementation Approach, Key Components, Integration Points     | architecture.md, tech-stack.md, codebase                           | "Which existing component/pattern implements this?"        |
| 6 | Risks        | Technical Risks and Mitigation                                                        | Story's existing risk table, decision-log/adr precedent            | "What's most likely to break or slip here?"                |

Aspects already covered by Step 1's exploration, or answered earlier in the same conversation, are skipped and marked explored rather than asked — the checklist stays fixed, but only genuinely open aspects consume a question.

## Output Format

```text
GRILL SESSION COMPLETE:
├── Mode:        [interview | sync]
├── Topic/Story: [topic string | #ID: Title]
├── Coverage:    [N/6 aspects covered (sync) | topics explored: list (interview)]
├── Assumptions: [list of "don't know" → recommendation-as-assumption items, or none]
├── Explored:    [KB/codebase sources consulted instead of asked]
├── Confirmed:   [explicit shared understanding: Yes]
└── Handoff:     [None | .pair/working/<file>]

SYNTHESIS:
[the raw requirements blob (interview) or the six-aspect alignment synthesis (sync)]
```

## Composition Interface

When composed by `/brainstorm` (phase 1, planned — #230):

- **Input**: `$mode` omitted (defaults `interview`); `$topic` from the free theme text or the `$root` issue's body; `$context` carries the issue if `$root` was given.
- **Output**: Returns the raw requirements blob (R3.7). `/brainstorm` carries it into phase 2 (domain integration) — grill never touches the PM tool or adoption files itself.

When composed by `/pair-process-refine-story` (phase 0, future extension):

- **Input**: `$mode: sync`; `$story` is the story being refined; `$context` carries the current (possibly partial) story body so grill doesn't re-fetch it.
- **Output**: Returns the alignment synthesis, pre-mapped to Refined User Story Template sections. `/pair-process-refine-story` merges it into the body it writes via `/pair-capability-write-issue` — grill itself never calls `/pair-capability-write-issue`.

When invoked **standalone**:

- No composition context required (decision Q8). `$mode` defaults to `interview`; if `$topic` is also omitted, the opening question asks for it directly. `sync` still requires `$story`.
- Synthesis is printed in conversation. A handoff file in `.pair/working/` is offered, never written silently.

## Example Transcripts

### Interview Mode (standalone, free topic)

```text
> /grill
AI:  What's the topic?
     Recommendation: none — this is genuinely open, your call.
You: caching strategy for the API layer
AI:  [explores codebase: finds no cache layer; checks tech-stack.md: Redis already adopted]
     Redis is already in tech-stack.md but unused for caching — reuse it or introduce another store?
     Recommendation: reuse Redis — avoids a new dependency.
You: don't know
AI:  [records "reuse Redis" as provisional answer, flagged as assumption]
     What's the target cache TTL?
     Recommendation: 5 minutes — matches the existing session-token TTL in auth config.
You: agreed
AI:  Do we have shared understanding here? (yes / no)
You: yes
AI:  GRILL SESSION COMPLETE — Mode: interview · Assumptions: 1 (store choice) · Handoff: none
```

### Sync Mode (composed by /pair-process-refine-story, phase 0)

```text
$mode: sync, $story: #142, $context: <current draft body>
AI:  [explores story body: Goal and AC present; Design, Risks missing]
     Goal and AC already covered — skipping.
     Who owns retry logic if the downstream call times out — caller or this story?
     Recommendation: this story — the caller has no visibility into the downstream contract.
You: agreed
AI:  [continues through Edge Cases, Dependencies, Design]
     What's most likely to break or slip here?
     Recommendation: the third-party rate limit — unconfirmed quota.
You: yes, flag that
AI:  Do we have shared understanding here? (yes / no)
You: yes
AI:  GRILL SESSION COMPLETE — Mode: sync · Coverage: 6/6 · returns alignment synthesis to /refine-story
```

## Edge Cases and Error Handling

- **User answers "don't know"**: the recommendation becomes the provisional answer, flagged as an assumption in the synthesis — never silently dropped, never blocking.
- **Session interrupted** (human stops, connection drops, or the composing skill's turn budget ends) before Step 4's explicit confirmation: offer the partial synthesis as a handoff file in `.pair/working/` rather than discarding it.
- **Aspect already answered earlier in the same conversation**: skip it, mark it explored with a reference to where it was answered — never re-ask.

## HALT Conditions

- `$mode: sync` with no `$story` resolvable from arguments or composer context (Step 0).

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (composing skill not installed → this skill still runs standalone) for the standard scenarios. Additional cases:

- If KB/codebase exploration is unavailable (no repo access), skip Step 1 (nothing marked explored), ask every aspect/topic question directly, and note in the synthesis that explore-first was skipped.
- If `.pair/working/` cannot be created or written, present the handoff content inline in conversation and tell the human to save it manually.

## Notes

- **Write-free by design**: single-writer responsibility stays with composers. Grill never writes adoption files or PM tool issues in any mode; the only file it ever writes is the optional `.pair/working/` handoff, on request or interruption.
- **Recommendation always present**: every question carries a recommended answer, adapted from mattpocock `grilling`.
- **Never auto-exit**: the exit condition is always an explicit shared-understanding confirmation — an empty question queue alone is not enough to end a session.
- The `.pair/working/` handoff format here is a minimal, self-contained default — expect it to align with the checkpoint capability once that lands, without changing grill's write-free contract.
