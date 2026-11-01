---
name: merge-discipline
version: "1.9.0"
user-invocable: true
description: "Hard gate before merging into a protected branch: run Parts A→B→C→R→D (OpenSpec archive association, rebase/conflict pre-check, coverage preference, pr-code-review with content-matched depth via pr-review-gate (unset ≡ auto), squash decision from commit quality + tip-pin merge). Do NOT merge while an associated OpenSpec change is still active; do NOT skip on a direct \"merge MR\" command; do NOT auto-select squash when two viable strategies exist — ask with a commit-quality recommendation; a single-commit or single-permitted-strategy MR concludes without prompting; after merging, sync the local workspace onto the resolved target branch. Triggers — 「合并 tip」「merge tip」「合并纪律」「push 后合并」「archive 合入」「合并前门控」「rebase 检查」「冲突预检」「合并前 rebase」「先 archive 再 merge」「合并前 code-review」 / merge discipline, archive-before-merge, rebase pre-check, coverage gate, pr code review before merge."
dependencies:
  - pr-code-review
---

# Merge Discipline

> Internal shared skill — the single source of truth for merge-time discipline. Five parts, run in order **A → B → C → R → D**: **OpenSpec archive association gate** (Part A) + **rebase/conflict pre-check** (Part B) + **coverage gate** (Part C) + **PR code review** (Part R, strong-dep `pr-code-review`) + **squash decision & tip pinning** (Part D). Referencing workflows declare this in frontmatter `dependencies` and abort at startup if missing.

## Prerequisite skill check

On load, scan frontmatter `dependencies`. If any is missing → print the Missing Notice below and **abort** (no silent degrade).

### Missing Notice

```
⚠️ merge-discipline is missing a strong dependency and cannot run

【Missing skill(s)】
- <name>: <one-line purpose>

【Why it's needed】
merge-discipline strongly depends on:
- `pr-code-review`: Part R — multi-perspective PR review with ≥80 confidence filter before tip-pin merge

【Install】
Install each missing skill by name (preferred):
  npx skills add FuDesign2008/open-skills -g --skill <name> --yes
Example for this skill's dependency:
  npx skills add FuDesign2008/open-skills -g --skill pr-code-review --yes
Or install every open-skills skill:
  npx skills add FuDesign2008/open-skills -g --skill '*' --yes

Re-trigger merge after installing.
```

When listing multiple missing skills, print **one** `npx skills add … --skill <name> --yes` line **per** missing name (do not only show `'*'`).

## When this applies

Any merge into a protected branch (`glab mr merge` / `gh pr merge` / `git merge <target>`) — whether from a workflow's branch-closeout decision, a **direct user merge command** ("merge MR" / "合并"), or AI preparing the merge call. "Keep branch" / "continue development" do not trigger.

When hosts use `feature-branch-closeout`, that skill owns the **closeout menu**; this skill runs **only after merge is selected** (or on a direct merge command). Do not redefine the full menu here.

**Execution order when merging: Part A (archive gate) → Part B (rebase) → Part C (coverage) → Part R (PR code review) → Part D (squash decision + tip pinning) → merge.** Part A runs first so archive work is not deferred past rebase/CI. A rebase changes the source tip, forcing Parts C/R/D to re-run on the new tip.

---

## Part A — OpenSpec archive association gate

Prevents **merge-then-archive**: implementation lands on the protected branch while OpenSpec delta specs / archive still live only on a follow-up docs PR.

### Association (either hit = associated)

1. **Diff hit**: the PR or branch diff includes paths under `openspec/changes/<name>/` that are **not** under `openspec/changes/archive/`.
2. **Session hit**: a session-bound OpenSpec change name still appears as active in `openspec list` (not archived).

### Decision matrix

| State | Action |
|---|---|
| Not associated | Pass through → Part B |
| Associated and change already archived (only under `openspec/changes/archive/…`, absent from `openspec list`) | Pass through → Part B |
| Associated and change still **active** | **Block merge**. Name the change(s). Require archive (sync main specs + move to `openspec/changes/archive/`) on the **same source tip**, then re-enter merge from Part A. Do **not** run Part B/C/D or the merge command. |

### Hard rules

- Direct user merge commands **MUST** run this Part — **no implicit skip**.
- User may force-continue only with **explicit** skip 留痕 (template below); default is block.
- Do **not** recommend a separate post-merge archive MR while the change is still associated and active (see Part D Strategy B — recovery only).

### Detect (illustrative)

```bash
# Diff hit (GitHub example — adapt for platform)
gh pr diff <id> --name-only | grep -E '^openspec/changes/[^/]+/' | grep -v '^openspec/changes/archive/'

# Session hit
openspec list --json   # active names; compare to session-bound change
```

### 留痕 templates

Location: PR description and `design.md` Verification Notes (when present).

| Case | Template |
|------|----------|
| User explicit skip | `【OpenSpec archive 门控跳过】用户显式跳过，关联 change 仍为 active。时间：<ISO>。决策人：用户。change：<name>。` |
| Implicit miss (merged without gate) | `【OpenSpec archive 门控漏跑】合并已发生但 Part A 未运行。时间：<ISO>。漏跑阶段：<合并前/合并后>。` |

### Red flags

- Merging because "stage 8 already said archive later" or "we'll open a docs PR after merge".
- Skipping Part A on a direct "merge MR" while `openspec/changes/<name>/` is still in the PR diff.
- Treating Strategy B as the happy path for an open, associated MR.

---

## Part B — Rebase / conflict pre-check

Prevents the **blind-merge-into-a-moving-target** failure: by the time the user says "merge", the target (`release/*`, `main`, …) has usually moved — teammates landed their own work. Merging without checking either fails at the platform (`mergeable=false`) or silently lands behind the tip. This Part makes the AI surface that and offer to rebase, instead of the user having to remember to ask.

### Detect

```bash
git fetch origin <target-branch>
BEHIND=$(git rev-list --count HEAD..origin/<target-branch>)
BASE=$(git merge-base HEAD origin/<target-branch>)
CONFLICTS=$(git merge-tree "$BASE" HEAD origin/<target-branch> | grep -c "^changed in both")
```

`<target-branch>` = the MR/PR base (query it via your platform's CLI) or the merge target the user named.

### Decision matrix

| State | Action |
|---|---|
| `BEHIND=0` and `CONFLICTS=0` | Clean — proceed to Part C |
| `BEHIND>0` and `CONFLICTS=0` | Report "target N commits ahead; rebase applies cleanly" → wait for user confirm |
| `CONFLICTS>0` | Report "target N ahead, ~M files conflict" → wait for user confirm |

No auto-rebase without confirmation — rebase rewrites the source branch and triggers a full CI rerun; the user owns that decision.

### On confirm — execute rebase (source branch only)

The source is the user's personal fix branch (`fix/jira-fix-…`), which team policy allows to force-push. The protected target is never rewritten by this Part.

```bash
git rebase origin/<target-branch>
# On conflict: delegate to git-conflict-resolve skill (mode=rebase — per-commit resolution)
git push --force-with-lease origin <source-branch>
```

If `git-conflict-resolve` is unavailable or the user aborts, stop — leave the worktree mid-rebase (`git rebase --abort` to bail) for human resolution.

### Scope boundary — this Part does NOT wait for CI

After `--force-with-lease` push, this Part **ends**: it reports "rebased, PR updated, CI rerunning" and returns control to the workflow. CI-gating and the actual merge stay with the workflow's normal closeout (Part C → Part D → merge) — the user comes back after CI is green, same as any post-review merge. This Part is a rebase repair tool, not a merge-through-CI orchestrator.

### Loop bound

Each merge attempt triggers at most one rebase. If the target moves again while waiting for CI, the next merge attempt re-enters from Part A and re-detects — bounded, not infinite.

### Red flags

- Merging without this Part because "CI is already green" (the green is on the old tip; target moved).
- Rebasing, then claiming merge done before Part D's ancestor check passes on the new tip.

---

## Part C — Coverage gate

Part C starts on merge intent. It does **not** auto-run the analyzer by default.

### 1. Resolve project preference

Scan `AGENTS.md` then `CLAUDE.md` (first match wins) for a line matching (case-insensitive key):

`coverage-gate:\s*(always|never|ask)\b`

| Value | Behavior |
|---|---|
| *(unset)* | Treat as `ask` |
| `ask` | On **every** merge, ask the user: run coverage for this merge, or skip? **MUST NOT** auto-run |
| `always` | Run gate steps without asking (subject to analyzer availability) |
| `never` | Skip analyzer; write project-preference 留痕; proceed to Part R |

### 2. Pre-detection (only if decision is **run**)

If `test-coverage-analyzer` is available, continue to gate steps. If not found, output "gate unavailable: test-coverage-analyzer not detected", write an environment-gap留痕, and let the user decide whether to proceed with merge.

### 3. Gate steps (only if decision is **run**)

Independent Bash permission — runs the analyzer script:

1. **Construct `--base`** (try in order, stop on first hit):
   - MR/PR: `gh pr view --json baseRefName -q .baseRefName` / `glab mr view <iid> -F json | jq .target_branch` → `--base <target>` (bare branch name; the script's `validate_ref` adds `origin/`)
   - On failure / detached HEAD / no remote → omit `--base`, rely on the script's 5-level fallback; warn "no explicit base, MR may misjudge as 0-diff"
   - Multi-repo MR → run gate per-repo, each with its own `--base`; any repo failing → overall pause

2. **Call the script** (read test-coverage-analyzer SKILL.md first to confirm param contract):
   `python3 "<SKILL_DIR>/scripts/analyze_coverage.py" "<project-root>" [--base <target>]`

3. **Decision matrix**:

   | Result | 🤖 Auto | 👤 Manual |
   |---|---|---|
   | ✅ Report generated + coverage meets threshold | Continue to Part R (PR code review) | Prompt pass, wait for user re-confirm |
   | ⚠️ Coverage below threshold | Pause, output report, await user (force/add-tests/abort) | same |
   | 💥 Crash / no report / exit 1 | Treat as gate-fail, pause | same |
   | 📭 No test code / 0% pass | Present report, pause for user judgment | same |
   | 🕳️ **Should-run** but gate not run and merge happened (implicit miss) | Pause merge, rerun gate; if already merged, write miss留痕 | same |

**Should-run** = preference `always`, or preference `ask` after the user chose run. Preference `never` or user-explicit skip under `ask` are **not** implicit misses.

### 留痕 templates

Location: PR description and `design.md` Verification Notes.

| Case | Template |
|------|----------|
| User explicit skip | `【覆盖率门控跳过】用户显式跳过，未运行 test-coverage-analyzer。时间：<ISO>。决策人：用户。` |
| Project preference never | `【覆盖率门控跳过】工程偏好 coverage-gate: never。时间：<ISO>。决策人：项目配置。` |
| Env gap (skill not found) | `【覆盖率门控跳过】未检测到 test-coverage-analyzer skill，门控不可用。时间：<ISO>。决策人：系统（环境缺漏）。` |
| Implicit miss | `【覆盖率门控漏跑】合并已发生但门控未运行（应跑未跑）。时间：<ISO>。漏跑阶段：<合并前/合并后>。` |

---

## Part R — PR code review (strong dependency)

Prevents **merge-without-PR-review**: coverage/CI can be green while the diff still carries high-confidence defects that a multi-perspective, dual-axis review would catch.

### 1. Resolve `pr-review-gate` preference

Scan `AGENTS.md` then `CLAUDE.md` (first match wins) for:

`pr-review-gate:\s*(always|never|ask|non-code-light|auto)\b`

| Value | Behavior |
|---|---|
| *(unset)* | Treat as `auto` (content-matched depth — surface classification + scale/risk escalation) |
| `always` | Run `pr-code-review` at `depth=full` |
| `auto` | Content-matched depth: classify surface (§2) + scale/risk escalation (§2.5) — no escalation hit → `light`; any escalation hit → `full` (application-code included) |
| `never` | Skip `pr-code-review`; write project-preference 留痕; proceed to Part D |
| `ask` | Ask the user: full / light / skip for this merge; MUST NOT auto-pick; skip needs user-explicit skip 留痕 |
| `non-code-light` | Classify the PR surface (§2); non-application-code → `depth=light`; application-code → same scale/risk ladder as `auto` |

### 2. Classify PR surface (when needed)

When preference is `non-code-light`, `auto`, or unset (or the user chose light under `ask`), classify the open PR/MR **three-dot** changed paths using the allow/deny table in [reference.md](reference.md)「Non-application-code surface」.

- **All paths allowlisted and none denylisted** → non-application-code
- **Any denylisted path** (or mixed) → application-code

### 2.5 Scale/risk escalation

Apply **after** surface classification when preference is `auto` (or unset), or when preference is `non-code-light` **and** the surface is application-code. (`non-code-light` + non-application-code stays `light` without this table.) Any single hit forces `depth=full`.

| Signal | Source | Rule |
|---|---|---|
| Large diff | three-dot diff stats | Total changed lines > 400 **or** changed files > 20 → full |
| Breaking-change signal | PR title / description / commit messages, case-insensitive | Matches `migration`, `schema`, `breaking`, `API contract`, `deprecat` → full |
| Post-fail re-entry | Part R history on this tip | A prior Part R **fail** on the same tip, re-presented after fixes → full |
| Sensitive path/keyword | changed paths + title / description / commits vs [reference.md](reference.md)「Sensitive paths and keywords」 | Any glob or keyword match → full |

No escalation hit → `light` (including application-code). Thresholds and the sensitive table are repo-tunable constants (see reference.md「Content-matched depth ladder」).

### 3. Run or skip

1. Confirm frontmatter dependency `pr-code-review` is available when a review run is required (prerequisite check already ran at load).
2. If preference is `never` (or `ask` + user skip): write 留痕 → Part D (do not load `pr-code-review`).
3. Otherwise load `pr-code-review` with the selected `depth` (`full` or `light`) against the open PR/MR about to be merged (follow that skill — Standards∥Spec, confidence ≥80).
4. **Decision matrix:**

| Result | Action |
|---|---|
| Pass — neither axis retains ≥80 Critical/Important | Proceed to Part D |
| Fail — either axis has ≥80 Critical/Important | **Block Part D.** Do **not** treat source-tip fixes alone as unlock. Either: (1) fix on the source tip, then **mandatory** re-run Part R on the new tip (§3.5), or (2) user **explicit** skip / accept-residual 留痕. Re-enter from Part A only when Part A/B association or rebase rules require it — not as a substitute for re-review. |
| Skill ineligible skip (closed/draft/already reviewed this session) | Treat as pass for this Part only if the PR is still the merge candidate and a prior ≥80-clean dual-axis review exists on **this tip**; otherwise pause for user. A clean review of a **previous** tip after fixes does **not** count. |

### 3.5 Fail → fix → re-review until clean (round cap)

When a review **run** fails and the agent applies source-tip fixes (not an explicit skip/accept 留痕):

1. Count each `pr-code-review` invocation in this merge attempt as one **round** (the initial fail is round 1).
2. After fixes land on the tip, **re-resolve depth** (§1–2.5; post-fail re-entry → full when that signal hits) and **re-run** `pr-code-review` on the new tip before Part D.
3. **Exit to Part D** only when a round **passes** (no ≥80 Critical/Important on either axis) or the user writes explicit skip / accept-residual 留痕.
4. **Cap = 3 rounds.** If round 3 still fails: **pause** and ask the user — continue (exactly one more review round; fail → pause again) / accept residual blocking with 留痕 / abort merge. Do **not** auto-enter Part D.
5. Preference `never` / ask-skip paths that never ran Part R do **not** enter this loop.

### 留痕

| Case | Template |
|------|----------|
| User explicit skip | `【PR code-review 门控跳过】用户显式跳过 Part R（pr-code-review）。时间：<ISO>。决策人：用户。PR：<url or id>。` |
| Accept residual after round cap | `【PR code-review 残留接受】用户在 Part R 轮次封顶后接受残留 ≥80 Critical/Important。时间：<ISO>。决策人：用户。PR：<url or id>。轮次：<n>。` |
| Project preference never | `【PR code-review 门控跳过】工程偏好 pr-review-gate: never。时间：<ISO>。决策人：项目配置。` |
| Light path used | Optional note in the review comment: `pr-review-gate: <non-code-light\|auto>; surface=<non-application-code\|application-code>; scale=<ok\|escalated>; sensitive=<ok\|hit>`; `depth=<light\|full>` |

### Red flags

- Skipping Part R because “CI is green” or “coverage-gate never” (coverage skip is not a Part R skip)
- Treating unset `pr-review-gate` as a blanket depth without classification — unset ≡ `auto` (content-matched: surface + scale/risk escalation); blanket `full`/`light`/`skip` all forbidden
- Calling Claude Code `/code-review` plugin as a substitute without loading `pr-code-review`
- Collapsing Standards and Spec into one ranked list and treating “overall look fine” as Part R pass
- Treating application-code as always-`full` under `auto` or `non-code-light` (full requires an escalation hit, or preference `always`)
- Entering Part D after fixing Part R findings **without** a new dual-axis-clean review on that tip (unless explicit skip/accept-residual 留痕)

---

## Part D — Squash decision + tip pinning (after Part R passes, before merge)

Part D owns everything between review pass and the merge command: the **squash decision** (Step 0) prevents merge-strategy-by-default, and **tip pinning** (Steps 1–4) prevents the stale-tip merge race. (Postmortem: `docs/mr-merge-stale-tip-archive-miss-incident.md`.)

### Step 0 — Squash decision (mandatory, before the merge command)

Prevents **merge-strategy-by-default**: the GitLab "Squash commits when merge request is accepted" checkbox and GitHub's squash merge method must be a surfaced, user-confirmed choice — never a platform default or a silent AI pick. Prompting exists for divergent outcomes; when fewer than two viable strategies exist there is nothing to choose, so Step 0 concludes instead of asking.

1. **List the commits** on the tip about to merge (same tip Step 1 will pin):

   ```bash
   gh pr view <id> --json commits        # GitHub
   glab mr commits <id>                  # GitLab (or the MR commits API)
   ```

2. **Collapse pre-check** — if either holds, state the conclusion plus a one-line reason and skip ahead to execution (the user may still override from the stated conclusion):
   - Exactly one commit ahead of base → "single commit: no-squash" (nothing to consolidate).
   - Repo/platform policy permits only one merge method → adopt that method and note the enforced policy.

3. **Classify and recommend** (two or more commits) — apply the decision table, state the recommendation with its rationale:

   | Commit history | Recommendation |
   |---|---|
   | Atomic commits with individual value (feature / reviewable enhancement / archive as separate commits) | **No-squash** — merge commit preserves history |
   | Trivial accumulation (fixup / typo / wip / CI-retry noise, no standalone value) | **Squash** — collapse into one commit |
   | Source branch will keep receiving development | **Lean no-squash** — squash cuts the commit graph shared with the target and breeds conflicts on later merges |

4. **Ask and wait** — present the recommendation and require an explicit user choice (squash / no-squash). Never auto-select between two viable strategies: direct merge commands and auto-mode host workflows all stop here (this ask is a sub-step of the merge flow, not a mode reversion). The user's explicit choice overrides the recommendation.

5. **Execute with the chosen strategy** — the strategy flows into Step 1's merge command (`gh pr merge <id> --merge|--squash …` / `glab mr merge <id> [--squash] …`, flags per your CLI version). A platform without squash support: state the gap and merge with the available method.

### Steps 1–4 — Tip pinning

Prevents the **stale-tip merge race**: archive/fix commits pushed seconds before merge fail to enter the target because the merge fast-forwards to the pre-push tip (whose pipeline was already green), while the freshly-pushed commits stay on the source branch.

1. **Pin the merge revision.**
   ```bash
   MERGE_SHA=$(git rev-parse origin/<source-branch>)   # or the SHA returned by push
   ```
   Merge with `glab mr merge <id> --sha "$MERGE_SHA" -y` (GitLab) or `gh pr merge <id> --match-head-commit "$MERGE_SHA"` (GitHub; older docs may say `--sha` — use the flag your `gh` supports), using the merge method chosen in Step 0. A bare merge with no tip pin is forbidden.
   If the platform CLI has no tip-pin flag: wait for that tip's pipeline to pass before merging, and treat step 3 as the mandatory backstop.

2. **Do not trust an instant `Pipeline succeeded`.**
   If a new commit was pushed just before merge, an immediately-appearing `Pipeline succeeded` is almost certainly the **old** tip's result. Verify the result's sha equals the just-pushed tip, or rely on step 1's tip pin.

3. **Ancestor check after merge (mandatory).**
   ```bash
   git fetch origin <target>
   git merge-base --is-ancestor "$MERGE_SHA" origin/<target> && echo OK || echo MISSING
   ```
   MISSING → freshly-pushed commits (archive / specs sync / fixes) did not enter the target. Do **not** claim completion, do **not** proceed to Jira writeback. Open a backfill MR (cherry-pick) or pause for the user.

4. **Dual strategy & fallback.**
   - **Strategy A (default):** MR is open and mergeable; any associated OpenSpec change is already archived (or there is no association) → merge implementation + archive on the **same** tip with tip pinned (run steps 1-3).
   - **Strategy B (recovery only):** implementation MR was **already merged accidentally** and archive is still pending → open a separate docs MR for archive; list explicitly "archive pending !N" with 留痕; never pretend archive is already on the target. **MUST NOT** be recommended while the MR is still open and associated with an **active** change — that case is Part A block, not Strategy B.

### Post-merge workspace sync (after the ancestor check passes)

The merge is only half the loop — the local workspace must return to the integration line before the next task starts. Resolve the target from the MR's base metadata (`gh pr view <id> --json baseRefName` / GitLab `target_branch`), reusing the base Part B already resolved; never assume `main` or `master`, since real targets are often `develop`, `release/*`, or integration branches.

1. **Target exists locally** → check it out and fast-forward: `git checkout <target> && git pull --ff-only origin <target>`; report one sync line (branch + new tip).
2. **Target missing locally** → give the fetch command to obtain it (`git fetch origin <target>:<target>`); a missing local copy is a reported outcome, not a silent skip.
3. **Fast-forward blocked** (diverged history) → report the divergence and hand the decision to the user; do not rebase or force-update on your own.
4. Offer to delete the merged source branch (local and remote) as explicit follow-up — cleanup ownership stays with `feature-branch-closeout`.

---

## Mode lifecycle

Asking the user under `ask`, or running the analyzer after opt-in, does not by itself trigger "auto reverts to manual" (sub-step of the merge flow). Gate pause (Part A block / below-threshold / crash / should-run implicit miss / wait for ask answer / Part R fail) = merge flow interrupted, reverts to manual per existing rules. Part B rebase execution follows the same rule: a user-confirmed rebase is a sub-step of the merge flow (does not itself revert to manual); an unresolved conflict or aborted rebase interrupts the merge flow and reverts to manual.

---

## Integration guide (for referencing workflows)

- **Keep in your own body:** your stage ordering line (e.g. `archive → branch-closeout → merge-discipline(A→B→C→R→D) → merge → writeback`), a one-line pointer to this skill, and 1-2 key red-flags. Do **not** copy the Part steps inline.
- **Delegate to this skill:** all five Parts — A (archive gate), B (rebase), C (coverage), R (PR code review via `pr-code-review`), D (tip pinning).
- **Pre-merge checklist (single source):** [reference.md](reference.md)「合并前检查清单」/ "Pre-merge checklist". Referencing workflows keep **one pointer sentence** only — do **not** paste the checklist into workflow `reference.md`.
- **Missing strong deps:** abort and print per-skill `npx skills add FuDesign2008/open-skills -g --skill <name> --yes` (see Prerequisite skill check).
