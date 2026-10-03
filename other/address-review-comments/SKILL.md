---
name: address-review-comments
description: Analyze, decide on, challenge, and implement a PR's open review comments end to end, with a human in the loop. Use when addressing PR review feedback, responding to reviewer comments, or when the user says "address review comments".
argument-hint: "[PR number — defaults to the current branch's PR]"
---

# Address review comments

Take the open review comments on a PR from "what is the reviewer really asking" through to an implemented, replied-to resolution. You steer; the human decides every judgment call. Handles every open thread, human or bot. Closed and resolved threads are context only.

## Process

### 1. Gather

Resolve the PR (the argument, or the current branch's PR via `gh pr view`). Pull its open review threads through `gh` / the GraphQL API: each comment with its file, line, author, body, and thread state. Resolved threads are context, not work. Always read the **actual current code**, not your recollection of it; the user may have changed it.

### 2. Triage

Sort each open thread into:

- **settled** — a pure mechanical fix, or the author already agreed an approach in-thread. Goes straight to implementation.
- **needs a decision** — everything else.

### 3. Decide (no code yet)

For each *needs a decision* thread, investigate the reviewer's underlying concern, not just the symptom they pointed at, until you can lay out the realistic options with their trade-offs. Then route by what is actually in dispute:

- **Correctness dispute** ("this finding is wrong / a false positive"): spawn a validator subagent that adversarially re-checks the finding against the actual code, given the user's rebuttal. One round only. It returns **concede** (a false positive, with a code-grounded reason) or **defend** (the issue holds, with the concrete evidence). Bias to concede when it cannot defend with evidence: the user raised the doubt, so the burden is on the finding.
- **Design or approach decision**: route through the `/grilling` skill rather than settling it unilaterally; always provide your recommended answer. If the comment opens an architectural, ADR-worthy decision (hard to reverse, or it shifts a documented term or boundary), run `/domain-modeling` alongside, so the resolution lands in the repo's vocabulary or an ADR.

No code is written in this phase. The goal is alignment. The validator and the grilling session inform the decision; **the user is the final authority** on every thread.

### 4. Checkpoint

If anything went through step 3, present a per-thread summary — the concern, the options considered, the decision reached, and the concrete change or an explicit "leave as-is" with rationale — and get the user's sign-off before implementing. When every thread was already settled, skip straight to implementation.

### 5. Implement

Apply the agreed changes. Each fix targets only what its comment raised: no opportunistic cleanup, no unrelated refactors, no removing ticket-referenced TODOs. Note any tangential improvements separately in the summary and ask before touching them.

### 6. Reply and resolve

Ask the user whether to commit/push and whether to reply to the threads. Then, per thread, post a single reply and set its state:

- **Addressed by a change** → reply with the rationale and "Addressed in `<commit>`."; resolve the thread (GraphQL `resolveReviewThread`).
- **Agreed, no change needed / confirmed correct** → a thumbs-up or short acknowledgement; resolve.
- **Conceded challenge** (the finding was a false positive) → reply that it was retracted as a false positive and why; resolve.
- **Leave-as-is** (intentional, out-of-scope, or a finding the user overrides after it was defended) → reply with the rationale but leave the thread **open**. Never unilaterally close a disagreement.

## Invariants

- The user may change the code at any point; work from, and commit, the actual current state, not your recollection.
- Only change what each comment asks for.
- The human is the final authority on every thread; validators and grilling sessions inform, they do not decide.
- A conceded challenge and a leave-as-is pushback are both signals the review retro will later read. Reply and (for concessions) resolve them honestly; do not scrub the disagreement record.
