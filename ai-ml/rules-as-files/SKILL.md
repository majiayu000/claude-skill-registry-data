---
name: rules-as-files
description: "Keep agent and team rules as one markdown file per rule with a short index line in CLAUDE.md or AGENTS.md. Use when the user states a new rule, asks to slim a bloated CLAUDE.md, resolve conflicting rules, log a declined decision, or argue a no-go verdict as numbered objections."
---

# Rules as files

A working method for rules that a human, their assistants and their AI agents
all follow. Each rule is one markdown file; the always-loaded layer carries only
a short pointer to it. The full specification is in [SPEC.md](SPEC.md); fill-in
templates are in [templates/](templates/).

This skill is instructions only. It reads and writes markdown files in the
user's own project and never runs programs or sends data anywhere.

## When to use it

- The user says a new rule in chat ("from now on...", "never again...", "always...").
- `CLAUDE.md` / `AGENTS.md` has grown into full prose rules and needs slimming.
- Two rules disagree and you must decide which one wins.
- The user rejects or defers a proposal worth remembering.
- You are about to tell the user "no-go" on something they want.

## 1. Write a rule (intake)

1. Ask the routing questions in order (SPEC section 4):
   - Could a human employee follow it? Then it is a behavioral rule file.
   - Is it about how the agent works internally (models, tools, paths)? Then agent config plus a memory note.
   - Is it a fact or preference, not a behavior? Then memory.
   - Is it "every time X, do Y" and deterministic? Then a hook or scheduled script, not prose.
2. Create one file from [templates/rule-template.md](templates/rule-template.md).
   Fill the frontmatter: `title`, `type`, `date_established` (today, from the
   clock), `status: active`, `origin` (who stated it), `authored_by`, `audience`.
   Always write the `Why` section.
3. Add exactly one index line to the always-loaded file:

   ```
   ## <Trigger: when this fires>
   <Essence in 1-3 sentences.>
   Canon: `<rule-file-name>`
   ```

4. Link at least one related rule in both directions.
5. Name the door: the skill, command, hook or scheduled job that will invoke the
   rule (SPEC section 9). If none exists yet, add the rule to a short list of
   doorless rules with the reason.
6. Report back where the rule lives and where its index line went. Do not
   postpone the intake because the index file is large; report its size instead
   (SPEC section 10).
7. Test before saying done: would a parallel session that never saw this chat
   pick the rule up by itself? If not, it is not captured.

## 2. Slim a bloated CLAUDE.md or AGENTS.md

1. Read the file and list every rule written as a full prose body.
2. For each, propose a rule file (body) plus an index line (trigger, essence,
   pointer). Show before and after on the user's real text, not on abstractions.
3. Move bodies only after the user agrees. Keep one home per rule; every other
   layer points to it.

## 3. Resolve a conflict between rules (SPEC section 3)

1. Explicit `supersedes` wins.
2. Otherwise a rule with `origin: owner` beats an agent-inferred rule, whatever the dates.
3. Otherwise newer `date_established` beats older on the same topic.
4. Never delete or silently edit the losing rule: set `status: superseded`, add a
   forward link, keep the file. History is data.

## 4. Keep the declined-decisions journal (SPEC section 5)

- When the user rejects or defers something non-trivial, append an entry in the
  same session using [templates/declined-decisions-template.md](templates/declined-decisions-template.md).
- Before proposing anything structural, scan the journal. Re-propose only when a
  recorded `Revisit if` condition holds, or as an explicit trade-off quoting the
  original decline.
- An overturned verdict is marked `OVERTURNED <date>` with a pointer to the new
  decision; the old text stays.

## 5. Argue a no-go as objections (SPEC section 6)

1. Give the verdict as a numbered list, one real objection per line.
2. Invite rebuttal plainly: "these are my objections, convince me."
3. Treat the rebuttal as data; it often changes the frame, not the arguments.
4. Summarize as a table: objection, dissolved (why) or stands. What stands
   becomes a boundary inside the decision, not a veto.
5. If a rebuttal did not close an objection, say so. Agreement must be argued,
   not conceded.

For a decision worth recording, use [templates/decision-memo-template.md](templates/decision-memo-template.md):
recall what is already known first, then options, decision, boundaries, risks and next steps.
