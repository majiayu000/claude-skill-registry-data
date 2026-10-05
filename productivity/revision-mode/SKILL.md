---
name: revision-mode
description: Use when a learner needs a structured review session prioritizing high-value topics by recency, error history, and upcoming deadlines.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [productivity, revision, exam-prep, retention]
status: stable
---

# Purpose

Run a structured, prioritized revision session targeting topics most likely to decay, most frequently missed, or most important for an upcoming deadline. Not random review — weighted prioritization to maximize learning per minute.

# Activation

- Upcoming deadline (interview, exam, demo) within 1–5 sessions. Learner requests review after a learning period. `weak-area-tracker` shows accumulated weak areas. 3+ sessions since last review.
- **Skip if**: learner needs new material first. Goal is project implementation → `build-with-me`. Only one topic to review → use `check-understanding`/`challenge-generator` directly.
- **Routing**: pull priorities from `weak-area-tracker`. Use `check-understanding` and `challenge-generator` as execution vehicles. After 3 consecutive clean revision passes on a topic: mark revision-complete and de-prioritize.

# Inputs

- Topics covered (from `learning-memory`), active weak areas, upcoming deadline + type, session time budget, self-assessed confidence per topic (optional).

# Priority Scoring (1–10)

- Weak area severity: 0–3 (from tracker). Recency (days since last review): 0–3. Deadline relevance: 0–2. Low self-reported confidence: 0–2.
- Score 7+ = must-revise. Score 4–6 = should-revise. Below 4 = defer.

# Workflow

1. **Scope** — Gather topics + weak areas. Ask: "Deadline? Least confident topics?" Apply priority scoring.
2. **Plan** — Present focused list: must-revise first, then should-revise if time permits. Cap at 4–5 topics max. State approach per topic: concept check / challenge / flashcard drill.
3. **Recap** — For each topic: ask learner to summarize in 2–3 sentences. Don't re-explain unless summary reveals a gap. 2–3 min cap per recap.
4. **Test** — 1–2 exercises per topic via `check-understanding` or `challenge-generator`. Mix modes. Run 3–5 due flashcards per topic if available.
5. **Check Exit** — Clean pass = correct response with correct reasoning on first attempt. After 3 clean passes across sessions: exit rotation. Below 50% pass rate this session: escalate to `misconception-detector`.
6. **Close** — Summarize: which topics are revision-complete, which need another round. Update `weak-area-tracker`. Recommend next session if deadline still approaching.

# Rules

- DO: revision is active — learner produces answers, not just reads.
- DO: include weak areas in every revision session until resolved.
- DO: state clean-pass criteria before the session, not after.
- DON'T: re-lecture topics the learner can summarize correctly — test immediately.
- DON'T: pack more than 5 topics per session.
- DON'T: skip the hardest topics in favor of comfortable ones — must-revise (7+) first.
- DON'T: let same topics appear indefinitely — enforce exit criteria.

# Output

Responses should contain: deadline + time budget, prioritized topic list (must-revise with scores and approach, should-revise if time permits), per-topic recall + test + outcome, and session summary (clean passes, still-needs-revision, exiting rotation, next session recommendation). Format naturally.

# Checklist

- [ ] Priority scoring applied before session plan.
- [ ] Must-revise topics addressed first.
- [ ] Every topic has at least one active retrieval exercise.
- [ ] Weak-area-tracker updated at session close.
