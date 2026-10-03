---
name: architect
description: Spawn the architect agent in goal-capture mode. User states a desire; architect researches, proposes paths, dialogues, files specs, opens a PR.
invocation: /architect "<goal>"
---

# /architect "\<goal\>"

Spawn the `architect` agent in **goal-capture mode**.

Pass the agent:
- The goal verbatim (the quoted string from the invocation)
- Mode: `goal-capture`
- Instruction: read the repo state silently before opening dialogue
  (no questions about what's in the repo)

## What the architect will do

1. Read `STATUS.md`, `ROADMAP.md`, `NEXT_STAGE_REPORT.md`, and relevant
   research notes.
2. Research externally if needed.
3. Form an opinion before presenting options. If the goal conflicts with
   project priorities, say so first.
4. Present variable-N solution paths with tradeoffs.
5. Ask one short open question to focus the dialogue.
6. After convergence: file new spec(s), update ROADMAP/STATUS if direction
   changes, open a PR.

## Examples

```
/architect "I want to render a prism dispersing light"
/architect "let's go after viewport perf"
/architect "what's the fastest path to a real astrophysical scene"
/architect "should we add pbrt-v4 scene import"
```
