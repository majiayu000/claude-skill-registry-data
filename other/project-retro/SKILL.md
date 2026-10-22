---
name: project-retro
description: >-
  Mines the current (or a described) coding session for friction and hard-won knowledge, then
  fixes it at the source instead of just writing it down: saves a repeatable trap to this
  project's `.claude/memory/` as a `gotcha`, or hands off to `skill-report` when the devkit
  itself should have caught the mistake. Use when the user says "capture what we learned",
  "do a retro", "write this down for next time", "what would make this faster next time", or
  after a session that involved real digging or more than one wrong turn.
user-invocable: true
argument-hint: [optional: what felt slow or went wrong]
---

# project-retro

`skill-report` already covers the half of this that's the devkit's job: a mistake a devkit
skill should have prevented. This skill covers the half that's the project's own: friction
that isn't the devkit's fault, and knowledge worth keeping even when nothing went wrong. Both
ends write to something the next session actually reads, not a narrative nobody reopens.

## Scope

- IN: a session that just happened (or one the user describes) in a project with the devkit
  loaded. Sorting what it cost into: save as a `gotcha`, hand off to `skill-report`, or offer
  it as a `.claude/memory/` entry of another type.
- OUT: a gotcha `feature-build` or `investigate-bug` already saved during this same session —
  check `.claude/memory/` first, don't write it twice. Inventing a new `.claude/memory/` entry
  type (the format is fixed by `project-init`'s templates; if nothing fits, say so and ask
  rather than extending it unprompted). Writing a new devkit skill directly — a real gap in the
  devkit becomes a `skill-report` issue, never a skill hand-rolled from inside a consumer
  project. A feature request with nothing concrete to show yet — say so and stop.

## Argument

`$ARGUMENTS` may name what felt slow or point at the incident. If it's empty, mine the current
conversation. If the session isn't in context (the user is describing an earlier one), ask for
each incident's three facts below rather than inventing one.

## Steps

1. **Gather the incidents.** For each one: what happened, the concrete cost (extra tool calls,
   a guess that had to be undone, time spent digging), and the general rule or fact it
   reveals. Include knowledge that took real digging but turned out *correct* the first time
   (a pattern reconstructed from CMS source, an API shape found by trial) — "nothing broke"
   isn't the same as "nothing worth keeping."
2. **Filter.** For each incident, would having it written down next time actually have saved
   work — not "maybe, a little"? Drop the rest. Three real incidents beat a longer list padded
   to look thorough.
3. **Check what's already captured.** Read `.claude/memory/MEMORY.md`. Drop anything
   `feature-build` or `investigate-bug` already wrote this session. If an incident is close to
   an existing entry, point at that entry instead of writing a near-duplicate.
4. **Sort what's left:**
   - A trap in the platform, stack, or process the project's own code or setup walked into —
     not caused by Claude getting something wrong → **gotcha**, written in
     `.claude/memory/`'s existing format (see its `README.md`).
   - Claude wrote or advised something wrong that a devkit skill should have prevented → hand
     off to `skill-report`, passing it the incident you already gathered so it doesn't
     re-interview the user.
   - Correct, hard-won knowledge that's neither of the above → check whether it's a `decision`
     or `reference` under the existing `.claude/memory/` types. If it genuinely fits neither
     (a reusable snippet or reconstructed API shape, not a fact or a pointer), say so in the
     hand-off instead of forcing it into a type that misdescribes it.
5. **Show the sorted list before writing anything.** One line per incident: its bucket, and
   where it's going. Write the memory entries, or draft the `skill-report` hand-off, only once
   the user says yes — same discipline `skill-report` itself uses before it posts.

## Rules

- Don't journal. "We ran X then Y then Z" isn't a finding unless a step in it broke or could
  break again.
- Don't invent generic advice. Every line traces to an incident that actually happened this
  session, not a general best practice that sounds right.
- State the general rule, not the one-off literal, unless the literal is the reusable thing
  itself (a real snippet, a real command).

## Hand off

One line per incident: saved to `.claude/memory/`, sent to `skill-report` (with its result),
or skipped and why. If another skill started this one, return that list and stop. That skill
decides what runs next.
