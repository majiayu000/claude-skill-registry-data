---
name: git-conflict-resolve
version: "1.3.0"
user-invocable: true
description: "Use when a Git merge or rebase produces code conflicts, especially when AI-automated conflict resolution is error-prone (picking the wrong side, losing a refactor, reverting to an older version) and semantic analysis plus logic verification is needed. Also applies when a multi-round rebase stops repeatedly and conflict files need to be aggregated across rounds. Triggers — 「解冲突」「处理冲突」「git-conflict-resolve」「解决 merge 冲突」「解决 rebase 冲突」「冲突解决」 / conflict resolve, resolve merge conflict, resolve rebase conflict."
---

# Git Conflict Resolution Workflow (git-conflict-resolve)

## Overview

A semantics-driven Git conflict resolution protocol that replaces blind `-X ours`/`-X theirs` strategies.

For each conflicted file: first run a semantic analysis to understand both sides' intent, then derive a resolution rule (with a confidence level). High-confidence conflicts are resolved automatically; medium-confidence conflicts show a recommendation and wait for confirmation; low-confidence conflicts show a three-way view and wait for a manual decision. After resolution, each file is logically verified one by one, and a final manual-review checklist is generated.

**Paired skill**: invoked by `git-release-finish` stage 6; can also be invoked standalone to handle any merge/rebase conflict.

---

## Input Parameters

| Parameter | Description | Example |
|------|------|------|
| `source` | The branch being merged in (usually a release branch) | `release/8.2.60` |
| `target` | The merge target branch (usually main/master) | `master` |
| `version` | Version number (used to name the merge branch) | `8.2.60` |
| `mode` | Conflict scenario: `merge` or `rebase` | `merge` |

Standalone invocation example:
> Run the `git-conflict-resolve` skill with source=release/8.2.60, target=master, version=8.2.60, mode=merge

---

## Sub-stage Y.0 — Mode Detection & Initialization

1. Read the input parameters and confirm `mode` (`merge` or `rebase`)
2. Initialize the **cumulative conflict file list** (a global variable that persists across all rounds — **must never be cleared** at any point)
3. Initialize according to mode:

**merge mode** (default):

```bash
# Create the merge branch from the target branch (no -X auto strategy, so conflicts surface naturally)
git checkout origin/<TARGET> -b merge-release/<VERSION>
git merge origin/<SOURCE> --no-commit --no-edit
```

> ⚠️ Do not use `-X ours` or `-X theirs` — blindly picking a side can silently drop logic. Conflicts are decided file-by-file via the semantic analysis below.

**rebase mode**:

```bash
# Create a local working branch from the remote source (avoids polluting the original remote branch)
git checkout origin/<SOURCE> -b rebase-release/<VERSION>

# Replay source's commits one by one onto target
git rebase origin/<TARGET>
# Stops on conflict → proceed to Y.1
# If rebase completes with no conflicts → skip Y.1–Y.4, go straight to Y.5
```

> ⚠️ When pushing the rebase result, if the target is a protected branch (release/*, main, master), a force push may be rejected by the remote (`remote: rejected`). Check branch protection before pushing; if necessary, push to a new branch instead (e.g. `rebase-release/<VERSION>`) and open a new MR, rather than force-pushing to the original branch.

---

## Sub-stage Y.1 — Conflict Inventory (Cross-round Aggregation)

> ⚠️ In rebase mode, every time a new conflict appears after `git rebase --continue`, **Y.1 must be re-run**, appending the new files to the cumulative list — never replacing it.

```bash
# Get the conflicted files for the current round
git diff --name-only --diff-filter=U
```

**Append rule**:

```
cumulative list = cumulative list ∪ current round's conflicted files
(set union — no duplicates, but the round in which each file first appeared is retained)
```

**Output format**:

```
【Conflict inventory — round N】
New conflicted files this round (M):
  - path/to/file-a.ts (new)
  - path/to/file-b.ts (new)

Cumulative conflict file list (K total, across all rounds):
  - path/to/file-a.ts (round 1)
  - path/to/file-b.ts (round 2)
  ...
```

**If the current round's conflict list is empty**:

| Mode | Meaning | Next action |
|------|------|---------|
| merge mode | git already auto-merged all content conflicts (but there may still be semantic issues) | **Skip Y.2–Y.4, go straight to Y.5**; focus verification on version fields and build-artifact paths |
| rebase mode | The current commit has no conflicts | Run `git rebase --continue`; if a new conflict appears, return to Y.1; if the rebase finishes, proceed to Y.5 |

→ If the list is non-empty, proceed to Y.1.5 to check for build artifacts before deciding whether to enter Y.2's semantic analysis.

---

## Sub-stage Y.1.5 — Build-Artifact Short-Circuit (compiled/bundled files)

> ⚠️ **This stage runs before Y.2's semantic analysis** — it is the key upfront gate for saving tokens and avoiding mis-resolutions.

Build artifacts (compiled/bundled derived files) are machine-generated: their content is huge (a single minified line can run to hundreds of thousands of characters), so reading them wastes a large number of tokens; compressed code has no "intent from either side" to analyze; and forcing a merge easily leaves conflict markers behind or keeps a stale version. Their authority is always the release branch — the correct approach is to **not read, not analyze, and directly take the release side**.

For each file in the cumulative list, classify it using the "Build Artifact Identification Checklist" in [reference.md](reference.md) (build-output directory prefixes ∪ file signatures ∪ project-specific additions):

- **Matches a build artifact** → do not read the three-way content, do not enter Y.2's semantic analysis; resolve directly using the short-circuit table below:

  | Conflict type | Resolution |
  |---------|---------|
  | Content conflict (UU) / Add-Add | `git checkout --theirs <FILE> && git add <FILE>` (take the release side) |
  | Whole-directory build artifact | `git rm -rfq <DIR> && git checkout origin/<SOURCE> -- <DIR> && git add <DIR>` |
  | Rename + hash conflict | Use git's rename metadata to get the filenames (**do not read file content**); delete the old hash file and take the new one from release — see Y.4 for details |

  After resolving, **still run the Y.4.5 instant verification** (scanning for residual conflict markers) to confirm nothing is left behind.

- **No match (source code/config)** → proceed to Y.2's normal semantic analysis.

> ⚠️ **Default to caution**: files with ambiguous boundaries (neither in a known build-output directory nor matching a clear artifact signature) **must never be short-circuited** — route them through Y.2. Misclassifying source code as a build artifact loses target-side changes, and that cost far outweighs reading one extra file — **when in doubt, read it rather than misjudge it**.

> 📖 See [reference.md](reference.md) for the identification checklist, detailed commands for each conflict type, and the rename+hash fallback and rationale.

---

## Sub-stage Y.1.6 — Mechanical Triage Fast Path (before semantic analysis)

> ⚠️ Runs after Y.1.5's build-artifact short-circuit and before Y.2's semantic analysis. Mechanical criteria produce evidence, not conclusions by default: "take ours" is valid only once the subset check proves it. When the mechanical criteria cannot decide, fall through to Y.2's normal semantic analysis and Y.3's confidence tiers.

For each remaining conflict block (source code / config / docs that passed Y.1.5):

**1. Subset diff check (first choice)** — is theirs a subset of ours?

```bash
diff <(ours_block) <(theirs_block) | grep -c '^>'
#   0  → theirs ⊆ ours → take ours (🟢 high confidence), record the criterion in the log
#   >0 → escalate: union merge or take-theirs analysis below
```

**2. Symbol-existence check (source files)** — verify theirs' top-level symbols (functions/classes/exports) exist in ours; when ours' method signatures already cover theirs' required parameters, ours is a functional superset. When a three-way comparison (base/ours/theirs) shows the two sides are alternative implementations of the same feature — a design divergence, not content loss — record that finding and resolve through the confidence tiers.

**3. Union merge with heading-key dedup (specs/docs)** — for files with heading structure (e.g. `## → ### Requirement: → #### Scenario:`), keep all of ours and append theirs' blocks whose headings are absent from ours; same-heading entries merge once, never duplicate.

**diff3 parsing trap** — before parsing conflict blocks from file content, detect the diff3 style (a `^\|{7,}` base section inside the block, or read `git config merge.conflictStyle`). With diff3, a conflict block has four parts: `<<<<<<< HEAD` ours, `||||||| base` base, `=======` separator, theirs. A parser that only knows the three-part form mistakes the base section for ours and concludes "ours is a superset" — a wrong verdict.

---

## Sub-stage Y.2 — Semantic Analysis

> ⚠️ This stage is read-only — do not modify any file.

For each conflicted file, do the following in order:

**1. Read the three-way content**

```bash
git show :1:<FILE>   # BASE: the common ancestor version
git show :2:<FILE>   # main side (ours): the target branch's version
git show :3:<FILE>   # release side (theirs): the source branch's version
```

> Note: in both merge and rebase modes, `:2:` = the main side and `:3:` = the release side, with the same semantics.

**2. Analyze the change deltas**

```bash
# Compute the common ancestor
MERGE_BASE=$(git merge-base origin/<SOURCE> origin/<TARGET>)

# What changed on the main side relative to BASE
git diff $MERGE_BASE origin/<TARGET> -- <FILE>

# What changed on the release side relative to BASE
git diff $MERGE_BASE origin/<SOURCE> -- <FILE>
```

**3. Output the semantic description**

```
【Semantic analysis — <FILE>】
main side intent: [unchanged / hotfix / feature development / refactor / deletion / version-field update / other]
  Specific changes: ...

release side intent: [unchanged / hotfix / feature development / refactor / deletion / version-field update / other]
  Specific changes: ...

Relationship between the two sides: [mutually exclusive (one overrides the other) / complementary (both must be kept) / one-sided change (the other side is identical to BASE)]
```

---

## Sub-stage Y.3 — Rule Derivation

Based on Y.2's semantic-analysis conclusions, derive a resolution rule and confidence level for each file.

### The three confidence tiers

| Confidence | Criteria | Next action |
|--------|---------|---------|
| 🟢 High | Intent is clear, one side has absolute authority, no risk of losing logic | Resolve automatically, output the action taken |
| 🟡 Medium | Mostly clear, but with local ambiguity or a need for partial merging | Show a recommendation and wait for the user to confirm A/B/C |
| 🔴 Low | Cannot determine an authoritative side, or both sides have important logic that must be preserved | Show the three-way view and let the user decide fully |

### Conflict-type identification (prerequisite for derivation)

Before deriving a rule, first identify the conflict's **structural type** — resolution strategies differ completely by type, and misclassifying one leads to residual conflict markers or lost changes.

**Two-step identification**:

**Step 1 — Determine the broad category from git status**:

```bash
git status --porcelain                        # conflict status codes
git diff --name-status --diff-filter=U        # rename info
```

| git status code | Category | Meaning |
|-----------|------|------|
| `UU` (both modified) | Content conflict | Both sides modified the same file |
| `UU` + conflict markers reference different filenames | **Rename conflict** | The diff3-format HEAD/base/theirs labels have different filenames |
| `AA` (both added) | Add/Add conflict | Both sides independently added a file with the same name |
| `DU` / `UD` | Delete/Modify conflict | One side deleted, the other modified |

**Step 2 — Refine using file signatures**:

> The primary identification and short-circuiting of build artifacts is already done in **Y.1.5** (a match takes the release side and never reaches Y.3). The signature check here is a **fallback**: if Y.1.5 missed it but Y.3 detects an artifact signature, treat it as a build artifact (take the release side).

```bash
# Build-artifact hash file (webpack/vite/rollup chunk)
echo "$FILE" | grep -qE '[0-9a-f]{8,}\.(js|css|map)$'

# Config file
echo "$FILE" | grep -qE '(^|/)(package\.json|tsconfig\.json|\.config\.(js|ts))$'
```

### Rule library

Organized by conflict type + confidence. Match the structural type first, then derive by scenario.

**🟢 High-confidence scenarios**:

| Conflict type | Scenario | Derived rule |
|---------|------|----------|
| Content conflict | `version`/`testVersion` field: updated on the release side | Take the release side (release is authoritative) |
| Content conflict | release deleted a function/module, main made **no change** to that code (identical to BASE) | Follow the release side's deletion intent (take the release side) |
| Content conflict | Build-artifact path (`dist/`, `resources/dist/`) with different hashes | Take the release side for the whole directory |
| Content conflict | release did a full refactor (same logic, different structure), main didn't touch that area | Take the release side |
| **Rename + build-artifact hash** | diff3 labels reference different hash filenames, filenames match `[0-9a-f]{8,}\.(js\|css\|map)` | **Delete the old hash file + take the new one from release** (see the dedicated Y.4 section) |
| Add/Add | Same-named build artifact added on both sides | Take the release side |

> ⚠️ **Rename + build-artifact hash is an error-prone scenario**: a simple `git checkout --theirs` won't work because the filename changed after the rename — the old hash file must be explicitly deleted and the new file explicitly pulled from release. See Y.4 for the detailed procedure.

**🟡 Medium-confidence scenarios**:

| Conflict type | Scenario | Derived rule |
|---------|------|----------|
| Content conflict | release deleted a function/module, but main **made an independent change** to that code (hotfix) | Manually confirm whether main's change is still needed |
| Content conflict | release refactored + main has an independent hotfix (both sides changed, in different directions) | Favor release, but manually confirm whether main's hotfix has already been superseded |
| Content conflict | Both sides changed import statements | Merge both sides' imports, manually confirm no duplicates |
| Content conflict | Multi-field config file: different fields changed on each side | List field-by-field, let the user choose |
| Rename + source code | A source file was renamed (not a build artifact) | Manually confirm the intent of the rename |

**🔴 Low-confidence scenarios**:

| Conflict type | Scenario | Derived rule |
|---------|------|----------|
| Content conflict | Both sides made substantive business-logic changes (complementary or related directions) | Show the three-way view — not recommended for auto-resolution |
| Add/Add | Same-named addition that is not a build artifact | Show the three-way view, merge manually |
| Delete/Modify | One side deleted, the other modified | Show the three-way view, manually confirm whether it still needs to be kept |
| Any | A file that doesn't fit any category above | Default to low confidence, show the three-way view |

---

## Sub-stage Y.4 — Resolution by Category

Process each file in order, according to its Y.3 confidence classification:

### 🟢 High confidence — resolve automatically

```bash
# Take the release side (theirs)
git checkout --theirs <FILE>
git add <FILE>

# Take the main side (ours)
git checkout --ours <FILE>
git add <FILE>

# Take the release side for a whole directory (build artifacts, etc.)
git rm -rfq <DIR>
git checkout origin/<SOURCE> -- <DIR>
git add <DIR>
```

#### Rename + build-artifact hash strategy (never reads file content)

> This scenario is normally already handled by the Y.1.5 upfront short-circuit (a build-artifact match takes the release side directly). If Y.1.5 didn't catch it (fallback), handle it with this strategy, and **prefer git's rename metadata for filenames — never read file content**.

After a rename, the filename changes, so `git checkout --theirs` may point to a path that no longer exists; both the old and new filenames must be handled explicitly:

```bash
# 1. Preferred: get both sides' filenames from git's rename metadata (never reads file content)
git diff --name-status --diff-filter=U
# Output looks like: R100 old-abc.js new-def.js → gives OLD_FILE / NEW_FILE

# 1b. Fallback: if rename metadata is missing, extract filenames only from the conflict-marker lines (do not read the full file)
OLD_FILE=$(git show :2:<FILE> | grep "^<<<<<<<" | sed 's/^.*HEAD://')
NEW_FILE=$(git show :3:<FILE> | grep "^>>>>>>>" | sed 's/^.*://' | tail -1)

# 2. Delete the old hash file (otherwise the repo ends up with two functionally identical chunks)
git rm -f "$OLD_FILE" 2>/dev/null

# 3. Take the new hash file from the release branch
git checkout origin/<SOURCE> -- "$NEW_FILE"
git add "$NEW_FILE"
```

> ⚠️ **Why a plain `git checkout --theirs` doesn't work**: in a rename conflict, the `--theirs` file path may differ from the current path in the working tree. Failing to delete the old file leaves two functionally identical chunks (old hash + new hash) in the repo, and the build may end up referencing the wrong one.

Output log:

```
✅ [High confidence] <FILE>
   Rule: release refactored, main unchanged → take the release side
   Action: git checkout --theirs <FILE> && git add <FILE>
```

### 🟡 Medium confidence — show a recommendation, wait for user confirmation

```
【Conflicted file】<FILE>
【main-side change】...
【release-side change】...
【AI recommendation】Favor release; main's hotfix has already been superseded by xxx in release
【Please choose】
A = Accept the AI's recommendation (take the release side)
B = Keep the main side
C = I'll edit it manually — let me know when it's done
```

### 🔴 Low confidence — three-way view, wait for the user's decision

```
【Conflicted file】<FILE>
【BASE (common ancestor), lines X–Y】
...(code)

【main side (ours), lines X–Y】
...(code)

【release side (theirs), lines X–Y】
...(code)

【AI analysis】Both sides made substantive logic changes — cannot determine an authoritative side
【Please choose】
A = Take the release side
B = Take the main side
C = I'll merge it manually — let me know when it's done
```

### Y.4.5 — Instant Verification (mandatory after resolving each file)

> ⚠️ **Fail-fast principle**: scan immediately after resolving each file, rather than waiting for Y.5's batch verification. A mistake in a single file is caught right away, and the rollback cost is low (only that one file needs redoing). Waiting until Y.5 risks having already forgotten how that file was resolved.

Immediately after finishing the resolution action for **each** file in Y.4 (`git checkout --theirs/--ours`, manual editing, the rename+hash strategy, etc.), run:

```bash
# Pair-first verdict (authoritative rule in git-release-finish Phase 0; same semantics here):
# a match counts as residue only when <, >, or | markers are present; pure '=' lines
# (license underlines, Markdown separators) are false positives.
if git grep -qE '^<{7,} |^>{7,} |^\|{7,} ' -- "$FILE" 2>/dev/null; then
  echo "❌ $FILE resolution failed: conflict markers remain"
  # Roll back to the conflicted state and re-enter Y.2 for analysis
  git checkout MERGE_HEAD -- "$FILE" 2>/dev/null
  return 1
elif git grep -qE '^={7,}$' -- "$FILE" 2>/dev/null; then
  echo "ℹ️ $FILE has pure '=' lines (no markers) — pair-first false positive, clean"
else
  echo "✅ $FILE is clean"
fi
```

**Why a precise regex instead of a broad match**: `<<<<<<<` (7 `<` characters + a space) locks onto git's conflict-marker format, excluding things like `===` separator lines in CSS comments or ASCII art. `^={7,}$` requires a line of pure equals signs to the end of the line, so a CSS comment like `/* ====== */` won't match (there's a `*/` after the equals signs). Pairing semantics follow the authoritative pair-first rule in git-release-finish Phase 0.

**Why `git grep` instead of `grep -r`**: `git grep` automatically respects `.gitignore` and only scans tracked files, naturally excluding untracked build artifacts, which combined with the precise regex forms a double filter.

### Continuing a multi-round rebase

Once all files in the current round have been processed:

```bash
git rebase --continue
```

If a new conflict appears → **return to Y.1**, append to the cumulative list, and continue through Y.2–Y.4.
If the rebase completes → proceed to Y.5.

---

## Sub-stage Y.5 — Logic Verification

> Verify **every file in the cumulative list** one by one (not just the current round).

**1. Verify release intent is fully preserved**

```bash
# Compare the resolution result against the original release-side version
git show origin/<SOURCE> -- <FILE>
```

Check: are the release side's key changes (functions, imports, logic blocks) fully preserved in the resolution result?

**2. Verify main's necessary changes**

```bash
# Compare the resolution result against the original main-side version
git show origin/<TARGET> -- <FILE>
```

Check: were any independent, necessary changes on the main side (e.g. a hotfix) mistakenly dropped?

**3. Check for residual conflict markers (within the cumulative list)**

> Do not scan the whole repo. Only scan the files in Y.1's cumulative list — these are the only files involved in this conflict resolution, and thus the only place markers could remain. A whole-repo scan would be swamped by false positives from things like CSS comments in build artifacts.

```bash
# Scan only the cumulative-list files; the verdict is pair-first (pure '=' lines without
# <, >, or | markers are false positives — authoritative rule in git-release-finish Phase 0)
for FILE in $CONFLICT_FILES_CUMULATIVE; do
  git grep -qE '^<{7,} |^>{7,} |^\|{7,} ' -- "$FILE" 2>/dev/null \
    && echo "❌ $FILE has residual markers"
done
```

**⚠️ Warning criteria** (mark as ⚠️ if any apply):

- A function/class/method that exists on the release side has disappeared from the resolution result
- Code that release deleted has reappeared in the resolution result (i.e. it was "reverted")
- An import statement from the release side is missing from the resolution result
- A version field (version/testVersion) doesn't match the release side
- release refactored some logic, but the resolution result fell back to the old implementation

**❌ Failure criteria** (mark as ❌ if any apply):

- The file still contains residual conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- The same function/variable appears twice in the resolution result (a duplicated merge)
- There's an obvious syntax error (e.g. an extra `}`, an unclosed bracket)

**Verification output**:

```
✅ <FILE> — logically consistent (release intent fully preserved, main's necessary changes handled)
⚠️ <FILE> — possibly lost a release change: function/logic xxx does not appear in the resolution result
❌ <FILE> — logic conflict: residual <<<<< markers or an obvious semantic contradiction
```

> ⚠️/❌ files: **must not be committed** — they must be reprocessed before proceeding to Y.6.

---

## Sub-stage Y.6 — Global Review Checklist + Commit

**Output a summary table** (covering all files in the cumulative list):

```
⚠️ The following files were changed during this conflict resolution — please review them carefully:

| File | Round appeared | Resolution | Confidence | Logic verification | Needs extra review |
|------|---------|---------|--------|---------|----------|
| src/effects/database/search-database.ts | round 1 | AI automatic (took release side) | 🟢 High | ✅ | — |
| package.json | round 1 | AI automatic (took release's version field) | 🟢 High | ✅ | — |
| src/components/editor.tsx | round 2 | User chose A (release side) | 🟡 Medium | ✅ | — |
| src/utils/helper.ts | round 1 | User merged manually | 🔴 Low | ⚠️ | ⚠️ Needs review |

Files that need extra review (⚠️/❌ verification, or 🔴 low confidence):
  - src/utils/helper.ts: verification result ⚠️, possibly lost a release change

After confirming the files above are logically correct, reply "continue" to complete the commit.
```

**After user confirmation (execute per mode)**:

**merge mode**:

```bash
git add -A
```

> ⚠️ **Pre-commit gate (L2 defense)**: before `git commit`, scan all staged files for residual conflict markers. This is the last line of defense before committing — it can still catch problems even if the Y.4.5 instant verification was skipped or went wrong.

```bash
# Scan all staged files; the verdict is pair-first (pure '=' lines are false positives,
# authoritative rule in git-release-finish Phase 0)
git diff --cached --name-only | while read f; do
  git grep -qE '^<{7,} |^>{7,} |^\|{7,} ' -- "$f" 2>/dev/null \
    && { echo "❌ Commit blocked: $f still contains conflict markers"; exit 1; }
done
# exit 1 → blocks the commit, go back to Y.4 to reprocess that file
```

Once the gate passes:

```bash
git commit --no-verify -m "Merge release/<VERSION> into <TARGET>"
```

> ⚠️ Only use `--no-verify` when pre-commit hooks block the merge commit for reasons like formatting warnings; if the hooks run type checks, fix the errors instead.

**rebase mode**:

```bash
# Each rebased commit has already been applied individually — no extra merge commit is needed
# Notify the caller (git-release-finish) to perform the final force-push
git rebase --continue   # if commits remain to finish from the last round
# Once the rebase completes, exit and let git-release-finish stage 6 take over the force-push
```

---

## Prohibited Behaviors (Red Flags)

> The following behaviors violate this protocol. If the AI notices it is about to do one of these, it must stop immediately and return to the correct step.

| Violation | Correct approach |
|---------|---------|
| **Clearing** the cumulative list and starting over when a new rebase round produces conflicts | Must **append** — the cumulative list persists throughout, and must never be cleared |
| Skipping the Y.4.5 instant verification after resolving a file in Y.4 and moving straight to the next one | Y.4.5 must run for every file — fail-fast principle |
| Skipping Y.5's logic verification because "high-confidence files should be fine" | Y.5 must run for **every file in the cumulative list**, with no exceptions |
| Auto-committing after generating the Y.6 review checklist without waiting for user confirmation | Must wait for the user to reply "continue" before running `git commit` |
| Forcing a commit through despite the Y.6 pre-commit gate detecting conflict markers, on the grounds of "low impact" | The gate is a hard block — must return to Y.4 to fix and re-run the gate |
| Describing both sides from memory in Y.2's semantic analysis without actually running `git show :1:/:2:/:3:` | Must run the commands to read the three-way content first, and analyze based on the actual content |
| Using `git checkout --theirs` (without deleting the old file) for a rename + build-artifact hash conflict | Must use Y.4's dedicated rename+hash strategy: delete the old file, take the new one |
| Applying the high-confidence rule to a file with complex changes on both sides, skipping medium/low-confidence manual confirmation | Confidence must be derived from Y.3's criteria — never subjectively inflated |
| Continuing to commit after logic verification produces ⚠️/❌, on the grounds of "low impact" | ⚠️/❌ files must not be committed — they must be reprocessed |
| Running a build artifact (compiled/bundled file) through Y.2's semantic analysis, or reading its three-way content | The Y.1.5 upfront short-circuit applies: a match takes the release side directly, with no reading or analysis (see reference.md) |
| Using `grep` to read file content to extract filenames for a rename + build-artifact hash conflict | Prefer the rename metadata from `git diff --name-status --diff-filter=U` to get filenames; the fallback only reads the conflict-marker lines, never the full file |

---

## Error Handling

| Scenario | How to handle it |
|------|------|
| `git show :1:/:2:/:3:` produces no output | The file has no corresponding stage — use `git status` to check its state (it may already be auto-resolved, or it may be a new file) |
| `git merge-base` errors out | Use `git log --oneline --graph -10` to check the branch topology and manually specify the base commit |
| `git rebase --continue` produces a conflict again | Normal — return to Y.1, append to the cumulative list, and keep looping |
| Logic verification produces a ❌ with no clear correct fix | Pause, show the user the three-way view for the ❌ file, and wait for a manual decision |
| `git checkout --theirs/--ours` errors with "pathspec not found" | Run `git add -A` first, then retry |

---

## Quick Reference Commands

```bash
# ── Conflict-marker detection (precise regex + pair-first verdict, shared by every defense layer) ──
# Matcher: git's conflict-marker format, 7+ characters at line start + space/end-of-line
# Verdict: a match is residue only when the marker regex matches too; pure '=' lines are false positives
RE='^<{7,} |^={7,}$|^>{7,} |^\|{7,} '
RE_MARKER='^<{7,} |^>{7,} |^\|{7,} '

# Y.4.5 single-file instant verification
git grep -qE "$RE_MARKER" -- "$FILE" 2>/dev/null && git grep -nE "$RE" -- "$FILE" 2>/dev/null

# Y.5 cumulative-list scan
for f in $CONFLICT_FILES; do git grep -qE "$RE_MARKER" -- "$f" 2>/dev/null && git grep -lE "$RE" -- "$f" 2>/dev/null; done

# Y.6 pre-commit gate (staged files)
git diff --cached --name-only | while read f; do
  git grep -qE "$RE_MARKER" -- "$f" 2>/dev/null && git grep -lE "$RE" -- "$f" 2>/dev/null && echo "❌ $f"
done

# ── Three-way version content ──
git show :1:<file>   # BASE
git show :2:<file>   # main side (ours)
git show :3:<file>   # release side (theirs)

# Each side's delta (compute MERGE_BASE first)
MERGE_BASE=$(git merge-base origin/$SRC origin/$TGT)
git diff $MERGE_BASE origin/$TGT -- <file>   # main's delta
git diff $MERGE_BASE origin/$SRC -- <file>   # release's delta

# ── Conflict-type identification ──
git status --porcelain                        # conflict status codes (UU/AA/DU/UD)
git diff --name-status --diff-filter=U        # rename info

# ── Resolve by confidence ──
git checkout --theirs <file> && git add <file>   # take the release side
git checkout --ours <file> && git add <file>     # take the main side

# Y.1.5 build-artifact short-circuit (match → take release side, no content read)
git checkout --theirs <file> && git add <file>                                       # content conflict / Add-Add
git rm -rfq <dir> && git checkout origin/<SOURCE> -- <dir> && git add <dir>           # whole-directory artifact

# rename + build-artifact hash (prefer rename metadata, never read file content)
git diff --name-status --diff-filter=U                                               # get OLD/NEW filenames
git rm -f "$OLD" 2>/dev/null && git checkout origin/<SOURCE> -- "$NEW" && git add "$NEW"

# continue the rebase
git rebase --continue
```
