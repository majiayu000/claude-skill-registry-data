---
name: compound-learnings
description: Captures a solved, non-obvious problem as a durable learning doc under docs/solutions/ with validated frontmatter, and retrieves matching learnings before new work starts. Use after a tricky bug fix, a surprising root cause, or a decision with real tradeoffs, and at the start of planning to check whether the team already learned this.
---

# Compound Learnings

Every non-obvious fix that lives only in one engineer's head (or one chat transcript) gets
re-discovered later at full cost. This skill writes it down once, in a place the next engineer
(human or agent) will find by grepping for the symptom.

Two halves: **capture** (after the work) and **retrieval** (before the work).

## The durable bar

Write a learning only when it passes this counterfactual:

> If this document did not exist, would a future engineer reading the final code, tests, and
> existing docs still be likely to repeat the mistake or redo substantial investigation?

Yes -> write it. No -> write nothing and say why.

Effort, diff size, and "it was hard" do not qualify a learning. What qualifies:

- A bug whose root cause was not where the symptom pointed.
- A fix that looks wrong or unnecessary without the story behind it.
- A failed approach that a reasonable engineer would try first.
- A decision with real tradeoffs where the losing option will look attractive again.
- A tooling or environment quirk that cost more than an hour.
- An existing learning that is now inaccurate (update it; a misleading doc is worse than none).

One learning per doc. A session that produced three learnings produces three docs.

## When to run

- Right after a non-obvious bug fix is verified (tests pass, behaviour confirmed).
- After a root cause turned out to be surprising.
- After a decision with tradeoffs was made and its rationale would otherwise be lost.
- When `opm:executing-plans` or `opm:verification-before-completion` finishes a task and the
  session contains reasoning that is not in the code.

Do not run it for routine work whose artefacts already explain themselves.

## Capture procedure

### 1. Check for an existing doc

Search `docs/solutions/` by symptom, error text, module, and tag before creating anything:

```bash
grep -rliE 'symptoms:.*(<error fragment>|<symptom keyword>)' docs/solutions/
grep -rliE '(title|tags):.*(<module>|<library>|<concept>)' docs/solutions/
grep -rli '<distinctive error string>' docs/solutions/
```

If a match covers the same root cause: update that doc (add the new symptom, correct the fix,
refresh the date) instead of creating a duplicate. If a match is adjacent but different, link
it via `related:`.

### 2. Choose category and slug

Category is the subdirectory under `docs/solutions/`. Use an existing one when it fits; the
canonical set is `build-errors`, `test-failures`, `runtime-errors`, `performance`, `database`,
`security`, `ui-bugs`, `integration`, `logic-errors`, `architecture`, `tooling`, `conventions`,
`workflow`. The slug is lowercase, hyphenated, and names the problem, not the fix:
`docs/solutions/runtime-errors/stale-closure-in-websocket-reconnect.md`.

### 3. Write the doc from the template

Copy `assets/resolution-template.md` (in this skill directory) and fill every section:

- **Problem** - what was observed and what it cost (1-3 sentences).
- **Investigation** - what was tried, in order, including the dead ends and why they were plausible.
- **Root cause** - the actual mechanism, at the level of "why", not "what".
- **Fix** - what changed, with the smallest code excerpt that shows it.
- **Prevention** - a test, lint rule, guard, or convention that stops recurrence. If nothing prevents it, say so.
- **References** - commits, PRs, issues, upstream docs, related learnings.

Frontmatter fields: `title`, `date`, `category`, `problem_type`, `symptoms[]`, `root_cause`,
`severity`, `tags[]`, `related[]`. Symptoms are the strings someone would grep for: error
messages, log lines, observable misbehaviour. Tags are lowercase-hyphenated technologies and concepts.
Quote any YAML value containing `: ` or ` #`.

### 4. Validate the frontmatter

```bash
node <skill-dir>/scripts/validate-frontmatter.js docs/solutions/<category>/<slug>.md
```

The script checks required fields, enum values for `problem_type`, `severity`, and `category`,
the date format, and YAML quoting hazards. Exit code 1 lists what to fix. Do not commit a doc
that fails validation.

### 5. Optionally index it

If `docs/solutions/INDEX.md` exists, append one line:

```markdown
- [<title>](<category>/<slug>.md) - <one-line root cause> (`<tag>`, `<tag>`)
```

If it does not exist, skip this step; grep over frontmatter is the primary retrieval path.

### 6. Report

State the path written or updated, the one-sentence root cause, and the prevention added.
If nothing was written, state which part of the durable bar failed.

## Retrieval: check the corpus before new work

Before planning (`opm:writing-plans`, `opm:milestone-planning`) or debugging, spend two minutes
looking for prior learnings. Grep frontmatter first, read only the matches:

```bash
# Discover categories that exist in this repo
ls docs/solutions/

# Match on the fields most likely to carry the signal, case-insensitive, in parallel
grep -rliE 'title:.*(<keyword>|<synonym>)' docs/solutions/
grep -rliE 'tags:.*(<library>|<concept>)' docs/solutions/
grep -rliE 'symptoms:' docs/solutions/ | xargs grep -liE '(<error fragment>|<behaviour>)'
grep -rliE 'problem_type: (<type>)' docs/solutions/
```

Scoring: a hit on `title`, `tags`, or `symptoms` is strong; a hit only on `problem_type` or
`category` is weak. Read the frontmatter (first ~20 lines) of strong hits, then the full doc of
the ones that still look relevant. Cap at five docs.

Turn what you find into planning inputs: constraints to respect, approaches known to fail,
tests that must exist, and files to read first. Note each doc's `date`; a learning can be
superseded by later code, and present evidence beats past notes. If the corpus has nothing,
say so; that absence is itself a signal that the current work may be worth capturing afterwards.

## Anti-patterns

- Writing a learning for every task. The bar exists so the corpus stays trustworthy.
- Recording the fix without the investigation. The dead ends are the valuable part.
- Vague symptoms ("it was slow"). Put in the exact error text or metric.
- Batching several learnings into one doc. Retrieval works per problem.
- Skipping the grep and creating a duplicate that later contradicts the original.

## Related skills

- `opm:tdd-workflow` - the reproducer test often becomes the Prevention section.
- `opm:writing-plans` and `opm:milestone-planning` - run retrieval at the start of both.
- `opm:brainstorming` - decisions with tradeoffs made there are capture candidates.

<!-- Adapted from EveryInc/compound-engineering-plugin (MIT) -->
