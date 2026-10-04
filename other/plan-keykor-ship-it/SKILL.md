---
name: plan
description: Opens a conversational planning session for a feature, bug, or ticket. Investigates the repo, discusses the approach with the user until a solution is agreed, and only then writes the plan to docs/plans/. Use whenever the user invokes it, describes a problem to solve, pastes a ticket, mentions an incident, or asks to plan a non-trivial change. Also on "plan this", "analyze this first", "what would we need to touch", "let's start with this" — or in Spanish "planeá", "analizá esto antes", "qué habría que tocar", "arranquemos con esto".
---

# Planning session

A conversation, not a form. The goal is to reach a solution agreed with the user and only
then write it down. The plan file is the result of the discussion, not the starting point.

Three phases: **listen -> explore -> discuss**. The plan gets written at the end, when the
user says to go.

Do not write production code here.

## 0. Intake — do NOT explore yet

This skill fires **before** the user has finished explaining. The first reply is not a plan
or an exploration: it opens the conversation.

If it fired without enough context, say in a line or two that you're ready and ask for:

- The problem or the expected behavior, in the user's own words
- The ticket(s) (id, and the pasted text if they have it handy)
- Anything they already know: where they suspect it is, what was tried, links

Then **stay listening**. The user will send context across several messages: description,
then the ticket, then a log, then a clarification. While they keep adding context, the right
response is to acknowledge in one line and wait for more.

Intake rules:

- **Do not start exploring the repo until the user says to.** Phrases like "that's it",
  "look at the repo", "go ahead" are the signal. When in doubt, ask.
- **One question at a time.**
- **Don't ask for what you can read.** If the ticket mentions a file or a service, look it
  up in the repo; don't ask the user.
- If there are **multiple tickets**, ask whether they go in one plan (one PR) or separately.
- If the user gave everything in the first message, confirm the ticket in one line and move
  on to exploring.

## 1. Explore

First, sync the checkout so you design against real code, not a stale copy:

```bash
git fetch origin
git pull --ff-only
```

`git fetch origin` refreshes every remote branch (so you know the real state of things), and
`--ff-only` updates the current branch only if it fast-forwards cleanly. If it can't (the
branch diverged, or there are uncommitted changes in the way), it stops without a merge or a
conflict — surface that to the user and let them sort it, don't force it.

- Read `CLAUDE.md` in full.
- Locate the files that will actually be touched. Cite them by path.
- Look for something similar already in the repo and follow that pattern.
- Identify the existing tests that cover that area.
- If the change crosses services, say which other repo has to be touched.

Use exploration subagents if the repo is large, so the main context stays clean for the
discussion.

## 2. Discuss the solution — the long phase

**No file gets written here.** This phase ends when the user says to go, and it can take
many messages. That is expected, not a problem.

### Open with options, not a conclusion

Present **two or three possible approaches** with their real cost: what each one touches,
what it breaks, what debt it leaves. Say which one you recommend and why, but don't present
it as closed.

If there's only one reasonable approach, say so and explain why the others don't fit.

### Actually discuss

- **If the user proposes something that seems wrong, say so.** With the concrete reason:
  which case it breaks, what gets complicated later. Caving because they insisted is the
  worst outcome: the cost shows up during implementation, when it's already expensive.
- **If the user is right, change your mind explicitly** and say which argument convinced
  you. They know the system and the business context better.
- **Bring up what exploration found that contradicts the request**: the problem is
  elsewhere, it's already solved, there's a case the proposal doesn't cover. Before, not
  after.
- **Ask about the edges**: what happens to existing data, to in-flight requests, to current
  consumers, to rollback.
- Short replies. It's a conversation, not a report. One idea per message.

### Close it out

When something is decided, name it: "so we go with X". That way the user sees the agreement
accumulating and what's still open stands out.

If the user asks how it's going, summarize in three lines: what's decided, what's left.

### Check the human-review list

Contrast the agreed approach against the "Changes that require human review" section of the
`CLAUDE.md`. If any apply, say so **during the discussion**, not at the end.

## 3. Write the plan — only when they say "go"

The signal is explicit: "go", "start", "write it", "ok, do it" — or in Spanish "dale",
"arrancá", "escribilo", "listo, hacelo".

Then save to `docs/plans/` with the ticket id as the name (or a short slug of the problem,
noting which name you used).

Sections: Problem - Scope (includes and does NOT include) - Approach and why - Numbered steps -
Tests - Risks - Open decisions.

The **Numbered steps** are the heart of it: each step spells out concretely **what gets
executed or changed** (the files, the commands to run) and **the commit that closes it** (its
message and scope). Write them so `ship` can follow them as the exact execute-and-commit
checklist — one commit per step, in the repo's commit format.

Two things the plan must capture from the discussion, or everything discussed is lost:

- **The discarded alternatives and why.** This is what stops someone (including the agent
  itself) from redoing the discussion from scratch a month later.
- **What the user corrected.** If they changed the approach midway, the reason goes in the
  plan.

Write "Problem" in the user's words, not the code's.

## 4. Confirm they read it, then start

After writing the plan: summarize in three lines (approach, number of steps, human-review
flags), point the user at the file, and **ask them to confirm they've read it before you
ship** — e.g. "¿Lo leíste? ¿Arranco con el ship?" / "Did you read it? Ready for me to ship?".
Do **not** invoke `ship` on your own here — wait for their explicit go.

The plan is exactly what `ship` executes commit-by-commit, so a quick read now catches a wrong
step before it turns into commits. If they want changes, revise the plan and ask again.

Only once they confirm, invoke the `ship` skill in the same turn. If there are open decisions
left, don't offer to ship yet: go back to step 2 and close them.

---

*Convention: `{{like-this}}` marks a value to replace. `<>` is avoided because it breaks skill parsing.*
