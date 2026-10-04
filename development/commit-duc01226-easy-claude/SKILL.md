---
name: commit
version: 2.4.0
description: '[Git] Use when asked to commit, stage and commit, or save changes. --push also pushes.'
---

## Quick Summary

**Goal:** Stage changes and create well-structured git commits following Conventional Commits format — and, when code changed, gate the commit on a user decision to verify (via `/workflow-integration-test --mode=green`, which drives the suite to green), confirm already-verified, or explicitly skip (default: verify first). Every commit message body OPENS with a mandatory `Estimate:` line carrying the derived story points and AI man-days for that staged diff.

**Summary:** (read-this-if-nothing-else digest — purpose + ALL main steps + gates)

- **PURPOSE** — produce a commit whose message a future reader can act on WITHOUT opening the diff: conventional subject, an `Estimate:` first body line, a purpose→what→how body, and a per-area Reviewers block. Three things are computed BEFORE the message exists (reviewers, estimate, doc triage) because they must live INSIDE it.
- **STEP 0 — EXPLICIT INTENT + LEASE.** After validating the user's literal Git request and resolving the exact repository, issue a short, session-scoped lease for only the requested operation(s). A lease is bounded bookkeeping, never user consent or native permission; revoke every issued lease in a `finally` path.
- **STEP 1-2 — ANALYZE + STAGE.** `git status` / `git diff --cached` / `git diff` / `git log --oneline -5`, then stage.
- **STEP 2.5 — DOCS TRIAGE.** Staged files matching doc-impact patterns → run `/docs-manager --mode=update`, re-stage the doc changes.
- **STEP 2.6 — NO-OP DOC GUARD (BLOCKING).** `doc-stamp-guard.cjs --staged` flags any staged file whose diff is only a date stamp or whitespace; on user approval `git restore --staged` those paths. NEVER revert the working tree.
- **STEP 2.7 — IDENTIFY REVIEWERS** (pre-commit, read-only): last author per staged file vs `HEAD`, commit author EXCLUDED, grouped BY AREA with the focus each owns.
- **STEP 2.9 — DERIVE THE ESTIMATE** via the carried `SYNC:estimation-framework` against the STAGED diff (or reuse the implemented plan/PBI/story frontmatter with `(source: <path>)`). SP is DERIVED from `likely_days`, never eyeballed; discount generated/lockfile/docs churn first.
- **STEP 3 — GENERATE MESSAGE.** Subject `type(scope): description`; body OPENS with the Estimate line, then purpose/kind → what changed → how it works, then the Reviewers block.
- **STEP 3.5 — TEST-VERIFY GATE (USER CHOICE — always).** `AskUserQuestion`, default **verify** via `/workflow-integration-test --mode=green`. Only an explicit **Yes — already verified** or **Skip** proceeds; NEVER choose skip on the user's behalf. If the gate mutates the staged set, **re-stage AND re-derive the estimate**.
- **STEP 3.6 — REVIEW GATE (BLOCKING — always).** Check the exact prepared commit candidate with `node .claude/hooks/lib/review-receipt.cjs check --target=commit-descriptor --descriptor-json='<exact descriptor JSON>'`. Ask the user to run review, use existing evidence, or Skip (reuse an actual same-candidate answer from this run), then proceed only for `CLEAN`, or a matching `review`/user-approved `skip` receipt; `ERROR` blocks. Otherwise `AskUserQuestion` offering all three `--fix-loop` reviews with ONE marked `(Recommended)` per **Review selection** (size and risk; heavier on a tie), plus user-approved skip using a snapshot and `issue --kind=skip` bound to this descriptor. NEVER choose skip for the user. A review receipt proves candidate identity only; it does not waive tests, spec reconciliation, other review gates, or the project CI overlay.
- **STEP 4 — COMMIT** with the HEREDOC form (subject → blank → Estimate → body → Reviewers → footer).
- **STEP 5 — VERIFY** via `git status` + `git log`; confirm the first body line IS the Estimate line, then re-present the reviewer assignment.
- **STEP 6 — REFRESH THE CODE GRAPH (optional, post-commit, BACKGROUND, non-blocking).** Only when `.code-graph/` exists: fire `/graph-code --mode=build --scope=sync` in the background so the commit that just moved HEAD is re-parsed AND the graph's `last_synced_commit` advances with it. NEVER blocks or gates the commit; a failure is reported, never retried inline.
- **FLAG** — `--push` (a.k.a. "commit and push") stages + commits + pushes via `git-manager`. Without it: **STOP after the commit**; NEVER push unprompted.
- **PULL REQUEST?** — the user asks to create, finish, update or mark ready a PR → invoke the `pull-request` skill instead. It commits through this skill, reviews the whole branch, opens or readies the PR and loops CI to green (see [Pull-request requests](#pull-request-requests--the-pull-request-skill)).

**Workflow:**

1. **Analyze Changes** — Run git status/diff to understand staged and unstaged changes
2. **Stage Changes** — Add relevant files (specific or all)
3. **Guard No-Op Docs** — unstage staged files whose diff is only a moved date stamp or whitespace (they cause merge conflicts and carry no information)
4. **Identify Reviewers** — from git history, list relevant reviewers (last author per touched file vs `HEAD`, excluding the commit author) and the area each must focus on — computed BEFORE the commit so the block can be embedded in the message body
5. **Derive Estimate** — Apply the carried `SYNC:estimation-framework` to the staged diff (or reuse the frontmatter of the plan/PBI/story this commit implements) to derive `story_points` + `man_days_ai` — computed BEFORE the message so the numbers can head the body
6. **Generate Message** — Detect type (feat/fix/refactor/etc.), extract scope from paths, write subject, open the body with the **Estimate** line from step 5, add a detailed body structured as **purpose/kind → what changed → how it works**, and append the **Reviewers** block from step 4
7. **Test-Verify Gate** — When staged changes include code that might need tests, ask the user (`AskUserQuestion`, default **verify**) to verify via `/workflow-integration-test --mode=green`, confirm **Yes — already verified**, or explicitly **Skip**. Default = verify first, and verify means drive the suite to green, not merely report it
8. **Review Gate** — Check the exact prepared commit candidate using `check --target=commit-descriptor --descriptor-json='<exact descriptor JSON>'`; block on `ERROR`. A clean candidate needs no receipt; a changed candidate needs a matching full-review or explicitly user-approved skip receipt. Ask the user to confirm existing evidence or choose one of the three `--fix-loop` reviews, recommending one per **Review selection** (Step 3.6), or to explicitly skip using `snapshot` + `issue --kind=skip` for this exact descriptor. NEVER skip on the user's behalf. The `review-commit-gate.cjs` hook independently checks the actual commit invocation.
9. **Commit** — Create commit with HEREDOC (title + Estimate line + detailed summary + Reviewers block + attribution footer)
10. **Verify** — Confirm with git status and git log

**Key Rules:**

- **Stamp the estimate on the FIRST body line** — every commit message opens its body with `Estimate: <n> SP | man_days_ai: <x>d | man_days_traditional: <y>d`. Story points and AI man-days are MANDATORY and DERIVED bottom-up per the carried `SYNC:estimation-framework` (or reused from the plan/PBI/story frontmatter this commit implements); the number describes THIS staged diff only
- Write a detailed body — **purpose/kind → what changed → how it works** — so the next human reading `git log`/`git blame` understands the change without opening the diff. As detailed as the change needs (wrap ~72 chars); no title-only commits for non-trivial changes
- Embed a **Reviewers** block in the commit message — the per-area reviewers (last author per touched file vs `HEAD`, commit author excluded) — computed BEFORE committing so it lives in the message body, not just as a side report
- When staged changes include code that might need tests, **gate the commit on test verification** — ask the user to verify via `/workflow-integration-test --mode=green` (default), confirm already-verified, or explicitly skip; only an explicit **Yes** or **Skip** proceeds straight to commit, and the agent NEVER chooses skip on the user's behalf
- **Gate the commit on the exact candidate (Step 3.6, blocking — always)** — derive the descriptor from the prepared commit invocation and check it with `node .claude/hooks/lib/review-receipt.cjs check --target=commit-descriptor --descriptor-json='<exact descriptor JSON>'`. `ERROR` blocks; `CLEAN` needs no receipt; a `CHANGED` candidate needs a matching full-review receipt or an explicitly user-approved skip receipt for that descriptor. Always ASK the user to confirm existing evidence or choose a `--fix-loop` review — recommend exactly one per **Review selection** (Step 3.6) and state the signal that chose it — or explicitly approve Skip by capturing this descriptor and issuing kind `skip`. NEVER choose skip yourself; `review-commit-gate.cjs` independently checks the actual commit invocation.
- Stop after the commit; push only when the user explicitly requests it (or passes `--push` / says "commit and push" → stage + commit + push via `git-manager`)
- Never commit secrets, credentials, or .env files
- Never use `--amend` or `--no-verify` unless explicitly requested
- Include `Generated with [Claude Code]` attribution footer

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Git Commit Skill

Stage changes and create well-structured git commits following Conventional Commits format.

## IMPORTANT: Scoped Git authority

There is no bypass marker for Git authority. Before the first
mutating Git statement, obtain the user's literal operation authority through
this skill's Git Request Contract, resolve the canonical project/repository,
and issue a short lease for the exact session and operation(s). Use the lease
CLI with structured JSON on stdin; do not interpolate untrusted command text
into a shell expression:

```bash
printf '%s' '{"projectDir":"<canonical-project>","repository":"<canonical-repository>","sessionId":"<session-id>","operations":["add","commit"],"sourceRequest":"<bounded description of the user request>"}' \
  | node .claude/hooks/lib/git-operation-lease.cjs issue
```

Store the returned `leaseId` without exposing it in the commit message or
logs. Include `push` only when the user explicitly requested push (for
example, `--push` / “commit and push”); a commit or implementation approval
never implies push. Revoke each issued lease in a `finally` path, including
when staging, verification, hooks, or the commit fails:

```bash
printf '%s' '{"projectDir":"<canonical-project>","repository":"<canonical-repository>","sessionId":"<session-id>","leaseId":"<lease-id>"}' \
  | node .claude/hooks/lib/git-operation-lease.cjs revoke
```

SessionEnd revokes any remaining records for the ending session on `clear` or
`exit`; `compact` never refreshes or revokes leases. The lease is bounded
bookkeeping recorded for the requested operations: no hook consumes it, so it
neither grants nor blocks any Git operation. The user's explicit request is the
authority; the lease is not a substitute for that request, native host
permissions, the test-verify gate, or the review receipt `review-commit-gate`
checks.

## User test and review choices

On every commit invocation with a candidate to publish, including a commit called by `pull-request`, ask the user about tests and review with explicit Skip options. This applies whether `portability.skillAutoTrigger` is true or false. A general autonomous/finish request never answers these questions. Existing evidence or receipts do not replace the question; offer the user confirmation of that evidence. Reuse an actual answer already given for this exact candidate in the current run instead of asking twice. Record the answer and candidate scope; preserve them through compaction/resume. The chosen fix-loop authorizes its required checks and fixes through convergence. Later candidate changes after a gate completes invalidate affected answers and require a fresh choice. Never infer an answer from silence.

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
# Stage only paths covered by the user's explicit scope.
git add -- <authorized-file> [<authorized-file> ...]
```

### Step 2.5: Docs-Update Triage

Before committing, check if staged files impact documentation:

1. Run `git diff --name-only --cached` to list staged files
2. Check if any staged file matches doc-impact patterns (resolve the concrete backend/frontend source paths from the project's structure reference / `docs/project-config.json`):
    - changes under the backend service source paths (per project config) → may impact the business spec root (default `docs/specs/`; `specRoots.business.path` in `docs/project-config.json` overrides)
    - `.claude/skills/**` → may impact `.claude/docs/skills/`
    - `.claude/hooks/**` → may impact `.claude/docs/hooks/`
    - `.claude/workflows.json` → may impact `CLAUDE.md` workflow table
    - changes under the frontend app source paths (per project config) → may impact frontend pattern docs
3. If matches found: invoke `/docs-manager --mode=update` skill, then re-stage any doc changes with `git add`
4. If no matches: skip (log "No doc-impacting files staged")

> `/docs-manager --mode=update`'s Phase 1 already runs `/prompt-enhance <doc>` on every reference doc it PATCHES (reference-docs root default `docs/project-reference/**`; `docsRoots.projectReference.path` in `docs/project-config.json` overrides) (see `docs-manager --mode=update` Step 1.3), keeping the doc concise yet AI-valuable before commit re-stages it — do not invoke `/prompt-enhance` again here.

### Step 2.6: No-Op Doc Guard (BLOCKING — runs after re-staging, before anything derives from the staged set)

Some staged files carry a diff that changes no meaning: a doc whose only delta is a moved date stamp (`Last scanned`, `Last verified`, `last_updated`, `Regenerated`) or whitespace. Committing one costs a merge conflict on every branch that also re-ran the generator, over a value neither branch decided. Catch it here, at the publish boundary — the framework's own writers are guarded, but a hand edit, another AI host, or an older tool is not.

```bash
node .claude/hooks/lib/doc-stamp-guard.cjs --staged
```

Exit `0` = nothing to report → continue. Exit `3` = one or more staged files are pure churn:

1. **Show the user the list** and confirm before acting — an unstage changes what they are about to publish.
2. On approval, unstage each one **and only these**:

   ```bash
   git restore --staged -- <path> [<path> ...]
   ```

3. **NEVER revert the working tree.** `git restore <path>` and `git checkout -- <path>` destroy the only copy of an uncommitted edit. Unstaging is fully recoverable; reverting is not. Leaving the file dirty in the working tree is the correct end state.
4. If unstaging empties the staged set entirely, **STOP** and tell the user there is nothing meaningful to commit — do not manufacture a commit.

This runs **after** Step 2.5 (which re-stages `/docs-manager --mode=update` output, the most likely source of such a diff) and **before** Steps 2.7/2.9, so reviewers and the estimate derive from the final staged set and need no re-derive.

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

| Situation                                                                       | Source of `story_points` / `man_days_ai`                                                         |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Commit implements a plan / PBI / story whose frontmatter already carries estimates | REUSE its `story_points` + `man_days_ai`; append `(source: <path>)` to the Estimate line          |
| Commit is a PARTIAL slice of such an artifact                                    | Derive the slice bottom-up — NEVER copy the whole artifact's number onto a partial commit         |
| No estimate artifact exists                                                      | Derive bottom-up from the staged diff per the framework                                           |

**Derivation (bottom-up — SP is DERIVED, never eyeballed):**

1. **Blast-radius pass** on `git diff --cached --stat` — touched areas, complex files (>500 LOC / central / multi-handler), downstream consumers, shared/common code.
2. Sum the **Reuse-vs-Create** tiers across UI + backend + tests → `bottom_up_hours`.
3. `likely_days = ceil(bottom_up_hours / 6) × productivity_factor`.
4. `story_points` = closest **SP→Days** bucket. Disagreement >50% → trust bottom-up and downgrade SP.
5. `man_days_ai` = the AI likely column for that SP (1≈0.25d · 2≈0.35d · 3≈0.65d · 5≈1.0d · 8≈1.5d · 13≈2.0d), reconciled against the bottom-up result; it already includes the 30% review overhead.
6. `man_days_traditional` = the no-AI likely column (1≈0.5d · 2≈1d · 3≈2d · 5≈4d · 8≈6d · 13≈10d), same reconciliation.

**Anti-inflation (discount BEFORE estimating — same guardrail `/git-developer-performance` applies):** generated code, lockfiles, ORM/designer snapshots, i18n re-sorting, bulk reformatting, and pure docs/spec churn earn **no** story points. A 4 000-line lockfile bump is 1 SP, not 8.

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
- `man_days_traditional` — the no-AI baseline (3–5yr dev, 6 productive hrs/day). **Recommended** — include it whenever derived — why: alone, `man_days_ai` is an absolute figure nobody can calibrate, while the pair makes the AI leverage on THIS diff readable straight from `git log`. Written for a human reader: `/git-developer-performance` derives its own numbers from the diff rather than reading this line (its `git log` format stops at `%s` — `.claude/skills/git-developer-performance/scripts/git-developer-performance.cjs:290`), so the pair earns its place by what a person reads, not by what a tool consumes.
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

| Change size                          | Body depth                                                                              |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| Trivial (typo, rename, formatting)   | Purpose line + 1 bullet; skip "how it works"                                             |
| Normal (feature/fix, single area)    | Purpose + 2–5 "what" bullets + a short "how it works"                                    |
| Complex (cross-cutting, subtle bug)  | Purpose + grouped "what" + a full "how it works" that spells out the key invariant / edge case / why-this-over-that |

### Step 3.5: Test-Verify Gate (blocking user choice — always)

Decide whether the staged changes carry **code that might need tests** — why: this gate is the only thing standing between an untested behaviour change and permanent history.

**Trigger detection** — run `git diff --cached --name-only` and classify the staged files:

- **Code that might need tests** → any change to production/source code: backend service source, frontend app source, shared libraries, scripts, hooks (`.cjs`), or other executable logic (resolve concrete source roots from `docs/project-config.json` / the project structure reference).
- **NOT a trigger (skip the gate)** → the staged set is _only_ docs (`docs/**`, `*.md`), specs (business spec root, default `docs/specs/**`; `specRoots.business.path` in `docs/project-config.json` overrides), test-spec/config text, changelog, or other non-executable content with no source-code change.

**If the gate is NOT triggered:** explain that no code changes are staged and ask the user to confirm **No tests required**, run tests, or explicitly Skip. Wait for an answer; record it before continuing to the review gate. A same-candidate answer already obtained by `pull-request` is reused.

**If the gate IS triggered:** STOP and ask the user with `AskUserQuestion` (default option is **No**):

> Header: `Test verify`
> Question: `Staged code changes may need tests. Verify before committing, or skip?`
> Options (in order — first is the default):
> 1. `Verify now — run /workflow-integration-test --mode=green` (Recommended) — do NOT commit yet; activate the `workflow-integration-test` workflow (`--mode=green`), which verifies the suite AND drives any failure to green (verify → adjudicate → fix → review → re-verify) before returning. Proceed to Step 4 only once the whole suite is green; if it escalates instead of converging, surface that and stop (no commit).
> 2. `Yes — already verified` — the user confirms the integration tests were run and passed; proceed directly to Step 4 (Commit).
> 3. `Skip — commit without verifying` — the user's explicit, recorded decision to commit unverified code; proceed to Step 4 and note `Test-Verify Gate: skipped by user` in the response (never in the commit message).

Rules:

- **Recommend option 1 (verify), but wait for an explicit answer.** A default selection or silence is not consent. Reuse only an actual same-candidate answer already obtained in this run.
- **Verify routes to `workflow-integration-test --mode=green`, not to a bare verify run** — why: a bare `integration-test --mode=verify` only reports the failures, leaving the user to hand-carry each one; the workflow owns the converge-to-green loop, so choosing "verify" actually clears the suite instead of just describing it.
- **Yes is an explicit user assertion** that the integration tests were run and passed; honour it and commit.
- **Skip is the user's call, and it is theirs alone to make.** Offer it, never recommend it, and NEVER select it yourself — why: an agent that can skip its own gate has no gate.
- Re-run this gate only once per commit; after a `verify → green`, proceed to commit without re-asking.
- **If the verify branch changed ANY file, re-stage and RE-DERIVE before Step 4.** Option 1 can land test or source fixes AFTER Step 2.9 already ran, so the diff the estimate described is no longer the diff being committed. Mirror Step 2.5: re-stage the new changes with `git add`, then re-run Step 2.9 over the updated `git diff --cached` and put the fresh numbers in the message. Options 2 and 3 mutate nothing, so the original Step 2.9 numbers stand.
- This gate is independent of `--push`: it runs before the commit in every mode.

### Step 3.6: Review Gate (blocking — always)

No commit may reach Step 4 without a review fix-loop receipt over the **current changeset**. This runs after Step 3.5 so the review covers the FINAL code — never commit content no fix-loop saw.

Derive the descriptor from the exact prepared `git commit` invocation. With no `-a`/`--all` and no path arguments, use `{"mode":"staged","literalPaths":[]}`; `-a`/`--all` uses `{"mode":"all","literalPaths":[]}`; explicit paths after `--` use `{"mode":"literal-paths","literalPaths":["exact/path",...]}`. Include the effective `cwd` when the commit runs below the repository root. For `git commit --amend` add `"amend":true` (e.g. `{"mode":"staged","literalPaths":[],"amend":true}`): the candidate is then measured against HEAD's parent — the same candidate `git reset --soft HEAD~1 && git commit` would produce — so the review must cover the amended commit's changes plus what is staged. For an amend, Steps 2.7 (reviewers), 2.9 (Estimate) and 3.5 (test trigger) likewise read the whole amended commit — `git diff --cached HEAD~1` (and `--name-only` / `--stat`) instead of `git diff --cached` — because the message describes the commit that results, not only the new increment. Never approximate a literal-path descriptor.

**Ask about review before using evidence:** offer the three review options below and explicit Skip even when a matching receipt exists. When available, also offer **Use existing review** or **Confirm prior skip** with its evidence and scope. Wait for the user. Reuse an actual same-candidate answer from `pull-request`; never substitute the parent skill's autonomy or a receipt for consent.

**Check the exact candidate:**

```bash
node .claude/hooks/lib/review-receipt.cjs check --target=commit-descriptor --descriptor-json='{"mode":"staged","literalPaths":[]}'
```

Use the descriptor matching the prepared invocation. Read the JSON:

- `status` is `ERROR` → STOP; candidate computation failed and must never be treated as `CLEAN`.
- `status` is `CLEAN` → the candidate contains no changes, so no receipt is needed; proceed to Step 4.
- `status` is `CHANGED` and `review` is a kind (`changes-review` | `why-review` | `workflow-review-changes`) → a matching full fix-loop reviewed this exact commit candidate; proceed to Step 4.
- `status` is `CHANGED`, `review` is `null`, and `skip` is `skip` → the user already approved skipping this exact candidate; proceed to Step 4.
- `status` is `CHANGED` and both `review` and `skip` are `null` → STOP and ask the user with `AskUserQuestion` (never commit yet):

  > Header: `Review gate`
  > Question: `No review fix-loop has covered this exact changeset. Review before committing, or skip?`
  > Options — the review chosen by [Review selection](#review-selection) first, labelled `(Recommended)`; then the other two reviews; Skip last:
  > - `Run /workflow-review-changes --fix-loop` — do NOT commit yet; invoke the `workflow-review-changes` workflow with this exact descriptor JSON (including `"amend":true` for an amend) so its review steps measure the same candidate. It runs the required reviews, validates findings, fixes at the owning layer, and repeats the full review workflow until it converges, then mints the receipt. Return to this step when it converges (and re-derive if it changed files). Its receipt covers the final reviewed candidate; refresh any test choice invalidated by its fixes.
  > - `Run /changes-review --fix-loop` — do NOT commit yet; activate the `changes-review` skill in `--fix-loop` mode with the same exact descriptor JSON. It reviews, validates findings, fixes at the owning layer, and runs a fresh full re-review until it converges, then mints the receipt. Return to this step when it converges (and re-derive if it changed files). Its receipt covers the final reviewed candidate; refresh any test choice invalidated by its fixes.
  > - `Run /why-review --fix-loop` — same (pass the same exact descriptor JSON), using the rationale-review loop (`why-review` in `--fix-loop` mode); it mints the receipt on convergence.
  > - `Skip — commit without review` — the user's explicit, recorded decision. Ask them to confirm, then mint the approved skip and proceed:

     ```bash
     node .claude/hooks/lib/review-receipt.cjs snapshot --target=commit-descriptor --descriptor-json='{"mode":"staged","literalPaths":[]}'
     node .claude/hooks/lib/review-receipt.cjs issue --kind=skip --scope=full-changeset --snapshot-json='<exact snapshot JSON returned above>' --reason="user approved skip"
     ```

     Use the exact descriptor from the prepared commit, not this staged-mode example when the invocation differs. The snapshot must be `CHANGED`; a clean candidate needs no skip receipt. Re-run `check` with the same descriptor before proceeding. Record `Review gate: skipped by user` in the response (never in the commit message).

Rules:

- **Recommend one review, then wait for the user's answer.** Neither a default selection nor silence authorizes execution or Skip.
- **Skip is the user's call alone.** Offer it, never recommend it, and NEVER select it yourself — an agent that can skip its own gate has no gate.
- **The receipt is bound to candidate identity** — repository/storage, base tree, and candidate tree — and `check` must use the same commit descriptor the hook will evaluate. Staging identical reviewed content preserves the tree identity; staging different content, changing the base/candidate, or selecting different paths does not. After a fix-loop, any later content change requires a fresh full review of that candidate before commit.
- **Minting is the fix-loop's job, not yours.** The three fix-loop skills mint the receipt at their terminal step; you only mint a `skip` receipt, and only after the user explicitly approves.
- **Mechanical enforcement:** `review-commit-gate.cjs` (a `PreToolUse` hook on Bash) refuses an agent `git commit` whose changeset has neither a review receipt nor a skip receipt — so a forgotten review cannot slip through. The check above exists so the gate is handled deliberately instead of by a hook bounce.
- **Receipt scope:** a review receipt establishes only that a qualifying full review covered the same candidate. It never waives the Test-Verify Gate, spec/test reconciliation, other required reviews, or `commit-local-ci-gate` overlay requirements.
- Re-run this gate only once per commit; after a review-or-skip decision, proceed to Step 4 without re-asking.
- This gate is independent of `--push`: it runs before the commit in every mode.

#### Review selection

Recommend the review that fits the change's size and risk — why: a fixed heaviest-first default spends the full workflow on a typo fix and trains users to skip.

| Review | What it does for the agent | Pick when |
| --- | --- | --- |
| `/why-review --fix-loop` | One adversarial pass over the rationale and correctness of a small, focused change, then a fresh full re-review. Cheapest. | Docs, config or comment-only changes; or one small module (roughly ≤3 files) with no behaviour or public-contract change. |
| `/changes-review --fix-loop` | Multi-dimension diff review (correctness, tests, conventions, spec drift, integration), then validate, fix and re-review. Medium. | A focused behaviour change in one module, or a moderate diff with tests. |
| `/workflow-review-changes --fix-loop` | The full review workflow: parallel architecture, security, performance, integration-test, production-readiness, domain and UI lenses plus why-review, re-run until it converges. Heaviest. | Any of: cross-module or public-contract change; security, auth, secrets or permissions; data or schema migration; hooks, gates or other framework enforcement; dependency upgrades; UI surfaces; a large diff. |

- Read the objective signals first: the candidate's file list, paths and `--stat` (for an amend, the whole amended commit). Any heavier signal outranks a lighter one.
- Tie or unclear → recommend the heavier review.
- Mark exactly ONE option `(Recommended)` and state the signal that chose it, e.g. `Recommended: /changes-review — behaviour change in one module, with tests`.
- All three reviews stay offered and the user chooses. Skip stays user-only: offered, never recommended. Every option is a fix-loop that mints the receipt; receipt semantics do not change.
- **Autonomous runs:** general autonomy never suppresses the test/review questions. Only an explicit answer already recorded for this exact candidate in this run settles a gate; never choose Skip yourself.

### Step 4: Commit

Use a structured message file/stdin so the mandatory body fields cannot be
silently dropped:

```bash
printf '%s\n' \
  'type(scope): subject' \
  '' \
  'Estimate: 3 SP | man_days_ai: 0.65d | man_days_traditional: 2d' \
  '' \
  '- summarize key change 1 with intent' \
  '- summarize key change 2 with impact' \
  '' \
  'Reviewers:' \
  '- <area>: Reviewer Name <reviewer@email> — focus on <what they own>' \
  '' \
  'Generated with [Claude Code]' \
  | git commit -F -
```

> The **Estimate** line comes from Step 2.9 — re-derived after Step 3.5 if that gate changed the staged set — and is ALWAYS the first line of the body.
> The **Reviewers** block comes from Step 2.7 (last author per staged file vs `HEAD`, commit author excluded, grouped by area). Omit the block only when every staged file is brand-new or author-owned with no external reviewer — in that case state `Reviewers: none (author-owned / new files)`.
> **`Fix-Origin:` trailer — opt-in, off by default.** Add it only if `commit.fixOriginTrailer` is `true` in `docs/project-config.json`. When the key is absent or `false`, the message carries no `Fix-Origin` line.
>
> When the project opts in, end the message with a blank line and then one trailer line, after `Generated with [Claude Code]`:
>
> ```text
> Fix-Origin: <feedback|regression|not-applicable>
> ```
>
> Use `feedback` for a fix requested through review or other feedback, `regression` for a defect introduced by earlier work, and `not-applicable` for commits that are not fixes. It is an author-declared measurement field for projects that opt in: the author states the label and nothing in the framework reads or checks it. It applies to new commits only — never reword existing commits to add it. Put the same field in the PR body so a squash merge keeps it on the default branch.

### Step 5: Verify

```bash
git status
git log -1
```

Confirm the committed body's FIRST line IS the **Estimate** line from Step 2.9 (`Estimate: <n> SP | man_days_ai: <x>d …`) — missing → the message is non-conformant; re-derive and record it, NEVER leave it out. Then confirm the body carries the **Reviewers** block from Step 2.7 (or the explicit `Reviewers: none (author-owned / new files)` line). Re-present the per-area reviewer assignment to the user as the final deliverable — why: they need it to request the right reviewers on the resulting PR.

### Step 6: Refresh Code Graph (post-commit — background, non-blocking)

**Skip entirely (silently) when `.code-graph/` does not exist** — the project has no knowledge graph and there is nothing to refresh.

When it does exist, fire `/graph-code --mode=build --scope=sync` **in the background** immediately after Step 5 verifies the commit — one Bash call with `run_in_background: true`, so the commit never waits on it:

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

- **This skill is the ONLY supported commit path** — a raw ad-hoc `git commit` from the agent is refused by `review-commit-gate.cjs` unless a review fix-loop receipt (or a user-approved `skip` receipt) exists for the changeset. Always run the Review Gate (Step 3.6) before committing
- **Stage only the user-authorized paths** before committing — never use a repository-wide `git add .` when unrelated work may be present; preserve other owners' index/worktree changes
- **Test-Verify Gate (Step 3.5):** when staged changes include code that might need tests, ask the user to verify via `/workflow-integration-test --mode=green` (default — it converges the suite to green), confirm already-verified, or explicitly skip; only an explicit **Yes** or user-chosen **Skip** commits without verifying, and the agent NEVER picks skip itself. For a candidate with no source-code change, ask the user to confirm No tests required, run tests, or Skip
- **Review Gate (Step 3.6, blocking — ALWAYS):** check `node .claude/hooks/lib/review-receipt.cjs check --target=commit-descriptor --descriptor-json='<exact prepared commit descriptor>'` against the exact planned commit candidate; `ERROR` blocks, `CLEAN` needs no receipt, and `CHANGED` requires a matching review or user-approved skip receipt. Always ask the user to confirm existing evidence or choose one of the three `--fix-loop` reviews (one recommended per **Review selection**, heavier on a tie) or explicitly approve skip; after approval, capture and issue the skip against that same descriptor with the `snapshot --target=commit-descriptor` and `issue --kind=skip --scope=full-changeset --snapshot-json=...` flow above. The agent NEVER chooses skip on the user's behalf. Candidate identity changes invalidate the receipt; unrelated worktree edits outside the prepared commit candidate do not.
- **Estimate line is MANDATORY and comes FIRST in the body** — `Estimate: <n> SP | man_days_ai: <x>d | man_days_traditional: <y>d`, derived bottom-up per the carried `SYNC:estimation-framework` against the STAGED diff (Step 2.9), or reused from the implemented plan/PBI/story frontmatter with `(source: <path>)`. Story points and AI man-days are required; discount generated/lockfile/docs churn before estimating
- **Stop after the commit; push** to remote only when the user explicitly requests it
- **Refresh the code graph after committing (Step 6)** — when `.code-graph/` exists, fire `/graph-code --mode=build --scope=sync` in the BACKGROUND (`run_in_background: true`) so the commit that moved HEAD is re-parsed and `last_synced_commit` advances with it; skip silently when the dir is absent. Non-blocking by design: it NEVER gates, delays, or fails the commit
- **Review staged changes** before committing
- **Never commit** secrets, credentials, or .env files
- **Amend only on an explicit amend request** (a plain commit request makes a new commit) — `git commit --amend` is gated like any commit (a receipt over the candidate against HEAD's parent, via an `"amend":true` descriptor); never amend a commit that is already pushed or that this task did not create — the same rule binds `git reset --soft HEAD~1` + commit, which produces the same result
- **Never skip** hooks with `--no-verify` unless explicitly requested
- Commit message MUST include a Conventional Commit title AND a detailed body — **purpose/kind → what changed → how it works**. As detailed as the change needs (wrap ~72 chars); title-only commit FORBIDDEN for non-trivial changes
- Optimize body for the next human reading `git log` / `git blame` — surface the non-obvious (key logic, invariants, edge cases, why-this-over-that), not just a list of touched files
- Include attribution footer: `Generated by AI`
- **Embed reviewers in the commit message** — BEFORE committing (Step 2.7), surface the last author per staged file vs `HEAD` (exclude the commit author), grouped by focus area, and write it as a `Reviewers:` block in the message body so the right reviewers travel with the commit/PR. Read-only; never blocks the commit.

## Push & PR Operations

**Arg `--push` (a.k.a. "commit and push"):** stage + commit + push in one shot — spawn `git-manager` immediately after committing. The former standalone stage-commit-push entry point, folded in; it adds no logic beyond the push delegation below.

This skill handles **commit** by default. A plain push delegates to the `git-manager` sub-agent (`subagent_type: "git-manager"`), which enforces conventional-commit validation and prevents `--no-verify` bypass. Spawn `git-manager` after committing when the user says "push".

### Pull-request requests → the `pull-request` skill

When the user asks for a pull request — create or open a PR, finish or update the current PR, make it ready to merge, or mark a draft ready — invoke the **`pull-request` skill** (`/pull-request`) instead of this skill or `git-manager`. It takes the work all the way to ready to merge, in the main session, asking the user about tests and review with explicit Skip options:

1. branch at the latest target (the base named in the request → an open PR's base → `pullRequest.targetBranch` in `docs/project-config.json` → `main`): a branch already merged into the target is replaced by a new branch from it; an unpushed branch behind it is rebased (stash, `git-conflict-resolve` on conflicts); a pushed branch is never rebased;
2. ask about tests and whole-branch review, run the chosen fix-loop over `<target>...HEAD` ∪ uncommitted changes or record an explicit user-approved skip;
3. commit through this skill;
4. push, and create the PR or mark it ready;
5. wait for CI, and fix, review and push again until every check passes.

A commit request that also mentions a PR routes to `pull-request`, which commits through this skill as one of its steps. — why: a PR opened straight after a commit skips the whole-branch review and the CI loop, so it is not ready to merge.

## Sub-Agent Type Override

> **MANDATORY:** Push operations spawn `git-manager` sub-agent (`subagent_type: "git-manager"`), NOT the main agent. Pull-request operations route to the `pull-request` skill (see above).
> **Rationale:** `git-manager` enforces conventional commits and prevents hook bypasses. `pull-request` owns the whole-branch review, PR creation and the CI loop.

## Related

- `changes-review` (branch-to-branch diffs)

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `estimation-framework` — Bottom-up estimation with derived story points and a min-max range; estimating effort → .claude/skills/shared/protocols/estimation-framework.md
- `sub-agent-selection` — Pick the sub-agent type from the routing guide; choosing which sub-agent to spawn → .claude/skills/shared/protocols/sub-agent-selection.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:estimation-framework:reminder -->

- **MANDATORY MUST ATTENTION** estimation: bottom-up phase hours drive `man_days_traditional` (`Σh/6 × productivity_factor`); SP DERIVED. UI cost usually dominates — bump SP one bucket if NEW UI surface (page/complex form/dashboard). Frontmatter MUST include `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`, `estimate_scope_included`, `estimate_scope_excluded`, `estimate_reasoning` (UI vs backend cost driver). Cap SP 3 for additive-on-existing-model+existing-UI unless test scope >1.5d. SP 13 SHOULD split, SP 21 MUST split.

<!-- /SYNC:estimation-framework:reminder -->


## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Stage changes and create well-structured Conventional-Commits commits — and, when code changed, gate the commit on a user decision to verify (via `/workflow-integration-test --mode=green`, which drives the suite to green), confirm already-verified, or explicitly skip (default: verify first). Every commit message body OPENS with a mandatory `Estimate:` line carrying the derived story points and AI man-days for that staged diff.

**IMPORTANT MUST ATTENTION main steps — execute in order, the skill AI keeps forgetting:** (0) VALIDATE explicit Git intent, resolve the canonical target, issue exact session-scoped lease(s), and record a `finally` revocation path; (1-2) ANALYZE + STAGE; (2.5) DOCS TRIAGE → `/docs-manager --mode=update` + re-stage; (2.7) IDENTIFY REVIEWERS — last author per staged file vs `HEAD`, author excluded, grouped BY AREA; (2.9) DERIVE THE ESTIMATE from the STAGED diff per the carried `SYNC:estimation-framework`, discounting generated/lockfile/docs churn first; (3) GENERATE MESSAGE — subject, then Estimate as the FIRST body line, then purpose → what → how, then Reviewers; (3.5) TEST-VERIFY GATE — `AskUserQuestion`, default verify, and **re-stage AND re-derive** if the gate mutated the staged set; (4) COMMIT via HEREDOC; (5) VERIFY the first body line IS the Estimate line, then re-present reviewers; (6) REFRESH THE CODE GRAPH in the BACKGROUND via `/graph-code --mode=build --scope=sync` when `.code-graph/` exists; finally revoke every issued lease. **STOP after the commit unless `--push`.** — why: three of these steps (2.7, 2.9, 2.5) must run BEFORE the message exists, so skipping one cannot be repaired afterwards without amending — which needs its own explicit amend request.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Sub-Agent Selection:** route specialized domains to the matching specialist; NEVER `code-reviewer`.

- **MANDATORY MUST ATTENTION — AI KEEPS FORGETTING:** candidate to publish? Ask about tests AND review BEFORE committing, including Skip; for docs-only changes confirm No tests required. For code, `AskUserQuestion` — verify via `/workflow-integration-test --mode=green` (default), **Yes — already verified**, or user-chosen **Skip**; NEVER select skip yourself — why: prevents committing unverified code, and a gate the agent can waive is not a gate
- **MANDATORY MUST ATTENTION — FIRST BODY LINE:** every commit message opens with `Estimate: <n> SP | man_days_ai: <x>d | man_days_traditional: <y>d`, derived bottom-up per `SYNC:estimation-framework` against the staged diff (Step 2.9) — SP is DERIVED never eyeballed, generated/lockfile/docs churn is discounted first, and the number covers THIS diff only — why: the estimate must travel with the commit, or velocity data has to be reconstructed from diffs after the fact
- **OPTIONAL — AFTER THE COMMIT:** when `.code-graph/` exists, you may fire `/graph-code --mode=build --scope=sync` in the BACKGROUND (Step 6) so the commit that moved HEAD is re-parsed and `last_synced_commit` advances — why: the `graph-auto-update` hook only fires on `Edit|Write|MultiEdit` and never sees a commit; `sync` (not `update`) is the HEAD-movement verb, and it is an accelerator, so it NEVER blocks or fails the commit
- **Estimation Framework:** bottom-up hours drive man-days; SP DERIVED from `likely_days`, never the driver.
- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**Anti-Rationalization:**

| Evasion                                          | Rebuttal                                                                                                  |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| "The user said commit, so just commit"           | Code changed → run the Test-Verify Gate first. `AskUserQuestion` to verify / already-verified / skip; default verify before committing. |
| "The user is clearly in a hurry — pick Skip"     | Skip is the user's decision alone. Offer it, never choose it. An agent that waives its own gate has no gate. |
| "Verify just means run the tests once"           | Verify routes to `/workflow-integration-test --mode=green` — it drives failures to green. Reporting red and committing anyway is not verification. |
| "Tests probably passed already"                  | Probably ≠ confirmed. Ask the user; default No runs verify. Only an explicit Yes commits without verifying. |
| "It's a small change, skip the verify question"  | Size doesn't decide — any code that might need tests triggers the gate. Skip only docs-, spec-, or config-only diffs. |
| "Asking is annoying, I'll just proceed"          | The confirmation is the point — AI keeps committing unverified code. Ask every time code changed.        |
| "It's a tiny commit, skip the Estimate line"     | The line is mandatory on EVERY commit. A tiny commit is `1 SP` / `man_days_ai: 0.25d` — cheap to write, and the omission is what breaks the velocity series. |
| "I'll just eyeball the story points"             | SP is DERIVED from bottom-up hours (blast radius → tiers → `Σh/6` → SP→Days bucket), never eyeballed. Eyeballing is the failure the framework exists to prevent. |
| "Huge diff, so it must be 13 SP"                 | Discount generated code, lockfiles, designer snapshots, i18n sorting, and bulk reformatting FIRST. Line count is not effort. |
| "The plan said 8 SP, stamp 8 on this commit"     | Only if the commit implements the WHOLE artifact. A partial slice is estimated bottom-up on its own staged diff. |
| "Graph update failed, so the commit failed"      | Step 6 is non-blocking. The commit stands; report the graph error in one line and stop. |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
