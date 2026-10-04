---
name: expedite
version: 0.2.0
license: MIT
description: Use when the user wants to act on an audit, fix the findings in a line-check/bug-hunt/security-sweep/latent-premises/retry-safety report, work a prioritized backlog, or asks to "fix the findings", "work the backlog", "clear the audit", or "do the high-leverage items". The step after the audit roster.
---

# expedite

The expeditor at the pass drives tickets from the board to plated, in priority order, and lets nothing leave half-cooked. This skill takes an audit backlog (from line-check, bug-hunt, security-sweep, latent-premises, or retry-safety) and executes it: highest-leverage finding first, one focused change at a time, each one verified before the next is started.

The audit roster is read-only on purpose. This is the separate step it hands off to. Findings already carry severity, effort, location, and a fix. The work is execution discipline, not re-analysis.

## Preconditions

Check before touching anything; stop and report if any fail:
- A backlog exists. The input is an audit report following the report contract (a `## Backlog` section, or `## Findings` to sort yourself). No report? Run line-check, bug-hunt, security-sweep, latent-premises, or retry-safety first, do not freelance.
- Working on a branch, never the default branch. Create one if needed (`expedite/<audit>-<date>`).
- Clean tree to start, so each finding's change is isolable.

## Execution

Work the backlog in leverage order (impact relative to effort), the order the report already sorted. If the report has only a `## Findings` section and no `## Backlog`, sort it yourself first: cheap high-impact items float to the top, severity breaks ties. An `L`-effort finding that cannot land in one focused session is not a half-job: attempt it only if it is cleanly isolable, otherwise surface it under Remaining with an estimate rather than leaving the tree mid-change.

For each finding:

1. **Read the finding, then the actual code at its "Where".** Confirm it still reproduces. Reality drifts from the report, and earlier fixes in this run may have moved or resolved later findings; a finding already fixed gets marked done and skipped, not "fixed" again. If an earlier change relocated the code, update the "Where" before proceeding.
2. **Make the smallest change that resolves it.** One finding, one focused change. Do not bundle, do not refactor adjacent code the finding did not name, do not gold-plate.
3. **For a bug or behavior change, write the failing test first** ([taste](../taste/SKILL.md)). Watch it fail, then make it pass; the failing test is the proof the change does what the finding claims. For a defect whose cause is unclear, reproduce it and trace it to the root cause before proposing a fix ([refire](../refire/SKILL.md)). A bandaid that masks the symptom is not a fix.
4. **Verify the finding is actually gone.** Re-check the "Where", run the relevant tests, run the command the fix claims to repair, and read the output before marking anything done ([check](../check/SKILL.md)). Evidence, not assertion.
5. **Commit per finding** with a message naming the effect, not the plumbing. Keeps the diff reviewable and lets any single fix be reverted alone.
6. **Mark the finding done in the backlog** with a one-line note (commit SHA or what changed), so the report becomes a live worklist.

If a fix resists you, that the problem will not verify gone after two focused attempts, do not commit a non-fix. Revert the partial change and move the finding to Remaining with what you tried, so the tree stays clean for the next finding.

When done with the runnable items, land the work: run the full suite one last time, then present the merge-or-PR options to the user and clean up the branch.

## Stop conditions (surface, do not guess)

A finding is out of bounds for autonomous execution when its fix would be destructive, public-facing, paid, hard to reverse, a breaking API change, or genuinely ambiguous in a way the report does not settle. Park it, leave it unstarted, note why at the top of the output, and keep going on the rest. The user decides the parked ones.

## Rules

- Leverage order, not severity order and not report order. A cheap high-impact fix beats an expensive critical one for sequencing; the backlog already encodes this.
- One finding per change. "While I was in there" is how an audit fix becomes an unreviewable rewrite.
- Never weaken a test or delete an assertion to make a finding "pass". That is faking the fix.
- Never mark a finding done without verifying the original problem is gone. The report is a checklist of resolved problems, not of attempts.
- Re-running the audit skill after expediting is the honest close: it should come back clean on what you fixed.

## Output shape

```markdown
## expedite: <repo> (<date>)
Branch: <branch>

### Parked (need a decision)
- [SEVERITY] title - why it is out of bounds for autonomous fixing

### Fixed
- [SEVERITY] title - what changed (<commit>)

### Skipped (already resolved)
- title - found already fixed at <where>

### Remaining
- anything left and why

**Next:** re-run <audit-skill> to confirm, then finish the branch.
```

## Common mistakes

- Re-auditing instead of executing. The findings are done; pull the trigger on the fix.
- Fixing top-to-bottom by severity, stalling on one expensive critical while ten cheap high-leverage items wait.
- Batching ten findings into one commit, so a single bad fix taints the whole set.
- Marking done off the fix being written, not off the problem being verified gone.
- Silently making a destructive or public-facing call that should have been parked for the user.
