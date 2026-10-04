---
name: plan-intake
description: Interview the user in their language (and read what already exists) to write a product's context in docs/context — problem, users, domain, constraints, environments, and every open gap with owner and question. Use when the user says "entrevistame", "intake", "relevamiento", "contexto del proyecto", "tengo una idea", "armá el contexto", "gather requirements", when project-new reaches gate 1, or when a new feature needs context the project doesn't have. Only asks what the house harness doesn't already answer.
---

# Intake — only what this product needs, never invented

The house harness (stack, coding, testing, security, CI, agent protocol) is already decided and
inherited. This interview covers **only the product**: why it exists, who uses it, its domain,
its hard limits and its environments. Target: 15–25 questions, fewer when documents exist.

Read before starting: `references/question-bank.md` and `references/context-format.md`.

## 1. Harvest before asking

1. Ask once what already exists in writing and where (briefs, notes, decks, screenshots, a
   repo, links). List what you found and confirm the list before reading.
2. Read each source against the question bank. Pre-fill every question it answers, citing the
   source id (`S1`, `S2`…). A document that is undated, a draft, or contradicts another source
   is **to confirm**, not answered.
3. Existing repo: read the README, manifests, CI and top-level folders (structure and commands,
   not logic). What you derive is **inferred** until the user confirms it.
4. Show the delta before any question:
   ```
   Sources: 3 (S1–S3) · Answered by documents: 11/26 · To confirm: 4 · To ask: 11
   ```

## 2. Interview the delta

- At most 4 questions per turn, with the multiple-choice tool when the answer space is known,
  always with a free-text path and an "I don't know yet" option that records a gap.
- Accept only measurable answers: a number, a name, a date, a regulation, a concrete example.
  Re-probe a vague one once — "how would we know it holds?", "what number?", "what happens if
  it doesn't?" — then record a gap instead of writing the vague version.
- High-signal probes: the last time this problem hurt (a concrete story), what they use today
  and why it fails, what would make them abandon the product, the rule that must never break.
- Separate wish from requirement: "is it required to launch, or where you want to get to?"
  Wishes go to the PRD's later scope, not to constraints.
- Three unanswered in a row in one block → stop the block, record gaps with the right owner,
  move on.

## 3. Write docs/context

Write the five files exactly as `references/context-format.md` shows:
`product.md`, `domain.md`, `constraints.md`, `environments.md`, `gaps.md`.

- **Never invent.** No source, no fact: write `[GAP-nnn]` inline and add the row to `gaps.md`
  (file, what's missing, owner, exact question, blocking yes/no).
- Every fact carries its source id; inferred facts are marked `(inferred, S3)`.
- Constraints are written as `[MUST]` / `[MUST NOT]` with something measurable; if breaking it
  has no named consequence, it is not a constraint — move it to the PRD.
- Rules that must never break (D03–D03d) become invariants in `domain.md`: `[INV-nnn]`, the rule,
  `class: <class>` and the source. Ask how it breaks to pick the class; two ways → two
  invariants. Ids never change or get reused. Money, one-time side effects, limits and other
  people's data are where the worst bugs live: don't close the domain block without asking.
- No vague phrases ("robust", "user-friendly", "best practices"…) — `python3 .keelokit/bin/doctor.py` rejects them.
- No secrets, no personal data of real people; accounts are named by owner, never with values.

## 4. Keep the profile true

If the project has `.keelokit/profile.toml`, update its `traits` from what the context now says:
`personal-data` when it stores anything that identifies a person, `payments` when money moves,
`i18n` for more than one language, `developer-facing` when its users are developers. A new
feature that needs something new (an API, a database, a mobile app, hosting) adds it too — and
say so to the user: it changes which rules apply and what the bug bash hunts.

## 5. Check and hand back

1. If the project has `.keelokit/bin/doctor.py`, run it and fix every `docs/context` error.
2. For a deep review, delegate to the `context-auditor` agent (it didn't write the context, so it
   catches invention and vagueness the author misses).
3. Report: sources used, questions asked, gaps open by owner (blocking first), and the questions
   to ask next.

Resumable: the files on disk are the state. On a new session, read `docs/context/` and
`gaps.md`, say what is covered and continue with the open gaps.
