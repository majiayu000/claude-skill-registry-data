---
name: git-release-finish
version: "2.2.0"
user-invocable: true
dependencies:
  - report-output-discipline
description: "Use when releasing a Git repository version — tagging, merging release branches into main, resolving conflicts, or syncing changes between release branches. Handles ambiguous tag naming (v-prefix vs plain), unknown main branch (master/main/develop), ff-only merge method (forces cherry-pick strategy), protected-branch rules, cross-release hash-sensitive sync, and MR/PR extra-file cleanup. Single or multi-repo. Triggers — 「发版」「打tag」「发布版本」「版本发布」「release流程」「git-release」「multi-repo release」「release同步到另一个release」 / release a version, tag and merge, finish release branch."
---

# Git Release Finish

## Prerequisite skill check

On load, verify `report-output-discipline` is available. If missing, abort and print:

`npx skills add FuDesign2008/open-skills -g --skill '*' --yes`

Do not silently fall back.

> **Role**: End-of-iteration release workflow — tag the release branch, create MR/PR into the main branch, resolve conflicts, clean up extra files, merge. Git operations are expressed as native commands; MR/PR operations are expressed as intents and the running agent picks its platform CLI (`glab` / `gh` / `tea` / equivalent) per its environment.
>
> **Pairing**: `git-release-start` (iteration start, creates the release branch) ↔ `git-release-finish` (this skill).
>
> **Dependency**: Phase 6 conflict resolution is delegated to the `git-conflict-resolve` skill (semantic analysis, multi-round aggregation).
>
> **Remote-first principle**: confirm remote state before any local action. Before tagging, `git fetch` and verify the remote commit SHA. Never tag an unverified local HEAD — it may be behind the remote. Prefer remote API tag creation when the platform supports it (avoids local-state drift); otherwise create the tag locally anchored to the verified remote SHA.

## Multi-repo discipline

> Single-repo runs may skip this section. Multi-repo runs (≥2 repos) must follow all three rules — each comes from a real postmortem.

**M.1 — Explicit working-directory isolation.** Tool-call layers have no persistent repo context. After `cd` to repo A, the next Bash call without `cd` still runs in A. Multi-repo parallel releases without explicit `cd` create MRs in the wrong repo, merge-tree the wrong branch, merge the wrong MR. **Every command block in a multi-repo run starts with `cd <REPO_PATH> &&`**, even when you are sure you are already there. Each confirmation table (Phase 1/2/3/3.5 output) has a Repo column.

**M.2 — Cross-repo failure-pattern propagation.** When one repo hits an environment limit (ff merge mode, protected-branch rule, CI pipeline requirement, CLI auth failure), **immediately run the same check on every repo that has not yet reached Phase 9**. This is a catch-up check, not main-flow duplication; Phase 3.5 already checks all repos in parallel.

| Repo A discovers | Run on repo B (and all not-yet-merged repos) |
|------|------|
| `merge_method = ff` | Phase 3.5 fingerprint; expect cherry-pick strategy |
| Release branch is protected (push=No one) | Check B's release branch protection; pre-plan the protected-branch fallback |
| CLI auth failure | Re-run platform `auth status` |
| Pipeline failure blocks merge | Check B's CI config and pipeline state |

**M.3 — Parallel/serial boundary.** Repo-independent operations run in parallel (tagging, MR/PR creation, conflict dry-run). **Conflict resolution (Phase 6) is strictly serial** — only one repo's worktree can be in a conflict state at a time.

## When to use / not to use

**Use when** (single-repo or multi-repo): tag naming is ambiguous or has evolved; main branch name is uncertain (master / main / develop varies per repo); release → main merge may have code conflicts; MR/PR branch may contain stray files (AI tool configs, temp scripts); a structured release report is needed.

**Do not use for**: non-Git hosting (SVN, Mercurial, etc.).

> The flow runs end-to-end. Every phase is mandatory regardless of repo count or how "simple" the release looks. "Looks simple this time" is the most common cause of skipping the pre-flight check and shipping residue into main.

**Pre-conditions**: platform CLI is installed and authenticated (verify auth before starting); each repo's remote is reachable; the version number (e.g. `8.2.60`) is confirmed with the user.

## Phase map

| Phase | Operation | Key tools |
|------|------|---------|
| **0** | **Pre-flight health check (residual marker scan)** | `git grep` + `git log -S` |
| 1 | Analyze tag naming convention | `git tag` |
| 2 | Create and push tag (remote-first) | `git fetch` / `git tag` / `git push` / remote API |
| 3 | Identify main development branch | `git remote show` + `git log` |
| **3.5** | **Environment fingerprint (merge_method, protection, ff detection)** | platform API + `git merge-base --is-ancestor` |
| 4 | Create MR/PR | platform CLI |
| 5 | Conflict dry-run | `git merge-tree` |
| 5.5 | Verify MR mergeability (mandatory after merge-tree=0) | platform CLI/API |
| 6 | Resolve conflicts (if any) | `git-conflict-resolve` skill |
| 7 | Clean MR/PR branch extra files (merge mode only) | `git ls-tree` + `comm` |
| **8** | **Residual marker gate (unconditional)** | `git grep` |
| 9 | Merge MR/PR | platform CLI |
| 10 | Output report | — |

**Phase 0, 3.5, and 8 are unconditional** — they run on every path. Phase 0 is the pre-flight insurer, 3.5 is the merge-constraint gate, 8 is the final pre-merge gate. None of them depend on whether Phase 5 detected conflicts.

### Execution paths

| Situation | Path |
|------|------|
| merge-tree=0 and MR is mergeable | **0**→1→2→3→**3.5**→4→5→**5.5**→**8**→**9**→10 (skip 6/7) |
| merge-tree=0 but MR is not mergeable | **0**→1→2→3→**3.5**→4→5→**5.5**→**6(rebase)**→**8**→**9**→10 (skip 7) |
| Conflicts > 0, source ≤ 3 commits and ≤ 1 conflicted file | **0**→1→2→3→**3.5**→4→5→**6(rebase)**→**8**→**9**→10 (skip 7) |
| Conflicts > 0, all other cases | **0**→1→2→3→**3.5**→4→5→**6(merge)**→**7**→**8**→**9**→10 |
| Phase 3.5 detects ff mode + non-fast-forward | **0**→1→2→3→**3.5(cherry-pick)**→**8**→**9**→10 (skip 4 default MR / 5 / 5.5 / 6 / 7; ff cherry-pick creates a `sync-release` MR — see `references/ff-cherry-pick.md`) |

> Phase 3.5 is a mandatory waypoint on every path. Its verdict decides whether the rest of the flow uses the default merge/rebase branch (paths 1–4) or the ff cherry-pick branch (path 5).

---

## Phase 0: Pre-flight health check (residual marker scan)

> **Unconditional.** Run on every repo before Phase 1. If the worktree or recent commits already contain conflict markers, clean them before releasing — otherwise the residue enters main via the merge.

**Why this is needed**: Phase 5's `git merge-tree` only detects *new* conflicts from a future merge; it does not see conflict markers already committed to branch history (a common artifact of failed AI auto-resolution that was still pushed). Without Phase 0, those markers ride the merge into main.

**The precise regex** (reused by every later scan in this skill):

```
^<{7,} |^={7,}$|^>{7,} |^\|{7,} 
```

Matches standard 7-char markers, non-standard 8+ char markers, and diff3 `||||||| base` markers. `git grep` honors `.gitignore` automatically, so untracked build artifacts are excluded. `^={7,}$` requires pure `=` to end-of-line, so CSS comments like `/* ====== */` do not match; `^<{7,} ` requires 7+ `<` followed by a space, so ordinary `<` operators do not match.

**Residue verdict — pair first** (authoritative rule; every scan in this skill and in `git-conflict-resolve` applies the same semantics): the regex above is a matcher, not a verdict. A match counts as true residue only when the same file also contains an opening/closing marker — `^<{7,} ` / `^>{7,} ` / `^\|{7,} `. A pure `=` line on its own is a false positive (third-party license headings like `The MIT License` underlined with `===============`, Markdown separator rules). A hit does not automatically mean residue — the pairing is the verdict.

**L4a — Worktree scan**:
```bash
git grep -lE '^<{7,} |^={7,}$|^>{7,} |^\|{7,} ' 2>/dev/null
```

**L4a triage — separate true residue from pure-`=` false positives**:
```bash
git grep -lE '^<{7,} |^={7,}$|^>{7,} |^\|{7,} ' 2>/dev/null | while read -r f; do
  if git grep -qE '^<{7,} |^>{7,} |^\|{7,} ' -- "$f" 2>/dev/null; then
    echo "TRUE RESIDUE: $f"
  else
    echo "false positive (pure '=' lines only): $f"
  fi
done
```

**L4b — Historical merge-commit pickaxe scan**:
```bash
git log --all --merges --since="30 days ago" \
  -S'^<<<<<<< ' --pickaxe-regex \
  --format="COMMIT: %h %s" --name-only 2>/dev/null
```

| Result | Action |
|------|------|
| L4a and L4b both empty | Healthy; proceed to Phase 1 |
| L4a triage finds true residue, or L4b non-empty | Abort. Clean the worktree (resolve or checkout a clean copy) and re-run |
| L4a matches are all pure `=` lines (no `<`/`>`/`\|` markers) | False positive. Record it in the scan output; proceed to Phase 1 |

> Do not "release first, clean later." Residue in main propagates to downstream CI/CD which builds on wrong content.

---

## Phase 1: Analyze tag naming convention

> Never assume uniform tag formatting. Analyze each repo separately.

```bash
git tag --sort=-version:refname | head -30
```

| Historical pattern | Convention |
|------|------|
| `8.2.52`, `8.2.51` | Plain: `{VERSION}` |
| `v8.2.40`, `v8.2.20` | v-prefix: `v{VERSION}` |
| `desktop-8.2.50`, `desktop-8.2.40` | Product-prefix: `desktop-{VERSION}` |
| `mobile-7.5.720` | Product-prefix: `mobile-{VERSION}` |

**Multi-product repos**: check the full tag list (not just the latest 10) for any `product-` prefix. Each product line maintains its own tags; this release only tags the current product line.

> Tag conventions can evolve. The same repo may have used `v8.2.60` historically and switched to `8.2.63` later. **Follow the most recent tag**; do not assume a prefix is required because old tags had one. If the history is internally inconsistent, ask the user which convention applies this release.

**Output (confirmation table)**:

| Repo | Release branch | Tag name | Latest historical example |
|------|------|------|------|
| repo-A | release/X.Y.Z | `X.Y.Z` | `8.2.52` |
| repo-B | release/X.Y.Z | `vX.Y.Z` | `v8.2.40` |

Align with the user on tag names before Phase 2.

---

## Phase 2: Create and push tag (remote-first)

### 2.0 Pre-checks (all platforms, mandatory)

Run in parallel per repo:
```bash
git fetch origin <RELEASE_BRANCH>
REMOTE_SHA=$(git rev-parse origin/<RELEASE_BRANCH>)
echo "remote $RELEASE_BRANCH HEAD: $REMOTE_SHA"

# Fork detection: is local behind remote?
LOCAL_SHA=$(git rev-parse HEAD)
BEHIND=$(git rev-list --count HEAD..origin/<RELEASE_BRANCH> 2>/dev/null || echo 0)
[ "$BEHIND" -gt 0 ] && echo "Local is $BEHIND behind remote; tag will anchor to remote SHA, not local HEAD"

# Tag-already-exists check
git ls-remote --tags origin | grep -q "refs/tags/<TAG_NAME>$" \
  && { echo "Tag <TAG_NAME> already exists on remote; aborting"; exit 1; }
```

### 2.1 Create the tag

Create the tag, **preferring remote API creation when the platform supports it** (avoids local-state drift); regardless of method, anchor to the verified `$REMOTE_SHA`.

- *Remote API path* (preferred when available): call the platform's "create tag" endpoint with `tag_name=<TAG_NAME>`, `ref=$REMOTE_SHA`, `message="Release <VERSION>"`. No `git push` needed — the tag is created directly on the remote. (If the CLI's `api` subcommand splits args, see Common Mistakes.)
- *Local-creation path* (otherwise): `git tag <TAG_NAME> $REMOTE_SHA && git push origin <TAG_NAME>`. The tag object is anchored to `$REMOTE_SHA`, not to local HEAD.

### 2.2 Verify the tag points at the right commit

```bash
REMOTE_SHA=$(git rev-parse origin/<RELEASE_BRANCH>)
TAG_SHA=$(git ls-remote origin refs/tags/<TAG_NAME> | awk '{print $1}')
echo "tag <TAG_NAME> -> $TAG_SHA"
echo "expected        -> $REMOTE_SHA"
# Annotated tags return the tag-object SHA from ls-remote; dereference with:
# git ls-remote origin "refs/tags/<TAG_NAME>^{}"
```

If `TAG_SHA ≠ REMOTE_SHA` (after dereferencing annotated tags), the tag landed on the wrong commit — delete and redo (see Common Mistakes).

**Output**: per-repo table of tag name, remote SHA, verified tag SHA, status.

---

## Phase 3: Identify main development branch

> The main branch may be `master`, `main`, or `develop`, and may differ per repo.

**Four layers of evidence, ranked by trust**:

1. **Remote merge history (strongest)**:
```bash
git log --oneline --merges -20 | grep -E "into '(master|main|develop)'"
```
Historical "Merge branch 'release/X.Y.Z' into 'master'" records reveal the target.

2. **Remote HEAD** (`git ls-remote --symref origin HEAD` is live and authoritative; `git remote show origin` is also live but times out often; `git symbolic-ref refs/remotes/origin/HEAD` is local cache and may be stale). Prefer the live query on disagreement.

3. **Branch-naming behavior and merged-MR distribution**: `sync-release/*-to-<X>` sync branches name their target in the branch name itself (`git branch -a | grep sync-release/`); when all version-release MRs land on one target branch, that distribution is behavioral evidence (platform API: merged MRs filtered by `target_branch`).

4. **User confirmation (fallback)**: when sources conflict or no history exists, list candidates and ask.

> **A candidate may be an active parallel branch, not a deprecated trunk.** A branch named `master` can be a living parallel CI branch — its own CI config with different images and install steps, triggered independently by the branch name, with recent commits from others — while trunk is `main`. Before treating a candidate as deprecated or cleaning it up, falsify this first: independent CI configuration or recent third-party commits mean it is an active parallel branch. Do not clean up an active parallel branch; record its real role in the Phase 10 report.

> Remote HEAD can point at a deprecated branch. After migrations or branch-policy changes, remote HEAD may still point at the old main. If remote HEAD's branch is hundreds of commits behind another candidate, treat remote HEAD as stale, rely on merge history, confirm with the user:
```bash
echo "HEAD candidate ahead of main: $(git rev-list --count origin/main..origin/<HEAD_BRANCH> 2>/dev/null)"
echo "main ahead of HEAD candidate: $(git rev-list --count origin/<HEAD_BRANCH>..origin/main 2>/dev/null)"
```

**Output**: per-repo table of source branch, target main, evidence source. Align with the user before Phase 4.

---

## Phase 3.5: Environment fingerprint (unconditional)

> **Unconditional.** Collect each repo's merge constraints before any MR/PR is created. This is the gate that prevents the classic "merge-tree=0, `can_be_merged=true`, but `mr merge` returns 406" trap.

**Why this is needed**: Phase 5's `merge-tree` and Phase 5.5's `can_be_merged` check only code-level mergeability. They are blind to project-level merge constraints. The most common trap is GitLab `merge_method = ff` (fast-forward-only): release is not a descendant of main (main moved after release branched) → `git merge-tree` reports 0 conflicts → MR `can_be_merged=true` (a merge result exists; **does not validate `merge_method` constraints**) → `mr merge` returns **406 "Branch cannot be merged"** because ff mode refuses to produce a merge commit and release cannot fast-forward to main. This trap is invisible to Phases 5/5.5 and only surfaces at Phase 9. Phase 3.5 moves that wall forward.

**Checks (run in parallel per repo)**:

1. **merge_method / merge-commit allowances** — Query the project's `merge_method` (GitLab) or `allow_merge_commit` / `allow_squash_merge` / `allow_rebase_merge` (GitHub) via your platform's API to detect ff-only mode.
2. **Release-branch protection rules** — Query `protected_branches` for `release/*` and `*`; record `push_access_levels` and `merge_access_levels` to detect push=No one. When `git-branch-protect` is available, also run its read-only `check-trunk` through `glab` or `gh`. Report a mismatch with "push denied, maintainer merge allowed". Do not run `set-trunk`. When the skill is not available, keep this fingerprint and continue.
3. **CI gate** — Query `only_allow_merge_if_pipeline_succeeds` (GitLab) or equivalent.
4. **Descendant check (ff-mode decision)**:
```bash
git merge-base --is-ancestor origin/<TARGET_BRANCH> origin/<RELEASE_BRANCH> \
  && echo "Descendant: yes (ff possible, default flow)" \
  || echo "Descendant: no (non-fast-forward; ff-mode repos must use cherry-pick)"
```

**Strategy table**:

| merge_method | release is descendant of target? | Strategy |
|------|------|------|
| `merge` / `rebase_merge` | any | Default merge strategy (Phase 6 merge mode) |
| `squash` | any | At Phase 9, drop `--squash=false` (project forces squash). N commits on release become 1 squash commit on main; record this in the Phase 10 report |
| `ff` | ✅ yes (fast-forward possible) | Default flow; `mr merge` succeeds directly |
| **`ff`** | ❌ **no (non-fast-forward)** | **Cherry-pick strategy** — see `references/ff-cherry-pick.md` |

> The ff + non-fast-forward combination is the single most common trap. Release branches usually diverge from main (both sides have new commits), so an ff-mode repo defaults to cherry-pick. Do not wait for the Phase 9 406.

**GitHub equivalent trap**: GitHub has no `merge_method=ff` toggle; instead it exposes three booleans. When `allow_merge_commit=false && allow_squash_merge=false && allow_rebase_merge=true` (rebase-only), PR merge **rewrites commits and changes their hashes** — effectively ff-only. Treat release → main PRs in this configuration the same way as ff-mode; cross-release sync follows the rebase/hash-changed path in `references/cross-release-sync.md`.

**Output**: per-repo environment fingerprint table (merge_method, release protection rule, CI gate, chosen strategy). Align with the user before Phase 4 whenever ff mode or protection rules look abnormal.

> **Protected branch + non-ff combo**: if release is protected (push=No one), Phase 6 rebase mode's force push will fail regardless of `merge_method`. Mark the strategy column "protected-branch fallback" so Phase 6 takes the fallback path.

---

## Phase 4: Create MR/PR

Run in parallel per repo. Create a merge request from `<RELEASE_BRANCH>` into `<MAIN_BRANCH>` via your platform's CLI (the agent picks `glab` / `gh` / `tea` per its environment). Title: `Release <VERSION>`. Keep the source branch (`--remove-source-branch=false` / `--delete-branch=false`). Record each MR/PR id and URL.

> If Phase 3.5 selected the ff cherry-pick strategy, skip this phase and follow `references/ff-cherry-pick.md` instead — the MR source branch will be `sync-release/<VERSION>-to-<TARGET>`, not the original release branch.

---

## Phase 5: Conflict detection (dry-run, no file modifications)

Run in parallel per repo:
```bash
BASE=$(git merge-base origin/<RELEASE_BRANCH> origin/<MAIN_BRANCH>)

# Content conflict count
git merge-tree $BASE origin/<RELEASE_BRANCH> origin/<MAIN_BRANCH> 2>&1 \
  | grep -c "^changed in both"

# Branch divergence
echo "release ahead: $(git rev-list --count origin/<MAIN_BRANCH>..origin/<RELEASE_BRANCH>)"
echo "main ahead:    $(git rev-list --count origin/<RELEASE_BRANCH>..origin/<MAIN_BRANCH>)"
```

> `git merge-tree` only counts text-content conflicts; it does not detect rename/rename conflicts (typical of build-artifact hash changes). Even at 0 conflicts, if the repo has build artifacts, run Phase 5.5.

**Result classification**:

| Content conflicts | source commits | Strategy |
|------|------|------|
| 0 | any | After MR creation, **verify mergeability** (Phase 5.5); only proceed to Phase 9 if mergeable |
| 0 (but MR is actually not mergeable) | any | **Rebase strategy** (Phase 6) |
| > 0 | ≤ 3 and ≤ 1 conflicted file | Rebase acceptable (per-commit resolution is affordable) |
| > 0 | all other cases | **Merge strategy** (Phase 6) |

> **merge-tree=0 trap**: a clean text merge does not mean the MR is mergeable. Structural divergence can still make the platform refuse the merge. Phase 5.5 is mandatory.
>
> **Rebase trap**: rebase stops at **every** conflicted commit. An 80-commit branch means dozens of interruptions. Unless source is very short (≤ 3 commits) and conflicts are minimal, prefer merge.

---

## Phase 5.5: Verify MR mergeability

> Mandatory whenever merge-tree reported 0. merge-tree=0 ≠ MR is mergeable.

Check the MR's `mergeable` / `can_be_merged` status via your platform's CLI/API. Then consult the table top-down — **the first matching row wins** (the rows are mutually exclusive):

| Result | Action |
|------|------|
| `can_be_merged` / `MERGEABLE`, **and** Phase 3.5 did **not** flag the ff trap | Proceed to Phase 9 |
| Not mergeable (`conflict` / `UNMERGEABLE`) | Switch to rebase strategy (Phase 6); do not proceed to Phase 9 |
| `can_be_merged`, but Phase 3.5 flagged `ff` mode + non-fast-forward | **Phase 9 `mr merge` will still return 406.** Switch to the cherry-pick strategy in `references/ff-cherry-pick.md`; do not proceed to Phase 9 |
| Stuck at `checking` (see unstall procedure below) | Platform recomputation is still pending — run the unstall procedure; do not classify as unmergeable |

> `can_be_merged` only means "code has no conflicts and a merge result exists." It does not bypass `merge_method=ff` or other project-level constraints. The full mechanism and authoritative judgment live in Phase 3.5.

### Unstalling a stuck `checking` status

Multi-repo runs hit this most: the previous MR just updated the target ref and the platform's async re-check queues behind it. When `merge_status` stays `checking` for N consecutive polls (default N=6, 4s interval) while `has_conflicts=false` and `state=opened`:

1. Call the platform's mergeability-recompute endpoint (GitLab: `GET /projects/:id/merge_requests/:iid/merge_ref`) to force a fresh computation.
2. Wait ~3s, then re-check `merge_status`.
3. If it turns `can_be_merged` → continue with the table above.
4. If it is still `checking` → keep polling; only after several recompute-and-wait rounds with no change treat it as a platform anomaly and surface to the user.

A stalled `checking` is an unfinished computation, not a merge verdict — it never means "unmergeable".

---

## Phase 6: Conflict resolution (delegate to `git-conflict-resolve`)

When Phase 5/5.5 indicates conflicts, delegate to the `git-conflict-resolve` skill — pass `source=<RELEASE_BRANCH>`, `target=<MAIN_BRANCH>`, `version=<VERSION>`, and `mode=merge` (default) or `mode=rebase` (only when Phase 5 classified source ≤ 3 commits and ≤ 1 conflicted file).

> Build artifacts (`dist/`, `resources/<bundle>/`, hash chunks) are auto-shortcircuited by `git-conflict-resolve`'s build-artifact auto-shortcut — no extra parameter needed.

If `git-conflict-resolve` cannot finish (user aborts, unresolvable conflict, or rebase interruption), **stop**. Keep the worktree as-is for human intervention; do not continue to later phases.

After `git-conflict-resolve` finishes and emits its global review checklist, and the user confirms, branch on mode:

**Merge mode** — push the merge branch and replace the MR:
```bash
git push origin merge-release/<VERSION>
# Close the conflict-stalled MR via your platform CLI.
# Create a new MR: source=merge-release/<VERSION>, target=<MAIN_BRANCH>.
```

**Rebase mode** — push the rebase result back to the release branch (original MR auto-updates):
```bash
git push origin rebase-release/<VERSION>:<RELEASE_BRANCH> --force-with-lease
```

> `--force-with-lease` refuses to push if the remote moved, preventing accidental overwrite of others' work. Before force-push, confirm with the user: **"Is anyone else working off this branch? Confirm force push."**

**Protected-branch fallback** (when force push is rejected with `! [remote rejected]` or `pre-receive hook declined`):

1. Push the rebase result to a new branch (normal push, not force): `git push origin rebase-release/<VERSION>`
2. Close the original MR
3. Create a new MR with source `rebase-release/<VERSION>` and target `<MAIN_BRANCH>`

The original release branch stays at its pre-rebase commit. Any later release → main sync must account for hash divergence (see `references/cross-release-sync.md`).

**Rebase skip audit** — if rebase printed `warning: skipped previously applied commit <SHA>`:
```bash
git show <SKIPPED_SHA> --stat --oneline
git log origin/<MAIN_BRANCH> --oneline --grep="<keyword>" | head -5
diff <(git show <SKIPPED_SHA> --format=) <(git show <TARGET_SHA> --format=)
```

| diff result | Action |
|------|------|
| Identical | Safe skip; no action |
| Different | The skipped commit is not fully contained; cherry-pick `<SKIPPED_SHA>` manually |

---

## Phase 7: Clean MR/PR extra files (merge mode only)

> Skip in rebase mode — rebase does not drag target's extra files in. Only applies to merge mode, where Phase 6 produced `merge-release/<VERSION>`.

Files present in `merge-release` but absent from **both** release and target are accidentally staged local files (often from `git add -A` during conflict resolution):
```bash
comm -23 \
  <(git ls-tree -r HEAD --name-only | sort) \
  <(sort \
      <(git ls-tree -r origin/<RELEASE_BRANCH> --name-only) \
      <(git ls-tree -r origin/<TARGET_BRANCH> --name-only) \
    | uniq)
```

Common offenders: AI tool configs (`.claude/`, `.omc/`, `.codemap/`, `opencode.json`), temp debug files (`ci-build-error.txt`, `ci-fix-log.txt`). Files present in **either** release or target are expected — do not remove.

Remove and amend:
```bash
git rm --cached -rf <EXTRA_PATH_1> <EXTRA_PATH_2>     # if "pathspec not found": git add -A first, then retry
git commit --amend --no-edit --no-verify
git push origin merge-release/<VERSION> --force-with-lease
```

Re-run the `comm -23` check; the count must be 0.

---

## Phase 8: Residual marker gate (unconditional)

> **Unconditional gate.** No matter what Phases 5/6/7 did, this runs before Phase 9. It is the last line of defense — even if `git-conflict-resolve`'s earlier defenses all failed, Phase 8 catches a commit carrying conflict markers.

### 8.1 Residual marker scan (uses the Phase 0 regex)

Scope is `git diff --name-only` (not the full repo) — only files changed by the merge can carry new residue. Full-repo scans drown in false positives from CSS `=========` comments, ASCII art, license files, and Markdown separators. The verdict is pair-first (Phase 0): pure `=` lines without `<`, `>`, or `|` markers are false positives, not residue.

```bash
BASE=$(git merge-base origin/<MAIN_BRANCH> HEAD)
git diff --name-only $BASE..HEAD | while read f; do
  if git grep -qE '^<{7,} |^>{7,} |^\|{7,} ' -- "$f" 2>/dev/null; then
    git grep -nE '^<{7,} |^={7,}$|^>{7,} |^\|{7,} ' -- "$f" 2>/dev/null
    echo "Residue in $f; merge forbidden"; exit 1
  elif git grep -qE '^={7,}$' -- "$f" 2>/dev/null; then
    echo "pure '=' lines in $f (no <, >, | markers) — pair-first false positive, not residue"
  fi
done
```

> Build-artifact conflicts are normally short-circuited by `git-conflict-resolve`'s build-artifact auto-shortcut (take release side, no residue). Phase 8 is the failsafe if the shortcut leaks a marker into an artifact.

On `exit 1`: **do not proceed to Phase 9.** Return to Phase 6, fix, re-run Phase 8.

### 8.2 Conditional enhancements (only when Phase 6 ran)

- **Conflict-file diff review** — for each file Phase 5 recorded as conflicted: `git diff origin/<MAIN_BRANCH>..HEAD -- <conflict_file>`. Check: both sides' imports/requires retained; both sides' new functions/classes retained; no duplicate symbol definitions; no commented-out code blocks (`//` or `/* */` wrapping whole logic); no unexpected deletions. Any failure → ❌.
- **Rebase skip equivalence** — if Phase 6 skipped commits during rebase, re-confirm diff equivalence (command in Phase 6). Non-empty diff → the skipped commit is not fully contained; manual cherry-pick required.

### 8.3 Verdict

| Verdict | Condition | Next |
|------|------|------|
| Pass | 8.1 no residue **and** 8.2 (if run) all pass | Proceed to Phase 9 |
| Fail | 8.1 detected residue, or any 8.2 check is ❌ | **Merge forbidden.** Return to Phase 6; re-run Phase 8 after fix |

**Output**:
```
[Residual Scan Report]
- 8.1 marker scan: 42 files in merge scope, no residue
- 8.2 diff review (if run):
  - .gitignore: 8.2.70 .omc/.sisyphus changes layered on master
  - src/bridge/api/MainProcessAPI.ts: both sides' new functions retained
- 8.2 rebase skip (if run):
  - skipped 7437368df: diff-equal to master 7421ca91b
Verdict: Pass — proceed to Phase 9
```

---

## Phase 9: Merge MR/PR

After user confirmation, run in parallel per repo:

1. **CI gate check**: query the MR's merge status; if state is not `mergeable` / `can_be_merged`, surface "CI may not have passed — confirm merge?" before proceeding.
2. **Merge**: invoke your platform's merge command. For GitLab with `merge_method=merge`, pass `--squash=false --remove-source-branch=false`. For `merge_method=squash`, drop `--squash=false` (project forces squash). For GitHub, use `--merge` (or `--squash` if the project requires it). Keep the source branch.
3. **Verify**: confirm the merge success output (`✓ Merged!` / `✓ Pull request ... was merged`). Then fetch and inspect the target branch:
```bash
git fetch origin <MAIN_BRANCH>
git log origin/<MAIN_BRANCH> --oneline -5
```
Confirm the latest commits include the release merge.

4. **Freeze check** — after this phase's merge succeeded and the tag from Phase 2 exists, when `git-branch-protect` is available. Read whether this release branch is frozen. When it already is, record the report. When it is not, show the live rule and ask the user to accept `freeze`; run it only after that acceptance. Do not call `rollback`. If the user declines, or the report says the branch is not frozen, keep the tag and the trunk merge, and copy that report into Phase 10. When the skill is not available, skip this step.

---

## Phase 10: Output report

Write to `$(git rev-parse --show-toplevel)/release-<VERSION>-report.md`. Registry row: `发布报告` in `report-output-discipline/reference.md` (`human` + `接入`). After the Markdown report is written, derive `release-<VERSION>-report.html` beside it following `report-output-discipline`, and report both paths.

The report contains:

1. **Tag summary**: repo / tag name / commit SHA / remote verification status
2. **MR/PR summary**: repo / source → target / id and URL / merge status
3. **Conflict details** (if any): branch divergence (commits-ahead per repo), target-only commits (conflict sources), conflicted files and resolution method — **cite the `git-conflict-resolve` skill's global review checklist directly** rather than regenerating it; list of cleaned-up extra files
4. **Manual follow-ups**: residual risks, pending cherry-picks, etc.
5. **Cross-release sync** (if any): source release / target release / strategy / conflict summary (see `references/cross-release-sync.md`)

---

## Common Mistakes

| Mistake | Consequence | Fix |
|------|------|------|
| Skipping Phase 0 because "it looks clean" | Historical residue from failed AI auto-resolution rides the merge into main | Run Phase 0 unconditionally on every repo |
| Tagging the local HEAD without verifying remote | Local is behind; tag lands on a stale commit | Always fetch and tag `$REMOTE_SHA`, never local HEAD |
| Creating MR before Phase 3.5 fingerprint | Hits 406 at Phase 9 in ff-mode repos; costly rollback | Phase 3.5 is mandatory on every path |
| Trusting `can_be_merged=true` as "merge will succeed" | ff-mode repos return 406 anyway | Cross-check Phase 3.5 verdict; first-matching-row wins in Phase 5.5 |
| Force-pushing a shared release branch without confirmation | Overwrites teammates' work | Confirm with user before `--force-with-lease` |
| Rebase on a 50-commit branch | Each conflicted commit halts rebase; days of interruptions | Use merge strategy unless ≤ 3 commits and ≤ 1 conflicted file |
| Multi-repo commands without `cd <REPO> &&` prefix | MR created in wrong repo, wrong MR merged | M.1: every command block in multi-repo runs starts with `cd <REPO_PATH> &&` |
| Stopping at the first repo's Phase 9 failure | Other repos hit the same wall | M.2: propagate failure pattern to all not-yet-merged repos immediately |
| Tag landed on wrong commit | Release points at wrong SHA | `git push origin --delete <TAG>` + `git tag -d <TAG>`, redo Phase 2 anchored to `$REMOTE_SHA`; the platform API may also delete tags remotely |
| Platform `api` reports `Accepts 1 arg(s), received 2` | Shell split the args | Quote each field: `-f "key=value"`; if rejected by that CLI version, use `--raw-field "key=value"`. Prefer upgrading the CLI |
| Cherry-pick produced empty commit ("previous cherry-pick is now empty") | Target already has the equivalent change | `git cherry-pick --skip`; use `--allow-empty` only if a record must be kept |
| `git rm --cached` reports "pathspec not found" | File is in worktree but not in index | `git add -A` to sync worktree to index, then retry |
| CLI auth expired mid-release | Commands fail with auth errors | Re-run platform `auth login`; restart from the failed phase |

---

## Appendix: pre-commit hook (optional L5 enhancement)

A git native hook that runs the Phase 0/8 marker regex on every staged content. Install once; it persists independently of any skill.

```bash
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# Reject staged content with git conflict markers (Phase 0/8 pair-first verdict)
# Pure '=' lines without <, >, or | markers are false positives (license underlines,
# Markdown separators) — they do not block.
# Scan the staged blobs directly: git diff output prefixes every line (+/-/space),
# which defeats the ^ anchors of the marker regex.
git diff --cached --name-only -z | while IFS= read -r -d '' f; do
  if git grep --cached -qE '^<{7,} |^>{7,} |^\|{7,} ' -- "$f" 2>/dev/null; then
    echo "pre-commit: staged content contains conflict markers ($f); commit blocked"
    exit 1
  fi
done || exit 1
exit 0
HOOK
chmod +x .git/hooks/pre-commit
```

- Bypassable with `git commit --no-verify` — L5 is enhancement, not a gate
- If a project already has a pre-commit hook, append the marker check to the existing hook
- Uses the Phase 0 regex with the same pair-first verdict

---

## References

- [`references/ff-cherry-pick.md`](references/ff-cherry-pick.md) — Complete cherry-pick flow when Phase 3.5 detects ff mode + non-fast-forward. Also covers hash-consistency nuances for ff projects.
- [`references/cross-release-sync.md`](references/cross-release-sync.md) — Decision tree and commands for syncing changes from `release/A` (already merged to main) to `release/B`, including the rebase/hash-changed trap.
