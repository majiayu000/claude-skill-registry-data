---
name: Stuck
description: Walk the 6-rung escalation ladder before declaring stuck or asking the principal. Most "stuck" is actually "haven't tried the next approach." Stopping is the last resort, not the first response.
---

# Stuck

Before posting "I'm blocked", "not sure how to proceed", or "should I…?" — walk this ladder. **Stopping is the last resort, not the first response.** Most obstacles aren't blockers; they're the next thing to try.

## When to use

- About to surface to the principal for help
- Hit an error, an obstacle, or genuine ambiguity
- Tempted to type "I'm stuck" or "this isn't working"
- Triggered by Caddy on prompts like: "blocked", "not sure how", "can't find", "need help", "should I ask", "stuck on", "this isn't working", "hitting a wall", "give up", "ask for help"

## The ladder (climb top-to-bottom; only stop at the bottom)

### Rung 1 — Try a different approach
Most obstacles aren't blockers. Did you try plan A? Try plan B.
- API call failed → retry with different params, fallback to alternative API
- Test broken → fix the test
- Compile error → read the error and fix it
- Library doesn't do what you expected → try a different method on the same library

### Rung 2 — Try 2-3 alternatives explicitly
Brainstorm 3 ways to solve this. Note them down. Try each.
- Can the data come from a different source?
- Can the problem be solved at a different layer (UI vs API vs DB)?
- Is there a workaround that gets 80% of the value?

If you can't think of 3 alternatives, you haven't thought hard enough — keep listing.

### Rung 3 — Use a helper
Spawn an exploration subagent with a **specific question**.
- Not "help me figure this out" — that's a survey.
- "Find all callers of `generateHeadline` and report whether any pass `null` for the `archetypeId` argument" — that's a question.

### Rung 4 — Re-read the user's request
Sometimes the path is in the wording. The principal often gives the answer; you just read past it.
- Did they specify a constraint you've been violating?
- Did they reference a file or pattern you haven't checked?
- Did they say "like X" — and have you actually looked at X?

### Rung 5 — Genuinely ask
Only if rungs 1-4 have failed AND the missing information is **user-only** (a product decision, a credential, an ambiguous behavior with no code-side answer).

The ask must be:
- **One question** (not a survey)
- **Surgical** (X or Y with consequences spelled out — see [`/envelope`](../envelope/SKILL.md))
- **Stated** ("After trying A, B, and C, the remaining ambiguity is whether X means Y or Z. Y produces outcome P; Z produces outcome Q. Which?")

### Rung 6 — Stop and report
Rare. Reserved for truly nothing-else-to-try situations.

The stop report must include:
- **Where stuck** (specific file/line/system)
- **What I tried** (rungs 1-4 explicitly listed, with what each yielded)
- **What would unblock** (specific resource, decision, or access — be precise)

## Concrete examples

### Example A: API rate-limited mid-port (NOT stuck)
- **Wrong:** "I'm blocked — Replicate is rate-limiting me."
- **Right:** Wait + retry (rung 1). If sustained → switch to a fallback provider (rung 2). If no fallback → use the library's built-in throttling (rung 1). Don't surface unless 30+ minutes of throttling persist.

### Example B: Code references a file you can't find (NOT stuck)
- **Wrong:** "I can't find `lib/whatever.ts` — where is it?"
- **Right:** Grep for the symbol the file exports. Read import paths in nearby files. Check if it was renamed. Ask only if 4 different searches fail.

### Example C: Genuinely ambiguous product decision (STUCK at rung 5)
- **Right:** "After reading the spec, the codebase, and PR #341, I see two valid interpretations of 'cap at 50 minutes': hard truncate or graceful early-end. Hard truncate is 5 LOC; graceful needs a 30-line state machine. Which?" — then wait.

## The shorthand

> Most "stuck" is actually "haven't tried the next approach." Three rungs of effort beat one rung of asking.

## Output format when stuck-checking

If you're about to surface, first output (silently to yourself, then act):

```
[STUCK CHECK]
Rung 1 (alternatives tried): {list}
Rung 2 (alternative paths considered): {list}
Rung 3 (subagent helper used): {yes/no — what question}
Rung 4 (re-read request): {what new clue surfaced}
Verdict: {SHIP / ASK / STOP}
```

If verdict is SHIP — proceed with the work.
If verdict is ASK — use [`/envelope`](../envelope/SKILL.md) to format the question (Envelope B).
If verdict is STOP — write the stop report.
