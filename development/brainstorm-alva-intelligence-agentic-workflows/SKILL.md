---
name: brainstorm
description: Run the brainstorming phase — resolve ambiguity from real service state, decide the obvious yourself, ask the user only for what genuinely needs them
---

# Brainstorming

Sharpens scope. The orchestrator loads the latest state of every relevant service, resolves every
ambiguity it can from evidence and best judgment, records those as decided facts, and asks the user
only for decisions that are genuinely ambiguous, a matter of taste, or expensive to reverse.
**Zero questions is a valid outcome.** Next phase: `prd_creation` for features,
`implementation` directly for bugs/improvements (no PRD).

**Read `references/question-patterns.md`** for question shape and pitfalls.

## Inputs (from `.workflow-state.json`)

- `active_feature`, `worker`
- `features[active_feature].type` — feature | bug | improvement
- `features[active_feature].initial_request` — raw user intake

## Outputs (back to `.workflow-state.json`)

- `brainstorming.service_state_snapshots` — per-service short snapshot
- `brainstorming.questions[]` — `{ id, prompt, options[], answer }` — only questions actually asked
- `brainstorming.decisions[]` — `{ topic, decision, rationale }` — obvious answers decided by the agent
- `brainstorming.summary` — 3–8 sentence direction
- `brainstorming.completed_at`
- `features[active_feature].phase_status = "completed"` (`"inprogress"` at start; do NOT auto-advance)

## Process

### Step 0: Activate phase

Flip `features[active_feature].phase_status` to `"inprogress"` in `.workflow-state.json`.
If the user asked to **skip** brainstorming, record `brainstorming.user_skipped = true`, write a
one-line summary of the request as-is, flip to `"completed"`, and move to the next phase.

### Step 1: Load latest service state

Identify candidate services from `initial_request`. For each, build a short snapshot with
grep/read of the actual code (paths, key symbols, recent behavior) — no code-graph MCP anywhere.

For external behavior (third-party SDKs, APIs, frameworks) where your training data may be stale,
use web search/fetch. Save under `brainstorming.external_state_snapshots[<vendor>]` with URL + fact.

### Step 2: Resolve ambiguity — evidence first, ask last

Walk every branch of the decision tree implied by `initial_request`. Resolve each one in order:

1. **Codebase first.** If the code, PRDs, or service state answers it, do that.
2. **Web search second.** External vendor/SDK/framework behavior. Cite the URL.
3. **Obvious answer → decide it yourself.** If the answer is obvious from convention, existing
   system behavior, or plain best practice, pick the best option and record it as a **decision**:
   `{ topic, decision, rationale }`. Do NOT ask the user for it. "No" is an acceptable answer if
   the user pushes back — stop that branch and record it.
4. **Ask the user last.** Only genuinely ambiguous, taste, or expensive-to-reverse calls become
   questions. No quotas.

### Step 3: Produce unresolved questions (often zero)

Only what survived Step 2 becomes `questions[]`: `{id, topic, options[], recommended_label,
rationale}`, `recommended: true` on exactly one option. Everything else is already a fact in
`decisions[]` or `summary`.

Fold questions into ONE structured ask (harness's ask tool, up to 4 questions in one call). If the
user answers something in free text, record it. If the user says **"no"** or declines a direction:
stop that branch cleanly, record the answer.

### Step 4: Write the summary

3–8 sentences. Facts resolved via codebase/web, the decisions taken by judgment (one line of
rationale each), and the direction. Save to `brainstorming.summary`; set `completed_at`.

### Step 5: Mark phase completed and stop

Flip `phase_status` to `"completed"`. Do NOT auto-advance. Tell the user the direction and that
the next phase is `/workflow next` — for bugs/improvements that lands straight in implementation.

## When to use

- New feature/bug/improvement filed via `/workflow start <slug>`.
- Resuming a feature still in `brainstorming`.

## When NOT to use

- The user says "skip brainstorming" — record and move on (Step 0).
- The user already supplied a complete PRD: one confirmation question ("validate it against
  current service state, or just register it?"), one-line summary citing their PRD.
