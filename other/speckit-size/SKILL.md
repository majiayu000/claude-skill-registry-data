---
name: "speckit-size"
description: "Route a piece of work to the amount of process it actually needs — trivial, one-session, feature, or project — and record the choice so the gates and /speckit-auto read it instead of assuming. Run it before /speckit-specify, or when a full spec cycle feels like paperwork for a small change."
argument-hint: "The work, in a sentence. Or nothing, to report the level already chosen."
compatibility: "Node 18+. Writes only the `level` field of .specify/feature.json."
metadata:
  author: "speckit-demo"
  source: "adapted from BMAD's scale-adaptive routing (docs.bmad-method.org/plan/choose-a-planning-path)"
user-invocable: true
disable-model-invocation: false
model: sonnet
---

## User Input

```text
$ARGUMENTS
```

## Phase 1 — classify, cheaply

```bash
node .claude/scripts/level.mjs suggest "<the work, one sentence>" --set
```

It sizes only the text it is given and reads no tracker: a bare `ST-<n>` or
issue URL is sized as those words, which is almost always `unsure`. For a
story, pass its title and the gist of its Build brief (`gh issue view <n> -R
george-hutanu/motor-fix-specs`); boards, a missing Build brief section or a
large story are reasons to answer 2 yourself when the classifier is unsure.

A local classifier answers first and costs nothing. It decides only the clear
cases: an edit to text or to a name only the code reads is 0, anything touching
a contract, data, identity, money or a new surface is 2, and an epic is 3. A
risky word always outranks a trivial one, and a word that adds behaviour makes
it `unsure`, never 0. Jev answers next if it has a key. Then:

- **It printed a level and `recorded for …`**: done, go to Phase 3. Do not
  re-argue a confident answer, except a 0 the description plainly contradicts
  (it adds or changes behaviour): then `set` the level it deserves.
- **It printed `unsure`, or `low confidence`**: answer the one question below
  in one or two sentences, then `node .claude/scripts/level.mjs set <0-3>`.

> **Is the intent already well defined?** It says what is true when done,
> what must not change and what is out of scope, completely enough that someone
> else could build it without guessing.

If you cannot say what "done" means without inventing a requirement, it is at
least 2. **Size the intent, not the diff:** a one-line change to what `--json`
emits is a contract change; a 400-line mechanical rename is not. Level 3 only
when more than one feature or epic must not diverge.

| Level | Name | When | Owes | Phases |
| --- | --- | --- | --- | --- |
| 0 | trivial | obvious, low-risk, reversible | nothing | edit, verify |
| 1 | one-session | one coherent unit, intent already clear | `spec.md`, `tasks.md` | specify → tests → implement → review |
| 2 | feature | the default: intent needs settling, design has choices | `spec.md`, `plan.md`, `tasks.md` | the full chain |
| 3 | project | several features that must not diverge | level 2, plus a shared brief | the full chain, per feature |

When unsure between two levels, take the higher one. A spare plan.md costs a
few minutes; a missing one costs a rewrite.

## Phase 2 — where it lands

`set` binds the level to the work it was sized for (`level_for` in
`.specify/feature.json`). On the feature's own branch that is the current
feature. Anywhere else it is `next`: it applies to no feature that exists, and
`/speckit-specify` hands it to the directory it creates (`level.mjs point`),
once, if that happens within 30 minutes. After that, or for a feature HEAD
already holds, the default applies and `point` says so: size again with
`--current`. Level 0 is never carried, since a trivial change creates no
feature. A level sized for another feature is ignored, so an old "trivial"
never shrinks new work. Force the target with `--current` or `--next`; for one
command only, use `SPECKIT_FEATURE_LEVEL=1 <command>`.
`node .claude/scripts/level.mjs` reads it back with its source and what waits.

## Phase 3 — say what it changed

One line: the level, and the phases it skips. For example: "level 1: no
plan.md, research.md or contracts/; `/speckit-tests` still runs first."

## What a level never does

It chooses **how much planning** a change carries, never whether it is tested.
`pre:edit:red-first` reads the spec and tasks, not the level; spec-drift still
wants `specs/` beside a `feat`/`fix`/`perf` commit to `apps/*/src` or
`libs/*/src`; `trace-matrix.mjs --check` still fails on untested requirements.
If a level could turn those off, 0 would be the way out of every gate.
`artifact-lint` is the only check that reads it, and only to stop asking for a
plan at levels 0 and 1.
