---
name: ship
description: Implement, veryify and review a feature based on its SPEC.
argument-hint: "[path to the SPEC /slice wrote]"
---

# Ship

`/slice` gives you a SPEC. This runs the rest of the chain against it:

```
Prepare  --> Implement --> Review --> Verify --> Explain
  prep        tdd          5 lenses    real app   artifact
  refactor                 + fix
```

Each step runs in a context that never saw the one before it. That's the whole
point — a session that just wrote the code is the worst possible reviewer of it,
and a session that watched the review happen writes a walkthrough that defends
the review instead of the change.

## Run it

Hand `assets/workflow.js` to the Workflow tool, with the SPEC path as `args`:

```
Workflow({
  scriptPath: "<this skill's directory>/assets/workflow.js",
  args: { spec: "docs/specs/<the-slug>.md" }
})
```

If `scriptPath` is refused, read the file and pass its contents as `script`
instead. Don't rewrite it inline from memory.

No SPEC path? Ask for one. The script throws without it, and every step after
`Prepare` measures itself against those acceptance criteria — the chain has
nothing to aim at otherwise.

## When it returns

The return value is the whole report — nothing reaches the user on its own. Open
the walkthrough for them (`Artifact` with `action: "open"` on `walkthrough`), then
say these four things before you summarize anything:

- `suiteGreen` — false means the branch is red, whatever else the run says
- `bugsFound` — the explainer hit something real while writing up
- `criteriaUnbuilt` and `reviewLeft` — what's still owed
- `verified` and `lensesUnchecked` — what nobody actually checked

A halted run returns `haltedAt` and `reason` instead, carrying every report the
run produced. Hand those over rather than summarizing them; someone is about to
pick the work up by hand and those reports are all they get.

## Why the script does the fan-out

A subagent has no tool for spawning subagents. Nested delegation doesn't exist,
and `agentType: 'general-purpose'` doesn't buy it either — both were checked.

That matters because `/multi-lens-review` is five reviewers held apart on purpose. Hand the
whole skill to one agent and it plays all five, which is the failure the skill
names in its own opening: one reviewer asked all five questions spends its
attention on naming nits and never reaches "those five files are one domain
object in a trenchcoat." So the script spawns the five itself, each told to read
one `agents/*.md` fragment and nothing else. The prompts stay in the review
skill; the script only owns the dispatch.

`/preparatory-refactor` loses its recon fan-out the same way, and takes the
fallback its own SKILL.md already sanctions — a timeboxed skim. Weaker, and the
report says so rather than letting a skim read as a sweep.

## Where it deviates from the skills

Three places, each because nobody is watching the run:

- `/preparatory-refactor` identifies and refuses to edit. Kept — a second agent
  makes the move, so the one proposing it isn't the one defending it.
- `/implement-with-tdd` says leave everything uncommitted. Overridden; every step
  commits through `/commit`, because the next one diffs against what the last one
  left, and `Explain` never saw the sessions that wrote the code. The commit
  messages are its only record of why.
- `/multi-lens-review` refuses to apply findings unasked. Overridden for what it files under
  Defects and Compatibility — the two that cost something the moment this ships,
  which is why its own synthesis sorts them first. Conventions, domains and
  fidelity are judgment calls, so they stay in the report for you.

The gate is the heading, not the score. Confidence would be the wrong axis: the
review skill sorts defects by consequence precisely because a confidence-95
off-by-one in a log line matters less than a confidence-82 unbounded delete.

## Where it stops

Every halt carries out every report the run produced, because a halt is where you
pick the work up by hand and those reports are all you get.

- **Prepare** — the refactor agent stopped, or left the suite red. A
  behavior-preserving move that breaks tests broke the one thing it promised.
- **Implement** — any of `/implement-with-tdd`'s own stops: budget overrun, a
  suite that won't run, a scope question. Those are yours to answer, and starting
  anyway is how a workflow decides one on your behalf and calls it progress.
- **Review** — no base branch resolved, an empty diff, or a diff past 1500 lines.
  All three would otherwise produce a clean-looking review of nothing: five agents
  handed an empty file go find something in the neighboring code, and five handed
  2000 lines review the front of it and say nothing about stopping.

A dead agent halts wherever it dies, and says so as a dead agent — not as a
finding about your repo.

## What stays outside

Everything before the SPEC — `/domain-model`, `/slice`, and the `/understand`,
`/eli5`, `/rubber-duck` passes you make over what they produce. Those are the
steps where you're the one doing the thinking, and handing them to a fleet of
agents defeats why you ran them.

`Verify` is the weak link in here. An agent can boot the app and drive it, but it
can't hand you the screen. Treat its report as "the app started and the criteria
appear to hold," then look yourself — especially at anything the artifact flags.
