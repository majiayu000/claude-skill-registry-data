---
name: handoff
description: Compact the current conversation into a handoff document so a fresh agent can pick up the work with zero prior context. Use when the user wants to end a session and continue later, is running low on context, says "write a handoff", "hand this off", "summarize for the next session", "compact this", or wants to transfer work to another agent or teammate.
metadata:
  argument-hint: What will the next session be used for?
  disable-model-invocation: "true"
---

# Handoff

Write a handoff document that lets a fresh agent (or human) continue this work without reading the original conversation. The reader has zero context: they haven't seen the chat, don't know the user's shorthand, and can't ask you clarifying questions. Everything they need must be in the document or reachable from it.

## Guiding principles

**Optimize for the reader's context budget.** The next agent will load this document into a fresh context window. Every paragraph you write is context they can't spend on the actual work. Be dense, not thorough — a good handoff is typically 1–3 pages, not a transcript.

**Reference, don't duplicate.** If content already lives in an artifact — a PRD, plan, ADR, issue, commit, diff, spec file, or previous handoff — link or path to it instead of restating it. The handoff is a map, not a warehouse. One-line summaries of what each artifact contains are fine; copying their contents is not.

**Failed attempts are first-class content.** The most expensive thing a fresh agent can do is re-walk a dead end. Record what was tried and didn't work, and *why* it didn't work, with the same care as what succeeded.

**Separate facts from beliefs.** Mark clearly what was verified (tests passed, user confirmed, output observed) versus what is assumed or inferred. A fresh agent inheriting an unmarked assumption as fact can compound the error for an entire session.

## Arguments

If the user passed arguments, treat them as a description of what the next session will focus on, and tailor the document accordingly:

- Weight the "Next steps" and "Suggested skills" sections toward that focus.
- Trim background that's irrelevant to it (still reference where it lives, in case).
- If the stated focus conflicts with the natural next step from this session, note the discrepancy briefly rather than silently dropping either.

If no arguments were passed, assume the next session continues the work where this one left off.

## Where to save

Save to the **temporary directory of the user's OS** — never the current workspace, so it doesn't pollute the repo or get committed:

- Detect the temp dir portably: use `$TMPDIR` if set, else `/tmp` on Linux/macOS, `%TEMP%` on Windows. In a script: Python `tempfile.gettempdir()` or Node `os.tmpdir()`.
- Filename: `handoff-<project-or-topic-slug>-<YYYYMMDD-HHmm>.md` (e.g., `handoff-gulf-equities-site-20260708-1432.md`).
- After writing, tell the user the full path and give a one-line summary of what the doc covers.

## Redaction

Before writing, sweep the conversation for sensitive material and redact it from the handoff:

- API keys, tokens, passwords, connection strings, private keys → replace with a placeholder that says where the real value lives: `[REDACTED — see .env DATABASE_URL]` or `[REDACTED — in 1Password vault "Client X"]`.
- PII (emails, phone numbers, addresses of real people) → redact unless it's essential to the work and the user's own info.
- Internal URLs or credentials embedded in commands → redact the secret portion, keep the command shape so it's still reproducible.

Never redact in a way that strands the next agent — always leave a pointer to where the real value can be obtained.

## Document structure

Use this template. Omit sections that are genuinely empty rather than padding them.

```markdown
# Handoff: [short title]

**Date:** [date] · **Session focus:** [one line] · **Next session:** [from arguments, or "continue"]

## Goal
What the overall effort is trying to achieve, in 1–3 sentences. The "why" behind the work.

## Current state
Where things stand right now. What's done, what's in progress, what's untouched.
Concrete: file paths, branch names, deployed URLs, which tests pass.

## Key decisions
Decisions made during the session and their rationale, one line each.
Include decisions *not* to do something.

## Dead ends
What was tried and abandoned, and why. Save the next agent from repeating it.

## Facts vs. assumptions
- **Verified:** things confirmed by tests, user statements, or observed output.
- **Assumed:** inferences not yet confirmed. Flag anything the next agent should verify early.

## Next steps
Ordered, concrete, actionable. The first item should be startable immediately with
no further investigation. Include acceptance criteria where they exist.

## Suggested skills
Skills the next agent should invoke, with a one-line reason each.
Only suggest skills that exist in the environment (check the available skills list);
if unsure a skill will be present next session, say so.

## References
Artifacts this handoff points to instead of duplicating:
paths, URLs, commit SHAs, issue numbers, doc links — each with a one-line description.

## Open questions
Things only the user can answer. Phrase them so the next agent can ask verbatim.
```

## Quality bar

Before finishing, reread the document as if you were the fresh agent and check:

1. Could I start the first "Next step" right now without asking anything? If not, the handoff is missing something.
2. Is anything in here retrievable from a referenced artifact? If yes, cut it and keep the reference.
3. Are there secrets or PII anywhere, including inside code blocks and command examples?
4. Would I re-attempt any of the dead ends based on what's written? If the "why it failed" isn't convincing, sharpen it.
5. Is every assumption labeled as one?

Do not include conversational filler, praise for the work done, or a narrative retelling of the session's chronology — the handoff is about state, not story.
