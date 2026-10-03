---
name: 10days
description: >
  Sweep GitHub issues opened or updated in an age window (default: last 10 days; the
  window is adjustable, e.g. an 11-14-day slice to avoid overlapping another sweep),
  evaluate PRS 4-axis ratings (priority, severity, appeal, effort cheapness, calc sum,
  and manual ovr overrides) taking highest-scored issues and operator overrides as a strong
  prioritization signal, verify each issue is still valid, reproducible, and not already
  fixed (fan out subagents to check issue state, comments, and git/commit history for completion
  evidence), build a marathon plan from the survivors, run swarm-preflight on it, then
  cut a branch and execute the marathon end-to-end with no pause inside a dedicated
  disposable full clone folder (using worktree isolation or throwaway sub-clones for
  individual parallel lanes underneath). This skill is a deliberate, operator-authorized
  exception to this repo's default "ask before cutting a branch / firing a marathon" rule
  (GUIDING-PRINCIPLES.md §8) — it exists specifically to run unattended. Trigger on "/10days",
  "run the 10 day sweep", or the operator's canned request: "look through recent GH issues within
  the last 10 days and check if they are still valid, reproducible, not completed already... add
  each one to a marathon file, run preflight, cut a new branch and execute on the marathon."
  Requires swarm-preflight.sh + marathon-plan.sh resolved from the harness root (bare repo
  root or a vendored `.xyz/` install — see Procedure Step 0), plus the swept repo's
  PROJECT/** + releases.db + gh (authenticated) + jq.
---

# /10days — recent-issue sweep → PRS rating prioritization → marathon → fire

Turn "what's landed in GitHub in the last N days that's still worth doing" into a fired
marathon, unattended. This is `start-marathon`'s more automated sibling: where
`start-marathon` stops at a plan and hands it to the operator, `/10days` carries the
plan through PRS rating evaluation, preflight, branch-cut, and execution in one run — because that is
literally what it was built for (a canned macOS text-replacement snippet that expects
one shot, no back-and-forth).

**Read this whole file before running anything.** The auto-fire behavior below is a
named exception to house convention, not an oversight — know why before you invoke it.

**Reviewed 2026-07-16 & Refined 2026-09-05** via `/consult --models agy` and `/relay-xyz` Codex:
incorporates PRS 4-axis rating system prioritization (GH-108: `pri/sev/appeal/effort`, `calc` sum,
and `ovr` manual overrides), full clone folder isolation per GH-564 and `WORKTREE-SAFETY.md`,
safe JSON in `find-doc.sh`, per-issue `swarm-preflight.sh` invocations, live marathon collision guards,
origin sync verification, and robust multi-lane execution containment.

## Guardrails (read first)

- **Sandbox off for `gh` and `git fetch`/`git push`** — every `gh` call and preflight
  run here fails under the Bash sandbox (TLS/keychain). Run with the sandbox disabled.
- **Auto-fire is intentional here, and only here.** `GUIDING-PRINCIPLES.md` §8 and the
  `start-marathon` skill both say never auto-fire a marathon —
  that default stands everywhere else in this repo. `/10days` was authorized by the
  operator (2026-07-16) to override the *pause*, not the *substance*: it still requires
  a clean working tree AND an idle coordination layer before cutting anything (Step 7),
  still runs every gate, still stops the run cold on a red gate or a git-safety
  violation, and still prints every command it runs. If any precondition in Step 7
  fails, stop and report — do not force through it.
- **Prioritize via PRS 4-Axis Ratings & Manual Overrides (GH-108).**
  - The canonical task rating system has four 1–100 axes: **pri** (priority/queue position),
    **sev** (severity/pain if left undone), **appeal** (attraction/energy), and **effort**
    (cheapness/ease — inverted, so 100 = easiest/cheapest, 1 = hardest). Higher is better on every axis.
  - **`calc` = equal-weighted sum of the four axes (range 4–400).** High-scoring issues provide a
    strong signal to prioritize candidates into earlier marathon waves.
  - **`ovr` (operator override) = manual score on the 4–400 scale.** An `ovr` score overrides `calc`
    arithmetic and represents an explicit operator pin to the front of the queue. Always sort
    manual overrides ahead of calculated scores when selecting and ordering marathon candidates.
- **Execute in a Disposable Full Clone Folder, Not the Primary Checkout (GH-564 & WORKTREE-SAFETY.md).**
  - Linked worktrees isolate working-tree files but share `.git/config`, remotes, refs, hooks, and
    stashes with their parent clone. Running mutation-heavy gates (`validate.sh`, `test/*.sh`) in a
    linked worktree can contaminate or corrupt the parent clone's `.git/config` and origin URLs (GH-564).
  - Always run the marathon and test gate validation in a **dedicated disposable full clone folder**
    (e.g. `~/marathon-clones/10days-YYYY-MM-DD-<repo-slug>` or `~/marathon-clones/marathon-gh-<umbrella>-<slug>`).
  - Within the marathon, parallel runner subagents may use isolated worktrees (`isolation: "worktree"`)
    or disposable sub-clones for independent edits, but the parent repo must remain protected.
- **Never mark an issue "already done" without evidence.** A hunch is not evidence. A
  merged commit/PR that references the issue number, or an existing capture doc parked
  in `PROJECT/3-COMPLETED`, is evidence.
- **Check for a concurrently-running marathon before touching the branch, not just the
  current branch name.** A dirty tree, a non-empty `.tick/locks/`, or a fresh untracked
  `PROJECT/2-WORKING/MARATHON-*` directory all mean something else is mid-flight —
  cutting a branch or firing on top of that state will collide with it. Step 7 checks
  all three, not just `git branch --show-current`.
- **Parallel lanes run in isolated worktrees or sub-clones, not on the shared tree.** Dispatching
  concurrent Agent calls directly against one working tree is a containment violation
  (GUIDING-PRINCIPLES.md §3/§4) — two lanes writing at once with no isolation can orphan
  each other's commits. Step 7 uses the Agent tool's `isolation: "worktree"` or disposable full
  clones for every parallel lane.
- **A lane only ever touches its contract's `artifacts` allowlist.** No lane edits
  the roadmap ledger beyond the intake row/pointer line this skill itself registers in Step 4.
- **Auto-drafted preflight contracts are a best-effort guess, not a verified fact —
  and the fix for a wrong guess has to land before firing, not in the after-the-fact
  report.** A wrong `artifacts` list makes `marathon-plan.sh`'s wave/collision map
  untrustworthy: two lanes it thinks are disjoint could actually touch the same file
  and race. Step 6.5 adds a cheap deterministic overlap check specifically to catch
  this before any wave runs concurrently, in addition to the Step 8 report flag.

## Preconditions — install once

Claude Code and Antigravity only scan their respective global skill directories, not this repo's
top-level `skills/`. Run this once from a harness clone:

```bash
bash skills/3-weekly/10days/install.sh   # symlinks this clone's skills/3-weekly/10days into ~/.claude/skills/ and ~/.gemini/config/skills/
```

## Procedure

### 0. Resolve harness root, confirm sweep target, and prepare full clone workspace

Resolve the harness root via the locator loop and evaluate its exported environment:

```bash
L=""
for candidate in "${XYZ_HARNESS:+$XYZ_HARNESS/skills/1-hourly/relay-xyz/find-harness.sh}" \
                 "$HOME/.claude/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.codex/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/config/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/antigravity/skills/relay-xyz/find-harness.sh" \
                 "$HOME/.gemini/antigravity-cli/skills/relay-xyz/find-harness.sh" \
                 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/relay-xyz/find-harness.sh" \
                 "$(git rev-parse --show-toplevel 2>/dev/null)/skills/1-hourly/relay-xyz/find-harness.sh"; do
  [ -n "$candidate" ] && [ -f "$candidate" ] && { L="$candidate"; break; }
done
[ -n "$L" ] || { echo "relay-xyz: locator not found — install the skill or set XYZ_HARNESS" >&2; exit 1; }
eval "$("$L" --env)"
```

Reference every harness script below as `$HARNESS/utils/…` — **not** bare `utils/…` paths, which
resolve to nothing (or to an unrelated `utils/` directory) in a vendored `.xyz/` install.

The two bundled scripts (Steps 1 and 2) ship beside this `SKILL.md`, so set `SKILL_DIR` to whatever
directory this file was loaded from — `~/.claude/skills/10days`, a clone's `skills/3-weekly/10days`, or a
vendored `.xyz/skills/3-weekly/10days` are all valid. Do **not** assume `skills/3-weekly/10days/` relative to the
swept repo; when sweeping a foreign repo that path does not exist:

```bash
SKILL_DIR=/absolute/path/to/this/skill/directory   # substitute the real one
```

**Confirm the target repository and prepare a verified, collision-free full clone folder (GH-564 & WORKTREE-SAFETY.md):**

```bash
TARGET_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"   # repo you intend to sweep
REPO_REMOTE="$(git remote get-url origin)"
REPO_SLUG="$(echo "$TARGET_REPO" | tr '/:' '--')"
SWEEP_DATE="$(date +%Y-%m-%d)"
SWEEP_TS="$(date +%Y%m%d-%H%M%S)"
MARATHON_CLONE="$HOME/marathon-clones/10days-${SWEEP_DATE}-${REPO_SLUG}-${SWEEP_TS}"

CURRENT_TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Pre-clone coordination check: assert source repo has clean tree, no active locks, and no untracked plans
SOURCE_STATUS="$(git -C "$CURRENT_TOPLEVEL" status --porcelain 2>/dev/null || true)"
[[ -z "$SOURCE_STATUS" ]] || { echo "Fatal: source repo has uncommitted/dirty state ($SOURCE_STATUS)" >&2; exit 1; }

if [[ -d "$CURRENT_TOPLEVEL/.tick/locks" ]]; then
  SOURCE_LOCKS="$(ls "$CURRENT_TOPLEVEL/.tick/locks" 2>/dev/null || true)"
  [[ -z "$SOURCE_LOCKS" ]] || { echo "Fatal: source repo has active tick locks in .tick/locks/ ($SOURCE_LOCKS)" >&2; exit 1; }
fi

# Prepare unique dedicated disposable full clone (never reuse/reset an existing dirty workspace):
mkdir -p "$HOME/marathon-clones"
git clone "$REPO_REMOTE" "$MARATHON_CLONE"
cd "$MARATHON_CLONE"

# Unconditional assertion: must be inside verified full clone matching REPO_REMOTE
[[ -d ".git" ]] || { echo "Fatal: workspace is not a full clone root (.git missing or worktree)" >&2; exit 1; }
[[ "$(git config --get remote.origin.url 2>/dev/null)" == "$REPO_REMOTE" ]] || { echo "Fatal: origin URL mismatch" >&2; exit 1; }

# Establish canonical base tracking checkout in the disposable clone before planning:
BASE_BRANCH="${XYZ_BASE_BRANCH:-development}"
git fetch origin "$BASE_BRANCH" --quiet
git checkout "$BASE_BRANCH"
git reset --hard "origin/$BASE_BRANCH"
[[ "$(git rev-list --count HEAD..origin/"$BASE_BRANCH")" -eq 0 ]] || { echo "Fatal: HEAD is behind origin/$BASE_BRANCH" >&2; exit 1; }
```

Run every subsequent step from the swept repo's **root** in the full clone.

### 1. Pull the candidate window (deterministic — no judgment calls)

```bash
bash "$SKILL_DIR/scan-issues.sh" [MAX_DAYS] [MIN_DAYS]   # default: 10 0  (last 10 days)
```

`MAX_DAYS` is how far back the window opens; `MIN_DAYS` (default 0 = today) is how
close to today it closes. Use the two-argument form to carve out a slice that skips a
range another sweep already owns — e.g. `scan-issues.sh 14 11` covers issues 11-14
days old and deliberately excludes the last 10 days.

Emits one JSON object per OPEN issue updated in the window (`{number, title, createdAt,
updatedAt, url, labels}`), sorted by issue number. This is a plain `gh issue list`
wrapper — it makes no validity/completion judgment, so it is safe to re-run and diff.

### 2. Cheap local reconcile and PRS ratings lookup

For every issue number from Step 1:

1. **Doc & Bucket Check:**
   ```bash
   bash "$SKILL_DIR/find-doc.sh" <N>
   ```
   - `bucket: "3-COMPLETED"` → strong already-done signal. Exclude immediately; note on the "propose closing #<N>" list.
   - `bucket: "2-WORKING"` with `has_contract: true` → preflight contract exists; route through Step 3 for freshness check.
   - `bucket: null` or `has_contract: false` → needs full Step 3 check and contract authoring in Step 4.

2. **PRS Ratings Extraction & Validation (GH-108):**
   Query `releases.db` (or capture doc frontmatter) for existing ratings:
   ```bash
   python3 "$HARNESS/utils/py/releases_app.py" roadmap show <N> 2>/dev/null || true
   ```
   - **Validate & Recompute Stored Ratings**:
     - Verify each axis (`rating_pri`, `rating_sev`, `rating_appeal`, `rating_effort`) is an integer in range `[1, 100]`.
     - Always recompute `calc = rating_pri + rating_sev + rating_appeal + rating_effort` (range `[4, 400]`) rather than trusting stored sums.
     - If `rating_ovr` (`ovr`) is present: verify it is an integer in range `[4, 400]`. If malformed or out of range, invalidate and mark it for clearing (`ovr: null`, `is_manual_override: false`).

**Gotcha to carry into Step 3:** `swarm-preflight.sh` fix-probes detect the *bug*, not
the *fix* (`grep_present` = bug still there, `grep_absent` = fix landed). Read a stale
doc's own probe definitions before trusting its verdict — don't assume "has a contract"
means "verdict is current."

### 3. Validity / reproducibility / completion / PRS evaluation fan-out (subagents)

For every issue that survives Step 2, spawn subagents (batch in groups of ~5-6 concurrent) to answer, with receipts:

- `gh issue view <N> --json title,body,comments,state,labels,url` — read the actual ask, comments, and any operator-posted scores.
- **Ledger & PRS cross-check**: query `releases.db` for roadmap items by GH number to extract existing PRS ratings and manual overrides.
- **Deterministic PRS Scoring Rubric for Unscored or Incomplete Issues (GH-108)**:
  If a candidate has no stored rating, or if stored axis values are partial, non-integer, or out of range `[1, 100]` (or `ovr` is malformed/out of range `[4, 400]`), assign deterministic integer point values based on observable properties:
  - **pri** (queue priority): `90` = critical path blocker / front-of-line ask; `60` = standard backlog task; `30` = minor/niche improvement.
  - **sev** (severity / pain): `90` = crash, data corruption, or severe gate blocker; `60` = functional bug / incorrect output; `30` = cosmetic / documentation / typo.
  - **appeal** (motivation / clarity): `90` = clear reproduction steps and unambiguous fix locus; `60` = clear ask needing modest investigation; `30` = open-ended or underspecified report.
  - **effort** (cheapness / ease — inverted): `90` = surgical single-file change ≤ 20 lines; `60` = moderate multi-file change ≤ 200 lines; `30` = massive architectural rework > 200 lines.
  - Compute `calc = pri + sev + appeal + effort` (range `[4, 400]`). Mark `provisional: true`.
  - **Override Handling & Explicit Clear**: If `ovr` is invalid or absent, clear it by running `roadmap rate --issue-num <N> --rated <P>/<S>/<A>/<E> --force` (omitting `--ovr`), and assert read-back via `roadmap show <N>` returns `ovr: null` and `is_manual_override: false`. Set `is_manual_override: true` if and only if a valid, verified `ovr` in range `[4, 400]` is present.
  - Persist newly evaluated ratings to `releases.db` via `releases roadmap rate` (see Step 4).
- `git log --all --oneline -i --grep="#<N>\b" --grep="GH-<N>\b"` — commit evidence.
- `gh pr list --state merged --search "<N> in:body"` (and `--search "#<N>"`) — merged PR evidence.
- If a capture doc exists (from Step 2), read its own "Status" table and frontmatter.

Return one structured verdict per issue:

```json
{
  "issue": N,
  "decision": "INCLUDE|EXCLUDE",
  "reason": "...",
  "evidence": ["commit abc123 fixes this", "..."],
  "already_done": false,
  "duplicate_of": null,
  "needs_contract": true,
  "prs": {
    "pri": 70,
    "sev": 80,
    "appeal": 60,
    "effort": 75,
    "calc": 285,
    "ovr": null,
    "effective_score": 285,
    "is_manual_override": false,
    "provisional": true
  }
}
```

**Prioritization Rules:**
- `effective_score` = `ovr` if present and valid (`[4, 400]`), else recomputed `calc` (`pri + sev + appeal + effort`).
- **Manual override items (`is_manual_override: true`) are operator pins**: rank them at the very front of the candidate queue regardless of arithmetic.
- **High calculated scores (`calc >= 250`, or `sev >= 75` / `pri >= 75`)**: serve as a strong signal to prioritize the candidate into earlier waves.
- `EXCLUDE` when: already fixed by commit/PR, duplicate, unreproducible, or not a work item.

> **Runtime-aware reproducibility (`runtime:*`-labeled issues only).** If an issue carries a
> `runtime:bash` label, reproduce it under `XYZ_PYTHON=0` before ruling it not-reproducible or
> already-fixed: since the default flipped, a plain repro runs the Python twin, so a Bash-path bug
> won't surface and would be falsely `EXCLUDE`d as "already done." `runtime:python`/`runtime:parity`
> reproduce under the default path. These labels exist only in `xyz-3-agents-swarm`, so this is a
> silent no-op for any other repo the sweep runs against.

### 4. Ensure every INCLUDE has a contract-carrying capture doc in `2-WORKING`

> **The acceptance criteria are COPIED, never restated (GH-400).** Everything downstream —
> preflight, the packet, the relay file, the builder, the reviewer — reads this doc; the issue
> text reaches none of them. So the moment you summarise the acceptance block, your summary *is*
> the contract and no role left in the pipeline can compare it to anything. Measured case:
> `rebalance-OS` #202 required a malformed row be *"proven to be either reconciled or surfaced,
> never silently dropped"*; the capture doc this step wrote asked instead to assert *"the actual
> current behavior (drop the row)"*; two independent marathon runs then delivered a test named
> `malformed_source_row_is_dropped`, and every gate reported success. Summarise the *background*
> as much as you like. **Reproduce the `## Acceptance` block byte-for-byte** (re-wrapping to ~80
> columns is fine — nothing else is). `swarm-preflight` now re-fetches the issue and refuses to
> emit a packet on unexplained divergence, so a restatement here does not merely risk a wrong
> build, it hard-fails the lane at Step 6.

For each `INCLUDE` verdict:

- **Doc already exists** (1-INBOX or 2-WORKING): move it to `2-WORKING` if it isn't
  there yet; add a `## Swarm Preflight Contract` block if `has_contract` was false.
  Update frontmatter with PRS ratings and override fields if newly evaluated.
  **If it has no `## Acceptance` section and the issue does, add one — copied verbatim.**
- **No doc exists**: author `PROJECT/2-WORKING/GH-<N>-<slug>.md` using this repo's
  standard capture-doc frontmatter (`gh_issue`, `source`, `title`, `status`, `created`,
  `updated`, `owner`, `doc_type`, `rating` (GH-108: `"pri/sev/appeal/effort <pri>/<sev>/<appeal>/<effort> · calc <calc>"`), `rating_ovr` (nullable integer `4–400`), `is_manual_override` (`true|false`), `ratings_provisional: true`, `goal`), where **`source` is the full tracking-issue URL** so a
  reader can diff the doc against the issue it claims to implement in one step. Give it an `## Acceptance` section copied
  verbatim from the issue's, plus a best-effort contract:

  ```markdown
  ## Swarm Preflight Contract
  ```json
  {
    "target":      { "repo": ".", "ref": "development" },
    "gate":        "bash validate.sh",
    "fix_probes":  [ /* inferred from the issue body — grep for the bug it describes */ ],
    "artifacts":   [ /* files the issue names, or the subagent identified as the touch surface */ ],
    "remediation": { "source": "issue#<N>", "criteria": "<one-line SUMMARY for ranking — NOT the definition of done; that is the verbatim ## Acceptance block>" },
    "lanes":       { "agy_safe": [], "orchestrator_only": [ /* kernel/.tick paths, if any */ ] }
  }
  ```
  ```

  **Persist ratings to releases.db**:
  ```bash
  python3 "$HARNESS/utils/py/releases_app.py" roadmap rate --issue-num <N> \
    --rated <P>/<S>/<A>/<E> [--ovr <O>] [--force]
  ```
  ```

  **`source:` is always the tracking issue (GH-425).** It must name this repository and the
  `gh_issue` number, not merely an issue with the same number in another repository. When an
  issue originated elsewhere, retain that URL under the established free-text `related:` field
  instead; do not delete it or put it in `source:`. For example:

  ```yaml
  gh_issue: 94
  source: https://github.com/Acme/tracking-repo/issues/94
  related:
    - "https://github.com/Upstream/origin-repo/issues/2 — originating issue"
  ```

  Preflight validates `source:` against the target repository and tracking issue. `related:`
  remains context rather than a new linted schema: it preserves the cross-repo provenance while
  keeping the gate's tracking-issue check deterministic.

  For a `runtime:bash`-labeled issue, set the gate to `"XYZ_PYTHON=0 bash validate.sh"` so the
  lane verifies against the Bash path the bug actually lives on, not the Python default (again, a
  no-op outside `xyz-3-agents-swarm`, where the label is absent).

  Mark it explicitly in the doc body: *"Contract auto-drafted by /10days from the issue
  text — artifacts/lanes not yet operator-verified."* This is the one place this skill
  guesses; the report in Step 8 must surface every auto-drafted contract by name.

- **When a criterion genuinely cannot be carried as written** — unreachable in this repo,
  superseded by later work, or deliberately split across lanes — do **not** quietly rewrite the
  list. Keep the issue's wording and record the delta in a section preflight can check:

  ```markdown
  ## Acceptance — deviations from the issue

  - [dropped] <verbatim issue criterion> — reason: <why>
  - [changed] <verbatim issue criterion> -> <replacement> — reason: <why>
  - [added]   <new criterion> — reason: <why>
  ```

  Each entry needs a real `— reason:`, and the entries must reconcile the two lists **exactly**:
  an entry naming a criterion that is not actually different is rejected, so the section cannot
  become a rubber stamp. This is the only supported way to diverge; there is no env-var bypass,
  because a deviation should live in the doc where the next reader finds it.

- **Audit the guess like `start-marathon` does**: do the declared `artifacts` paths
  actually exist (or, for a new file, does the issue actually call for creating one at
  that path)? Does the set plausibly match the issue's real subject, not a generic or
  copy-pasted guess? A contract that fails this sniff test is a placeholder — its
  collision map can't be trusted at all; drop that issue back to `needs_contract` and
  exclude it from this run rather than firing on an untrustworthy guess.

- Park intake via `python3 "$HARNESS/utils/py/releases_app.py" roadmap add` (the canonical roadmap ledger since GH-169/GH-269; for legacy repos using ROADMAP.md, append a pointer line) so `$HARNESS/utils/marathon-plan.sh` discovers it in Step 5.

### 5. Build and rank the marathon file

```bash
"$HARNESS/utils/marathon-plan.sh" --deep
```

`--deep` delegates to `$HARNESS/utils/swarm-preflight.sh --dry-run` per ready item for an
authoritative freshness verdict while ranking (slower, needs network — that's fine,
`gh`/network access is already required by this point). Writes
`PROJECT/2-WORKING/MARATHON-PLAN-<today>.md` — this is "the marathon file" the
operator's snippet refers to. Read its Held/Flagged section: anything held here drops
out of the fire list in Step 6, with the reason already stated by the planner.

**`marathon-plan.sh` ranks the ENTIRE ROADMAP ledger, not just this sweep's issues —
filter its waves down to this run's candidate set and order by effective PRS score before treating anything as fireable:**
1. Intersect the plan's assigned items with this sweep's `INCLUDE` set. Drop unrelated or unselected issues.
2. Order surviving issues by **effective PRS score**:
   - **Manual overrides (`ovr`)** first — operator front-of-line pins supersede calculated arithmetic.
   - **Highest `calc` sums (`pri + sev + appeal + effort`)** next.
   - Secondary tiebreakers: highest `sev` (severity), then highest `pri` (priority).
3. Respect the planner's zone constraints (kernel ≤ 1 per wave) and wave serialization, slotting the highest-scored candidates into the earliest available wave slots.

### 6. Preflight the fire list — one issue per invocation

```bash
for N in <surviving issue numbers>; do
  "$HARNESS/utils/swarm-preflight.sh" --gh-issue "$N"
done
```

**Run it once per issue, never bundled** (`--gh-issue N --gh-issue M` in one call is a
different feature — `merge-contracts.mjs` folds every listed issue into *one* packet, so
a single invalid contract fails the *entire* bundle and stops filtering per-issue; that
is not what this step needs). No `--dry-run` — this run is going to fire, so let it
write the real packet, one per issue. Read the verdict per exit code: `0` ready · `3`
contract missing/invalid · `4` stale/already landed (drop it, propose closing the GH
issue — the fix shipped without this run knowing) · `5` not marathon-ready · `6`
blocked/missing-target · `7` ambiguous. Only exit-0 issues carry into Step 6.5. Every
non-zero drop gets one line in the Step 8 report with its exit code and reason — never
silently disappear an issue from the count.

**An `exit 5` reading `acceptance criteria diverge from issue #N` is your own Step 4 output being
rejected (GH-400), not a defect in the issue.** Preflight re-fetched the issue and found the doc's
`## Acceptance` block says something the issue does not. Fix it by going back to the doc and copying
the issue's block verbatim — or, if the difference is deliberate, by declaring it under
`## Acceptance — deviations from the issue` as Step 4 specifies. Do **not** work around it by
deleting the doc's acceptance section (a doc with none, against an issue that has one, is refused
too) and do not drop the issue from the run on these grounds. The check reports `unknown` and does
not block when it simply cannot see the issue (no `gh`, unauthenticated, offline, or an issue with
no `## Acceptance` section), so a green run offline is not evidence the criteria were verified —
the packet says which of the two it was.

### 6.5. Cross-issue artifact-overlap check — before any wave runs concurrently

`marathon-plan.sh` already groups exit-0 issues into waves by disjoint `artifacts`
sets. That grouping is only as trustworthy as the contracts feeding it, and Step 4 can
include auto-drafted ones. Before accepting a wave's concurrency as safe:

- Diff every pair of lanes slotted into the same wave: do their `artifacts` lists
  literally intersect (a bug in the planner or the contract) or does either lane's
  underlying issue body/title mention a file path that appears in the other lane's
  `artifacts`? Either signal is enough.
- Any lane pair with a hit — **serialize them**: move one to the next wave regardless
  of what the planner computed. This costs wall-clock time, not correctness; the
  planner's wave grouping is an optimization, not a safety guarantee, once an
  auto-drafted contract is in the mix.
- Log every serialization decision so Step 8 can report it — a silently-reordered wave
  is still a surprise the operator should see.

### 7. Cut the branch, commit planning artifacts, and execute — no pause (see Guardrails)

**Preconditions & Collision Predicates — verify inside the dedicated full clone workspace:**

```bash
BASE_BRANCH="${XYZ_BASE_BRANCH:-development}"

# 1. Assert not already on a marathon/* branch
CURRENT_BRANCH="$(git branch --show-current)"
[[ "$CURRENT_BRANCH" != marathon/* ]] || { echo "Fatal: already on a marathon branch ($CURRENT_BRANCH)" >&2; exit 1; }

# 2. Assert no active tick locks / claims
ACTIVE_LOCKS="$(ls .tick/locks/ 2>/dev/null || true)"
[[ -z "$ACTIVE_LOCKS" ]] || { echo "Fatal: active tick locks found in .tick/locks/" >&2; exit 1; }

# 3. Assert no foreign untracked marathon plan in PROJECT/2-WORKING
FOREIGN_UNTRACKED_PLANS="$(git status --porcelain --untracked-files=all -- PROJECT/2-WORKING 2>/dev/null | grep -E '^\?\?[[:space:]]+PROJECT/2-WORKING/MARATHON-' | grep -v "MARATHON-PLAN-${SWEEP_DATE}.md" || true)"
[[ -z "$FOREIGN_UNTRACKED_PLANS" ]] || { echo "Fatal: foreign untracked marathon plan found: $FOREIGN_UNTRACKED_PLANS" >&2; exit 1; }
```

If any check fails, stop and report which one, and do not touch the branch.

Then:

1. **Branch Cut & Planning Artifact Commit**:
   - Cut branch from canonical base: `BRANCH_NAME="${packet_suggested_branch:-marathon/10days-${SWEEP_DATE}}" && git checkout -b "$BRANCH_NAME"`.
   - Stage and commit the deliberate intake capture docs (including any `1-INBOX` moves), marathon plan, and updated roadmap ledger:
     ```bash
     git add -A -- PROJECT/1-INBOX PROJECT/2-WORKING releases.db releases.sql
     if [[ -f "ROADMAP.md" ]]; then git add ROADMAP.md; fi
     git commit -m "chore(marathon): initialize 10days marathon plan and roadmap ledger for ${SWEEP_DATE}"
     ```
   - Assert clean working tree before dispatching lane agents:
     ```bash
     [[ -z "$(git status --porcelain)" ]] || { echo "Fatal: uncommitted state remaining after plan commit" >&2; exit 1; }
     ```
   - Ensure the final PR targets `$BASE_BRANCH` (`development`), never `main`.
2. Execute per the proven **Marathon execution pattern (GH-221 builder/orchestrator split)**:
   - **Claude Code is the orchestrator and reviewer**, not a default builder. It plans waves, dispatches builder lanes, and verifies emitted artifacts / test gates.
   - **Agy CLI and Codex CLI are the default headless builders** (`--builder agy` / `--builder codex`, subscription-billed / cost-blind).
   - **Claude CLI is NOT a builder by default** — use a headless Claude CLI builder only with explicit user confirmation/cost acknowledgement.
   - Walk the MARATHON-PLAN doc's waves in order, respecting any Step 6.5 serialization:
     - Within a wave, dispatch one builder turn per lane with `isolation: "worktree"` (or in dedicated disposable sub-clones beneath the full clone) to prevent concurrent lanes from writing over each other. Respect zone caps (kernel ≤ 1 per wave).
     - Each lane agent writes only inside its contract's `artifacts` allowlist.
   - After all of a wave's lane agents return, before merging any lane's worktree
     commit(s), verify that lane's worktree base against the marathon branch's start
     commit: `git merge-base --is-ancestor <marathon-branch-start-sha> <lane-worktree-HEAD>`.
     **Confirmed live 2026-07-17 (GH-225): `isolation:"worktree"` lanes can silently
     branch from a stale historical commit instead of the marathon branch** — do not
     assume the ancestry check will pass. If it passes, fast-forward/merge as normal. If
     it fails, the worktree is based on a stale/unrelated point — **cherry-pick the
     lane's specific new commit(s) onto the marathon branch instead; never `git merge`
     the isolation branch wholesale** in that case, or it silently reintroduces every
     already-superseded file state between the stale base and the marathon branch tip.
     Merge/cherry-pick each lane **one at a time** (not concurrently) so the branch ref
     never has two writers racing it.
   - Once a lane's commit(s) are merged, remove its worktree: `git worktree remove
     <path>` (fall back to `git worktree remove --force <path>` if it still reports
     uncommitted/stray state). Do this for every lane in the wave, right alongside the
     gate check below — left as-is, a run with several parallel lanes accumulates
     orphaned worktree directories under the repo's git metadata across sessions. A
     removal failure does not stop the run: record the lane, path, and error for the
     Step 8 report and continue.
   - After a wave's merges land, run its gate (the contract's `gate`, default
     `bash validate.sh`) **before starting the next wave.** Running this gate inside the
     full clone folder ensures tests cannot contaminate the primary repo (GH-564). A red gate
     stops the run — do not advance to the next wave, do not force-merge, report it in Step 8
     and leave the branch as-is for the operator to inspect.
3. Commit per lane/wave with a message referencing the GH issue number(s) it closes.

### 8. Report

One final summary, always — even (especially) on a partial or stopped run:

- **Scan Window & Intake Counts**: N days scanned, total open issues reviewed.
- **PRS Ratings & Prioritization Table**:
  - Issue number, title, 4-axis ratings (`pri/sev/appeal/effort`), `calc` sum, `ovr` override, effective score, and ranking verdict.
  - Explicitly highlight any **manual overrides (`ovr`)** and high-scoring quick wins.
- **Exclusion Ledger**: items excluded with reasons (already-done / duplicate / not
  reproducible / not-a-work-item / held-by-preflight / held-by-planner).
- **Execution Ledger**:
  - Included and fired issues, with their issue numbers, branch, and final commit(s).
  - Full clone folder path used for execution.
  - Every **auto-drafted contract**, named individually, flagged for operator review.
  - Every **Step 6.5 serialization** — which lane pairs were pulled out of a concurrent
    wave and why, so a wave that ran slower than expected isn't a mystery.
  - Every gate result per wave (green/red) and, if red, exactly where the run stopped.
  - Every **worktree-cleanup failure** — lane, worktree path, and the `git worktree
    remove` error — if any lane's worktree failed to remove after its merge. Never
    silently ignore a leftover worktree; if none failed, say so explicitly (all
    worktrees removed cleanly).
  - Branch name, and whether it's ready for a PR or still mid-marathon.

Never mask a stopped run as a finished one — an honest partial report is the point of
this whole skill (GUIDING-PRINCIPLES.md §8: the operator decides, but only if they know
what actually happened).

## Bundled deterministic scripts

- [`scan-issues.sh`](scan-issues.sh) — Step 1, the GH window pull. No judgment calls.
- [`find-doc.sh`](find-doc.sh) — Step 2, the capture-doc lookup for one issue number. No
  judgment calls.

Both exist so the mechanical parts of this sweep run byte-identical every time instead
of being re-typed as ad hoc `gh`/`ls`/`grep` one-liners each invocation.
