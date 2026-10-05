---
name: review-initiative-split
description: Blind-review `TASK_GRAPH.md` and optional `SPLIT_OPTIONS.md`, then write `SPLIT_REVIEW.md` with a ready/not_ready verdict before any child packets are hydrated.
---

# review-initiative-split

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/final-state-authoring-policy.md`
- initiative `INDEX.md`, `BRIEF.md`, `UBIQUITOUS_LANGUAGE.md`, `DECISIONS.md`, `INVARIANTS.md`, `REPO_MAP.md`, `CONTRACTS.md`, `TASK_GRAPH.md`, `OPEN_QUESTIONS.md`
- optional `SPLIT_OPTIONS.md`
- `../../references/communication-mode.md`

## Review for
- child tasks are independently understandable
- dependencies are explicit and sane
- child scope / out-of-scope / validation fit are explicit enough for later hydration
- contract surfaces are named where they matter
- `Packet Root` is explicit and sane for every child
- task graph does not hide critical shared context outside the initiative packet
- child-status names and sequencing match the canonical contract exactly

## Output
Write `SPLIT_REVIEW.md` with:
- `Verdict: ready | not_ready`
- findings `S#`
- required changes
- preserve notes

## Status
- on `not_ready`, return initiative `Status: split_drafting`
- on `ready`, set initiative `Status: active`

## Do not
- rescue ambiguous split logic with remembered chat context
- leave split approval implicit in chat only

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
