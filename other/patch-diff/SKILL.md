---
name: patch-diff
description: Diff two npm-package versions for added/removed security-control invocations (T3.1). Per-target wrapper around bin/npm_version_diff.py. Use when a target ships a vulnerable library version and a fix exists upstream — the diff highlights what control was added so you can grep the target for the same gap.
---

# patch-diff

## Purpose
Bug bounty value: when a CVE points at a library, the fix commit
usually adds a sanitizer / role check / encoding step. Diff the two
versions to extract the exact control delta — then search the target
for callsites of the OLD api that are still missing the NEW control.

## Inputs
- `targets/<name>/status.json`
- `<package>` from npm
- `<old_version>` (vulnerable) and `<new_version>` (fixed)
- `npm` in PATH

## Steps
1. Identify the package + versions to compare. Pull from one of:
   - `package.json` of the target
   - the CVE description on npm advisories
   - GHSA database (`gh-advisory-database`)
2. Run:
   ```
   python3 bin/npm_version_diff.py targets/<name> <package> <old> <new>
   ```
3. Review `targets/<name>/diffs/<package>_<old>_<new>.md`. Each row:
   `<file> | <control_pattern> | <delta>`. Positive delta = control
   was ADDED in the fix. Negative = removed.
4. For each ADDED control, grep `targets/<name>/sources/` for callers
   of the same APIs that DON'T invoke the control. Cross-reference
   with `opus-gap-audit` using the new control as the qname.

## Outputs
- `targets/<name>/diffs/<package>_<old>_<new>.md`
- `status.json.phases.patch_diff_<package>`

## Failure modes
- `npm` missing → script writes `status: skipped`. Install
  `node` + `npm`.
- Package version unpublished / yanked → `npm pack` fails; check
  `npmjs.com/package/<package>` for the version list.
- Control delta = 0 across all files → either the fix is non-source
  (e.g. dependency bump) or the patterns in `CONTROL_PATTERNS` don't
  cover this library's idiom. Add new patterns to
  `bin/npm_version_diff.py:CONTROL_PATTERNS`.

## Result block
```json
"phases": { "patch_diff_<package>": {
    "status": "done", "ts": "<iso>",
    "package": "...", "old": "...", "new": "...",
    "files_added": N, "files_removed": N, "files_common": N,
    "control_changes": N,
    "output": "diffs/<package>_<old>_<new>.md" } }
```
