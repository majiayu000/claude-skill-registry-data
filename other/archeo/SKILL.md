---
name: archeo
description: Comment-archaeology sweep - find work items hiding in TODO/FIXME/for-now comments and plan-doc ledgers, judge them, file issues, queue trivial fixes. Good idle-loop activity.
---

# Comment Archaeology

Work items recorded only in comments, PR bodies, or plan ledgers get rediscovered by audits years later or never. This sweep finds them, judges them, and converts the real ones into issues (the searchable, labelable record) per the residuals-to-issues policy.

## Finder pass

Scan for deferral language (ripgrep; comments and docs both):

```bash
rg -n 'TODO|FIXME|HACK|XXX|for now|temporar|deferred|follow-up|revisit|residual|inversion target|placeholder' --type rust -g '!target' | grep -v 'test'   # triage test hits separately, don't drop them
rg -n 'deferred|residual|open question|未|TBD' docs/plans/ docs/*.md
```

For scale, dispatch finder agents per area (src/store, src/search, src/cli, docs/plans) with a shared output format: `file:line | quote | claimed reason`.

## Judge pass

For each hit, decide (nested judge agents for big batches; fable for judgment):

- **Already done** — the deferral shipped but the comment survived → queue a comment scrub (trivial lane).
- **Stale premise** — the referenced issue/feature is closed/deleted → scrub or rewrite to the surviving invariant.
- **Real work >30min** — file an issue NOW (`gh issue create` via PowerShell, `--body-file`). Batch related nits into one umbrella issue — over-filing discredits the policy. The comment keeps only the timeless invariant; the work item moves to the issue.
- **Real work <30min** — queue into a trivial-fix lane (lane-implementer agent, one branch for the batch).

## Constraints

- The provenance lint bans issue refs in comments — when rewriting a comment, state the invariant, never "see #1234".
- Closing umbrella issues orphans their sub-phases — check before closing any umbrella surfaced here.
- Plan-doc ledgers (docs/plans/*.md) claim completeness ("every deferral is listed") — verify the claim against the sweep results and amend the ledger when it lied.

## Output

Report: N hits → already-done / stale / issued (#s) / queued-trivial, plus the scrub branch if one was opened. Land via /land.
