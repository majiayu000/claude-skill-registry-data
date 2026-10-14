---
name: commit
description: '[Git] Use when asked to "commit", "stage and commit", "save changes", or after completing implementation tasks. Flag: --push (a.k.a. "commit and push") stages + commits + pushes to remote in one shot.'
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

## Quick Summary

**Goal:** Stage changes and create well-structured git commits following Conventional Commits format — and, when code changed, gate the commit on a user decision to verify (via `$workflow-integration-test-green`, which drives the suite to green), confirm already-verified, or explicitly skip (default: verify first). Every commit message body OPENS with a mandatory `Estimate:` line carrying the derived story points and AI man-days for that staged diff.

**Summary:** (read-this-if-nothing-else digest — purpose + ALL main steps + gates)

- **PURPOSE** — produce a commit whose message a future reader can act on WITHOUT opening the diff: conventional subject, an `Estimate:` first body line, a purpose→what→how body, and a per-area Reviewers block. Three things are computed BEFORE the message exists (reviewers, estimate, doc triage) because they must live INSIDE it.
- **STEP 0 — BYPASS MARKER.** Create `tmp/claude-temp/.commit-skill-active` before any `git add`/`git commit`, and **ALWAYS remove it afterwards** — success or failure.
- **STEP 1-2 — ANALYZE + STAGE.** `git status` / `git diff --cached` / `git diff` / `git log --oneline -5`, then stage.
- **STEP 2.5 — DOCS TRIAGE.** Staged files matching doc-impact patterns → run `$docs-update`, re-stage the doc changes.
- **STEP 2.7 — IDENTIFY REVIEWERS** (pre-commit, read-only): last author per staged file vs `HEAD`, commit author EXCLUDED, grouped BY AREA with the focus each owns.
- **STEP 2.9 — DERIVE THE ESTIMATE** via the carried `SYNC:estimation-framework` against the STAGED diff (or reuse the implemented plan/PBI/story frontmatter with `(source: <path>)`). SP is DERIVED from `likely_days`, never eyeballed; discount generated/lockfile/docs churn first.
- **STEP 3 — GENERATE MESSAGE.** Subject `type(scope): description`; body OPENS with the Estimate line, then purpose/kind → what changed → how it works, then the Reviewers block.
- **STEP 3.5 — TEST-VERIFY GATE (BLOCKING when code changed).** ask the user directly, default **verify** via `$workflow-integration-test-green`. Only an explicit **Yes — already verified** or **Skip** proceeds; NEVER choose skip on the user's behalf. If the gate mutates the staged set, **re-stage AND re-derive the estimate**.
- **STEP 4 — COMMIT** with the HEREDOC form (subject → blank → Estimate → body → Reviewers → footer).
- **STEP 5 — VERIFY** via `git status` + `git log`; confirm the first body line IS the Estimate line, then re-present the reviewer assignment.
- **STEP 6 — REFRESH THE CODE GRAPH (post-commit, BACKGROUND, non-blocking).** Only when `.code-graph/` exists: fire `$graph-build --scope=sync` in the background so the commit that just moved HEAD is re-parsed AND the graph's `last_synced_commit` advances with it. NEVER blocks or gates the commit; a failure is reported, never retried inline.
- **FLAG** — `--push` (a.k.a. "commit and push") stages + commits + pushes via `git-manager`. Without it: **STOP after the commit**; NEVER push unprompted.

**Workflow:**

1. **Analyze Changes** — Run git status/diff to understand staged and unstaged changes
2. **Stage Changes** — Add relevant files (specific or all)
3. **Identify Reviewers** — from git history, list relevant reviewers (last author per touched file vs `HEAD`, excluding the commit author) and the area each must focus on — computed BEFORE the commit so the block can be embedded in the message body
4. **Derive Estimate** — Apply the carried `SYNC:estimation-framework` to the staged diff (or reuse the frontmatter of the plan/PBI/story this commit implements) to derive `story_points` + `man_days_ai` — computed BEFORE the message so the numbers can head the body
5. **Generate Message** — Detect type (feat/fix/refactor/etc.), extract scope from paths, write subject, open the body with the **Estimate** line from step 4, add a detailed body structured as **purpose/kind → what changed → how it works**, and append the **Reviewers** block from step 3
6. **Test-Verify Gate** — When staged changes include code that might need tests, ask the user (ask the user directly, default **verify**) to verify via `$workflow-integration-test-green`, confirm **Yes — already verified**, or explicitly **Skip**. Default = verify first, and verify means drive the suite to green, not merely report it
7. **Commit** — Create commit with HEREDOC (title + Estimate line + detailed summary + Reviewers block + attribution footer)
8. **Verify** — Confirm with git status and git log

**Key Rules:**

- **Stamp the estimate on the FIRST body line** — every commit message opens its body with `Estimate: <n> SP | man_days_ai: <x>d | man_days_traditional: <y>d`. Story points and AI man-days are MANDATORY and DERIVED bottom-up per the carried `SYNC:estimation-framework` (or reused from the plan/PBI/story frontmatter this commit implements); the number describes THIS staged diff only
- Write a detailed body — **purpose/kind → what changed → how it works** — so the next human reading `git log`/`git blame` understands the change without opening the diff. As detailed as the change needs (wrap ~72 chars); no title-only commits for non-trivial changes
- Embed a **Reviewers** block in the commit message — the per-area reviewers (last author per touched file vs `HEAD`, commit author excluded) — computed BEFORE committing so it lives in the message body, not just as a side report
- When staged changes include code that might need tests, **gate the commit on test verification** — ask the user to verify via `$workflow-integration-test-green` (default), confirm already-verified, or explicitly skip; only an explicit **Yes** or **Skip** proceeds straight to commit, and the agent NEVER chooses skip on the user's behalf
- Stop after the commit; push only when the user explicitly requests it (or passes `--push` / says "commit and push" → stage + commit + push via `git-manager`)
- Never commit secrets, credentials, or .env files
- Never use `--amend` or `--no-verify` unless explicitly requested
- Include `Generated with [Claude Code]` attribution footer

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Git Commit Skill

Stage changes and create well-structured git commits following Conventional Commits format.

## IMPORTANT: Bypass git-commit-block Hook

Before running any `git add` or `git commit` commands, create the marker file to bypass the `git-commit-block` hook:

```bash
PROJ=$(git rev-parse --show-toplevel) && mkdir -p "$PROJ/tmp/claude-temp" && touch "$PROJ/tmp/claude-temp/.commit-skill-active"
```

After committing (success or failure), **always** clean up the marker:

```bash
rm -f "$(git rev-parse --show-toplevel)/tmp/claude-temp/.commit-skill-active"
```

## Workflow

### Step 1: Analyze Changes

```bash
# Check current status (never use -uall flag)
git status

# See staged changes
git diff --cached

# See unstaged changes
git diff

# Check recent commit style
git log --oneline -5
```

### Step 2: Stage Changes

```bash
# Stage all changes
git add .

# Or stage specific files
git add <file-path>
```

### Step 2.5: Docs-Update Triage

Before committing, check if staged files impact documentation:

1. Run `git diff --name-only --cached` to list staged files
2. Check if any staged file matches doc-impact patterns (resolve the concrete backend/frontend source paths from the project's structure reference / `docs/project-config.json`):
    - changes under the backend service source paths (per project config) → may impact `docs/specs/`
    - `.claude/skills/**` → may impact `.claude/docs/skills/`
    - `.claude/hooks/**` → may impact `.claude/docs/hooks/`
    - `.claude/workflows.json` → may impact `CLAUDE.md` workflow table
    - changes under the frontend app source paths (per project config) → may impact frontend pattern docs
3. If matches found: invoke `$docs-update` skill, then re-stage any doc changes with `git add`
4. If no matches: skip (log "No doc-impacting files staged")

> `$docs-update`'s Phase 1 already runs `$prompt-enhance <doc>` on every `docs/project-reference/**` doc it PATCHES (see `docs-update` Step 1.3), keeping the doc concise yet AI-valuable before commit re-stages it — do not invoke `$prompt-enhance` again here.

### Step 2.7: Identify Reviewers (pre-commit — feeds the message)

Runs **BEFORE** the commit so the result can be embedded in the commit message body (see Step 3). Read-only (git log/blame only) — it NEVER blocks the commit and never messages anyone.

For each **staged** file, find the **LAST author who touched it** (against `HEAD`, the soon-to-be parent) — that author is the natural reviewer for the area.

Rules:

- **EXCLUDE the commit author** from the "ask to review" list (you don't ask yourself to review) — but still surface files where the author is the only prior toucher as **author-owned, no external reviewer**.
- **Brand-new files (no prior history)** → mark `NEW FILE — reviewer = owner of its source/sibling file`.
- **GROUP reviewers by change AREA** (which feature/subsystem each owns) and state WHICH AREA each must focus on — not a flat name list.
- Fetch each reviewer's email for tagging.

Collect the raw last-author-per-staged-file data:

```bash
# Staged files in this pending commit
git diff --cached --name-only \
  | while read -r f; do
      author=$(git log -1 --format='%an' HEAD -- "$f" 2>/dev/null)
      email=$(git log -1 --format='%ae' HEAD -- "$f" 2>/dev/null)
      date=$(git log -1 --format='%ad' --date=short HEAD -- "$f" 2>/dev/null)
      [ -z "$author" ] && author="(NEW FILE — reviewer = source/sibling owner)" && date="-"
      printf '%s\t%s\t%s\t%s\n' "$author" "$email" "$date" "$f"
    done
```

Then: collapse by author, map each author's files to the change area, drop the commit author, and render the **Reviewers** block to embed in the commit message (Step 3) and to present to the user:

| Reviewer | Email | Focus area | Files |
| -------- | ----- | ---------- | ----- |

Follow the table with a short **recommended review assignment by feature** list (area → reviewer). The skill does NOT auto-message anyone — this is the user's deliverable.

### Step 2.9: Derive the Estimate (pre-commit — feeds the message)

Runs **BEFORE** the commit so `story_points` and `man_days_ai` can head the message body (Step 3). Apply the **`SYNC:estimation-framework`** block this skill carries (see below) to the **OBSERVED staged scope** — post-hoc, with full diff visibility.

**Source of the numbers — prefer an approved artifact over a fresh guess:**

| Situation                                                                          | Source of `story_points` / `man_days_ai`                                                  |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Commit implements a plan / PBI / story whose frontmatter already carries estimates | REUSE its `story_points` + `man_days_ai`; append `(source: <path>)` to the Estimate line  |
| Commit is a PARTIAL slice of such an artifact                                      | Derive the slice bottom-up — NEVER copy the whole artifact's number onto a partial commit |
| No estimate artifact exists                                                        | Derive bottom-up from the staged diff per the framework                                   |

**Derivation (bottom-up — SP is DERIVED, never eyeballed):**

1. **Blast-radius pass** on `git diff --cached --stat` — touched areas, complex files (>500 LOC / central / multi-handler), downstream consumers, shared/common code.
2. Sum the **Reuse-vs-Create** tiers across UI + backend + tests → `bottom_up_hours`.
3. `likely_days = ceil(bottom_up_hours / 6) × productivity_factor`.
4. `story_points` = closest **SP→Days** bucket. Disagreement >50% → trust bottom-up and downgrade SP.
5. `man_days_ai` = the AI likely column for that SP (1≈0.25d · 2≈0.35d · 3≈0.65d · 5≈1.0d · 8≈1.5d · 13≈2.0d), reconciled against the bottom-up result; it already includes the 30% review overhead.
6. `man_days_traditional` = the no-AI likely column (1≈0.5d · 2≈1d · 3≈2d · 5≈4d · 8≈6d · 13≈10d), same reconciliation.

**Anti-inflation (discount BEFORE estimating — same guardrail `$git-developer-performance` applies):** generated code, lockfiles, ORM/designer snapshots, i18n re-sorting, bulk reformatting, and pure docs/spec churn earn **no** story points. A 4 000-line lockfile bump is 1 SP, not 8.

**Scope of the number:** the estimate describes **THIS commit's staged diff only** — not the branch, not the whole feature it belongs to. A `--push` run does not change this.

> **Never block on the estimate.** It is derived from evidence already on disk (the staged diff), so it never asks the user and never gates the commit. If the diff is genuinely unestimable (e.g. a pure merge commit with no resolved content), emit `Estimate: 0 SP | man_days_ai: 0d — integration only, no authored change` rather than omitting the line.

### Step 3: Generate Commit Message

Analyze staged changes and generate message following **Conventional Commits**:

```
<type>(<scope>): <subject>

Estimate: <story_points> SP | man_days_ai: <x>d | man_days_traditional: <y>d

<detailed summary of changes>

Reviewers:
- <area>: <Reviewer Name> <email> — focus on <what they own>
```

#### Type Detection

| Change Pattern          | Type       |
| ----------------------- | ---------- |
| New file/feature        | `feat`     |
| Bug fix, error handling | `fix`      |
| Code restructure        | `refactor` |
| Documentation only      | `docs`     |
| Tests only              | `test`     |
| Dependencies, config    | `chore`    |
| Performance improvement | `perf`     |
| Formatting only         | `style`    |

#### Scope Rules

Extract from file paths:

- `{configured-source-root}/auth/` → `auth`
- `.claude/skills/` → `claude-skills`
- `libs/{shared-lib}/` → `{shared-lib}`
- Multiple unrelated areas → omit scope

#### Subject Rules

- Imperative mood ("add" not "added")
- Lowercase start
- No period at end
- Max 50 characters

#### Estimate Line (MANDATORY — the FIRST line of the body)

```
Estimate: <story_points> SP | man_days_ai: <x>d | man_days_traditional: <y>d
```

- Placed **immediately after the blank line that follows the subject** — above purpose/what/how. NEVER in the footer, NEVER folded into the subject (the subject stays imperative, lowercase, ≤50 chars per Conventional Commits), NEVER omitted.
- `story_points` — Fibonacci `1 | 2 | 3 | 5 | 8 | 13 | 21`, DERIVED per Step 2.9. **Required.** `0` is the ONE value outside that set, reserved for the unestimable case Step 2.9 names (a pure merge/integration commit with no authored content) — NEVER as a rounding-down of real work.
- `man_days_ai` — AI-assisted man-days for this staged diff (Claude Code + project context, review overhead included). **Required.**
- `man_days_traditional` — the no-AI baseline (3–5yr dev, 6 productive hrs/day). **Recommended** — include it whenever derived — why: alone, `man_days_ai` is an absolute figure nobody can calibrate, while the pair makes the AI leverage on THIS diff readable straight from `git log`. Written for a human reader: `$git-developer-performance` derives its own numbers from the diff rather than reading this line (its `git log` format stops at `%s` — `.claude/skills/git-developer-performance/scripts/git-developer-performance.cjs:290`), so the pair earns its place by what a person reads, not by what a tool consumes.
- **Ranges** are allowed and preferred once `likely_days ≥3`: `man_days_ai: 1.0-1.5d | man_days_traditional: 4-6d`.
- Append ` (source: <path>)` when the numbers were REUSED from a plan/PBI/story frontmatter instead of derived from the diff.
- SP ≥13 on a single commit → the commit is doing too much; say so in the body ("SHOULD have been split") rather than quietly shipping the number.

#### Body Rules (MANDATORY) — write so a human understands fastest

> Body is the deliverable. Optimize for the next person running `git log` / `git blame` — they understand the change **without opening the diff**. As detailed as the change needs; no artificial brevity limit — wrap ~72 chars, stop once nothing new said. Title-only commit FORBIDDEN for any non-trivial change. — why: the diff shows WHAT; the body must carry WHY + HOW, which the diff cannot.

Three parts (omit one only when genuinely empty):

1. **Purpose / kind** — name the kind AND why it exists: feature · bug fix (state the symptom removed) · enhancement · refactor (state behaviour-preserving) · perf · security · chore. 1–2 sentences answering _"what problem does this solve?"_.
2. **What changed** — concrete edits grouped by **behaviour**, never by file. Each bullet specific — NEVER "update code", "fix stuff", "minor fixes".
3. **How it works / why this way** — the part reviewers need: mechanism, key logic, invariants relied on, edge cases preserved, and any non-obvious decision ("did X instead of obvious Y because Z"). Focus the non-obvious; NEVER narrate boilerplate. Ordering/timing/security invariant or subtle failure mode → call it out explicitly.

> **Teach-the-reader mindset (from the `understand` skill):** cover BOTH high-level motivation (why it matters) AND low-level logic (business rules, edge cases). Surface what a reader would NOT guess from the diff — write the explanation you would want to receive.

**Detail dial — scale body to the change:**

| Change size                         | Body depth                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Trivial (typo, rename, formatting)  | Purpose line + 1 bullet; skip "how it works"                                                                        |
| Normal (feature/fix, single area)   | Purpose + 2–5 "what" bullets + a short "how it works"                                                               |
| Complex (cross-cutting, subtle bug) | Purpose + grouped "what" + a full "how it works" that spells out the key invariant / edge case / why-this-over-that |

### Step 3.5: Test-Verify Gate (blocking — only when code changed)

Decide whether the staged changes carry **code that might need tests** — why: this gate is the only thing standing between an untested behaviour change and permanent history.

**Trigger detection** — run `git diff --cached --name-only` and classify the staged files:

- **Code that might need tests** → any change to production/source code: backend service source, frontend app source, shared libraries, scripts, hooks (`.cjs`), or other executable logic (resolve concrete source roots from `docs/project-config.json` / the project structure reference).
- **NOT a trigger (skip the gate)** → the staged set is _only_ docs (`docs/**`, `*.md`), specs (`docs/specs/**`), test-spec/config text, changelog, or other non-executable content with no source-code change.

**If the gate is NOT triggered:** log `Test-Verify Gate: skipped (no code changes staged)` and continue to Step 4.

**If the gate IS triggered:** STOP and ask the user with ask the user directly (default option is **No**):

> Header: `Test verify`
> Question: `Staged code changes may need tests. Verify before committing, or skip?`
> Options (in order — first is the default):
>
> 1. `Verify now — run $workflow-integration-test-green` (Recommended) — do NOT commit yet; activate the `workflow-integration-test-green` workflow, which verifies the suite AND drives any failure to green (verify → adjudicate → fix → review → re-verify) before returning. Proceed to Step 4 only once the whole suite is green; if it escalates instead of converging, surface that and stop (no commit).
> 2. `Yes — already verified` — the user confirms the integration tests were run and passed; proceed directly to Step 4 (Commit).
> 3. `Skip — commit without verifying` — the user's explicit, recorded decision to commit unverified code; proceed to Step 4 and note `Test-Verify Gate: skipped by user` in the response (never in the commit message).

Rules:

- **Default is option 1 (verify).** If the user does not actively choose "Yes" or "Skip", treat it as verify-first — never commit unverified code on assumption.
- **Verify routes to `workflow-integration-test-green`, not to a bare verify run** — why: a bare `integration-test-verify` only reports the failures, leaving the user to hand-carry each one; the workflow owns the converge-to-green loop, so choosing "verify" actually clears the suite instead of just describing it.
- **Yes is an explicit user assertion** that the integration tests were run and passed; honour it and commit.
- **Skip is the user's call, and it is theirs alone to make.** Offer it, never recommend it, and NEVER select it yourself — why: an agent that can skip its own gate has no gate.
- Re-run this gate only once per commit; after a `verify → green`, proceed to commit without re-asking.
- **If the verify branch changed ANY file, re-stage and RE-DERIVE before Step 4.** Option 1 can land test or source fixes AFTER Step 2.9 already ran, so the diff the estimate described is no longer the diff being committed. Mirror Step 2.5: re-stage the new changes with `git add`, then re-run Step 2.9 over the updated `git diff --cached` and put the fresh numbers in the message. Options 2 and 3 mutate nothing, so the original Step 2.9 numbers stand.
- This gate is independent of `--push`: it runs before the commit in every mode.

### Step 4: Commit

Use HEREDOC for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject

Estimate: 3 SP | man_days_ai: 0.65d | man_days_traditional: 2d

- summarize key change 1 with intent
- summarize key change 2 with impact

Reviewers:
- <area>: Reviewer Name <reviewer@email> — focus on <what they own>

Generated by AI
EOF
)"
```

> The **Estimate** line comes from Step 2.9 — re-derived after Step 3.5 if that gate changed the staged set — and is ALWAYS the first line of the body.
> The **Reviewers** block comes from Step 2.7 (last author per staged file vs `HEAD`, commit author excluded, grouped by area). Omit the block only when every staged file is brand-new or author-owned with no external reviewer — in that case state `Reviewers: none (author-owned / new files)`.

### Step 5: Verify

```bash
git status
git log -1
```

Confirm the committed body's FIRST line IS the **Estimate** line from Step 2.9 (`Estimate: <n> SP | man_days_ai: <x>d …`) — missing → the message is non-conformant; re-derive and record it, NEVER leave it out. Then confirm the body carries the **Reviewers** block from Step 2.7 (or the explicit `Reviewers: none (author-owned / new files)` line). Re-present the per-area reviewer assignment to the user as the final deliverable — why: they need it to request the right reviewers on the resulting PR.

### Step 6: Refresh Code Graph (post-commit — background, non-blocking)

**Skip entirely (silently) when `.code-graph/` does not exist** — the project has no knowledge graph and there is nothing to refresh.

When it does exist, fire `$graph-build --scope=sync` **in the background** immediately after Step 5 verifies the commit — one Bash call with `run_in_background: true`, so the commit never waits on it:

```bash
if [ -d ".code-graph" ]; then python .claude/scripts/code_graph sync --json; fi
```

- **Why after the commit, not before:** a commit MOVES `HEAD`. `sync` diffs the graph's stored `last_synced_commit` against the current `HEAD`, so running it AFTER `git commit` re-parses exactly the files this commit introduced. Run it before and `HEAD` has not moved yet, so there is nothing for it to see.
- **Why `sync` and not `update`:** `sync` is the HEAD-movement verb — it advances the stored `last_synced_commit` as well as the nodes. `update` only re-parses the working tree and leaves that bookkeeping pointing at the PRE-commit HEAD, which then reads as stale to `graph-prompt-sync` and forces a redundant re-sync on the next prompt. Committing is a HEAD move, so it takes the HEAD-move verb.
- **Why background:** the `graph-auto-update` PostToolUse hook only fires on `Edit|Write|MultiEdit`, so a commit leaves the graph's node set stale for any file the session did not itself edit (merges, checkouts, externally-changed files) — but graph freshness is an accelerator, NEVER a commit gate. It MUST NOT block, delay, or fail the commit.
- **Report** the background result briefly when it returns (files synced/added/deleted, or `up_to_date`). If it errors (Python/deps missing, lock held by a concurrent update), state the error in one line and stop — NEVER retry inline and NEVER treat it as a commit failure.

> **Safety net, not the only net.** If this step is skipped or fails, the `graph-prompt-sync` UserPromptSubmit hook detects the moved HEAD on the next prompt and syncs then. Step 6 exists so the graph is already current for the rest of THIS session, not because the commit is the only chance to catch it.

> The `--push` path pushes first, then refreshes the graph — the push is the user-visible operation and must not wait on graph work either.

## Examples

```
feat(order): add warehouse filter to list

Estimate: 3 SP | man_days_ai: 0.65d | man_days_traditional: 2d

- add warehouse query parameter in order list endpoint
- wire frontend filter control to request payload
- update tests for filtered and unfiltered list behavior

Reviewers:
- order backend: Jane Doe <jane@acme.com> — focus on the list endpoint query change
- order UI: Bob Lee <bob@acme.com> — focus on the filter control wiring

Generated by AI

fix(validation): handle empty date range

Estimate: 1 SP | man_days_ai: 0.25d | man_days_traditional: 0.5d

- guard null/empty date inputs before parsing
- return validation message instead of throwing format exception

Reviewers: none (author-owned / new files)

Generated by AI
```

## Critical Rules

- **ALWAYS stage all unstaged changes** before committing — run `git add .` (or specific files) so nothing is left behind
- **Test-Verify Gate (Step 3.5):** when staged changes include code that might need tests, ask the user to verify via `$workflow-integration-test-green` (default — it converges the suite to green), confirm already-verified, or explicitly skip; only an explicit **Yes** or user-chosen **Skip** commits without verifying, and the agent NEVER picks skip itself. Bypass the gate entirely only when the staged set is docs/specs/config with no source-code change
- **Estimate line is MANDATORY and comes FIRST in the body** — `Estimate: <n> SP | man_days_ai: <x>d | man_days_traditional: <y>d`, derived bottom-up per the carried `SYNC:estimation-framework` against the STAGED diff (Step 2.9), or reused from the implemented plan/PBI/story frontmatter with `(source: <path>)`. Story points and AI man-days are required; discount generated/lockfile/docs churn before estimating
- **Stop after the commit; push** to remote only when the user explicitly requests it
- **Refresh the code graph after committing (Step 6)** — when `.code-graph/` exists, fire `$graph-build --scope=sync` in the BACKGROUND (`run_in_background: true`) so the commit that moved HEAD is re-parsed and `last_synced_commit` advances with it; skip silently when the dir is absent. Non-blocking by design: it NEVER gates, delays, or fails the commit
- **Review staged changes** before committing
- **Never commit** secrets, credentials, or .env files
- **Never use** `git commit --amend` unless explicitly requested AND the commit was created in this session AND not yet pushed
- **Never skip** hooks with `--no-verify` unless explicitly requested
- Commit message MUST include a Conventional Commit title AND a detailed body — **purpose/kind → what changed → how it works**. As detailed as the change needs (wrap ~72 chars); title-only commit FORBIDDEN for non-trivial changes
- Optimize body for the next human reading `git log` / `git blame` — surface the non-obvious (key logic, invariants, edge cases, why-this-over-that), not just a list of touched files
- Include attribution footer: `Generated by AI`
- **Embed reviewers in the commit message** — BEFORE committing (Step 2.7), surface the last author per staged file vs `HEAD` (exclude the commit author), grouped by focus area, and write it as a `Reviewers:` block in the message body so the right reviewers travel with the commit/PR. Read-only; never blocks the commit.

## Push & PR Operations

**Arg `--push` (a.k.a. "commit and push"):** stage + commit + push in one shot — spawn `git-manager` immediately after committing. The former standalone stage-commit-push entry point, folded in; it adds no logic beyond the push delegation below.

This skill handles **commit** by default. Push-to-remote and PR creation delegate to the `git-manager` sub-agent (`agent_type: "git-manager"`), which enforces conventional-commit validation, prevents `--no-verify` bypass, and creates PRs with structured summaries.

Spawn `git-manager` after committing when the user says "push", "create PR", or "open PR".

## Sub-Agent Type Override

> **MANDATORY:** Push and PR operations spawn `git-manager` sub-agent (`agent_type: "git-manager"`), NOT the main agent.
> **Rationale:** `git-manager` enforces conventional commits, prevents hook bypasses, and handles PR creation with structured summaries.

## Related

- `changelog`
- `branch-comparison`

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

<!-- SYNC:sub-agent-selection -->

> **Sub-Agent Selection** — Full routing contract: `.claude/skills/shared/sub-agent-selection-guide.md`
> **Rule:** Route specialized domains (architecture, security, performance, DB, E2E, integration-test, git) to the matching specialist agent (see guide above) — NEVER use `code-reviewer` for these. — why: `code-reviewer` lacks each domain's checklist, so specialized issues slip through.

<!-- /SYNC:sub-agent-selection -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:estimation-framework -->

> **Estimation Framework** — Bottom-up first; SP DERIVED; output min-max range when likely ≥3d. Stack-agnostic. Baseline: 3-5yr dev, 6 productive hrs/day. AI estimate assumes Claude Code + project context.
>
> **Method:**
>
> 1. **Blast Radius pass** (below) — drives code AND test cost
> 2. Decompose phases → hours/phase → `bottom_up_hours = Σ phase_hours`
> 3. `likely_days = ceil(bottom_up_hours / 6) × productivity_factor`
> 4. Sum **Risk Margin** (base + add-ons) → `max_days = likely_days × (1 + margin)`
> 5. `min_days = likely_days × 0.9`
> 6. Output as range when `likely_days ≥3`; single point allowed `<3` (still record margin)
> 7. `man_days_ai` = same range × AI speedup
> 8. `story_points` DERIVED from `likely_days` via SP-Days — NEVER driver. Disagreement >50% → trust bottom-up
>
> **Productivity factor:** 0.8 strong scaffolding+codegen+AI hooks · 1.0 mature default · 1.2 weak patterns · 1.5 greenfield
>
> **Cost Driver Heuristic (apply BEFORE work-type row):**
>
> - **UI dominates** in CRUD/business apps — 1.5-3x backend (states, validation, responsive, a11y, polish)
> - **Backend dominates ONLY:** multi-aggregate invariants, cross-service contracts, schema migrations, heavy query/perf, new event flows
>
> **Reuse-vs-Create axis (PRIMARY lever, per layer):**
>
> | UI tier                                      | Cost     |
> | -------------------------------------------- | -------- |
> | Reuse component on existing screen           | 0.1-0.3d |
> | Add control/column to existing screen        | 0.3-0.8d |
> | Compose components into NEW screen           | 1-2d     |
> | NEW screen, custom layout/states/validation  | 2-4d     |
> | NEW shared/common component (themed, tested) | 3-6d+    |
>
> | Backend tier                                         | Cost      |
> | ---------------------------------------------------- | --------- |
> | Reuse query/handler from new place                   | 0.1-0.3d  |
> | Small update existing handler/entity                 | 0.3-0.8d  |
> | NEW query on existing repo/model                     | 0.5-1d    |
> | NEW command/handler on existing aggregate (additive) | 1-2d      |
> | NEW aggregate/entity (repo, validation, events)      | 2-4d      |
> | NEW cross-service contract OR schema migration       | 2-4d each |
> | Multi-aggregate invariant / heavy domain rule        | 3-5d      |
>
> **Rule:** Sum tiers across UI+backend+tests, apply productivity factor. Reuse short-circuits tiers — call out.
>
> **Test-Scope drivers (compute test_count EXPLICITLY — "+tests" hand-wave is #1 failure):**
>
> | Driver                            | Count                                                  |
> | --------------------------------- | ------------------------------------------------------ |
> | Happy-path journeys               | 1 per story / AC main flow                             |
> | State-machine transitions         | reachable transitions × allowed actors                 |
> | Multi-entity state combos         | state(A) × state(B) — REACHABLE only, not Cartesian    |
> | Authorization matrix              | (owner, non-owner, elevated, unauth) × each mutation   |
> | Validation rules                  | 1 per required field / boundary / format / cross-field |
> | UI states (per new screen/dialog) | happy, loading, empty, error, partial — present only   |
> | Negative paths / invariants       | 1 per violatable business rule                         |
>
> | Test tier (Trad, incl. setup+assert+flake) | Cost     |
> | ------------------------------------------ | -------- |
> | 1-5 cases, fixtures reused                 | 0.3-0.5d |
> | 6-12 cases, 1 new fixture                  | 0.5-1d   |
> | 13-25 cases, multi-entity setup            | 1-2d     |
> | 26-50 cases OR new state-machine coverage  | 2-3d     |
> | >50 cases OR full E2E journey              | 3-5d     |
>
> **Test multipliers:** new fixture/seed harness +0.5d · cross-service/bus assertion +0.3d each · UI E2E ×1.5 · each new role +1-2 cases
>
> **Blast Radius (mandatory pre-pass — affects code AND test):**
>
> 1. Files/components directly modified — count
> 2. Of those, "complex" (>500 LOC, multi-handler, central, frequently-modified) — count
> 3. Downstream consumers (callers, event subscribers, cross-service) — list
> 4. Shared/common code touched (multi-app blast) — yes/no
> 5. Regression scope — areas needing re-test
>
> **Rule:** Complex touch → add `risk_factors`. Each downstream consumer → +1-3 regression cases. Blast >5 areas OR >2 complex → re-evaluate SPLIT before estimating.
>
> **Risk Margin (drives max bound):**
>
> | likely_days         | Base margin                     |
> | ------------------- | ------------------------------- |
> | <1d trivial         | +10%                            |
> | 1-2d small additive | +20%                            |
> | 3-4d real feature   | +35%                            |
> | 5-7d large          | +50%                            |
> | 8-10d very large    | +75%                            |
> | >10d                | +100% AND **flag SHOULD SPLIT** |
>
> **Risk-factor add-ons (additive — enumerate in `risk_factors`):**
>
> | Factor                                                                | +margin |
> | --------------------------------------------------------------------- | ------- |
> | `touches-complex-existing-feature` (>500 LOC, multi-handler, central) | +20%    |
> | `cross-service-contract` change                                       | +25%    |
> | `schema-migration-on-populated-data`                                  | +25%    |
> | `new-tech-or-unfamiliar-pattern`                                      | +30%    |
> | `regression-fan-out` (≥3 downstream areas re-test)                    | +20%    |
> | `performance-or-latency-critical`                                     | +20%    |
> | `concurrency-race-event-ordering`                                     | +25%    |
> | `shared-common-code` (multi-consumer/multi-app)                       | +25%    |
> | `unclear-requirements-or-design`                                      | +30%    |
>
> **Collapse rule:** total margin >100% → STOP, split (padding past 2x is dishonesty). Margin <15% on `likely_days ≥5` → under-estimated, widen.
>
> **Work-Type Caps (hard ceilings on `likely_days`):**
> | Work type | Max SP | Max likely |
> | --- | --- | --- |
> | Single field / config flag / style fix | 1 | 0.5d |
> | Add property to existing model + bind to existing UI | 2 | 1d |
> | **Additive endpoint + minor UI control** (button/menu/column), reuses fixtures | **3** | **2-3d** |
> | Additive endpoint + **NEW UI surface** OR additive multi-layer + new domain rule + 2+ test files | 5 | 3-5d |
> | NEW model/aggregate OR migration OR cross-module contract OR heavy test (>1.5d) OR NEW UI + non-trivial backend | 8 | 5-7d |
> | NEW UI surface + (NEW aggregate OR migration OR cross-service contract) | 13 | SHOULD split |
> | Cross-service contract + migration combined | 13 | SHOULD split |
> | Beyond | 21 | MUST split |
>
> **SP→Days (validation only):** 1=0.5d/0.25d · 2=1d/0.35d · 3=2d/0.65d · 5=4d/1.0d · 8=6d/1.5d · 13=10d/2.0d (Trad/AI likely)
> **AI speedup:** SP 1≈2x · 2-3≈3x · 5-8≈4x · 13+≈5x. AI cost = `(code_gen × 1.3) + (test_gen × 1.3)` (30% review overhead).
>
> **MANDATORY frontmatter:**
>
> ```yaml
> story_points: <n>
> complexity: low | medium | high | critical
> man_days_traditional: '<min>-<max>d' # range when likely ≥3d; '<N>d' when <3d
> man_days_ai: '<min>-<max>d'
> risk_margin_pct: <n> # base + add-ons
> risk_factors: [touches-complex-existing-feature, regression-fan-out] # closed-list from add-ons; [] if none
> blast_radius:
>     touched_areas: <n>
>     complex_touched: <n>
>     downstream_consumers: [list or count]
>     shared_common_code: yes | no
> estimate_scope_included: [code, integration-tests, frontend, i18n, docs]
> estimate_scope_excluded: [unit-tests, e2e, perf, deployment, code-review-rounds]
> estimate_reasoning: |
>     5-7 lines covering:
>     (a) UI tier — row applied
>     (b) Backend tier — row applied
>     (c) Test scope — case breakdown by driver, file count, fixtures, tier row
>     (d) Cost driver — dominant tier + why
>     (e) Blast radius — touched, complex, regression scope
>     (f) Risk factors — list driving margin; why not larger/smaller
>     Example: "UI: compose Form/Table/Dialog → NEW screen (~1.5d). Backend: NEW command on existing aggregate,
>     reuses validation+repo (~1d). Tests: 4 transitions × 2 actors + 3 validation + 2 UI states = 13 cases,
>     1 new fixture → tier 13-25 ~1.5d. Driver: UI composition + new states. Blast: 4 areas, 1 complex.
>     Risk: base 35% + touches-complex +20% = 55% → max 3.9d → range 2.5-4d."
> ```
>
> **Sanity self-check:**
>
> - `likely_days ≥3d` and single-point? → reject, must be range
> - Margin <15% on `likely_days ≥5d`? → under-estimated, widen
> - Margin >100%? → STOP, split instead of buffer
> - Complex existing feature touched, no regression budget in `(c)`? → reject
> - Blast `>5` areas OR `>2` complex, no split discussion? → reject
> - Purely additive on existing model AND existing UI? → cap SP 3 unless tests >1.5d
> - NEW UI surface (page/complex form/dashboard)? → SP 5+ even if backend one endpoint
> - Backend cross-service / migration / multi-aggregate? → SP 8+ regardless of UI
> - `bottom_up_hours / 6` vs SP-Days disagreement >50%? → trust bottom-up, downgrade SP
> - Without tests, SP drops ≥1 bucket? → tests dominate; state explicitly
> - Reasoning called out UI vs backend vs blast vs risk factors? → if missing, add

<!-- /SYNC:estimation-framework -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:estimation-framework:reminder -->

- **MANDATORY MUST ATTENTION** estimation: bottom-up phase hours drive `man_days_traditional` (`Σh/6 × productivity_factor`); SP DERIVED. UI cost usually dominates — bump SP one bucket if NEW UI surface (page/complex form/dashboard). Frontmatter MUST include `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`, `estimate_scope_included`, `estimate_scope_excluded`, `estimate_reasoning` (UI vs backend cost driver). Cap SP 3 for additive-on-existing-model+existing-UI unless test scope >1.5d. SP 13 SHOULD split, SP 21 MUST split.
  <!-- /SYNC:estimation-framework:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `spawn_agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.

<!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Stage changes and create well-structured Conventional-Commits commits — and, when code changed, gate the commit on a user decision to verify (via `$workflow-integration-test-green`, which drives the suite to green), confirm already-verified, or explicitly skip (default: verify first). Every commit message body OPENS with a mandatory `Estimate:` line carrying the derived story points and AI man-days for that staged diff.

**IMPORTANT MUST ATTENTION main steps — execute in order, the skill AI keeps forgetting:** (0) CREATE the `tmp/claude-temp/.commit-skill-active` bypass marker, and ALWAYS remove it afterwards; (1-2) ANALYZE + STAGE; (2.5) DOCS TRIAGE → `$docs-update` + re-stage; (2.7) IDENTIFY REVIEWERS — last author per staged file vs `HEAD`, author excluded, grouped BY AREA; (2.9) DERIVE THE ESTIMATE from the STAGED diff per the carried `SYNC:estimation-framework`, discounting generated/lockfile/docs churn first; (3) GENERATE MESSAGE — subject, then Estimate as the FIRST body line, then purpose → what → how, then Reviewers; (3.5) TEST-VERIFY GATE — ask the user directly, default verify, and **re-stage AND re-derive** if the gate mutated the staged set; (4) COMMIT via HEREDOC; (5) VERIFY the first body line IS the Estimate line, then re-present reviewers; (6) REFRESH THE CODE GRAPH in the BACKGROUND via `$graph-build --scope=sync` when `.code-graph/` exists. **STOP after the commit unless `--push`.** — why: three of these steps (2.7, 2.9, 2.5) must run BEFORE the message exists, so skipping one cannot be repaired afterwards without amending — which is forbidden.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Sub-Agent Selection:** route specialized domains to the matching specialist; NEVER `code-reviewer`.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** traced `file:line` proof per claim; confidence >80% to act, never guess.

- **MANDATORY MUST ATTENTION — AI KEEPS FORGETTING:** code changed? ask the user directly BEFORE committing — verify via `$workflow-integration-test-green` (default), **Yes — already verified**, or user-chosen **Skip**; NEVER select skip yourself — why: prevents committing unverified code, and a gate the agent can waive is not a gate
- **MANDATORY MUST ATTENTION — FIRST BODY LINE:** every commit message opens with `Estimate: <n> SP | man_days_ai: <x>d | man_days_traditional: <y>d`, derived bottom-up per `SYNC:estimation-framework` against the staged diff (Step 2.9) — SP is DERIVED never eyeballed, generated/lockfile/docs churn is discounted first, and the number covers THIS diff only — why: the estimate must travel with the commit, or velocity data has to be reconstructed from diffs after the fact
- **MANDATORY MUST ATTENTION — AFTER THE COMMIT:** when `.code-graph/` exists, fire `$graph-build --scope=sync` in the BACKGROUND (Step 6) so the commit that moved HEAD is re-parsed and `last_synced_commit` advances — why: the `graph-auto-update` hook only fires on `Edit|Write|MultiEdit` and never sees a commit; `sync` (not `update`) is the HEAD-movement verb, and it is an accelerator, so it NEVER blocks or fails the commit
- **Estimation Framework:** bottom-up hours drive man-days; SP DERIVED from `likely_days`, never the driver.
- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**Anti-Rationalization:**

| Evasion                                          | Rebuttal                                                                                                                                                         |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "The user said commit, so just commit"           | Code changed → run the Test-Verify Gate first. ask the user directly to verify / already-verified / skip; default verify before committing.                      |
| "The user is clearly in a hurry — pick Skip"     | Skip is the user's decision alone. Offer it, never choose it. An agent that waives its own gate has no gate.                                                     |
| "Verify just means run the tests once"           | Verify routes to `$workflow-integration-test-green` — it drives failures to green. Reporting red and committing anyway is not verification.                      |
| "Tests probably passed already"                  | Probably ≠ confirmed. Ask the user; default No runs verify. Only an explicit Yes commits without verifying.                                                      |
| "It's a small change, skip the verify question"  | Size doesn't decide — any code that might need tests triggers the gate. Skip only docs/specs/config-only diffs.                                                  |
| "Asking is annoying, I'll just proceed"          | The confirmation is the point — AI keeps committing unverified code. Ask every time code changed.                                                                |
| "It's a tiny commit, skip the Estimate line"     | The line is mandatory on EVERY commit. A tiny commit is `1 SP` / `man_days_ai: 0.25d` — cheap to write, and the omission is what breaks the velocity series.     |
| "I'll just eyeball the story points"             | SP is DERIVED from bottom-up hours (blast radius → tiers → `Σh/6` → SP→Days bucket), never eyeballed. Eyeballing is the failure the framework exists to prevent. |
| "Huge diff, so it must be 13 SP"                 | Discount generated code, lockfiles, designer snapshots, i18n sorting, and bulk reformatting FIRST. Line count is not effort.                                     |
| "The plan said 8 SP, stamp 8 on this commit"     | Only if the commit implements the WHOLE artifact. A partial slice is estimated bottom-up on its own staged diff.                                                 |
| "The graph hook already updated it, skip Step 6" | The hook fires on `Edit\|Write\|MultiEdit` only — it never sees a commit. Fire the background refresh when `.code-graph/` exists.                                |
| "Graph update failed, so the commit failed"      | Step 6 is non-blocking. The commit stands; report the graph error in one line and stop.                                                                          |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
