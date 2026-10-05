---
name: clarify-work
description: Clarify non-trivial engineering work before implementation by resolving ambiguity, terminology, constraints, and the smallest viable path. Use when a request is broad, fuzzy, architectural, cross-cutting, or has hidden product decisions.
---

# Clarify Work

Use this before implementation when the request is not already issue-sized.

## Workflow

1. Restate the outcome in one sentence.
2. Name assumptions and unknowns that can change the implementation.
3. Keep only unknowns that block a safe, issue-shaped execution boundary. Estimate the initial number of blocking questions from all available context before asking any. Prefer 1-3 by omitting non-blocking questions, not by combining unrelated decisions.
4. If the estimate is zero, skip the interview and continue to the execution boundary.
5. Ask exactly one blocking question per user turn, then wait for the answer. Prefix each planned question with `Question n/N · [bar]`, where `N` is the initial estimate. Render the bar with exactly `N` cells: `n` filled `■` cells followed by `N - n` empty `□` cells.
6. After each answer, reassess the current blocker and the remaining blockers. Treat an incomplete or ambiguous answer, or a newly discovered blocker, as a follow-up labeled `Follow-up k (after Question n/N) · [bar]`. Keep the original `N`; do not advance `n` or consume the next planned question until the current blocker is resolved. Render the follow-up bar at position `n`, without changing `N`.
7. When no blocking questions remain, identify the planning track: quick, standard, or deep.
8. State the smallest viable approach and non-goals.
9. Convert broad work into issue-shaped execution units when needed.

## Output

- Outcome
- Assumptions
- Open questions
- Suggested execution boundary
- Verification signal

## Guardrails

- Do not plan around hypothetical future requirements.
- During the interview, include only the current question and context needed to answer it.
- Do not start implementation while key terms or ownership boundaries are unclear.
- When project terminology or documented decisions change during clarification, record the outcome in the project's domain docs (glossary, ADRs) before implementation starts.
