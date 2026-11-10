---
name: check-upstream-skills
description: Report what changed upstream in the vendored skills' source repos since the last sync, then sync what the user picks.
disable-model-invocation: true
---

`.claude/skills/upstream.json` is the manifest: each upstream source, its `syncedSha`, and every upstream path with a `status` (`vendored`, `reference-only`, `declined`), a `reason` for declined, and `notes` recording deliberate divergences of the local copy, and a `derivedInto` list of its forks: a bare name is a skill at `.claude/skills/<name>/`, an entry with a slash a repo-relative path.

## 1. Run the report

`node .claude/skills/check-upstream-skills/check.ts <scratchpad>/upstream-check`. It clones or fetches each source and prints the report; it writes nothing in the repo. Exit 1 means something moved; exit 0 prints "Up to date." and you are done.

## 2. Brief the user

Read the `.patch` file it names. For every changed tracked path, give a one-line verdict: what changed, and whether to take it. Its report line ends `forks: <paths>` when it has forks; give each fork its own one-line verdict on whether to apply the same change at that path. Name each unclassified skill, each path gone upstream, and each promoted-set change, with a suggested status. Mention declined and in-progress changes only when one looks like a reason to revisit the decision.

Done when every line of the report has a verdict, and the user has chosen what to take.

## 3. Sync what the user chose

- **Take a vendored change:** copy the upstream folder over `.claude/skills/<name>/`, then reapply every divergence its `notes` record, so the copy differs from upstream only by those notes.
- **Take a change into a fork:** edit the fork by hand to apply the change the user chose. A fork is this repo's own, so upstream is never copied over it.
- **Classify a skill:** add its path with a status; a declined one gets a one-line `reason`.
- **Bump** the `syncedSha` of each path you synced or reviewed; once every path is reviewed, bump the source's `syncedSha` and copy the upstream `plugin.json` `skills` list into `promoted`.

Done when a rerun of step 1 lists only the changes the user chose to leave.
