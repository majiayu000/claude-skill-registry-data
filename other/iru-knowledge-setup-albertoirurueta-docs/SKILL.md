---
name: iru-knowledge-setup
description: Create the `knowledge/` directory at the repository root with its five subdirectories — `inbox`,
  `meetings`, `people`, `agreements`, and `pending` — each containing a `.gitkeep` file so git tracks the empty
  directory. Invoke as `/iru-knowledge-setup`. Idempotent — safe to re-run; only creates whichever
  directories/`.gitkeep` files don't already exist, and never overwrites or deletes existing content. Use once,
  before `iru-knowledge-process-inbox` or `iru-knowledge-complete` are run for the first time in a repository, to
  bootstrap the knowledge base's folder structure.
model: haiku
---

# Knowledge Setup

Bootstrap the `knowledge/` directory structure at the repository root that `iru-knowledge-process-inbox` and
`iru-knowledge-complete` depend on.

## Step 1 — Check current state

Check whether `knowledge/` already exists at the repository root, and which of its five subdirectories
(`inbox`, `meetings`, `people`, `agreements`, `pending`) already exist. This skill is idempotent — never delete
or modify any existing content; only fill in what's missing.

## Step 2 — Create the directory structure

For each of `inbox`, `meetings`, `people`, `agreements`, `pending` under `knowledge/` that doesn't already
exist, create it. In every one of the five directories — both pre-existing and newly created — ensure a
`.gitkeep` file exists: git doesn't track empty directories, so `.gitkeep` is what lets these directories survive
a commit before real content lands in them. Skip adding `.gitkeep` to a directory that already contains other
files — it no longer needs one.

## Step 3 — Report

List each of the five directories with its status (created / already existed) and whether a `.gitkeep` was
added. Confirm the knowledge base is ready for `iru-knowledge-process-inbox`.
