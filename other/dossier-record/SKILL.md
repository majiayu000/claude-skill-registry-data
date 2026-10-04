---
name: "Dossier: Record"
description: "Record a durable fact about a person Jason works with, in their own dossier file"
when_to_use: "Whenever Jason says something durable about a named person he works with: their role, expertise, preferences, what they care about, how they review or respond, how to work with them. Also when he introduces someone new, or asks for something about a person to be noted."
metadata:
  family: dossier
# No model or effort on purpose. This skill fires inline, mid-turn, inside
# whatever the session was already doing; both fields override the session
# absolutely while a skill is active, so setting either would downgrade the
# turn that triggered it.
disable-model-invocation: false # the trigger is a fact landing in conversation, which Claude sees before Jason thinks to record it; step 4 is the gate
user-invocable: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Edit"]
argument-hint: "[name] [what to record]"
---

# Record a person fact

Files live in `~/.claude/library/profiles/dossier/{slug}.md`, one per person, gitignored.
`library/profiles/dossier/README.md` holds the schema and is the authority on file shape.

This skill fires in the middle of other work. It must be quiet: one line of
output, no summary, no restating what Jason just said back to him.

## Step 1: Should this fire at all

Fires on a **durable attribute** of a named person Jason works with:

- Role, seniority, ownership: "Izaak leads fac-cra"
- Expertise and its limits: "Jaz is light on YAML but picks things up fast"
- Preferences and standards: "Dan wants PRs smaller"
- What they care about, what they reject, how they review
- How to work with them: pitch, handover, register, what to leave out
- Relationships: "Jaz, Max and I work together"
- Pronouns, when stated

Stays silent on:

- Routing and tasking: "send it to Dan", "ask Jess for the spreadsheet"
- One-off state: "Dan's on leave next week", "Jaz is reviewing it today"
- Passing mentions with no claim attached
- Anything about a person Jason does not work with, unless he asks for it
- Third-party gossip. A claim about someone's character, relayed from someone
  else, is not a working fact.

When it does not fire, do nothing and say nothing. A skill that announces its
own restraint is worse than one that never ran.

## Step 1a: Parse an explicit `/dossier-record` invocation

This step only applies when the skill was invoked explicitly as
`/dossier-record ...`; it does not apply to the inline auto-fire path above,
where the fact already sitting in conversation *is* the argument and Step 1's
gate is the only gate that runs. An arg-count check on the inline path would
make the skill demand arguments instead of quietly recording what was just
said, which defeats the point of it firing inline at all.

For an explicit invocation, split `$ARGUMENTS` on whitespace and read the
first token:

- **First token is `"new"`**: the new-person variant.
  `/dossier-record "new" <name> <fact 1> [fact 2] [fact 3] ...`: token 2 is
  the person's name, every token after it is a separate fact to record for a
  person who should not already exist. If `<name>` resolves to an existing
  file (exact match or near miss per Step 2), stop and say so rather than
  silently treating this as a normal record: `"new"` is a claim that nobody
  has recorded this person yet, and that claim is worth surfacing when it is
  wrong. Fewer than two tokens after `"new"` (no name, or a name with no
  fact): request the name and at least one fact, tersely, and stop.
- **Fewer than two tokens overall** (no name, or a name with nothing to
  record): request both, tersely, and stop:
  ```
  Usage: /dossier-record <name> <fact> [fact 2] [fact 3] ...
         /dossier-record "new" <name> <fact> [fact 2] ...
  ```
- **Two or more tokens, first token well-formed as a name and second
  well-formed as a fact**: token 1 is the person (resolved per Step 2), token
  2 is the first fact. Any further tokens (3+) are **additional, separate
  facts** about the same person, not more of the second fact: each becomes
  its own bullet under Step 3, not one bullet with everything folded in.
  "Well-formed" here just means non-empty and not itself another recognised
  keyword; this skill does not reject a name or fact for looking unusual, it
  only checks that both slots have something in them before treating the
  rest as extra facts.

## Step 2: Resolve the person

```bash
ls ~/.claude/library/profiles/dossier/
```

- **Exact slug match**: open that file.
- **Near miss** (`izak` against `izaak`, a nickname, a surname): ask which
  person is meant before writing. Two files for one person is the failure mode
  that makes the whole directory untrustworthy.
- **No match**: new person, so create the file from the README's schema with
  what is known and an `## Open questions` section listing what is not. A file
  with one fact and three open questions is doing its job; it gives the next
  fact somewhere to land. Leave `id` unset; `linkedProfileIds` starts `[]`.
  Then run
  `python3 "$HOME"/.claude/library/scripts/assign_profile_ids.py` so the new
  file gets its `id` immediately: waiting until a persona derivation needs it
  (see Step 2a) would leave a freshly created file id-less in the meantime.

## Step 2a: Record a persona link (only when asked to)

Fires when a `red-*` skill's persona derivation (Step 1c in
`library/references/red/methodology.md`) has invented a name for a persona
derived from this entry and needs the link recorded on the dossier side. Not
part of the normal fact-recording flow; this skill is invoked for that
purpose specifically.

1. Append `["{persona's id}", true, "{today}", "{linkDescription}"]` to this
   person's `linkedProfileIds` (`isSource: true`, since this entry is the
   origin), and the id (not the persona's invented name) is what makes the
   link. `linkDescription` can be as specific as this file already is; it
   never leaves the machine.
2. Update `updated` too, since the file changed.
3. Report the persona's id back to whatever asked for it. Nothing else
   changes; this step never touches `## Facts` or any other section, and never
   writes the persona's own fields (`needs`, `stake`, and so on) here.

Written once per persona derivation, updated again only on a refresh (the
existing link is reused, never duplicated).

## Step 3: Write the fact

Append one bullet to `## Facts`, in Jason's words where he gave them, with
today's date in backticks at the end of the line. When Step 1a handed over
more than one fact, repeat this step once per fact, in order: each is its
own bullet, checked against Step 4's contradiction gate independently, so one
contradicting fact among several does not block the rest from being written.

- **Mark inference.** A fact Jason stated stands bare. Anything worked out from
  context takes `*(inferred)*`. This matters most when the file is later used
  to predict how someone behaves.
- **One fact per bullet.** A sentence carrying three claims becomes three
  bullets, each separately correctable.
- **Absolute dates.** "Last week" becomes the date.
- **Pronouns are only ever recorded when stated.** `unstated` stays in the
  frontmatter until Jason says otherwise, and everything written about that
  person uses they/them in the meantime.
- Update `updated`.

Facts about how to work with someone go under `## Working with them` instead.
An answered open question is deleted from `## Open questions` when its answer
is added to `## Facts`.

## Step 4: The contradiction gate

If the new fact contradicts a line already in the file, **write neither**.
Raise it in one line, quote both versions, ask which holds. The correction is
usually the more interesting fact, and silently overwriting loses the fact that
something changed.

Additive facts need no permission. This gate exists for conflicts alone.

## Step 5: Index it

A new person gets a one-line pointer in the People section of
`~/.claude/projects/-Users-jasonwarren--claude/memory/MEMORY.md`:

```markdown
- **Name**: one-line hook, [dossier](../../../../library/profiles/dossier/{slug}.md)
```

Existing people need no index change unless the one-line hook is now wrong.

## Step 6: Report

One line. `Recorded: Jaz is light on advanced skill builds → library/profiles/dossier/jaz.md`.
Then carry on with whatever the turn was actually about.

## Rules

- **Local only.** These files are gitignored on purpose. Never copy dossier
  content into a tracked file, a commit message, a PR description, an artefact
  or anything published. A guide written for a person is calibrated against
  their file; it never names them or quotes it.
- **Working notes.** Record what changes how work gets done. Personal detail
  Jason volunteers in passing stays out of the file.
- **Jason can always see it.** Anything in these files should be something he
  would be comfortable reading aloud to the person it describes.
