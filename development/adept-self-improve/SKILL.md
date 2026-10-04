---
id: adept-self-improve
description: "Capture a durable lesson, correction, or convention from this session as a reusable adept skill, then sync it to every harness. Apply when the user corrects you, when a fix generalizes, or when you say 'I'll remember that.'"
activation: agent
allowed-tools:
  - "Bash"
  - "Read"
  - "Edit"
  - "Write"
---

# Self-improve: turn lessons into skills

adept skills are portable memory. A lesson written as a skill is loaded by **every** harness
on **every** future session — not lost when this context ends. When you learn something
durable, capture it instead of forgetting it.

## When to capture

Capture when the lesson is **durable and reusable**, not one-off:

- The user **corrects** you ("we always use X, not Y", "don't touch Z").
- A fix or pattern **generalizes** beyond the file you're in.
- You discover a **project convention** the code doesn't make obvious (a build gate, a
  naming rule, a required pre-PR step).
- You catch yourself thinking *"I'll remember that for next time."* — you won't; the skill will.

**Don't** capture: secrets, one-shot facts, anything already obvious from the code or
existing skills. Improve an existing skill before adding a near-duplicate (`adept skill list`).

## The loop

```bash
adept skill list                       # does a skill already cover this? edit it if so
adept skill add <kebab-id> --edit      # else scaffold a new one
# write a triggering description + a tight, harness-neutral body
adept sync                             # render to every enabled harness
adept status && adept diff             # confirm it landed clean
```

Then tell the user, in one line, what you captured and where — they own the memory, so
let them veto it. Commit the new skill with their normal review.

## What makes a captured lesson good

- **Description = trigger.** Front-load *when it applies* so a future agent loads it at the
  right moment. See [[authoring-adept-skills]] for crafting the description and activation.
- **Atomic.** One lesson per skill. If it needs "and also…", it's two skills.
- **Reason, not just rule.** "Use sentinel errors so callers can `errors.Is`" beats "use
  sentinel errors" — the why survives refactors the rule wouldn't.

## Confirm before you persist

Capturing is an outward, durable act: it changes how every future session behaves. Surface
what you're about to write and let the user confirm — don't silently rewrite the project's
shared memory. See [[using-adept]] for the surrounding CLI.
