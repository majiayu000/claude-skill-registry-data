---
name: task-flow-cycle
kind: pattern
rule: task-flow
description: Pattern of rule task-flow. Load when an edit of a rule, a hook, a check or a role is chosen and when its result is judged. The worst driver from the report, one metric and its direction in the task, the verdict from the next report, and the plain name of an edit that moved nothing.
---
<!-- rt-kit v0.34.0 · patterns/task-flow-cycle.md · 1ecd9c22c48c · правится надстройкой, не здесь -->

# The improvement cycle

Pattern of the rule `task-flow`. What must be true meanwhile — the law
`docs/constitution/work-conduct.md`.

## When to use

- An edit of a rule, a hook, a check or a role is being chosen.
- A task about such an edit is being written.
- The result of such an edit is being judged.

An edit chosen by opinion has no way to be proved wrong, so nobody learns whether it helped. A repair
of something broken is not an improvement and needs no cycle: its task names the failure instead.

## Order

### The report opens the cycle

The cycle begins with the numbers, not with an idea of what to improve.

```bash
npx agent-kit metrics
```

The worst driver of the main metric is named with its numbers: which resource, how many refusals,
runs or minutes. A tree that sends its numbers reads the same in the receiver over all its copies. No
data means no cycle: the text says so, and nothing is chosen by a guess.

### One task, one metric, one direction

The task changes one thing and carries one line:

```markdown
**Metric:** empty refusals of `git-guard-push`, down. Baseline: 0.42 over 30 days, noise 0.05.
```

- **The direction is a word, not a target.** A target needs a baseline first, and two weeks of data
  or ten accepted tasks come before one.
- **Two metrics mean two tasks.** Two edits in one release cannot be told apart in the next report.
- **The edit does not raise its own numbers.** The observations are not edited, and a metric is not
  redefined by the task that is judged by it.

### The next report gives the verdict

The same trees are compared, on a version with the edit against themselves before it. A tree that has
not installed the version does not count.

- **The executor who made the edit gives no verdict.** The role `goal-critic` reads the numbers.
- **A movement below the noise is not a result.** The noise is the spread of the metric between the
  weeks of the baseline, and it is named with it.

### An edit that moved nothing is named so

The report says «не сдвинулось», with the two numbers. It is not reworded as a partial success and not
explained by the days being unusual. Such an edit is reverted or kept by a decision of the owner, and
the next cycle starts from the report again.

## Common misses

- **A metric picked after the edit.** A number chosen once the result is known finds a movement in any
  edit. The line stands in the task before the first commit.
- **Reading one's own tree as the package.** One tree is the partial view: it lacks completeness and
  repeated mistakes.
- **A rising count taken for a worse rule.** More refusals also come from more work. A share is read
  against its denominator.
