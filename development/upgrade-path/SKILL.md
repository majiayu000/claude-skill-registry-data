---
name: upgrade-path
description: Work toward the next major framework upgrade (Spring Boot, Rails, Django, React, and the like) in small, bounded steps using the Mikado Method, tracked in UPGRADE-PATH.md.
disable-model-invocation: true
---

# Upgrade path

All state lives in `UPGRADE-PATH.md` at the repo root; every run reads it
first and leaves it updated.

Each run is exactly one of two modes, chosen by the user or, failing
that, by the graph. Run Explore when the graph is empty or has no open
leaves, otherwise Execute.

## Explore

Never fix anything.

1. Read `UPGRADE-PATH.md`. If missing, create it from
   [the template](references/UPGRADE-PATH.template.md).
2. Attempt the root goal (bump the core framework to the next major
   version), or the lowest open node if one is chosen.
3. Build and run tests. Record each distinct breakage as a child node
   under what it blocks, with a short note on why.
4. Revert all code changes. Keep only the edit to `UPGRADE-PATH.md`.

## Execute

A leaf is an open node with no open children.

1. Read `UPGRADE-PATH.md`. Pick one open leaf.
2. Make the change.
3. If CI is green: commit, mark the node `[x]`, note what you learned.
4. If it reveals problems you can't fix in a small step: revert, add
   those problems as child nodes, and stop.

## Rules

- Never fix forward on a red build. Revert and record instead.
- Never work on more than one node per run.
- Never push the state from an Explore attempt.
- Mark a node `[!]` when it's blocked by something outside the repo
  (upstream release, another team), and say what it waits for.
- When the framework provides a migration aid that reports deprecated or
  renamed settings at runtime, keep it enabled for the whole campaign so
  renames show up as warnings instead of failing silently.

## What to record on each node

Only what's relevant:

- dependency and versions (from → to)
- whether the framework's managed versions set it, or the project pins
  it (and why)
- required migrations, such as a package or module rename
- known incompatibilities and what the error looked like
- hard constraints ("can't go past X until Y")

Keep notes short. Record where things stand and drop the history.
