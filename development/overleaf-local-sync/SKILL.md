---
name: overleaf-local-sync
description: Reconcile local LaTeX manuscripts and Overleaf projects in both directions, preserve collaborator edits, apply incremental editor changes and selected figure uploads, and verify source and compiled PDF consistency. Use for pulling Overleaf changes, pushing local revisions, or recovering an out-of-sync editor.
---

# Overleaf Local Sync

Synchronize the requested manuscript changes while retaining edits made on either side. Default to the browser workflow when the user requests edits “as a human,” incremental changes, or preservation of Overleaf review history. Reuse an established Overleaf Git workflow when available and consistent with the user's request; fetch and merge, never force-push or replace the project to resolve divergence.

## Establish the comparison

1. Identify the local manuscript root, exact Overleaf project, authorized browser session, and requested changes. Reuse the existing project tab and desktop. Record project URLs, account details, browser endpoints, and snapshots in private or ignored state, outside submission packages.
2. Inspect local Git status. Preserve current work with a scoped commit/tag when requested or established by the project; otherwise use a private source snapshot. Do not sweep unrelated files into a commit.
3. Download fresh Overleaf source **before editing**. Preserve unsaved browser text before reloading an offline or out-of-sync editor; cached editor contents are not proof of current server state. Read [browser-workflow.md](references/browser-workflow.md) for source downloads, recovery, and UI edits.
4. Identify the last verified common baseline, **B**, current local files, **L**, and fresh remote source, **R**. Explicitly map local and Overleaf filenames and normalize only known path tokens for comparison. Read [comparison-helper.md](references/comparison-helper.md) to use the bundled read-only planner.

| Comparison | Action |
| --- | --- |
| L = R | Already converged; keep the content. |
| L = B; R changed | Pull the remote edit into local. |
| R = B; L changed | Stage the local edit for Overleaf. |
| Both changed differently | Review a three-way text merge; preserve both changes where compatible. |
| Binary conflict, missing file, or overlapping edits | Resolve the specific conflict; do not guess from timestamps or silently delete. |
| No verified baseline | Compare and reconcile explicitly. A new remote download alone is not a common baseline. |

Import collaborator changes before making the requested local revision. For renamed figures, translate paths through the mapping rather than changing the local directory layout unnecessarily. A clean text merge still needs a content review, particularly for equations, citations, and meaning.

## Apply the authorized change

1. Make the requested local edit on the reconciled version. Keep writing, figure redesign, and bibliography changes within the user's scope. When an edited PPT is the source, export that reviewed file, crop excess page margins, and inspect the figure rather than recreating it.
2. Build using the project's established command and check the relevant PDF pages, references, and actual page limit. Preserve template and compiler settings. Do not impose another paper's page count or bibliography convention.
3. Download remote source again immediately before remote mutation. If it changed since R, reconcile those edits and update the proposed patches. Recheck each exact old text at the moment of editing; a snapshot cannot lock out concurrent collaborators.
4. Apply only the required text hunks through normal editor controls. Keep existing Reviewing/Editing mode and suggestions/comments; do not accept or reject collaborators' review history. Use exact old-text matches and expected occurrence counts. If a match fails, inspect the current source before retrying.
5. Upload only the selected new/revised assets in their correct folder. Confirm the intended same-name overwrite. Do not upload a complete project ZIP or overwrite existing `main.tex` to change a figure. A new text file may be uploaded when it does not already exist. Binary replacement has no prose redline; retain its source version and hash.

Proceed with changes already authorized by the user. Ask only for a missing decision that affects meaning, a real conflict that cannot be resolved from context, or access that is unavailable. Skill use alone adds no confirmation gate.

## Verify and checkpoint

- Wait for saves and compile completion. Inspect the actual error/warning state; a preview or upload toast alone is insufficient.
- Download the resulting source and PDF. Compare before/after source hashes, require intended files to match the staged result, and examine any unexpected change. Preserve concurrent collaborator changes rather than rolling them back to satisfy a checksum.
- Compare local and remote again with the filename mapping. Inspect changed figure/pages in the compiled PDF and confirm project-specific limits and reference integrity. ZIP bytes and PDF bytes may differ due to packaging/build metadata; compare source entries and rendered output appropriately.
- Only after verification, record the new common baseline, source hashes, local commit, mapping version, build result, and evidence locations in private state. Keep the immediately previous verified baseline. If differences remain or the sync is partial, record them explicitly and do not label it fully synchronized.
- Report what was pulled, what was pushed, and the verification result. Never claim an upload or sync completed from a local build alone.

## Tools

- `scripts/overleaf_sync.py plan`: compare B/L/R and write a report plus proposed text merges to a **new private output folder**; never modifies input files or contacts Overleaf.
- `scripts/overleaf_sync.py verify`: check remote before/after changes against an explicit file allowlist and optional staged expected files.
- `scripts/browser_download.py`: download source and optionally PDF through an existing logged-in Playwright/CDP tab. Requires the `playwright` Python package in the selected interpreter. It creates no browser/profile and makes no manuscript edits. If controls differ, inspect the live UI and use the available browser tool instead of forcing clicks or calling hidden mutation APIs.

Run `--help` for arguments. For UI-only environments, follow the browser reference without the helper scripts. The comparison helper needs Python 3.10+ and Git only when proposing a text merge.
