---
name: git-fork-divergence
description: "Measure, track, and monitor fork divergence velocity and overlap. Leading indicators for rebase difficulty — aggregate conflict heatmap, per-file delta, and divergence velocity across consecutive checks."
version: 1.4.0
author: Hermes Agent
metadata:
  hermes:
    tags: [git, fork, divergence, rebase, upstream, sync, conflict, monitoring, heatmap]
    triggers: [divergence-check, fork-health, rebase-risk, conflict-heatmap, upstream-overlap, velocity-tracking, ahead-behind]
    related_skills: [dynamic-upstream-merger]
---

# Git Fork Divergence Monitoring

Monitor how far your local fork has diverged from upstream, at what velocity, and which files are at risk. The goal is to surface rebase difficulty *before* you attempt the rebase.

## Quick Check

```bash
git fetch origin
MERGE_BASE=$(git merge-base HEAD origin/main)
AHEAD=$(git rev-list --count origin/main..HEAD)
BEHIND=$(git rev-list --count HEAD..origin/main)
echo "Ahead: $AHEAD | Behind: $BEHIND | Merge base: $MERGE_BASE"
```

## Aggregate Conflict Heatmap

Get a single number: how many files did BOTH you AND upstream change in a recent window?

```bash
MY_FILES=$(git diff origin/main..HEAD --name-only | sort -u)
UPSTREAM_FILES=$(git log origin/main --name-only --since="48 hours ago" | \
  grep -v '^$' | grep -v '^commit\|^Author\|^Date\|^Merge\|^    ' | sort -u)
OVERLAP=$(comm -12 <(echo "$MY_FILES") <(echo "$UPSTREAM_FILES") | wc -l)
echo "Conflict heatmap: $OVERLAP overlapping files"

# Show which core files overlap
comm -12 <(echo "$MY_FILES") <(echo "$UPSTREAM_FILES") | \
  grep -v '\.github\|website\|\.gitignore\|locales\|contributor\|infographic\|\.png' | sort
```

**Interpretation:**
| Overlap | Risk | Action |
|---------|------|--------|
| 0-5 | 🟢 Low | Likely clean rebase |
| 5-30 | 🟡 Moderate | Expect some manual resolution |
| 30-100 | 🔴 High | Significant reconciliation needed |
| 100+ | ❌ Critical | Defer or prepare full manual merge |

**Python-only overlap** (truer "core code" risk):
```bash
comm -12 <(echo "$MY_FILES") <(echo "$UPSTREAM_FILES") | grep '\.py$' | wc -l
```

## Precise Merge-Base Heatmap

For accurate overlap since divergence (not just last N hours):

```bash
MERGE_BASE=$(git merge-base HEAD origin/main)
MY_FILES=$(git diff --name-only $MERGE_BASE..HEAD | sort -u)
UPSTREAM_FILES=$(git diff --name-only $MERGE_BASE..origin/main | sort -u)
OVERLAP=$(comm -12 <(echo "$MY_FILES") <(echo "$UPSTREAM_FILES"))
echo "Overlapping files: $(echo "$OVERLAP" | wc -l)"
echo "$OVERLAP" | sort
```

## Divergence Velocity Tracking

Track how fast the behind-count grows across consecutive checks:

```bash
# Record the behind-count each check cycle
echo "Behind: $(git rev-list --count HEAD..origin/main)"

# Compare against a stored previous value
OLD_BEHIND=${1:-0}
NEW_BEHIND=$(git rev-list --count HEAD..origin/main)
echo "Since last check: $((NEW_BEHIND - OLD_BEHIND)) new upstream commits"
echo "Velocity: $(echo "scale=1; ($NEW_BEHIND - $OLD_BEHIND) / $HOURS_SINCE_LAST" | bc) commits/hour"
```

**State-free delta — reflog method.** If you didn't store last check's behind-count, the pre-fetch origin tip is still in the reflog: `git fetch origin main -q && PREV=$(git rev-parse origin/main@{1})`, then `git rev-list --count $PREV..origin/main` = exact new upstream commits since the previous fetch, and `git diff --stat $PREV origin/main -- <files>` = per-file impact. **More reliable than `--since` windows**: `git log --since`/`--until` parse timestamps in the LOCAL timezone, so a cross-day/cross-zone window can silently return 0 new commits while divergence actually jumped (verified Aug 2 2026: local 20:31 EDT window vs upstream commits capped at 17:08 UTC → 0 results despite +52 behind).

**Decision rules:**
- **Velocity < 1 commit/h** and behind < 100: rebase can wait until the next scheduled session
- **Velocity > 5 commits/h** or behind > 500: **rebase window is closing** — pull within this session
- **Velocity > 20 commits/h** and behind > 200: emergency — upstream is in a sprint; rebase difficulty compounds exponentially with time

## Key Files Overlap Check

Quick check on your most-critical patched files:

```bash
git log --oneline --format="%h %s" HEAD..origin/main -- tools/approval.py tools/tirith_security.py
git log --oneline --format="%h %s" HEAD..origin/main -- hermes_cli/web_server.py gateway/run.py
```

If any of your critical fix files appear in upstream's recent log, that file is a guaranteed conflict zone.

## Per-File Delta Size

For each overlapping file, measure how much upstream changed it:

```bash
for f in $(comm -12 <(git diff origin/main..HEAD --name-only | sort -u) \
                  <(git log origin/main --name-only --since="48 hours ago" | \
                    grep -v '^$' | grep -v '^commit\|^Author\|^Date\|^Merge\|^    ' | \
                    sort -u)); do
  STAT=$(git diff --stat origin/main..origin/main~1 -- "$f" 2>/dev/null | tail -1)
  if [ -n "$STAT" ]; then
    echo "  $f — $STAT"
  fi
done
```

## Structural Refactoring Detection

Upstream file extractions (splitting a large file into multiple modules) create a unique class of rebase conflict that standard overlap checks miss. The signature:

1. Upstream deletes a large block of code from an existing file and moves it to a new file
2. Your fork still has the old structure, so `git diff origin/main..HEAD` shows a massive `+N/-0` for code you didn't actually write — a **phantom diff**
3. The standard conflict heatmap counts 1 overlapping file but the actual resolution work may be 4000+ lines
4. The new file that upstream created exists only in their tree — your fork has no copy and no reference to it

### Detection

```bash
MERGE_BASE=$(git merge-base HEAD origin/main)

# 1. Files upstream deleted since merge base — likely moved their content elsewhere
echo "--- DELETED UPSTREAM ---"
git diff --diff-filter=D --name-only $MERGE_BASE..origin/main | sort -u

# 2. Files upstream created since merge base — potential extraction targets
echo "--- CREATED UPSTREAM ---"
git diff --diff-filter=A --name-only $MERGE_BASE..origin/main | sort -u

# 3. Our files with suspiciously large diffs (phantom diffs: +2000+ lines)
# These may be code that upstream already extracted to a new module, making
# our diff look like a huge addition when in fact it's just the old structure
echo "--- PHANTOM DIFF CANDIDATES (our files with >1000-line diffs) ---"
git diff origin/main..HEAD --name-only -l1000 --diff-filter=M | sort -u | \
  while read f; do
    STAT=$(git diff origin/main..HEAD -- "$f" --stat | tail -1)
    echo "  $STAT"
  done

# 4. Cross-reference: does a deleted-upstream file match a phantom-diff file?
echo "--- STRUCTURAL REFACTOR RISK ---"
LARGE=$(git diff origin/main..HEAD --name-only -l1000 --diff-filter=M | sort -u)
DELETED=$(git diff --diff-filter=D --name-only $MERGE_BASE..origin/main | sort -u)
comm -12 <(echo "$LARGE") <(echo "$DELETED")
```

### Interpretation

| Signal | Meaning | Action |
|--------|---------|--------|
| Our file has +4000 line diff; upstream deleted the same file | Upstream extracted the content to a new module | Accept new module; drop our inline copy; re-apply semantic changes on upstream's new structure |
| Upstream created a new file (`config_defaults.py`) our fork doesn't have | Upstream split a god-file | The new file must exist in your branch after rebase; usually a pure addition with no conflict |
| Upstream deleted + created in the same commit range | Pure data move | Identify the commit with `git show --stat <hash>`; this is the easiest structural conflict to resolve (no semantic overlap, just file placement) |

### Worked Example: config_defaults.py Extraction

On Jul 29 2026, upstream Hermes Agent extracted `DEFAULT_CONFIG` + `OPTIONAL_ENV_VARS` (4160 lines) from `hermes_cli/config.py` into a new `hermes_cli/config_defaults.py`. The local fork showed a 4882-line diff on `config.py` — but 4160 of those lines were the unchanged DEFAULT_CONFIG dict that the fork still inlines because it never received the extraction commit.

Detection:
```bash
# Created file signals the extraction target
git diff --diff-filter=A --name-only $MERGE_BASE..origin/main | grep config
# → hermes_cli/config_defaults.py

# Deleted-from file is what our fork shows as a huge diff
git diff --diff-filter=M --name-only origin/main..HEAD -l1000 | grep config
# → hermes_cli/config.py (4882-line diff — mostly inline DEFAULT_CONFIG)

# The extraction commit
git log --oneline $MERGE_BASE..origin/main -- hermes_cli/config_defaults.py
# → 1fe06115d1 refactor: extract DEFAULT_CONFIG + OPTIONAL_ENV_VARS to config_defaults.py
```

Resolution:
1. Accept upstream's new `hermes_cli/config_defaults.py` as-is
2. Drop the inline `DEFAULT_CONFIG = { ... }` block from config.py (the 4160-line dict)
3. Keep our semantic changes (install method fixes, Homebrew support, etc.) applied to the slimmed-down `config.py`
4. If our semantic changes touched the DEFAULT_CONFIG dict itself, those changes need to be migrated to the new `config_defaults.py` instead

## Per-Patch Rebase-Readiness Audit

The heatmap tells you *how many* files overlap and *which ones*. But a file overlap is not binary — your local patch may be completely independent of upstream's changes to the same file, it may be obsoleted by an equivalent upstream fix, or it may conflict because both changed the exact same lines.

Use this audit to assess each local patch individually before attempting a rebase:

```bash
MERGE_BASE=$(git merge-base HEAD origin/main)

# List all local patches (commits on your branch not in upstream)
echo "=== LOCAL PATCHES ==="
git log --oneline origin/main..HEAD
echo ""

# For each local patch, check if upstream touched the same files
for patch in $(git rev-list origin/main..HEAD); do
  files=$(git diff --name-only $patch^..$patch 2>/dev/null)
  echo "=== PATCH: $(git log --oneline $patch -1 | head -1) ==="
  for f in $files; do
    up_count=$(git log --oneline $MERGE_BASE..origin/main -- "$f" 2>/dev/null | wc -l)
    if [ "$up_count" -gt 0 ]; then
      echo "  🟡 $f — $up_count upstream commit(s) since fork"
    fi
  done
done
```

### Audit Checklist (per patch)

For each patch file that upstream has also modified:

1. **Is the fix still missing upstream?** Check the specific line the patch changes:
   ```bash
   git show origin/main:tools/approval.py | grep -n "shlex.split\|posix="
   ```
   If upstream still has the old/broken version, the patch is **still needed**.

2. **Was it obsoleted by an equivalent upstream fix?** Upstream may have fixed the same bug a different way. Compare approaches side-by-side:
   ```bash
   # Our version
   git show HEAD:tools/approval.py | sed -n '2015,2022p'
   # Upstream version
   git show origin/main:tools/approval.py | sed -n '2015,2022p'
   ```
   If upstream's fix is equivalent or better, the local patch can be **dropped**.

3. **Is the patch complementary to upstream's new code?** Upstream may have added a more comprehensive version of your pattern. Example: upstream added a `_hardline_rm_path` helper covering `~` and `$HOME` recursive patterns, while your patch adds a narrower `rm ~/` entry. The two coexist safely — **keep both**.

4. **Does upstream's rewrite remove the code your patch targets?** If upstream deleted the function or variable your patch modifies entirely (common in refactors), the patch will produce a **modify/delete** conflict during rebase. Decide whether to re-apply the intent on upstream's new structure or drop it.

5. **Did upstream change the BODY of a function your patch touches — not just the file?** Same file AND same function is the sharpest conflict signal, and it's easy to miss with a file-level overlap check. Observed Aug 2 2026: upstream `48e825456` swapped `load_config()` → `load_config_readonly()` INSIDE `load_permanent_allowlist()` — the exact function our lazy-init patch defers. Verdict was **compatible** (orthogonal: they changed the loader, we deferred the call — they compose), but it adds a 4th merge touchpoint inside the patched function that the rebase must preserve. Detection: `git show <sha> -- <file> | grep <function-name>` and read whether upstream's changed lines overlap your patch's lines. Classify: orthogonal (composes, note it in rebase plan) vs same-lines (real conflict) vs removed-function (modify/delete).

6. **Verify patch survival with the EXACT committed form, not a loose substring.** `grep -c "rm ~/"` returns 0 on a patch whose committed entry is the regex `\brm\s+(-[^\s]*\s+)*~/` (Aug 2 2026 — nearly flagged an intact patch as lost). When checking whether a local patch is still in the tree, grep for the literal committed pattern (from `git show <commit> -- <file>`) or count distinct refs, not a human-readable paraphrase. Same applies to checking upstream: `git show origin/main:<file> | grep -n` the exact committed string.

### Outcome Classifications

| Result | Meaning | Rebase Action |
|--------|---------|---------------|
| ✅ Still needed | Upstream has not fixed it | Keep the patch; expect clean apply |
| ✅ Obsoleted by equivalent upstream fix | Upstream fixed it a different way | Drop the patch |
| ✅ Upstream's approach is better | Upstream has a more comprehensive version | Accept upstream's version; drop or narrow local patch |
| ✅ Complementary | Local patch covers a gap upstream's version missed | Keep both — they coexist |
| ❌ Modify/delete conflict | Upstream removed code your patch targets | Must re-implement intent on new upstream structure |
| ❌ Structural conflict | Upstream extracted code to a new file | Migrate patch to upstream's new module structure |
| 🟡 Semantic drift | Upstream changed function signatures/types your patch depends on | May need rework even if git reports no conflict |

### Worked Example: approval.py Multi-Patch Audit

From the Hermes Agent Forge pulse logs (Jul 30 2026, 14 local patches, 3253 behind):

```bash
cd ~/AppData/Local/hermes/hermes-agent
git fetch origin

# Check shlex.split (3 approval.py commits)
git show origin/main:tools/approval.py | grep -n "posix=True"
# → line 2018: argv = shlex.split(command, posix=True)
# Still uses posix=True — upstream hasn't adopted the Windows fix.

# Check lazy-init
git show origin/main:tools/approval.py | tail -3
# → line 4161: load_permanent_allowlist()  (module-level call)
# Still loads at import time — upstream hasn't adopted lazy-init.

# Check rm ~/ DANGEROUS_PATTERNS
git show origin/main:tools/approval.py | grep -n "rm.*~/"
# No match — upstream doesn't have this pattern.
# But upstream HAS added _hardline_rm_path + _RM_FLAG_PREFIX for ~/$HOME.
# These are complementary — both needed.

# Check upstream's new additions
git show origin/main:tools/approval.py | grep -n "flags after operands"
# → New pattern for rm build/ -rf detection (openai/codex#33464 port)
# Additive — won't conflict with our patches.
```

**Result**: All 3 patches confirmed still needed. Net rebase effort is lower than feared because upstream's deletions (denial breaker, smart_policy) touch code we never carried.

### Phantom-Diff vs Per-Patch Distinction

The **Structural Refactoring Detection** section above catches file extractions (`config_defaults.py`) where a single file shows +4000 lines of phantom diff. The **Per-Patch Audit** here catches the complementary case: small, targeted patches on files that upstream rewrote heavily. Use both — they cover different classes of rebase risk.

## Authoritative Conflict Check (`git merge-tree --write-tree`)

The heatmap and per-patch audits are **predictive heuristics**. The definitive "will the rebase actually conflict" answer comes from `git merge-tree --write-tree`, which performs a real merge in memory and reports exact conflicts:

```bash
MB=$(git merge-base HEAD origin/main)
git merge-tree --write-tree --name-only HEAD origin/main 2>&1 | grep CONFLICT
```

- **Exit code 1 = conflicts exist** (first output line is the merged-tree SHA; `--name-only` then lists conflicted paths). Exit 0 = clean merge.
- Output is typed per conflict: `CONFLICT (content): <file>`, `CONFLICT (add/add): <file>`, `CONFLICT (modify/delete): <file>` — the type dictates the resolution class (add/add = combine both suites, modify/delete = re-implement intent on upstream's new structure).
- `--name-only` keeps output to just the conflict list; the full form dumps the merged tree diff, which is noisy.
- **Conflict count flips non-linearly with divergence.** Verified Aug 11 2026: at 573-behind the check returned **0 textual conflicts** (all auto-mergeable), at 1059-behind it surfaced **5 real conflicts** (`lifecycle_guard.py`, `model_switch.py`, `models.py`, an add/add test file, `terminal_tool.py`) — as upstream's churn lands on your patched files, clean zones become merge work. Re-run the check every cycle once behind > 500, not just when the heatmap looks hot.
- Complement with the changed-on-both-sides file list to see the full surface (files that auto-merge but still need semantic review):
  ```bash
  comm -12 <(git diff --name-only $MB HEAD | sort) <(git diff --name-only $MB origin/main | sort)
  ```

**Pitfall — legacy `git merge-tree <base> <ours> <theirs>` output is NOT text-parseable.** It interleaves raw binary blobs (PNG bytes `0x89`, etc.) and "changed in both" blocks that carry no filename, so grep/regex extraction of the conflicting-file list fails (UnicodeDecodeError on the binary; empty/duplicate file lists from the anonymous blocks). Always use the `--write-tree` form for programmatic conflict detection.

## Pitfalls

- **`--name-only` vs merge-base.** `git diff origin/main..HEAD --name-only` compares HEAD to upstream's tip, not your merge base. When behind by 500+ commits, many more files appear as "your changes" than actually are (the diff compares across the full gap). Use the merge-base approach for accurate overlap.
- **Phantom diffs hide rebase cost.** A single overlapping file with a +4000/-0 diff (your inline copy of code upstream already extracted) looks like 1 file on the heatmap but can be 4+ hours of manual resolution. Always check large-diff candidates separately.
- **New upstream files are invisible to overlap checks.** If upstream moves code to a new file your fork doesn't have, the standard `comm -12` overlap shows zero hits on that file — but your local changes to the old file are now structurally incompatible. Always check `--diff-filter=A` upstream.
- **Pure data moves are deceptive.** A commit that shows `+4166/-4159` across only 2 files has zero semantic overlap but creates a structural conflict. Don't skip these in risk assessment just because the overlap count is low.
- **Pulse/cron workflow:** Divergence grows between pulses. If you check at 08:00 ET (behind=100) and again at 16:00 ET (behind=300), the 200 new commits in 8 hours mean velocity is ~25/h. Don't defer — schedule rebase within the session.
- **Noise filtering.** The `comm -12` overlap includes ALL overlapping files: CI configs, test files, docs, images. Always filter with `grep -v` for meaningful signal. `.py$` files are the best single metric for Python projects.
- **Large repo collections.** For multi-repo setups (100+ repos), a full `for d in */; do git -C "$d" ...` loop gets killed. Use `find .git -newer` timestamp gate as a pre-filter (see `recurring-status-checks` for pattern).
- **Stale `origin/main` under-reports divergence — fetch every cycle.** A behind-count measured against an un-fetched `origin/main` is wrong, and silently: Aug 2 2026 dev-lead pulse measured 3701 against a ref from the previous day's fetch, then `git fetch` revealed the true count 3796 (+95 commits, ~8/h re-accelerating). Worse, a no-fetch cycle corrupts the NEXT cycle's reflog delta (`origin/main@{1}` points at a ref that never moved). Rule: `git fetch` is step 1 of every measurement, no exceptions.
- **A SUDDEN behind-count COLLAPSE is a reset event, not improvement.** Behind-count only grows from upstream activity; it can only fall when someone resets/force-pulls/rebase-onto-origin. A collapse between checks (e.g. 4226 → 64 behind in 21h, Aug 4 2026) means the local stack was wiped and selectively restored — a full loss audit is required, not a celebratory "divergence improving" line. Reconstruct via `git reflog` (look for `reset: moving to origin/main` + `cherry-pick:` entries), enumerate which local commits from the last pulse are missing from `git log --oneline origin/main..HEAD`, and check recoverability with `git cat-file -t <sha>`. Full workflow: `fork-patch-maintenance` §4h Post-Reset Aftermath Audit.

**Lost-patch restorability probe (verified Aug 7 2026).** Before attempting a cherry-pick restore of a lost patch, run the ~30-second probe in `references/lost-patch-restorability-probe.md` per SHA — `git cat-file -t <sha>` (object still in DB?), `git show <sha> --stat` (files touched), `ls` the target files (still exist?). It predicts clean-apply vs conflict-resolution: rewritten-target files → plan semantic re-apply on upstream's new structure, not a blind cherry-pick; deleted-target files → modify/delete conflict, re-implement or drop.
- **Add/add collision: you and upstream both ADDED the same path since the merge-base.** Signature: `git diff origin/main...HEAD -- <file>` shows `new file` yet `git ls-tree origin/main -- <file>` shows the path exists upstream. Common cause: you cherry-picked the function half of an upstream feature commit but wrote your own test file under the same path upstream used; their follow-up PRs then evolve their copy. Detection loop: `git diff origin/main...HEAD --name-only --diff-filter=A | while read f; do git ls-tree origin/main -- "$f" >/dev/null 2>&1 && echo "ADD/ADD: $f"; done`. Rebase reality: real merge work — combine both suites, don't pick one. **Early warning: upstream commits landing on YOUR test files = parallel work on the same feature.**
- **A clean/"byte-identical" classification is per-pulse, not persistent.** When upstream continues evolving the same feature area (new kwargs, call-site rework, follow-up PRs), a zone you declared context-shift-only last cycle becomes real merge work again — and the signature of a function you adopted can change under you (`cache_only` kwarg added; your `timeout=1.5 if for_picker`-style call-site hack becomes obsolete). Re-sweep every cycle, re-check adopted-function signatures, and plan to ADOPT the new upstream semantics rather than keep your old call shape. Full worked example (Aug 7→10 2026, model_switch.py cached-catalog zone + add/add test collision): `references/windowed-conflict-surface-sweep.md`.
- **Weighted zone hits beat a flat file union for triage.** Per-window commit counts per conflict zone:
  ```bash
  git log --oneline <base>..origin/main --name-only --format="" | sort | uniq -c | sort -rn | grep -E 'approval.py|run.py|model_switch|config_defaults'
  ```
  Tells you which zone is hottest RIGHT NOW (e.g. 8 commits on `gateway/run.py` vs 1 on `model_switch.py` in the same window), which is sharper than the flat `--name-only` union that only says "touched or not".
- **Two-dot diff misattributes YOUR OWN hunks as upstream churn.** When locating "upstream" hunks via `git diff HEAD..origin/main -- <file> | grep -E '^@@'`, the old-side line numbers are YOUR tree's lines — and every line your local commits added appears as a `-` deletion because upstream lacks it. A hunk "landing exactly on your call site" (e.g. old-:2501 matching your #29 `_native_tool_arg` call site) is just your own addition, not upstream activity — false alarm. The true upstream-only surface anchors at the fork point:
  ```bash
  git diff $(git merge-base HEAD origin/main)..origin/main -- <file> | grep -E '^@@'
  ```
  Old-side numbers then refer to the merge-base file; only hunks falling inside your added line ranges are genuine overlap. For per-commit precision use `git show <sha> -- <file> | grep -E '^@@'`. Verified Aug 11 2026 (file_operations.py): combined diff showed hunks at old-:2501/:2516/:2600 matching #29's call sites; merge-base-anchored diff showed ALL upstream hunks ≤:1957 plus one 1-line hunk at :2684 → clean context-shift, and the previous pulse's flagged "small conflict zone added by #29" was retracted as a non-issue. Worked example: `references/windowed-conflict-surface-sweep.md` §Two-dot diff trap.

## Related Skills

- `dynamic-upstream-merger` — full rebase/merge lifecycle with per-file delta analysis, semantic change analysis, and post-rebase validation
- `recurring-status-checks` — cron-based status monitoring with divergence tracking and escalation

## Reference Files

- `references/windowed-conflict-surface-sweep.md` — per-cycle triage sweep: which patched files upstream touched since last check, hunk-region classification ladder (incl. **add/add collision** on same-named test files), **last-instance drift** (upstream migrated a pattern your patch still uses — merges clean but needs rebase-time adaptation), **signature evolution** (upstream adds kwargs to a function you adopted — your call-site hack becomes obsolete), **free-gains triage** (upstream hits on files outside your stack / brand-new upstream modules = adopt-on-rebase wins, not risks; quantify hunk distance by line numbers), the **two-dot diff trap** (combined `git diff HEAD..origin/main` hunks include your own additions — anchor at the merge-base for the true upstream surface), and the **digest-script `[SILENT]` vs job-gate mismatch** pitfall (append-digest-style scripts self-suppress on their own quiet-hours gate — don't read their `[SILENT]` as an order to suppress your report). Worked examples: model_switch.py `cached_fetch_api_models` vs OmniRoute picker, Aug 7→10 2026; file_operations.py #29 clean-surface verification, Aug 11 2026; resource_limits.py free-gain + digest-gate mismatch, Aug 11 2026.
