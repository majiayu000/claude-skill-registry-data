---
name: grill-me
description: Use when someone asks to grill me on this, stress-test this plan or idea, poke holes in this, or make sure I've thought of everything before committing to a plan, design, or decision.
argument-hint: [topic or plan]
allowed-tools: Read, Glob, Grep, Write
---

## What This Skill Does

Stress-tests any plan, design, or idea — a new skill concept, a code architecture, a process change, a product decision, anything not yet built — by interrogating it one question at a time, each with a recommended answer, until every decision, dependency, assumption, risk, and branch is resolved. The subject matter is never fixed; the value is the interrogation process itself.

This is a diagnostic/decision skill. It never writes code or builds anything itself — see Guardrails.

## Step 1: Identify the Subject

- If `$ARGUMENTS` is provided, that's the subject to interrogate.
- If `$ARGUMENTS` is empty, use whatever plan/idea/design is currently being discussed in the conversation. If nothing recent is clearly a "plan," ask the user what they want grilled before proceeding.

## Step 2: Build the Open-Items List

Read through the subject and identify every point that's underspecified, ambiguous, or unstated:

- **Decisions** — choices that haven't been explicitly made (e.g. "which approach," "what should happen when X")
- **Dependencies** — things this plan relies on that haven't been confirmed (other systems, files, people, timing)
- **Assumptions** — things being taken for granted that could be wrong
- **Risks** — ways this could fail, be misused, or produce bad outcomes
- **Branches** — edge cases or alternate paths not yet accounted for

Create one task per open item with TaskCreate. This list is the visible, verifiable record of what's left to resolve — the exit condition is this list reaching zero open tasks, not your own say-so.

Skip anything whose answer is already stated elsewhere in the conversation or is genuinely inconsequential to the plan's success. Don't manufacture questions for the sake of a longer interview.

**Scope check:** if the open-items list grows past roughly 15-20 tasks, pause before continuing. Tell the user the plan may be too large or too vague for one interrogation session and suggest splitting it into smaller pieces. This is a soft pause — if the user wants to continue anyway, keep going.

## Step 3: Interrogate, One Question at a Time

For each open item, in roughly the order that unblocks the most other items first (e.g. foundational decisions before edge cases that depend on them):

1. Formulate the question clearly, scoped to that one item.
2. Work out your own recommended answer based on the context available (the subject, the conversation, the codebase if relevant).
3. Ask via AskUserQuestion with the recommended answer as the **first** option, labeled with "(Recommended)" in the label text, plus 2-3 genuinely distinct alternatives grounded in the subject's actual context (the plan's own details, the codebase, prior answers in this session) — never vague or generic placeholder options invented just to fill slots.
4. When the user answers, mark that item's task complete via TaskUpdate.
5. If the answer contradicts something already resolved, reopen that earlier task (re-create or mark it back to in_progress) and note the contradiction to the user before continuing — don't silently overwrite it.
6. Do not re-litigate an item that's already resolved and uncontradicted, even if a later question is related.

Continue until the open-items list is empty.

## Step 4: Summarize

Post an in-chat structured summary. Only if the user explicitly asks to save it, write it to `output/grill-me/<subject-slug>-summary.md`:

```
## Grill Session Summary: [subject]

**Resolved decisions:**
- [item]: [chosen answer]

**Dependencies confirmed:**
- [item]: [answer]

**Assumptions checked:**
- [item]: [answer]

**Risks addressed:**
- [item]: [answer / mitigation]

**Ready-to-execute plan:**
[Short synthesis of the final, fully-specified plan given all the answers above]
```

## Notes

- **Never build.** This skill only interrogates and produces a resolved plan. Even if the resolved plan becomes completely clear mid-session, do not start writing code, files, or skills as part of this session — hand the resolved plan back to the user (or the relevant build skill, e.g. `skill-builder`, if installed) as a separate next step.
- Don't ask about items with an obvious or trivial answer — this erodes trust in the process and wastes the user's time.
- If the subject is itself a skill idea, this pairs naturally before `skill-builder`'s own Discovery Interview (if that skill is installed), but grill-me is general-purpose and not limited to skills.
- If nothing about the subject is actually underspecified (a fully-formed plan), say so plainly and skip the interview rather than inventing items.
