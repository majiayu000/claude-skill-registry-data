---
name: find-your-unknowns
description: >
  Before turning an agent loose on a coding task, surface the decisions you never specified —
  the gaps between your prompt (the "map") and the real codebase (the "territory"). Runs six
  prompt patterns (blind-spot pass, brainstorm/prototype, interview-me, reference-as-map,
  implementation-notes logging, quiz-me) to enumerate unknowns and shape the architecture up
  front. Use when the user says "help me scope this before I build it", "what am I missing",
  "find my blind spots", "interview me about this feature", "I don't know this codebase / this
  domain, help me prompt better", "de-risk this before the big run", or "surface the unknowns"
  — and BEFORE kicking off a large or architecture-shaping agent run on an under-specified task.
---

# find-your-unknowns

A more capable agent traverses more of the codebase, so it hits more decisions you never wrote
down — and drifts. The fix is to find those decisions *before* the big run. Your prompt is a
**map**; the codebase is the **territory**. This skill surfaces everywhere the territory holds
something your map doesn't.

## When to use vs. skip
- **Use** before a large, ambiguous, or architecture-shaping task, or when you (or the user) are
  new to this codebase or domain.
- **Skip** for a small, fully-specified change where the territory is already known — running the
  full battery would be ceremony.

## Inputs
- A **task/goal** (what the user wants built or changed).
- A **target repo or subsystem** you can read.
- Optionally: reference code/mockups, and context about the user's taste, stage, and constraints.

## Workflow

Don't blindly run all six. Pick by the *kind* of unknown in play (see table), run those, then
consolidate. Note the **When** column: only patterns 1–4 run during this scoping pass. Pattern 5
is an instruction you *produce now* but inject into the later build run; pattern 6 runs *after* the
build. Each pattern's full prompt template is in `references/prompt-patterns.md`.

| Kind of unknown | Pattern | When | Skip if |
|---|---|---|---|
| "I don't even know what I don't know here" | **1. Blind-spot pass** | scoping | rarely — this is the anchor |
| Aesthetic / "know it when I see it" | **2. Brainstorm & prototype** | scoping | the surface isn't primarily visual |
| Under-specified requirements | **3. Interview me** | scoping | requirements are already crisp |
| An example is easier than a spec | **4. Reference — give it another map** | scoping | you have no reference to point at |
| Deviations that only appear mid-build | **5. Implementation notes** | build-time | never — it's a cheap always-on trail |
| Do *I* actually understand the result? | **6. Quiz me** | post-build | you already own the result cold |

### The six patterns (in the order you'd typically reach for them)

1. **Blind-spot pass** — Read the target area and enumerate the *unknown unknowns*: the relevant
   things this task touches that the user hasn't mentioned. Output a list of blind spots + better
   prompting suggestions. Works for a new codebase *or* a new domain.
2. **Brainstorm & prototype** — For decisions the user can only judge by reacting: generate a few
   **wildly different** options (e.g. an HTML page with 3–4 distinct design directions) so they can
   point at one instead of specifying it.
3. **Interview me** — Have the agent interview the *user*, and explicitly
   **prioritize questions that would change the architecture**. Under-specified requirements become
   explicit before any code is written.
4. **Reference — give it another map** — Instead of writing a spec, point the agent at existing
   code (even in another language/system) or a mockup: "read this, understand it, use it as the
   starting point." An example often carries intent a spec can't.
5. **Implementation notes** — Inject an instruction into the *main* run: whenever the agent hits a
   decision not covered by the spec, **log the deviation and why** before proceeding. You get a
   visible trail of where the run left the map.
6. **Quiz me** — After the work, have the agent quiz the user on what actually happened, so they
   understand it well enough to own the PR/merge. Keeps the human in the loop.

### Consolidate
After running the chosen patterns, produce one artifact:
- **Unknowns** — the merged list of surfaced blind spots / open questions.
- **Architecture-shaping answers** — what the interview/references settled that affects structure.
- **A logging instruction** to paste into the main agent run (pattern 5), so mid-run deviations
  keep surfacing.

Then proceed to the real build with far fewer hidden decisions.

## Guardrails
- This is **discovery, not the build.** Don't start implementing during the unknown-finding pass —
  the point is to surface decisions, not make them silently.
- **Prefer context over constraints.** When you prompt the agent for these passes, give it context
  and let it reason; avoid piling on "do not do X" rules.
- Treat the model empirically — build intuition about where *this* codebase and *this* model surprise
  you, rather than assuming fixed rules.

## Reference
- `references/prompt-patterns.md` — the full, copy-pasteable prompt template for each of the six patterns.
