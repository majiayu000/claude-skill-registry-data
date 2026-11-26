---
name: shaping
description: >-
  Turns a raw idea into an approved spec by questioning the user first. Use when the user has a new feature or product idea, says "I want to build...", or a request is vague with a design choice open. Not for clear small edits or bugs.
license: Apache-2.0
metadata:
  level: "process"
  uses: "documenting"
  agents: ""
  tokens: "983"
---

Turns a raw idea into an approved spec. You ask and propose; the user decides, and their words go in the spec. Nothing gets built here.

Uses: foma-skills:documenting (a decision that outlives the spec: a library chosen, an approach rejected).

## Steps
1. *Always.* Look before you ask: read the CLAUDE.md contract, `$ARGUMENTS`, anything the user pointed at, and the code or material the idea touches (grep, then ranges). If a spec for this idea exists, continue it. Never ask what the project or the conversation already answers.
2. *Always.* Pick the path and say it in one line.
   - Small, clear change (1-2 files, no design choice): say "small change, doing it directly" and stop; do the task.
   - Everything that matters is in the request: play it back in ≤5 lines with a short design (approach, why not the others), ask for ok, then hand off. No spec file unless asked.
   - The conversation already settled it: go to step 6, no re-interview.
   - Otherwise: the full path below.
3. Why first. Play the idea back as a problem in 2-3 lines, then ask open discovery questions, one per message, with no options attached: the last concrete time this hurt, what they do today instead, what success looks like to them. Then the appetite: how much time it is worth, and what gets cut first if it runs over.
4. Grill the decision tree in rounds. Track coverage internally, never print it: problem, user, workaround, success, appetite, scope, not-doing, constraints, risks, assumptions (clear / partial / missing). The frontier is every open decision whose prerequisites are settled; ask it, ≤4 questions per round, numbered, recommended answer first, worded so "yes" accepts. A question that depends on another open one waits a round. Keep only questions whose answer changes the spec. After each round, append the answers to the spec's Clarifications.
5. Challenge before agreeing: turn claims into "what would have to be true for this?", give the skeptic's view and the opposite premise, run a pre-mortem ("it shipped and failed - why?"), name the 2-3 riskiest assumptions. Then lay out approaches in a message of their own: 2-3 real ones including a smaller one (does it need to exist at all?), each with its trade-off, your pick and why. The user picks.
6. Write the spec (Branches). Show its path, your calls for the user to check, and open questions; ask for approval. Edit on feedback.
7. Stop when the frontier is empty, the user says stop, or after 4 decision rounds: write what is known, list the rest under Open questions.

## Rules
- Never build before the spec is approved: no product code, scaffolding, installs or implementation skills. Reading and exploring are fine; a throwaway spike the user said yes to stays labelled throwaway.
- Never rewrite the idea as theirs. Their wording goes in the spec; your defaults are marked as your call with a reason. A default they never heard is one they couldn't reject.
- Never offer a menu before you know why; options steer. Discovery questions are open.
- Never approve on first contact. "Sounds good" covers only what you showed.
- Facts are yours, decisions are theirs: look facts up (or send a fresh subagent) and ask only about decisions.
- One question call at a time; put the context line in its own message before the dialog. If the dialog is unavailable or comes back empty, ask the same numbered round in plain text.
- Plain language, their vocabulary, no process jargon; whenever seeing helps (a screen, a flow), sketch it in a few text lines.
- If it is really several independent projects, say so, agree on an order, shape one at a time.

## Branches
If creating or updating the spec file, read `references/spec.md`.

## Report
- Path taken, spec file, rounds asked.
- Your calls in the spec, open questions.
- Not checked: <...>

Next: once the spec is approved, ask for a plan (foma-skills:planning). A visual choice goes to `/foma-skills:design-interview`.
