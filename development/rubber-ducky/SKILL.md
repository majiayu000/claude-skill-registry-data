---
name: rubber-ducky
description: >-
  Use when you've planned a non-trivial change and are about to implement it, finished a complex
  or multi-file piece of work, just wrote tests, or are stuck on repeated failures — and any time
  the user says "rubber duck this", "rubber ducky", "get a second opinion", "sanity-check my plan",
  "poke holes in this", "what am I missing", "critique my approach", "review this before I build it",
  or "/rubber-ducky". Spawns independent read-only critics on DIFFERENT Claude models than the one
  driving the session to catch blind spots, design flaws, and substantive bugs while course
  corrections are still cheap. Skip it only for small, obvious, well-understood changes. Do NOT use
  for reviewing a finished diff or PR — use /review for that; rubber-ducky pressure-tests your own
  in-progress thinking before and during implementation.
---

# Rubber Ducky

A built-in critic. Before committing to a non-trivial change, you stop, articulate your current
thinking, and have it scrutinized by independent reviewers running on **different models** than the
one driving this session. Unlike a real rubber duck, this one talks back: it returns a structured
critique you can act on.

## Why this works

Rubber-duck debugging works because *articulating* your reasoning forces the gaps into view. This
version adds two things a desk toy can't:

1. **It talks back.** The reviewers return concrete, categorized feedback — not silence.
2. **It doesn't share your blind spots.** The reviewers run on the two Claude models you are *not*
   using right now, with a clean context. A model that didn't produce the work is far more likely
   to see what's wrong with it. You get genuinely independent perspectives, not a re-run of the same
   reasoning that produced the plan.

The single highest-leverage moment is **after you've planned a change but before you've written the
code**. A design flaw caught here costs a paragraph to fix; caught after implementation it costs a
rewrite.

## rubber-ducky vs /review

Both are read-only critics, but they fire at different stages:

- **rubber-ducky** pressure-tests *your own in-progress thinking* — a plan, a design, an approach,
  tests you just wrote — usually **before or during** implementation, using cross-model critics.
- **/review** evaluates a *finished change* — a branch diff or a PR — after the code exists.

Reach for the duck while the decision is still cheap to change; reach for /review when the work is done.

## When to consult the duck

Consult it at high-leverage moments, not only when stuck:

- **After planning a non-trivial change, before implementing it.** Highest leverage. Corrections are
  cheapest here.
- **Mid-implementation on complex or multi-file work**, to check for blind spots before you're in too deep.
- **After writing tests**, to validate the coverage is real and the behavior actually satisfies the
  original request — not just that the tests pass.
- **Reactively, when you hit repeated failures or unexpected results.** Get an independent analysis
  instead of retrying the same approach a fourth time.
- **Whenever the user explicitly asks** ("rubber duck this", "/rubber-ducky", "poke holes in this").

**Skip it** for small, well-understood changes — a one-line fix, a rename, an obvious bug. The duck
adds an extra reasoning pass on two other models; that cost is worth it for architecture, multi-file
changes, and unfamiliar code, and is just friction for trivial edits. If you decide to skip, say so
in one line and move on.

## How it works

### 1. Decide it's worth it

If the change is trivial or you're highly confident, skip the duck and say why in one line. Otherwise
continue.

### 2. Pick the two critic models

You know your current session model from your environment (e.g. Opus, Sonnet, or Haiku). Select the
**two model aliases the session is NOT using** from `{opus, sonnet, haiku}`:

| Session model | Critic 1 | Critic 2 |
|---------------|----------|----------|
| Opus          | `sonnet` | `haiku`  |
| Sonnet        | `opus`   | `haiku`  |
| Haiku         | `opus`   | `sonnet` |

Two reviewers on different models surface different failure modes; agreement between them is a strong
signal, disagreement is worth flagging. If only one other model is available in this harness, run one
critic — the cross-model independence still holds.

### 3. Articulate the work (the brief)

Write a concise brief the reviewers can act on cold — they don't share your conversation. Include:

- **The goal** — what this change is actually trying to accomplish, and why.
- **The work to review** — the plan, design, diff, or tests. Paste short artifacts inline; for larger
  ones, give exact file paths (and a diff range or commit) and let the reviewer read them.
- **Key assumptions** you're making, and anything you're unsure about or want pressure-tested.
- **Scope boundaries** — what is explicitly out of scope, so the reviewer doesn't flag it.

A vague brief gets a vague critique. Be specific about what "success" means.

### 4. Spawn both critics in parallel

Spawn the two reviewers in a **single message with two subagent calls** so they run concurrently. Use
a general-purpose subagent, set the `model` to the alias for each critic, and give each the same brief
wrapped in the critic instructions below. The reviewers are **read-only**: the brief tells them never
to edit files or run mutating commands. They explore the codebase to understand context, then report
back. They do not change anything — you decide what to do with the feedback.

### 5. Synthesize the two critiques

- **Where the two models agree** → high confidence; treat it as real.
- **Where they disagree** → flag it explicitly; use your own judgment, and investigate if it's blocking.
- **Dedup** overlapping findings. Order by severity: blocking first.

### 6. Decide and report back

Summarize for the user what *mattered* and what you'll do about it — don't dump both critiques verbatim:

> "The duck flagged a blind spot in my plan around concurrent writes to the cache — both models caught
> it — so I'm adding a lock before I implement. Sonnet also suggested X (non-blocking); I'll skip that
> for now."

Then act on the blocking items (or let the user decide). The duck reviews; you remain the one who
changes code.

## The critic instructions

Send each reviewer a prompt built from this template. Fill in the brief from step 3.

```
You are a rubber-duck critic giving a constructive second opinion. You did NOT write this
work — that's the point. Your job is to find real problems while they're still cheap to fix.

You are READ-ONLY. Read any files and run any read-only commands you need to understand the
work in context (how it integrates, what it assumes, what it touches). Never edit files, never
run a command that changes state. You review; someone else decides.

## The work under review

<GOAL>
<THE PLAN / DESIGN / DIFF / TESTS, or file paths + diff range to read>
<KEY ASSUMPTIONS AND OPEN QUESTIONS>
<WHAT IS OUT OF SCOPE>

## What to look for

Substantive issues that genuinely threaten the success of this work: bugs, logic errors,
race conditions, security vulnerabilities, design flaws, anti-patterns, performance
bottlenecks, missing edge cases, tests that pass without actually validating the behavior,
and assumptions that don't hold.

## What to ignore

Do NOT comment on style, formatting, naming conventions, comment grammar, minor refactors,
or "best practices" that don't prevent an actual problem. If the work is sound, say so —
do not invent issues to seem useful.

## How to report

For every issue: state the **issue**, its **impact** (why it matters), and a **concrete
suggested fix**. Categorize each by severity:

### Blocking
Issues that must be fixed for the work to succeed.

### Non-blocking
Issues that should be fixed to improve quality but won't cause failure.

### Suggestions
Lower-priority improvements that still have real impact.

If you find no issues in a category, write "None." If you find no issues at all, say so
explicitly and briefly explain why the approach looks sound.
```

## Output contract (what good looks like)

The reviewers return findings in three severity tiers. When you relay results to the user, preserve
that structure but stay concise:

- **Blocking** — must fix. Lead with these.
- **Non-blocking** — should fix.
- **Suggestions** — nice to have.

Each finding is *issue → impact → fix*. "No issues found" is a valid and valuable result — report it
plainly rather than manufacturing nitpicks.

## Guardrails

- The duck **never modifies files or runs anything stateful** — it is a critic, not an editor.
- Don't let the duck slow down trivial work. Triviality is your call; when in doubt on a non-trivial
  change, consult it.
- The reviewers see only what's in the brief plus what they read from the codebase — they have no
  access to this conversation. If the brief omits the goal or a key constraint, the critique will miss it.
