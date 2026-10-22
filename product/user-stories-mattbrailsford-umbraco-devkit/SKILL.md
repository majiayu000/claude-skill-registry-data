---
name: user-stories
description: >-
  Writes, splits and refines user stories with Given/When/Then acceptance criteria in
  STORIES.md, feeding bdd-specs. Use when turning a feature request or a vague ask into a
  testable backlog entry.

---

# User stories

Turn product intent into stories that flow straight into `bdd-specs` with no manual
reshaping. The structure here is a contract, not decoration — get it right and stories
become specs become code with nothing lost in translation.

**Honest framing:** this is a discipline this plugin introduces, not one already standard
across Umbraco projects — don't present it to a team as "the Umbraco way." It's a real,
well-understood technique worth adopting on its own merits, and it's what makes
`bdd-specs`'s handoff work cleanly.

## Where this writes

`STORIES.md` in the feature's plan folder (owned by `feature-plan`, which usually dispatches
this skill as its first step). If invoked standalone before `feature-plan` has run, still write
to the same file, and note that `feature-plan` still needs to run to turn the stories into an
ordered, dependency-aware task list in `PLAN.md`.

## *The pipeline this sits in*

```
feature request ──▶ [user-stories] ──▶ STORIES.md ──▶ [bdd-specs] ──▶ specs ──▶ code
```

Map deliberately:

| Story artifact | Becomes in bdd-specs |
|---|---|
| One story | One Feature (one test class) |
| One acceptance criterion | One Scenario (a nested test-class group, or a `#region`) |
| Given/When/Then steps | The Scenario's arrange / act / assert |
| Each distinct Then | One Specification (one `[Test]`, one assertion) |
| Happy-path criteria | Listed first, exhaustively |
| Error/edge criteria | A separate, clearly-named "sad path" group |

Write acceptance criteria as Given/When/Then from the start — that single habit is what
keeps the handoff clean.

## Workflow

### 1. Establish context before writing

Don't invent the role, the goal, or the value. If handed something vague ("add
notifications"), ask:

- **Who** is this for? Be specific — "content editor with publish rights," not "user."
- **What** do they want to do?
- **Why** — a story whose "so that" is hollow ("...so that I can use the feature") is usually
  a task, not a story.
- What does *done* look like, observably?
- What's explicitly **out of scope** for this story?

Ask the smallest number of questions that unblock you. If told "just draft it and I'll
correct it," do that — draft, mark assumptions with `> ASSUMPTION:` lines, and let the
reaction do the specifying.

### 2. Write the story

```
As a <specific role>,
I want <capability>,
so that <outcome / value>.
```

Then acceptance criteria, each a self-contained scenario:

```
AC1 — <short name>
  Given <starting state>
  When  <action>
  Then  <single observable outcome>
```

One outcome per `Then` — "and also" is a second criterion, since it becomes a second
Specification downstream. Happy path exhaustively first, then error/edge criteria under a
clearly separated heading.

Error criteria are where two outcomes most often slip into one `Then`: "the request is refused
and no file is returned", "no email is sent and a warning is logged". Each is two criteria.
Before writing the file, reread every `Then` and split any that joins two results with "and".
One result described by several values ("the file has the rows `news,4` and `old,0`") is
still one outcome.

### 3. Quality-gate with INVEST

The two failures that matter most in practice:

- **Too big (not Small).** Can't enumerate its acceptance criteria, or it spans multiple
  roles/outcomes? Split it. Prefer vertical slices (a thin end-to-end capability — e.g. "an
  editor can save a draft note on a content item," backend + UI together) over horizontal
  ones ("build the API," "build the UI"), because a vertical slice is independently valuable
  and testable on its own.
- **Not Testable.** Can't phrase the acceptance criteria as Given/When/Then with an
  observable outcome? The story is underspecified — go back to step 1, don't lower the bar.

(The full INVEST set — Independent, Negotiable, Valuable, Estimable, Small, Testable — is a
useful checklist if a story feels off in a way these two don't explain, but these two catch
the common failure modes.)

### 4. Epics

An epic is a container, not a big story — a heading grouping child stories. Decompose only as
far as the near-term plan needs; leave later stories as one-line placeholders. Over-
decomposing a backlog that will change is waste.

### 5. Definition of Ready / Definition of Done

These are team agreements, not house rules — confirm them with the user rather than asserting
defaults. Capture the agreed version once, at the top of `STORIES.md`, so every story in that
feature inherits it instead of restating it. Reasonable starting points to offer (not impose):
**Ready** — role/capability/value all stated and non-hollow, Given/When/Then acceptance
criteria cover the happy path, out-of-scope is explicit, passes INVEST. **Done** — all
acceptance criteria pass as executable specs (via `bdd-specs`), sad-path criteria are covered
too, plus whatever the team adds (review, docs, deployed behind a flag, etc.).

## Scope boundaries

- **In scope:** writing stories, splitting/refining them, acceptance criteria, epic
  decomposition, turning a feature request into a structured backlog entry.
- **Out of scope:** story-point estimation and sprint capacity — team rituals that depend on
  a team's own history and velocity. Offer relative-size flags (S/M/L, or "this is too big,
  split it") instead of fabricated point numbers.
- **Hand off, don't overlap:** generating executable specs is `bdd-specs`'s job.
  Sequencing into an ordered task list is `feature-plan`'s job. Produce the story, point at
  the next step, don't do it here.

## Output

Write stories following `plain-writing`: plain words, one behaviour per criterion, and
every name, number and condition kept.

Write or update `STORIES.md`. If stories already exist there, merge — preserve story ids
already in use (specs reference them) and append or amend rather than rewriting wholesale.
After writing, report how many stories the file now holds and that it's ready for
`bdd-specs`.
