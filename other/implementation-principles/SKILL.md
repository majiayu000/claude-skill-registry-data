---
name: implementation-principles
description: Shared implementation guidance for making minimal, correct, maintainable code changes that fit existing systems.
compatibility: opencode
metadata:
  audience: engineers
  purpose: implementation-guidance
---
## What I do

Provide shared implementation guidance for execution-oriented agents.

## The Excellence Bar — make it kick-ass, not half-assed

**This is the first principle. Every other rule below sits underneath it.**

Aim for the excellent version of the work, not the adequate one. When you can see two ways to satisfy a `## Changes` item — one that meets the letter of the requirement and one that meets the spirit — pick the one that meets the spirit, even if it's marginally harder. If the spec asks for a feature, the user wants the feature to actually rip — not a stub that satisfies the acceptance criteria on paper.

**Self-check at the end of every task:** "Would I be proud to show this to a senior engineer who cares about this codebase?" If the honest answer is no, the work isn't done.

**Outcome excellence, not extra scope.** The Excellence Bar raises quality of in-scope work. It is NOT a license for scope creep. If you see broader work that would make the result better, surface it to the delivery lead — do not self-authorize. Doing the agreed thing exceptionally well beats doing more things adequately.

## Core principles

- Understand the existing code before changing it.
- **Make the smallest change that fully satisfies the requirement.** "Correct" means the feature actually works end-to-end for its intended user — not that the code compiles, not that the tests you wrote pass, not that it looks plausible. End-to-end working behavior is the bar.
- Preserve project conventions unless they are clearly harmful.
- Prefer direct, maintainable code over cleverness or indirection.
- Avoid introducing abstractions without a concrete need.
- Keep scope tight and avoid opportunistic rewrites.

## Anti-punt — hard items are not grounds for silent descoping

If a `## Changes` item or acceptance criterion turns out to be harder than expected, you have exactly three options:

1. **Complete it.** Hardness is the default state of real work.
2. **Halt and surface a clear blocker report.** Name what you tried, the specific obstacle, and what you need to proceed.
3. **Get explicit sign-off to descope.** Ask the delivery lead or user. Wait for an answer.

**Silent descoping is a failure mode, not pragmatism.** Reframing a required item as "out of scope" mid-delivery, declaring a stub "done," or omitting a hard item from your final report without flagging it — these are the behaviors this section exists to prevent. The Boundaries section of a spec names work that is OUT of scope at design time. Items in Changes and Acceptance Criteria are IN scope and mandatory; they cannot migrate to Boundaries during delivery.

## Practical behavior

- Identify the smallest set of files and components that need to change.
- Reuse existing utilities, patterns, and boundaries when appropriate.
- If the requested design does not fit the actual code cleanly, say so and adjust pragmatically.
- Keep new names, helpers, and layers to a minimum.
- Consider operational consequences, not just compilation success.

## When to use me

Use this skill for nearly all coding tasks that turn requirements or plans into concrete code changes. Pair with `agent-reliability` for verification, scope honesty, and persistence rules.
