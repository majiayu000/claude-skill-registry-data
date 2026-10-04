---
name: label-setup
description: >
  Create or reconcile a repository's labels from the preset in `labels.yml`.
  Writes labels only — never deletes, never touches labels outside the preset.
  Invoke with /label-setup.
disable-model-invocation: true
---

# Label Setup

Bring the repository's labels into line with the preset in `labels.yml` by running the steps below in order.

## Hard limits

- Write labels only, and only with `gh label create` and `gh label edit`. Never run `gh label delete`.
- Only preset names drive action. A repo label absent from `labels.yml` is left untouched.
- The preset is read-only input: never edit `labels.yml`.
- No git or codebase changes of any kind.

## Preconditions

1. Confirm the repo is reachable and `gh` is authenticated: `gh repo view`. If it fails, stop and tell the user to check the repo or run `gh auth login`.
2. Read the preset from `labels.yml` beside this file. If it is missing or empty, stop.

## Plan the changes

3. Fetch the repo's current labels once: `gh label list --json name,color,description --limit 500`.
4. For each preset label, match by exact name against that list and sort it into one of three buckets:
   - **Create** — no repo label has this name.
   - **Reconcile** — a repo label has this name but its color or description differs from the preset. Compare color case-insensitively and ignore a leading `#`; compare description as exact text.
   - **Skip** — a repo label has this name and both fields already match.
5. Assemble the exact `gh` command for each create and reconcile. Quote every name:
   - Create: `gh label create "feature" --color 0e8a16 --description "Brand-new capability"`
   - Reconcile: `gh label edit "priority: high" --color b60205 --description "High priority"`

## Confirm, then run

6. Show the plan before running anything: the create list, the reconcile list with each label's current values next to the preset values, and the skip count. Print the exact commands from step 5.
7. Ask once for approval.
8. On approval, run the commands in order. If a command fails, stop and report which label failed and why; do not roll back labels already changed.
9. Report the result: how many labels were created, reconciled, and skipped.
