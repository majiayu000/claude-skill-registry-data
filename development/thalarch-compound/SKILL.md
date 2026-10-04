---
name: thalarch-compound
description: >
  Extracts reusable, verified engineering knowledge after difficult tasks so future work gets
  cheaper. Use after a non-trivial bug fix, architecture discovery, recurring failure, benchmark,
  or review that revealed a stable lesson. Routes useful outcomes through thalarch-experience,
  thalarch-memory, and optionally thalarch-project-brain while rejecting guesses, sensitive data,
  task-specific noise, and overbroad generalization.
---

# Thalarch Compound

A completed task may contain knowledge worth keeping. Compounding is the **post-task learning gate**,
not automatic persistence.

## 1. Candidate lesson

A lesson qualifies only if:

- supported by evidence from this run;
- likely to matter again;
- not obvious from ordinary code reading;
- stable enough to outlive this task;
- compact enough to retrieve without flooding future context.

Examples:

- a hidden build/test prerequisite;
- an ownership/lifecycle invariant;
- a recurring integration contract;
- a reliable diagnostic command;
- a repository-specific convention;
- a failure pattern and its proven discriminator;
- a benchmark/teacher finding that generalizes beyond one case.

## 2. Distill through experience

For meaningful outcomes, use `thalarch-experience` to convert the final evidence ledger into a
compact card:

`trigger → context → problem → discriminator → intervention → evidence → transfer → counterexample`.

Preserve useful disproven approaches when they prevent a realistic future mistake. Do not preserve
the debugging transcript or private chain-of-thought.

## 3. Classify memory

Pass the distilled candidate through `thalarch-memory`:

- `IGNORE` — weak, obvious, duplicate, noisy, or non-reusable;
- `SESSION` — useful only to finish/recover the current task;
- `PROJECT` — durable repository/product knowledge;
- `GENERAL` — transferable engineering knowledge with a strong generalization basis.

A single successful anecdote should not automatically become `GENERAL`.

## 4. Persistence boundary

Store, by default, only in the current work artifact/ledger.

Durable persistence requires an authorized sink. Do not modify `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`,
repository docs, `.thalarch/brain/`, or user-level memory merely because a lesson exists.

When project-local durable memory is explicitly authorized, use `thalarch-project-brain` and prefer
updating/deduplicating an existing entry over appending another near-duplicate.

When a host-native durable memory/RAG system is authorized, use it through `thalarch-memory` with the
same evidence, privacy, scope, freshness, and retirement rules.

## 5. Privacy and data minimization

Never compound:

- secrets, credentials, auth material;
- private chain-of-thought;
- raw sensitive personal data when a non-sensitive engineering lesson is sufficient;
- entire logs/messages/documents when a compact derived lesson is enough;
- benchmark answer keys or case-specific hacks.

## 6. Generalization gate

Promote a lesson beyond project scope only when a stable mechanism/contract supports it, multiple
independent cases agree, a frozen evaluation/holdout demonstrates broader benefit, or a human
explicitly curates it with known limits.

Write durable lessons as:

`Context → invariant/lesson → evidence → when to apply → when NOT to apply`.

Delete or retire stale lessons. Knowledge bloat is also debt.

## 7. Teacher/eval handoff

When `thalarch-teacher` or `thalarch-autoresearch` produced the evidence, retain both wins and
counterexamples. A holdout failure is valuable memory about the boundary of a rule; do not hide it to
make the system look smarter.
