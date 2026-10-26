---
name: lanes
description: Set, increase, or decrease the parallel lanes of a meta-orchestrator run by grouping queued issues into file-disjoint streams, with a cost line and a confirm step. Use for "/lanes 3", "more lanes" / "go faster in parallel", "fewer lanes", or when meta-orchestrator setup reaches `parallel:`.
argument-hint: "<n> | increase | decrease"
---

A lane is one stream of issues the orchestrator works in series, in its own worktree. Lanes run side by side, so they must never touch the same files.

## 0. Is there a run?

Look for `skilleddocs/orchestrator/scope.md` in the repo.

- Missing, and not called from meta-orchestrator setup → say "No meta-orchestrator run here, so there is nothing to parallelise; lanes only exist inside one (its merge gate is what keeps them safe)." Offer to start one with `/meta-orchestrator <repo>`. Stop.
- Called from setup → the queue is setup's `scope` minus `exclude`, in `order`; return the confirmed lanes and the §5 step 2 entry text to setup instead of writing §5 yourself (setup writes them and logs that entry as ledger 001).

## 1. Predict file sets

For each queued issue (open, in scope, not excluded, not already merged), in queue order:

1. Paths named in the issue body, its comments, or a linked plan.
2. Only when the issue names no paths: area labels (`area:site`, `docs`, `hooks`, ...) mapped to the directories they cover. Added to named paths, a broad label directory would merge every lane.
3. A quick `git grep -l` for the identifiers, commands or file names the issue mentions, keeping only where the change lands: the file defining an identifier the issue changes, or files the issue names. A file that only imports, re-exports or calls the identifier (a package `__init__.py`, a `cli.py`) is not in the set, unless the issue renames the identifier or changes its signature, so the callers must be edited too; then those callers are in. A behaviour change alone keeps callers out.

Record a file set per issue. Mark it **uncertain** when it rests only on a label or a guess, or the issue says "and wherever else". Shared files every change touches (a changelog, a lockfile, a generated count) count as overlap like any other file; name them in the proposal's Why line.

## 2. Group

- Two issues whose file sets overlap go in the same lane, in queue order. Overlap is transitive.
- The connected groups that result are the **independent streams**. Treat an uncertain issue as overlapping anything in its predicted area: the directories of its area label, or with no label the directories of its predicted files. An unbounded issue ("and wherever else", or no file predictable at all) does not join lanes by overlap, which would collapse every lane into one; put it in a lane named `serial`, which runs only when no other lane has an issue in flight. Once every issue queued ahead of a serial issue has started, the other lanes finish their in-flight issue and start nothing new until it merges, so it can't starve. `serial` never runs alongside another lane, so it does not count toward `parallel` or the §3 count. A swarm batch item takes its lane's slot, so a batch never exceeds the lane count.
- Pinned issues (scope.md `lanes:` or the user) stay in their lane.
- Name each lane after its area (`site`, `hooks`, `docs`), not a number.

## 3. Decide the count

`/lanes <n>`:
- n ≤ streams and n ≤ 4 → merge the smallest streams together until there are n lanes; balance by issue count. Tie (several equally small) → merge the pair sharing the most area (a common top directory or label), then the one whose first issue is queued latest. A merged lane takes the shared area's name when one covers both and is narrower than the package or repo root, else both names joined by `-` (`core-inventory`; also when the only shared area is `src/` or the package folder, which names nothing).
- n > streams, or n > 4 → ask before writing anything. Show the best-guess grouping at the largest safe count and the options, for example: "Only 2 independent streams found (site, hooks). Options: (a) 2 lanes (Recommended); (b) 3 lanes by splitting `site` on #41, which risks a conflict on `site/build.py` (uncertain prediction); (c) n lanes anyway, extra lanes idle until new streams appear." Past 4, add that the single merge gate becomes the bottleneck. Never cap silently.

`/lanes increase`: usually +1. Split the longest lane where its issues are file-disjoint. Add more than one only when several independent streams are already waiting in single lanes. Nothing splits cleanly → say so and ask.

`/lanes decrease`: −1. Merge two lanes whose upcoming issues collide, else fold the shortest lane into the nearest (most shared area). From 1 → say it is already serial.

## 4. Propose and confirm

Show, then wait for an explicit yes:

```
Lanes: 3 (was 2)
  site:   #41 #44 #47        site/, scripts/build_site.py
  hooks:  #43 #46            hooks/
  docs:   #45 #48 (?)        README.md, CONTRIBUTING.md   (? = uncertain)
  serial: #49 (?)            unbounded; runs only when no other lane has an issue in flight
Why: #45 and #48 both edit README.md; site and hooks share no files.
Cost: 3 lanes ≈ 3× tokens/hour, about the same tokens per issue. <numeric line>
Change anything? You can pin an issue to a lane, rename a lane, or move an issue.
```

- Numeric line, when the ledger records subagent token counts: average tokens per merged issue × lanes ÷ average hours per issue, e.g. "≈ 1.2M tokens/hour at 3 lanes (ledger: ~400k per issue)". No counts in the ledger → leave the qualitative line only.
- Apply pins, renames and moves the user asks for, re-check overlap (warn when a move puts overlapping issues in different lanes), and show the proposal again. Write nothing until yes.

## 5. Write

1. In scope.md's yaml block set `parallel: <n>` and a `lanes:` map, lane name → issues in order, `!` after a pinned issue:
   ```yaml
   parallel: 3
   lanes:
     site: [41, 44!, 47]
     hooks: [43, 46]
     docs: [45, 48]
   ```
2. Append a ledger `decision` entry: old → new count, lane membership, the reason, and "decided by: user" with the confirmed proposal.
3. Commit both as meta-orchestrator §5 does for ledger entries (`docs_commit` rules apply).

## 6. Mid-run effect

- The orchestrator applies the change at its next loop. It never kills an in-flight agent.
- A removed lane finishes its current issue; its remaining issues move to the lanes chosen in §3.
- An added lane starts at that next loop with its first issue.
- Tell the user this in one line after writing.
