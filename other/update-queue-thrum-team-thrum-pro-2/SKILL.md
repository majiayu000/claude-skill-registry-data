---
name: update-queue
description: "Use to reconcile your own thrum queue against ground truth - 'update my queue', 'audit my queue', 'my queue is stale', 'reconcile the queue', 'clean up done bundles', or at any session start / lull when you are about to conclude nothing is pending. Verifies each live bundle against git + beads + merge state, drops rot, adds missing committed work. Any role. A repeatable subset of a full multi-agent reconcile - scoped to YOUR queue only."
---

# Thrum: Update Your Queue (reconcile against ground truth)

Reconcile YOUR OWN `thrum queue` so its status matches reality: drop finished
rot, verify each live bundle against git + beads + merge state, add committed
work that is missing. Scoped to your queue only — cross-agent reconciles are a
larger pass (see the final section). Run it at session start, at a lull, or
whenever the queue can no longer be trusted at a glance.

Edit only your OWN queue. Handing work to another agent is a message,
never a write to their queue (see the `using-the-queue` skill).

---

## Step 1 — Snapshot the denominator

```bash
thrum queue list
thrum queue list --json | jq -r '.bundles[].status' | sort | uniq -c   # status counts
```

Read the whole list yourself. The status counts are the before-number to
reconcile against and report the delta from. Use `--json` for the tally, not
the text table: the JSON machine surface (`{"bundles": [...]}`) is a stable
contract, while the text table's column layout and footer line are not.

Two staleness classes to expect:

- **done-rot** — bundles left `done` from prior sessions, never dropped.
- **zombie live** — bundles marked `in_progress`/`blocked` (or `pending`) whose
  work has actually landed or been superseded.

`done` is a waypoint, not a resting place — it stays visible and `start`
reopens it. Only `drop` removes a bundle, and it deletes every item inside.

## Step 2 — Drop done-rot (cheap, no verification)

Every `done` bundle you are not deliberately keeping this session → `drop`.
Batch it:

```bash
thrum queue list | awk -F'\t' '$2=="done"{print $1}' | while read id; do
  thrum queue drop "$id" && echo "dropped: $id"
done
```

Keep a done bundle past this step only as a deliberate act (e.g. it may reopen
on a pending review finding) — never as the default.

## Step 3 — Verify each live bundle against ground truth

For every `in_progress`/`blocked` bundle, and any `pending` you suspect has
landed, use its lookup key to check reality. The key is the bundle's
`--ref bead:<id>` and/or a branch/SHA named in its title:

```bash
thrum queue show <bundle-id>          # read refs + title to get the key
bd show <bead-id>                     # open vs closed  (NEVER `bd list --all`)
git merge-base --is-ancestor <sha> origin/<trunk> && echo MERGED || echo NOT-MERGED
git --no-pager log --oneline --merges origin/<trunk> | grep <branch-or-sha>  # find the merge commit
```

🔴 **`--is-ancestor` answers "is this SHA reachable", not "is this content
present".** A squash- or cherry-pick-merged branch is NOT an ancestor yet its
content is on trunk — for those, `git diff <sha> origin/<trunk> -- <files>`
(empty ⇒ content landed), never ancestry alone.

🔴 **Run the check so it COULD come back negative.** Point the same
merge/ancestor check at one bundle you KNOW is still open — it must report
NOT-MERGED. A verification that cannot fail is not verifying; this control is
what separated the in-depth audit from a guess.

Classify each bundle from the evidence:

| Evidence | Verdict | Action |
|---|---|---|
| Bead closed AND content on trunk | merged | `done` then `drop` |
| Bead open / branch not landed | still open | keep (`start` if wrongly `done`) |
| Some work landed, more owed | partial | keep; make its status reflect reality |
| Work replaced by newer bundle/approach | superseded | `drop` |
| Committed/dispatched work with NO bundle | missing | add in Step 5 |
| Evidence unclear | unsure | keep — never drop on a guess |

Two-phase close for a landed bundle (make the state machine explicit):

```bash
thrum queue done <bundle-id> && thrum queue drop <bundle-id>
```

## Step 4 — Delegate the cross-referencing when it does not fit in one pass

More than ~6 live bundles to verify → dispatch read-only sub-agents, one slice
each, rather than checking them inline (see `efficient-multi-agent-research`).
Consume consolidated verdicts and make every drop/keep/add/start call yourself
— the sub-agents only gather evidence.

Give each sub-agent:

- its slice of bundles (id + ref + title),
- the exact recipe from Step 3 (`bd show`, `--is-ancestor` + the content-diff
  caveat, the discriminating control),
- the verdict table above as the required return format
  (`bundle-id → merged | open | partial | superseded | unsure`, with the
  one-line evidence for each),
- **READ-ONLY git fence**: `show`, `log`, `diff`, `grep`, `rev-parse`,
  `merge-base`, `status` ONLY — never `checkout`/`reset`/`restore`/`stash`/
  `clean`/`rebase`/`commit`/`push`, in any directory; never enter another
  worktree.
- pinned `model:` (per `choosing-subagent-models`; a cheap tier for mechanical lookups — the
  Agent tool takes no `effort`, so carry the tier via the agent definition or
  the tmux launch flags).

## Step 5 — Add missing committed work

Work you have actually committed to that has no bundle is invisible after a
restart. Add each — branches you own, dispatches you accepted, in-flight epics
— with its backlog ref:

```bash
thrum queue add --title "<what>" --ref bead:<id> --priority <N>
```

## Step 6 — Accept ambiguity, then report

Anything still `unsure` stays. A false negative (keeping stale work) is cheap;
a false positive (`drop` deletes the bundle and its items) is not — never drop
on a guess.

Re-run the status counts and report the delta:

```bash
thrum queue list --json | jq -r '.bundles[].status' | sort | uniq -c
```

One line: dropped N, added M, reclassified K; note anything left deliberately
unsure for a deeper pass.

---

## What this skill is NOT

This reconciles YOUR queue. A whole-fleet or cross-agent reconcile — auditing
what every agent is doing, routing orphaned work, re-deriving ownership — is a
larger, coordinator-scoped pass. This is the routine, repeatable subset you run
on your own queue to keep it trustworthy between those.
