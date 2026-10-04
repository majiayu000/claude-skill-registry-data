---
name: ship
description: Answers "ship this", "what's next in the pipeline", "where am I in the pipeline", "what's left before I open a PR", and "take this to PR" by routing work through the delivery pipeline (explain, plan, test design, implement, verify live, review, describe, demo). It checks where the current branch stands with cheap read-only checks, names the current stage and the one next stage with the skill or command that runs it, and asks before starting it; it can also jump to a named stage or hand the remaining stages to a multi-agent run. Use when the user asks which delivery step or skill comes next. Not for "what's next" about code, a function, or a plan step; answer those directly.
argument-hint: "[stage | all]"
---

# Ship

Say where the work stands and which one stage comes next. This skill only routes: every stage's rules live in that stage's own skill, so it never restates them and never does stage work itself.

**Project settings**: on every invocation, read `.claude/shipyard/ship.md` in the project root if it exists; its settings win over the defaults here. It can set which stages the project uses, the base branch, where plans and stage reports live, and per-stage overrides such as when to skip a stage. Its shape is in [references/overlay-example.md](references/overlay-example.md).

## Stages

| # | Stage | Runs with | Enter when | Skip when |
|---|---|---|---|---|
| 0 | explain | walkthrough | the user needs the area or the change explained | the user knows the area |
| 1 | plan | the platform's plan mode | there is a goal but no plan | a one-file, obvious change |
| 2 | test design | design-tests (test-designer agent) | a plan or spec exists and the diff has no tests for it | tests for the change are already in the diff; docs-only change |
| 3 | implement | this session; prisma-workflow when a Prisma schema changes | tests are designed, or the diff is partial | never; prisma-workflow only when a schema file changed |
| 4 | verify live | live-verify (live-verifier agent) | code and tests are in the diff | docs-only, test-only, or no runnable app (a library) |
| 5 | review | `/shipyard-delivery:pr-review` | verified or verify skipped | never |
| 6 | describe | `/shipyard-delivery:pr-description` (flow-diagram for diagrams) | reviewed, no PR yet or its description is stale | the user isn't opening a PR |
| 7 | demo | no skill yet | a PR is open | always, until a demo skill exists |

A schema file changed with no new migration generated for it means stage 3 isn't done: route to prisma-workflow before verify live or review. Cross-cutting, at any stage: flow-diagram, skill-auditor, the signal output style. `/shipyard-delivery:build-workflow` runs several stages as one multi-agent run and decides itself when one agent is enough.

## Steps

Steps are agent-owned unless marked.

```
- [ ] 1 Read settings
- [ ] 2 Look
- [ ] 3 Place the work
- [ ] 4 Report (gate)
- [ ] 5 Start on a yes
```

1. **Read settings.** Base branch: the settings, else the remote's default branch, else whichever of `main` or `master` exists.
2. **Look, read-only and cheap.** No builds, no test runs, no writes. With a shell: current branch, changed files against the merge base plus uncommitted ones, whether a pull request is open (the code host's CLI, if installed and authenticated; otherwise "PR: unknown"). Without one: `.git/HEAD` for the branch, `.git/logs/HEAD` for its commits, and file globs. Without a shell there is no diff: infer the change from the branch's commit messages and the files they name, and say the diff is inferred. Also look for a plan file, test files for the changed code, Prisma schema files and their migrations, and stage reports the settings name. Test results are a claim (commit message, the user, CI), never a run.
3. **Place the work.** Walk the table top-down. The current stage is the last one done, or one left half-done; the next stage is the first whose work isn't done and isn't skipped, which may be the half-done one. Evidence of a later stage (code in the diff, an open PR) marks the stages before it done. Signals that conflict (tests in the diff but no code, say) get named, not guessed past.
4. **Report**, in this shape:

   ```
   Stage: <n> <name> — <evidence, one line>
   Skipped: <stage (why)>, ...
   next: <n> <name> — <skill or command>
   Then: <the remaining stages, in order>
   ```

   Then **STOP — WAIT**: ask whether to start the next stage. `next:` names one stage; `Then:` is orientation, not a queue.
5. **Start on a yes.** A skill the model may invoke (walkthrough, design-tests, prisma-workflow, live-verify, flow-diagram): invoke it. pr-review, pr-description, and build-workflow are user-invoked only; the platform blocks the model from invoking them, so print the exact command (`/shipyard-delivery:pr-review`) for the user to run, and don't reproduce their steps by hand. Plan and implement are the platform's own: tell the user to enter plan mode, or continue in this session.

## Arguments

- **A stage** (number, name, or skill name): jump to it. If its entry condition isn't met, say which and **STOP — WAIT** before starting it anyway.
- **`all`**: hand the remaining stages to a multi-agent run: print `/shipyard-delivery:build-workflow <plan file> <remaining stages>`. It shows its own run plan and waits for a go.
- **Nothing**: steps 1 to 4.

Demo has no skill yet: when it comes next, say so and name it as the last stage; don't substitute another skill.

`next:` the stage the user confirms, through its own skill; this skill hands off and ends.
