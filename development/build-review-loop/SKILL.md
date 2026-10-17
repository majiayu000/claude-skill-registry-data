---
name: build-review-loop
description: "Use when the user says 'review loop N times', 'build then review', 'fix and re-review', or wants an iterative quality gate with different models building vs reviewing. Orchestrates N rounds of build-review-fix using Cursor CLI for build and Codex or another model for review."
license: MIT
metadata:
  version: 1.4.5
  author: moonlight-lupin
  platforms: [linux, macos, windows]
  hermes:
    tags: [build, review, iterative, cursor, codex, quality-gate, cross-model]
    related_skills: [cursor-cli, codex, council-code-review]
---

# Build-Review Loop

Orchestrate N rounds of build → review → fix → re-review using different models for building vs reviewing (cross-model diversity). The orchestrator (Hermes) manages the loop, verifies independently, and delivers structured reviews.

## MANDATORY: delegate the build — never hand-code mid-loop

**User correction:** "didnt see you using cursor cli". The orchestrator started hand-writing fixes in the repo instead of dispatching Cursor. That violates this skill's core contract even when the fix is small. Non-trivial dev work means: orchestrator writes a spec file, Cursor (user's default: `cursor-grok-4.6-high`, `--force`) implements, orchestrator verifies independently, Codex/Claude/Cursor review, iterate. Hand-editing is only acceptable for trivial mechanical fixes (a typo, a one-line version bump) — and even then, say so explicitly when deviating. If unsure whether it counts as non-trivial, delegate.

See also `references/generated-frontmatter-and-reviewer-outages.md` — reviewer-lane outage substitution pattern + the f-string YAML frontmatter double-failure class (`:`/`#` scalars break YAML; `safe_dump` default width wraps it) + the untracked-files reviewer trap.
See also `references/persistent-loop-plan.md` — multi-session or multi-batch loops: loop state lives in loop-*.md files, not memory; resume with `scripts/loop_plan_check.py`, attest briefs with `scripts/attest_file.py`. Ported from planning-with-files; the native plugin was NOT installed (see `references/planning-with-files-adaptation.md`).
See also `references/evidence-pairs.md` — every delivered batch carries a before/after evidence pair (screenshot, measured number, or output pair), embedded in the PR body or delivery message. Ported from michaelshimeles/skills.
See also `references/mobile-app-verification.md` — APK/dex/baked-config artifact verification gates, version stamping, the 4-layer Android WebView network stack (cleartext / mixed-content / ws scheme / CORS), backgrounded-JavaScript login-death bugs, multi-round review convergence on lifecycle code.
See also `references/sync-pipeline-review-patterns.md` — reviewing app ↔ external-source-of-truth sync code (Google Sheets, SaaS mirrors): fetch-inside-lock, status-clear scoping to processed snapshots, append reconcile/marker placement under dynamic column maps, blank-cell semantics, static-path auth whitelists.
See also `references/review-findings-adjudication.md` — adjudicating reviewer BLOCKINGs against the dispatch spec (dismiss with cause, never silently), the four recurring test-quality findings (hook-bypass, loose string-greps, single-open DOM tests, over-broad state selectors) and their fixes, and fix-round routing back to the builder.
See also `references/production-reachability-review.md` — the dead-feature cluster: public functions with tests but zero production callers (unreachable user stories while the suite stays green), test-only enrichment kwargs the runtime never passes, and the per-batch grep pass that catches it.
See also `references/extraction-from-filled-docs.md` — fill-template extraction domain depth: fingerprint/structural context, collapse ordering + XML validity + unclaimed-content preservation, path-escape and hardlink guards, and the reviewer traps for extraction code.

## When to Use

- User says "review loop N times" or "build then review with codex" or "fix and re-review"
- User wants Cursor to build, Codex to review, then Cursor to fix, Codex to re-review
- Iterative quality gate: keep reviewing until clean or N rounds exhausted
- Any task where the user wants separation of concerns: one model builds, another reviews

## When NOT to Use

- Single review pass — use `council-code-review` (parallel 3-model review) or `codex`/`cursor-cli` directly
- Pure code review without fixes — use `codex exec --sandbox read-only`
- Simple one-file fix — just delegate to Cursor or Codex directly

## Prerequisites

- **Cursor CLI** installed: `~/.local/bin/agent` (binary is `agent`, not `cursor`)
  - Auth: `CURSOR_API_KEY` in `~/.hermes/.env`
  - Build/fix model: `cursor-grok-4.6-high` (user's canonical implementation preference). Model pins go stale when the upstream CLI renames its catalog — a name that worked last session can vanish. Verify against the live list before assuming a pin (see `pitfalls-dispatch-semantics.md` — model-name pins).
- **Codex CLI** installed: `npm install -g @openai/codex`
  - Auth: Codex OAuth or `OPENAI_API_KEY`
  - Review model: GPT-6 Sol (`gpt-6-sol`, pinned 2026-09-24; dispatch with `-c model_reasoning_effort="high"` — default effort is `none`)
  - Needs `pty=true` and a git repo
- Both tools verified: `which agent && which codex`

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Hermes (Orchestrator)                          │
│                                                 │
│  1. Write spec/brief (if not already written)   │
│  2. Dispatch Cursor (Grok 4.6 High) to build    │
│  3. Verify output independently                 │
│  4. Dispatch Codex (GPT-6 Sol, effort high) to review│
│  5. Synthesize structured review                │
│  6. If issues found + loops remaining:          │
│     a. Dispatch Cursor to fix                    │
│     b. Re-verify                                 │
│     c. Dispatch Codex to re-review              │
│     d. Synthesize re-review                     │
│     e. Repeat until clean or loops exhausted    │
│  7. Deliver final verdict                       │
└─────────────────────────────────────────────────┘
```

## Pre-generated diff is the review input for multi-file rounds

Do not point reviewers at the whole tree. After each build/fix round, export
the exact delta and dispatch every reviewer against it:

```bash
git diff <base-commit>..<round-commit> > /tmp/review-diff-<proj>.diff
codex exec --sandbox danger-full-access \
  "Read ONLY /tmp/review-diff-<proj>.diff (plus the current files it touches
   in <repo>). Verify each finding is resolved... Review only, change nothing."
```

Benefits observed across two projects: bounded context (no tree-walk budget
burn), the reviewer cannot re-litigate untouched files, and the diff doubles
as the fix brief's evidence attachment. Codex confirmation passes on a ~2k-line
fix diff complete in ~10 min. Muse requires this shape to complete at all
(see `muse-review-quirks`).

## Workflow

### Step 1 — Prepare the brief (if building from scratch)

Write a self-contained brief at `<project-dir>/BRIEF.md`:
- Context (what the project is, why)
- Reference to spec file (SPEC.md)
- Reference code paths (proven code to adapt)
- Acceptance criteria / verification checks
- Constraints (what NOT to change), plus: "Do NOT `git commit` — the orchestrator commits after review." (See Pitfalls — "The reviewer commits — the implementer never commits".)

See `design-specs` skill for spec format. The brief is the spec's implementation-focused companion.

### Step 2 — Initialize git (Codex needs a repo)

```bash
cd <project-dir>
git init
git add -A
git commit -m "initial: pre-build scaffold"
```

Codex requires a git repo. Always init before dispatching the review.

### Step 2b — Identify integration boundaries (Hermes, before build)

Before dispatching the builder, identify every **integration boundary** that will
change shape — any function return type, API payload, event format, or data
structure that crosses a module seam. These are the points where a stale mock in
tests can silently mask a real bug.

For each boundary changed, write down:
1. **The old shape** (if it exists) — what callers currently expect
2. **The new shape** — what the builder will produce
3. **The test that covers it** — which test exercises this boundary
4. **Does the test use the real shape or a hand-rolled mock?** — if a mock,
   it must be updated to match the new shape

Add a section to the brief:

```markdown
## Integration boundaries changed

| Boundary | Old shape | New shape | Test | Mock updated? |
|---|---|---|---|---|
| _exec_run_backtest return | {metrics: {sharpe, cagr}} | {comparison: [{label, metrics}]} | test_agent.py::test_... | YES |
| data.load_panel | (new) | data.load_panel(cfg, override) | test_data.py | N/A (new) |
```

**For safety-critical paths** (evidence gates, trading logic, anything touching
money or agent answers): **Hermes writes the contract test first** — before
dispatching the builder. This is not full TDD — it's one test at the integration
boundary that encodes the expected behavior. The key: **Hermes writes the test,
Cursor writes the code.** Cross-model diversity at the test level is what makes
the test honest. Cursor has been caught writing `assert condition or True`
(always passes), deleting inconvenient test files, and mocking
wrong payload shapes. A Cursor-written test-first is no more trustworthy than a
Cursor-written test-after.

Workflow:
1. **Hermes** writes the contract test in the test file, encoding the expected
   behavior from the brief. The test should FAIL against the current code (red).
2. **Hermes** runs the test and confirms it fails for the right reason (not a
   syntax error or import failure — the assertion itself must fail).
3. **Hermes** commits the test.
4. **Cursor** builds the implementation. The brief tells Cursor: "a test at
   `tests/test_X.py::test_Y` already encodes the expected behavior — your
   implementation must make it pass. Do NOT modify or delete this test."
5. **Hermes** verifies after build: the test passes, AND the test file is
   unchanged (`git diff` shows no modifications to the test Hermes wrote).

```python
# Written by Hermes, not Cursor:
def test_run_backtest_comparison_evidence_recorded():
    """run_backtest returns {comparison: [{label, metrics}]} — evidence ledger
    must contain the nested metrics, not silently drop them."""
    # This test should FAIL before the fix is built, then PASS after.
```

**Why this matters:** One B1-class bug (2026-08-03) went undetected through
5 commits and 2 review rounds because the test mocking `run_backtest` used a
stale payload shape (`{"metrics": {...}}`) instead of the real shape
(`{"comparison": [{"label": ..., "metrics": {...}}]}`). The test passed, the
real code was broken, and the agent silently replaced backtest answers with
fallback. A Hermes-written contract test at the boundary would have caught this
immediately — and Cursor couldn't have weakened it.

**For refactors** (moving code, deepening modules, deleting parallel
implementations): existing tests verify behavior preservation. The brief defines
the shape. Contract tests are optional — the existing test suite is the safety
net. But if a function's return shape changes, its callers' tests must be
updated to use the real shape, not a stale mock.

**For bug fixes:** Hermes writes a regression test first that reproduces the bug
(red), then Cursor fixes the implementation to make it pass. Same cross-model
principle: Hermes encodes "this is the correct behavior," Cursor makes it work.

| Change type | Who writes tests | When |
|---|---|---|
| New feature / safety-critical path | **Hermes** — contract test first | Before Cursor builds |
| Bug fix | **Hermes** — regression test first | Before Cursor fixes |
| Refactor (behavior preservation) | Existing tests | Already in place |

### Step 3 — Build loop (Cursor)

Dispatch Cursor with the builder model:

```bash
agent -p --force --model "cursor-grok-4.6-high" --sandbox disabled \
  "Read the brief at BRIEF.md and spec at SPEC.md. Implement fully. Run verification checks and report." \
  2>&1 | tail -5
```

Run with `background=true, notify_on_complete=true`. Working directory = project dir.

After the process exits, capture the dispatch result (delegate-result.v1 — see `references/dispatch-result-contract.md`): `python3 <skill-dir>/scripts/capture_dispatch_result.py --repo <project-dir> --task "build R1" --implementer cursor --model <model-that-ran> --exit-code <N> --report <report-file> --out /tmp/<proj>-dispatch-r1.json`. Verification and review start from this file's `touchedFiles`, not from memory.
- `cursor-grok-4.6-high` — default for implementation (user's canonical preference, full effort, normal speed — NOT fast)
- `composer-2.5` — faster, lighter tasks
- User may specify a different model — respect their choice

### Step 4 — Verify independently (Hermes)

**Do NOT trust the builder's self-report.** Run verification checks yourself:

1. Check files exist: `search_files` or `ls`
2. Run import checks: `python3 -c "from src.X import Y; print('OK')"`
3. Run schema tests: `python3 -c "from src.db import init_db; ..."`
4. Run any spec-defined verification commands
5. Check line counts, grep for expected patterns
6. **Check mock payload shapes match real outputs** — for each integration boundary
   listed in Step 2b, verify that the test uses the **actual payload shape** from the
   real function, not a hand-rolled approximation. Grep for the test's mock data and
   compare it to the real function's return. This is the check that would have caught
   the earlier B1-class bug (stale mock → silent evidence-gate failure).

If verification fails, the failing check is ground truth and **vetoes the build's "done" claim** — do not soften it into a review note. A failing test overrides any DONE/APPROVED signal, exactly as a public-test failure overrides the manager's verdict in GVS5H's orchestration loop. Immediately:

1. Write the failure (command, expected vs actual, first failing case) into the review file as a BLOCKING Hermes-verified issue.
2. If the loop continues, the fix brief must lead with this failing check as its acceptance criterion — the fix round is not complete until that exact command passes.
3. On re-review, re-run the vetoing check first; a round that fixes other findings but leaves the vetoing check red is not a passing round.

### Step 4b — Spec-compliance pre-check (Hermes, before Codex)

Before dispatching Codex, add a spec-compliance pass to Hermes verification. This catches issues Hermes traditionally misses — tests pass but the behavior doesn't match the spec.

1. **Re-read the spec's component specs** — cross-check each config field, API contract, and constraint against the implementation
2. **Check whitelists and permission boundaries** — are there keys/endpoints that should be read-only but are writable? Are there fields the spec says to exclude that are present?
3. **Verify graceful-degradation paths** — does the code skip when a dependency is missing, or does it crash? Tests often only test the happy path
4. **Check for spec-mentioned features that are missing entirely** — did the builder skip a task from the brief?
5. **Cross-project checklist** — run the 7-item reviewer checklist: time helpers, config sprawl, god files, O(N) lookups, FTS5 usage, OAuth scope enforcement, degradation paths

The pattern: Hermes verifies *does it run + do tests pass + does it match the spec*, Codex verifies *is it correct + are there edge cases*. Both layers are needed; neither is sufficient alone.

### Step 5 — Commit the build (before review)

```bash
cd <project-dir>
git add -A
git commit -m "build: initial implementation (Cursor Grok 4.6 High)"
```

Commit only what the dispatch result's `touchedFiles` captured (see `dispatch-result-contract.md`): any file present at commit time but absent from the capture is a scope deviation — adjudicate it, don't absorb it. This gives Codex a clean base to review against, and lets us diff fixes in later loops.

### Step 6 — Review (Codex)

Write a review prompt to `/tmp/review-prompt.md`:

```markdown
# Review Task: <project name>

Review the codebase at <project-dir>. Focus on:
- Data-integrity bugs (wrong types, silent data loss, mixed contracts)
- Edge cases the builder likely missed (empty inputs, concurrent access, error paths)
- Spec compliance (read SPEC.md — does the code match the spec?)
- Security (auth bypass, injection, data leakage between tenants)
- Missing error handling, missing validation

Read SPEC.md first, then review each file in src/.

Output a structured review:
- BLOCKING: must fix before ship
- MAJOR: should fix before ship
- MINOR: polish, not blocking
- NIT: style/cleanup

For each issue: file, line (approx), description, suggested fix.

Do NOT make file changes — review only.
```

**Delta-round prompt shape (signal control):** every re-review gets the same three tasks, explicitly:
1. Verify your previous findings are fixed — name them (list the finding IDs).
2. Hunt for NEW issues **introduced by the fixes themselves** — this question must be literal in the prompt; a reviewer told only to "verify fixes" will confirm them and stop hunting.
3. Verdict: approve or request changes, numbered findings.

Plus the closer: "Do not re-report fixed items." Without this scoping, reviewers re-litigate closed items every round and new signal drowns.

**Fix-brief acceptance gates:** every fix brief carries (a) the acceptance-criterion probes for the fix itself, and (b) at least one standing regression check that must NOT change — e.g. a byte-identical render probe against the PRE-FEATURE baseline (`git show <pre-feature-commit>:<file>`), a spec-named empty-state behavior, a live-install divergence probe. A fix round that satisfies all item probes while breaking a standing property is a failed round: a trend-CSS-gate fix was verified byte-identical against the PREVIOUS round's renderer (which already contained the CSS) instead of the commit BEFORE the feature series began — the wrong baseline reported a false diff and cost a re-derivation before the true baseline was found. Always diff byte-identity against the pre-feature commit, never the previous fix round.

**Post-fix confirmation pass (before ship):** after a fix round, dispatch the ORIGINAL reviewer scoped to the fix diff plus the files it touches: "verify each of your N findings is resolved — not superficially patched — RESOLVED/NOT-RESOLVED per finding, then a final SHIP/DO-NOT-SHIP verdict." A fix round can self-verify green (all tests passing, smoke checks clean) while leaving real residuals: the confirmation pass exists because the builder's fix verification and the reviewer's adversarial probe are different activities. Reproduce every NOT-RESOLVED claim yourself before dispatching the next fix round (see Pitfalls — "Reproduce every reviewer finding before it enters a fix brief") — reproduction separates real residuals from reviewer error and hands the builder exact probe scripts.

Dispatch Codex:

```bash
codex exec --sandbox danger-full-access \
  "Read /tmp/review-prompt.md and review the codebase. Output your review as text." \
  2>&1 | tail -800
```

Run with `background=true, pty=true, notify_on_complete=true`.

**Codex sandbox note:** `~/.hermes/` paths need `--sandbox danger-full-access`. For paths outside `~/.hermes/`, `--sandbox read-only` works for review-only, but can't run tests. Use `--sandbox workspace-write` if tests need to run.

**Codex output:** May be truncated with `tail -800`. Collect full output via `process(action="log", session_id=<id>, limit=800)`. If Codex just echoes file content without analysis, retry with a more explicit prompt.

### Step 7 — Synthesize review (Hermes)

Combine:
- Hermes verification results (Step 4)
- Codex review findings (Step 6)

Produce a structured review:

```markdown
## Review Round N — <project>

### Verdict: APPROVE / APPROVE WITH FIX / REQUEST CHANGES

### Hermes Verification
| Check | Result |
|---|---|
| Import check | ✅/❌ |
| Schema init | ✅/❌ |
| Chunker test | ✅/❌ |
| ... | ... |

### Codex Findings
| # | Severity | File | Issue | Suggested Fix |
|---|---|---|---|---|
| 1 | BLOCKING | ... | ... | ... |

### Combined Issues (deduplicated, Hermes-verified)
...

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Step 8 — Fix loop (if issues found + loops remaining)

Write a fix brief for Cursor:

```bash
agent -p --force --model "cursor-grok-4.6-high" --sandbox disabled \
  "Read the review at /tmp/review-N.md. Fix every BLOCKING and MAJOR issue. Read the spec at SPEC.md for context. Do NOT change anything not mentioned in the review. Run verification checks after fixing." \
  2>&1 | tail -5
```

Run with `background=true, notify_on_complete=true`.

After Cursor finishes:
1. Re-run Hermes verification (Step 4)
2. `git add -A && git commit -m "fix: round N issues (Cursor Grok 4.6 High)"`
3. Dispatch Codex re-review (Step 6, but pass prior review file)
4. Synthesize re-review (Step 7)

### Step 9 — Loop or deliver

- **No BLOCKING issues** → deliver final verdict (APPROVE or APPROVE WITH FIX)
- **BLOCKING issues remain + loops remaining** → go to Step 8
- **BLOCKING issues remain + no loops remaining** → deliver REQUEST CHANGES with remaining issues

### Step 10 — Review gate before push

**NEVER push without a Codex review pass.** The user requires: build → commit → Codex review → fix → push. A prior session pushed code without a separate Codex review and the user corrected it explicitly: "Codex review first before push please."

A green live smoke or e2e run does NOT satisfy this gate: it proves the feature works under production conditions, not that the code is review-clean. Run the review before merge or push even when the smoke evidence is fresh and complete — a verified runtime run is not review approval, and closing the loop without it costs a full user-visible correction round.

The gate applies to every batch, not just the final one. In multi-batch work:
1. Commit each batch locally (Step 5)
2. After all batches complete, dispatch ONE Codex review covering the full diff (`git diff <base>..HEAD`)
3. Fix any Codex findings (NIT/MINOR: Hermes may apply directly; MAJOR/BLOCKING: dispatch Cursor)
4. Push only after Codex approves

Alternatively, review each batch separately if the diff is large. The key: no push until Codex has reviewed and the review is clean or only has NITs.

### Step 11 — Push and monitor CI

After Codex approves and fixes are committed:

```bash
git push origin <branch>
```

Before pushing, embed **evidence pairs** (see `references/evidence-pairs.md`): capture the before state while reproducing the issue, the after with the same method, and put the pair in the PR body or delivery message. No visual surface → measured numbers or output pairs.

Monitor CI:
```bash
gh run list --limit 1 --json status,conclusion
```

Wait for `conclusion: "success"` before telling the user the work is shipped. If CI fails, investigate before reporting success.

## Multi-Batch Work

When a phase has more than 3 tasks, batch them by dependency and risk. See `references/multi-batch-sequencing.md` for the full pattern and worked examples.

For multi-batch loops, ALSO create the persistent loop plan (Phase 0, before the first dispatch): `loop-plan.md` / `loop-findings.md` / `loop-progress.md` per `references/persistent-loop-plan.md`, and update it after every dispatch capture, review verdict, and commit. Resume every new session with `scripts/loop_plan_check.py loop-plan.md` — the resume pointer replaces memory-based resumption. Gate the loop's completion with `--gate` before delivering.

When the task is replacing N existing modules with a new module (e.g. migrating file-based state stores to SQLite WAL), the brief must include a full caller inventory — every file that imports from the modules being deleted. See `references/full-module-replacement-scoping.md` for the scoping methodology and SQLite WAL migration pattern.

Key rules:
- 2-3 tasks per batch, 10-30 new tests per batch
- Highest-risk batch first
- Verify independently between batches (do NOT trust Cursor's self-report)
- Commit between batches (gives Codex clean diff boundaries)
- Write the next brief while the current batch builds
- Codex review covers the full diff after all batches complete (or per-batch if diff is large)

For a release-hardening-shaped cycle (security gap + backup format + docs +
constraints run as parallel same-repo batches with red contract tests first),
see `references/beta-gate-release-hardening.md`.

For the cycle-principles distilled from those worked examples (one missing
responsibility, reviewer-contradicts-your-own-rule, deferred findings as
design questions), see `references/review-findings-adjudication.md`.

For integrating an external party's field briefing (a deployment operator's
report of live failures + suggested upstream fixes) into this loop —
verify-then-trust, red tests extending the briefing's named test contract,
and the traps (fixes at the wrong layer test green and do nothing;
subprocess "missing-key" tests that secretly exercise the with-key branch) —
see `references/field-briefing-integration.md`.

## Convergence Pattern

Each round should produce strictly fewer findings:

| Round | BLOCKING | MAJOR | MINOR | Fixer |
|---|---|---|---|---|
| R1 | 4-6 | 5-10 | 5-15 | Cursor |
| R2 | 1-3 | 2-5 | 3-8 | Cursor |
| R3 | 0-1 | 1-3 | 2-5 | Cursor |

If findings INCREASE between rounds, the fixes introduced regressions. Stop and investigate before continuing.

Exception — deep security/correctness sweeps: a strong reviewer given free rein (e.g. Opus thinking-high on a parser/extractor) can legitimately return MORE findings each early round — round 1 surfaced ~35, a later delta round ~22, another ~19, mostly NEW edge cases in code the earlier rounds never probed, not regressions. Convergence still held eventually. When findings grow but the character shifts (new areas probed vs. old items reopened), treat it as a deep sweep still in progress, not a regression signal; the regression alarm is for findings REOPENING closed items. Adjudicate every new finding before fixing, and remember the reviewer's report is a snapshot — re-probe against current HEAD (see Pitfalls — "Re-adjudicate reviewer findings against current HEAD").

## Cross-Model Diversity

The key principle: **the reviewer should be a different model than the builder.**

- Builder: `cursor-grok-4.6-high` (Grok 4.7 High)
- Reviewer: `codex` (GPT-6 Sol, effort high)

Different models have different blind spots. Grok may miss what GPT catches and vice versa. This is load-bearing — a single-model build+review catches fewer issues than cross-model.

If the user specifies different models, respect their choice. The pattern works with any builder/reviewer pair.

## Bot Mode Integration

Hermes Bot Mode is enabled on this install. Two specialist bots are available as teammates:

| Bot | Profile | Model | Role | Tools |
|-----|---------|-------|------|-------|
| **Coder** | `coder` | GPT-6 Sol (OpenAI Codex) | Builds features, fixes bugs, writes tests | `cursor-cli` only — drives Cursor CLI with `cursor-grok-4.6-high` |
| **Code Reviewer** | `code_reviewer` | GPT-6 Sol (OpenAI Codex) | Independent review | `codex` (GPT-6 Sol, effort high), `claude-code` (Opus 5.5), `cursor-cli` (Grok 4.7) — picks model per review type |

Both bots run on GPT-6 Sol as their main model. Both share the main `~/.hermes/skills/` bank via symlink (no per-profile skill maintenance). The BM25 skill-retrieval plugin serves all profiles. Toolsets: `terminal`, `file`, `code_execution`.

### Delegating to a bot from the orchestrator

Send a message to a bot's canonical Bot Chat:

```bash
hermes -p coder chat --in ~ -c "Bot Chat" --create-if-missing -Q -q \
  "Message from 🤖 hermes (@hermes): <task description>"
```

Run with `background=true, notify_on_complete=true`. The reply arrives as a new message when the bot finishes.

### When to use bots vs delegate_task

| | `delegate_task` | Bot Mode (`hermes -p <bot>`) |
|-|-----------------|-------------------------------|
| Isolation | Separate conversation, same process | Fully independent profile + model |
| Model | Same model as parent | Bot's own model (GPT-6 Sol) |
| Tool access | Subset of parent tools | Bot's own toolset config |
| Persistence | Lost when parent exits | Bot Chat sessions are eternal |
| Use case | Quick parallel subtasks | Cross-model build/review with persistent context |

### Build-review loop with bots

The build-review loop can now use bots instead of raw CLI dispatch:

1. **Build**: message `@coder` with the brief — it runs Cursor CLI to implement
2. **Review**: message `@code_reviewer` with the review prompt — it runs Codex + Claude Code to review
3. **Fix**: message `@coder` with the review findings
4. **Re-review**: message `@code_reviewer` for the re-review

This gives each bot persistent context across rounds (their Bot Chat remembers prior messages), and the cross-model diversity is built into the bot profiles.

### Bot-to-bot handoff

Bots can message each other directly. The orchestrator can ask Coder to send its output to Code Reviewer:

```
hermes -p coder chat -c "Bot Chat" -Q -q \
  "Message from 🤖 hermes (@hermes): Build the feature, then send the diff to @code_reviewer for review."
```

The messaging protocol is auto-injected into Bot Chat sessions via `agent.bot_mode_protocol` (default: true). No manual setup needed.

## Final Round Diversity

For the final review round, consider using a THIRD model (different from both builder and reviewer) for maximum diversity. Options:
- `claude-code` (Claude Opus 5.5 — current Opus generation) — strong at cross-file analysis and architecture
- `cursor-cli` with a different model — e.g. `claude-opus-5-5-medium` if the builder used Grok

This is optional — the user may be satisfied with builder+reviewer diversity alone.

## Quick Reference — User Says

| User says | What to do |
|---|---|
| "review loop 2 times" | Build → review → fix → re-review (2 full cycles) |
| "review loop 3 times" | Build → review → fix → re-review → fix → re-review (3 cycles) |
| "build then review with codex" | Build (Cursor) → review (Codex), 1 cycle |
| "have cursor build, codex review" | Same as above — Cursor builds, Codex reviews |
| "fix and re-review" | Fix (Cursor) → re-review (Codex), continuing from prior review |
| "review loop until clean" | Keep looping until 0 BLOCKING issues (cap at 5 rounds) |

## Pitfalls

Core loop-discipline rules that apply to every run. Clustered rules split from this list in the
2026-10-16 refactor — re-read the covering file when the case applies:

| Case you hit | Read |
|---|---|
| Dispatching, polling, parallel builds, model pins, brief races | `references/pitfalls-dispatch-semantics.md` |
| Fix rounds: wrong-layer fixes, red-test triage, gate probes, two-sided and live verification | `references/pitfalls-fix-round-verification.md` |
| CLI flags, git mechanics, contract-test mechanics, error classification, push hygiene | `references/tool-mechanics-pitfalls.md` |
| Security property tests: setdefault bypass, per-surface authorization, inert tests, exempt paths, handler splits | `references/security-property-tests.md` |
| A feature wired into the documented path is dead in production | `references/production-reachability-review.md` |
| Reviewer BLOCKINGs against the dispatch spec, contract-test contradictions | `references/review-findings-adjudication.md` |
| Deferred findings as design questions, hazard-class design-away, reviewer-contradicts-your-own-rule | `references/review-findings-adjudication.md` |
| Data integrity, migration safety, idempotency, CLI contract probes | `references/data-integrity-principles.md` |

Symptom index for rules whose bodies live in the files above:
- A passing test that checks nothing is worse than a missing one → `security-property-tests.md` P1-P3
- Exempt paths in property tests must have a real separate test → `security-property-tests.md` P4
- Split argument-dispatching handlers for honest scope classification → `security-property-tests.md` P5

1. **Don't trust the builder's self-report** — "all checks passed" from Cursor is a claim, not a fact. Run checks yourself.

2. **Findings increasing between rounds = regressions** — stop and investigate before continuing.

3. **Commit between rounds** — `git add -A && git commit` after each fix round so Codex can diff against the prior state.

4. **Builder and reviewer must be different models** — same model reviewing its own work has blind spots. Cross-model diversity is the whole point.

5. **Stale mock payloads mask integration bugs** — when a test mocks a function's return shape, and the real function's return shape changes, the test still passes against the stale mock. This is invisible to all review rounds unless someone explicitly compares the mock to the real output. Always verify mock payload shapes match the real function's actual return at each integration boundary (Step 4 check #6). One B1-class bug (5 commits, 2 review rounds, silent agent failure) was caused by exactly this.

6. **The orchestrator NEVER hand-codes fixes — not even one-line patches** — when `build-review-loop` is the active workflow, Hermes dispatches ALL code changes through Cursor CLI. No exceptions for "it's just a CSP header" or "it's a one-line docstring fix." The user corrected this mid-build: the orchestrator read the review findings and started patching a report module directly. The user said "didnt use cursor cli?" — Hermes had to stop, write a brief for the remaining fixes, and dispatch Cursor. The rationale: (a) the user chose this workflow specifically for cross-model diversity, so bypassing it defeats the purpose; (b) even small fixes can introduce regressions that only the reviewer catches; (c) dispatching through Cursor creates a commit boundary that Codex can diff against. If a fix is truly too small to justify a full Cursor dispatch (e.g. a typo in a comment), say so to the user and ask — do not silently hand-code it.

7. **Audit existing API surface before implementing "full CRUD" from a roadmap** — roadmaps describe desired state, not current state. Before dispatching a builder to "add CRUD endpoints", grep the existing routers and engine functions. One build assumed missing CRUD for all priority entities, but the REST API already had GET/POST/action endpoints. The actual gap was only PATCH (update) for draft records. Always grep the existing routers (`@router.` decorators) and the engine functions of every module before writing the brief.

8. **Cursor CLI is the BUILDER, Codex is the REVIEWER — never swap roles** — when the user says "have cursor and Claude code review", the reviewers are Codex (GPT-6 Sol) and Claude Code (Opus). Cursor CLI (Grok) is the builder/fixer. The user corrected this explicitly in Aug 2026: "Reviewed should be codex not cursor" when I dispatched Cursor as a reviewer. The cross-model diversity principle requires the reviewer to be a DIFFERENT model than the builder. If Cursor built it, Cursor cannot review it — same-model review shares blind spots. The default reviewer pair is Codex + Opus. Cursor is only used for fixes after the review identifies findings. If the user says "review", dispatch Codex and/or Claude Code. If the user says "fix", dispatch Cursor.

9. **Round-2 reviews audit the previous round's FIXES — expect new findings in freshly changed code, and verify them before re-fixing** — when an external review returns after a fix round (e.g. "10 Fixed / 3 New"), the New findings are almost always regressions introduced by the fixes themselves. One round-2 review found exactly three: (a) the CSV formula-injection guard was lifted into a shared helper and applied to every exporter, but its prefix list contained `-`, so every negative number in six export surfaces (including a bank-upload CSV) exported as text `'-700` — a guard written for mostly-text list reports was inherited unchanged by financial exports where negatives are half the data; (b) a totals rewrite changed `total_debits`/`total_credits` from gross column sums to net-by-account while the line columns stayed gross, and the same commit patched the two DISPLAY surfaces (web template + CSV exporter) to sum the lines themselves — resolving the display but splitting the answer: JSON API and MCP returned one foot, UI and CSV another; (c) validation added at read time without adding the matching check at creation — the CLI could still issue names the API refuses to serve. Two structural lessons: **a value computed on one surface and re-derived on others will drift** — compute it once at the source and make every surface read the same field (the review's direction: the total should be computed once, in the shared engine function, not independently in the template and the CSV exporter); **validation added at one gate must be checked against every other gate for the same object** — validate at creation, not just at read. Also note the review's meta-observation: all three new findings lived in code that HAD tests added in that round — the tests simply lacked a negative number, a two-sided account, and an uppercase entity name. When fixing, add the missing assertion cases, not just the fix. A fourth regression mechanism from a later delta re-review: **a bulk copy step added to satisfy one finding can silently undo a validation fix from another** — a 'copy top-level files' change copied the source's own config files over the validated, credential-filtered manifests the same round had generated, reopening a BLOCKING the review had already closed. When a fix round adds any bulk copy or generation step, exclude tool-owned output filenames from the copy loop and generate validated outputs AFTER any bulk copy, never before.

10. **Multi-candidate external reviews: get scope decision before dispatching** — when an external review returns multiple refactor candidates (e.g. "4 deepening candidates, top recommendation X"), do NOT start building the recommended one immediately. Summarise each candidate with verified evidence, give your read, then ask the user which scope to run (top-only / top+paired / all-in-sequence / discuss). A user may say "all four in sequence" — which turns one batch into a 5-batch cycle with a different commit budget. Scope is the user's call; sequence and batching are yours. Validated on a 4-candidate deepening review; the user chose all four in sequence.

11. **Review findings that contradict the brief's design assumption — verify in source, then re-derive the fix rule, before dispatching** — when a reviewer flags a design decision the orchestrator itself encoded (Opus's B1: "v2 skip is wrong"), do not reflexively forward the finding to the builder. First verify the claim against source (here: `_ensure_hash_backfill` at db.py:487 runs before `_ensure_dr_cr_repair` at 488 — confirmed), then re-derive the correct rule (historical v2 digests attested repaired values → repair amounts + keep description converges with the chain), THEN write the red tests encoding the corrected rule and only then dispatch. The corrected insight went into the brief as the fix's central rationale — a builder given only "make the review finding go away" might have implemented a hash-rewrite (breaking tamper-evidence) instead of the value-convergence fix. Also: split review findings into fix-now (verified, cheap, testable) vs defer-with-record (need product decisions — rename atomicity, MCP scoping), and write the deferrals into the ADR's "Known deferred items" section in the same brief so they don't evaporate.

12. **Deferred review findings need a written destination in the same brief** — when a dual review returns more findings than can be fixed in one round (Opus: 8 MAJOR), do not silently drop the ones you skip. Split into fix-now vs defer-with-reason, and instruct the builder to write the deferrals into a durable in-repo document (e.g. an ADR section titled "Known deferred items") with one line each. This converts "we didn't get to it" into an auditable backlog the next session can pick up — and stops the NEXT review round from re-reporting the same items as new findings. Validate the builder's resolution table independently before committing: re-run the affected suites yourself and diff the contract-test file to confirm the builder didn't touch it. Validated on a deepening-cycle fix round 3: the builder's claimed test totals were independently reproduced before commit.

13. **A builder's "tests pass" mid-build is not completion — wait for the full-suite verification it was briefed to run** — when a long build (25-35 min) is briefed to run the full suite before reporting, intermediate probes (targeted suites passing at minute 25) are NOT the finish line. The builder may spend its remaining time on the full-suite verification + report writing. Wait for the process to exit (notify_on_complete fires); then verify. Do not commit based on mid-build probes, and do not kill a healthy long-running build to "check progress" — check progress with read-only probes (pytest on the contract-test file, git status) instead. Validated on a round-4 build: contract tests green at the 25-minute mark; the builder ran another 10 minutes of full-suite verification before exiting cleanly.

14. **Test fixtures must never reference real companies, clients, or the user's employer** — when writing contract tests or examples, use neutral fictional names ("Foo Holdings Ltd", "Acme"), never names connected to the user's actual world. The user corrected this mid-build: a review artifact used the user's real employer name, and the user interrupted the build to have every occurrence removed. Real names in fixtures leak business relationships into pushed repos, search indexes, and AI training data. Before committing any test file, scan fixtures for names that match the user's employers, clients, or domains mentioned in conversation/memory; replace with neutral fictions. Save durable "never use X" facts to memory AND treat every future fixture as suspect until checked.

15. **The reviewer commits — the implementer never commits** — the commit belongs to the party that verified the work. Builders (Cursor) run with commit capability disabled; reviewers (Codex/Opus) run read-only on the diff. A builder that lands a commit removes the review boundary — the reviewer can no longer diff the work against a clean base. Related discipline (ported from delegate-skills): between dispatch and the orchestrator's commit, the uncommitted working tree is the implementer's work — the only copy. Never run `git checkout`/`reset`/`clean`/branch switch before inspecting; `git status` + `git diff` + `git diff --cached`, open untracked files directly (no diff shows them), and only then decide — including a legitimate discard. Validated Sep 2026 on the delegate-skills port.

16. **A running builder reads its brief once at dispatch — superseding the brief in-place is a race, not a redirect** — the builder reads the brief file at startup; overwriting it mid-flight only redirects the builder if it happens to re-read later. A round where this gamble lost delivered the previous round's scope entirely, and the remaining findings needed a second dispatch anyway. Rule: never rely on in-place brief supersede to change a dispatched builder's scope. Let the round finish, verify what it actually did, then write a fresh numbered brief covering ONLY the remaining items with explicit context ("the previous round covered X — do not redo it"). After any ambiguous round, grep the builder's log for which brief it read before judging its output, and probe a canary behavior that distinguishes old-brief from new-brief work (e.g. the headline finding still reproducing = stale brief).

   **Mid-build user steers are scope changes, not hand-edit invitations.** When the user sends a correction or addition while a build runs, do not edit the built files directly to absorb it — that bypasses the delegation contract AND leaves the brief stale, so the reviewer later flags a brief/code conflict that costs a round. Queue the steer: let the round finish, verify, add the steer to the fix brief (or a fresh numbered brief) with its acceptance criteria, and update BRIEF.md to match the new scope in the same commit. The brief, the code, and the review must agree on scope before the next dispatch.

17. **Re-adjudicate reviewer findings against current HEAD, probing through the public entry point** — a reviewer's report is a snapshot of an earlier commit; if fix commits landed after the reviewer started, its "regression" claims may describe code already fixed. Re-run the reviewer's exact probe against HEAD before writing a fix brief. Probe through the PUBLIC entry point (the CLI command or top-level function), never by calling the guard helper in isolation: an isolated helper call can show a leak the guarded call path already prevents, and a single guarded-path probe can miss a leak on a sibling call path for the same data class (e.g. env vs headers in the same server converter) — check every call site of the guard before declaring an item closed.

18. **Verify the verification harness before reporting a fix as failed** — when an independent re-probe says a fix did NOT land, first rule out harness bugs: a probe can compare the wrong shape (parsed dict vs field: `safe_load('description: "no"')` returns a dict — compare `.get('description')`, not the dict), count intended behaviour as an anomaly (a tokenised constant after a fingerprint fix), or probe an isolated helper instead of the public path (see #36). The agent-skills #12/#13 loop (Sep 2026) produced a 0/9 yaml-roundtrip reading and a 500/500 churn reading that were BOTH orchestrator harness bugs; the builder's fixes were correct. Rule: before relaying "the fix didn't land", re-derive what the probe actually asserts and rerun with a corrected probe; never adjudicate a builder's fix off a single suspicious probe. Also rule out missing probe preconditions: a reproduction probe that skips setup the real path requires (registered capability facts, seeded state rows) makes correct code look broken — derive the probe's fixture from the passing test's setup, not a minimal guess. Validated on an orchestrator verification round: a degraded-skip probe without registered facts showed no skip while the dedicated test passed.

19. **Reproduce every reviewer finding before it enters a fix brief** — run the reviewer's exact probe (or a minimal equivalent) against current HEAD before dispatching. Three payoffs, all observed in the #12/#13 loop (Sep 2026): (a) wrong claims get caught BEFORE costing a builder round — the hardlink data-loss claim failed to reproduce twice under the orchestrator's probes and was twice re-verified by the builder before the real failure mode surfaced; (b) builders get exact probe scripts instead of prose, so they verify with the same evidence; (c) each reproduced finding becomes a permanent regression test in the same round. A finding that cannot be reproduced gets marked "verify-first" in the brief with the probe evidence attached — never silently accepted, never silently dropped.

20. **Assume fixes introduce findings — probe adjacent logic on every fix round** — from round 3 onward in the #12/#13 loop, roughly half of all findings were regressions caused by EARLIER fixes: tighter arg validation added → validation error text echoed the raw secret into the report (G1); row-collapse fix added → unique nested content destroyed (D3); constant-promotion fix added → over-fired on repeating instances (E1); schema-validation fix added → bulk copy step overwrote the validated manifests (F1/R1). Rule: every fix brief requires (a) a regression test for the fixed finding AND (b) a probe of the immediately adjacent behaviors — the same guard's sibling call sites, the same rule's boundary values, anything sharing the mutated function. The convergence exception (deep sweeps) covers reviewers finding NEW code paths; this pitfall covers YOUR fixes breaking boundaries they touch. Both are normal; neither means the loop is failing.

21. **Verify two-sided fixes on BOTH sides** — a fix round can satisfy the probe on the surface you test and leave the sibling surface broken: a divergence disclosure was rendered in text but NOT in HTML because only the text-renderer branch was updated. When a finding spans multiple output surfaces (text/html/markdown) or both persistence paths (module function vs method), probe each surface separately in the same verification pass. Single-surface verification declared a round verified while the HTML path stayed silent until the next review round caught it.

22. **Mid-build user requirement additions go into the NEXT numbered brief — never hand-edited into the running build; the spec update lands in the SAME commit round** — when the user adds or changes requirements while a build is in flight: (1) capture the addition in SPEC.md immediately with NEW numbered subsections (e.g. §3b, §6b) rather than rewriting existing sections — the in-flight round read the old spec, and numbered additions make the delta unambiguous to the next round and the reviewer; (2) update endpoint lists, data model, and UI sections in the same spec edit so it stays internally consistent (a column-map change must propagate to the API contract and data model in the same edit — an incomplete spec edit costs a review round); (3) let the in-flight round finish on its original brief; (4) write a FRESH numbered brief (BRIEF2.md — never overwrite the brief a dispatched builder already read, see 'A running builder reads its brief once at dispatch') naming the prior commit as the baseline ("extend it, do not rewrite from scratch") and enumerating ONLY the delta. Never let a user addition silently ride along un-specified — an undocumented feature is a review finding waiting to happen.

23. **UI-restructure rounds need a fresh-session browser smoke by the orchestrator — builders cannot run a live browser** — a filter/layout change can pass every pytest HTML assertion and JS DOM-stub while breaking the real first-load path: the default-selection state (e.g. "no category selected" renders an empty list on a fresh session) is exactly the state stubs never exercise. Builders routinely report "could not click through a live browser in this session" — treat that as a verification gap the ORCHESTRATOR owns, not a residual risk to mention in the delivery. After deploy, drive the real URL headless as a FRESH visitor (login via in-page fetch, reload, count rendered list items, read the control's value) before committing or calling the round shipped. Also make "empty list" vs "no search matches" distinguishable states for staff — they look identical to a filtered-list UI but mean different things.

 44. **Read back long spec/brief writes before attesting and dispatching** — a long file write can land garbled or truncated (mid-write corruption); the write tool's 'verified' flag confirms bytes on disk, not that the CONTENT is coherent. A builder reads the brief once at startup: a garbled spec silently scopes the entire round wrong, and `attest_file.py attest` on the garbled file locks the corruption in as the tamper-evidence baseline. Rule: after writing any SPEC.md/BRIEF.md you intend to dispatch, verify the body reads clean end-to-end (spot-check head, middle, and tail via read_file or the write result) and re-write on any garble — BEFORE attesting, committing, or dispatching. Never attest a file you have not read since the last write.

25. **Derive spec data shapes from the real producers, not from your mental model — a wrong-shape spec builds dead code that its own tests pass** — when a feature snapshots or aggregates data produced elsewhere, read the producer's actual return statements and copy their literal shapes into SPEC.md: field names, flat vs nested, numeric vs string (one briefing collector returned `"outstanding_ar": "0"` as a STRING — the trend flattener silently dropped it everywhere). A spec written from mental model produces three failures at once: aggregation logic that never fires on real payloads, counters probing field names that exist nowhere in the repo, and contract tests built from the same wrong spec that pass against fixtures. The builder implements the spec literally and will not flag the mismatch — that is correct builder behavior, so the obligation is on the spec author. Before writing SPEC.md, grep each producer's return statement and one live record; if a mismatch surfaces at review, reconcile with a probe of a real payload and fix at the producer or the spec, not with a silent coercion in the middle. Validated on a mid-build review round (reviewer finding: "the spec described shapes the codebase doesn't produce; the builder implemented the spec literally").

26. **Verify a dispatch exists before reporting it — an announced-but-never-executed dispatch surfaces only at status time** — "dispatching the builder now" in a delivery message is not a dispatch; if the turn ends without the tool call, the user's next "status?" finds no process and the workflow has silently stalled. Before any "builder running" or "builder dispatched" line, confirm the process exists (pgrep the CLI command or check the background-process list). Pair with tool-mechanics #3: a `--print` dispatch missing `--trust` exits 0 immediately, so "completed normally" on a suspiciously fast build means it never ran.

## Red Flags

Observable symptoms, each mapping to the rule that fixes it. The rule's single source of truth
lives in **## Pitfalls** (loop discipline), **## Workflow** (steps), or the **Verification Checklist** —
do not add symptom-only duplicates of those here. The items below are rules that exist nowhere else:

- BLOCKING issues ignored because "loops exhausted" — deliver REQUEST CHANGES, not silent approval. The loop budget bounds rework, not honesty.
- Missing role gates on write endpoints — `require_auth` is not `require_write_role`. Authentication without authorization is an open endpoint.
- A value computed on one surface and re-derived on others — totals summed in template + exporter while the DB holds another number. Compute once, propagate the result.
- A guard/sanitizer applied unconditionally to a field whose domain includes values that look like the threat — over-matching guards corrupt legitimate data. Parse and match the actual pattern.
- Validation added at one gate (read/resolve) without checking every other gate (creation/registration) for the same invariant.
- A refusal/degradation error that states the cause but not the remedy — name the flag or action that fixes it.
- Multi-step state writes (register + set label) where the idempotent re-run cannot repair a mid-sequence failure — make each step independently idempotent.
- Build artifacts (BRIEF.md, review diffs, review outputs) committed to the repo root — these are internal scratch, keep them out of the repo (see Release Hygiene Checklist).

## Verification Checklist

- [ ] Brief/spec written and accessible to both builder and reviewer
- [ ] Brief and any Hermes-written contract-test files attested before dispatch (`attest_file.py attest`) and verified after the build exits — TAMPERED is a BLOCKING finding (see `tool-mechanics-pitfalls.md` — contract tests satisfied by unsanctioned design changes); re-attest after ANY orchestrator-side post-build edit of those tests, and commit the re-attestation in the same commit as the test fix
- [ ] Multi-batch loop: loop-plan.md created at Phase 0, updated after every state change, every session resumed via `loop_plan_check.py` (not memory), completion gated with `--gate`
- [ ] Git repo initialized before Codex review
- [ ] Builder dispatched with correct model (`cursor-grok-4.6-high` unless user specifies)
- [ ] Hermes runs verification checks independently (not trusting builder self-report)
- [ ] Sample-test veto honored: any failing Hermes verification auto-becomes a BLOCKING issue and the fix brief's acceptance criterion (Step 4)
- [ ] Build committed before review
- [ ] Reviewer dispatched with different model than builder
- [ ] Review prompt written to `/tmp/review-prompt.md` (not inlined)
- [ ] Findings synthesized by Hermes (deduped, severity-rated)
- [ ] Fixes committed between rounds
- [ ] Each round produces fewer findings than the last (convergence check)
- [ ] Final verdict delivered (APPROVE / APPROVE WITH FIX / REQUEST CHANGES)
- [ ] If N loops requested: exactly N review rounds completed
- [ ] Integration boundaries identified (Step 2b) — brief lists each changed shape
- [ ] Mock payload shapes verified against real outputs (Step 4 check #6)
- [ ] Contract tests written by **Hermes** for safety-critical paths (evidence gates, trading logic, agent answers) — committed before Cursor builds
- [ ] Hermes-written tests intact after build (`git diff` shows no Cursor modifications to test files Hermes authored)
- [ ] Codex review completed BEFORE push (Step 10) — no push without review
- [ ] Evidence pairs embedded in the delivery: before captured during reproduction, after with the same method, pair in the PR body or delivery message
- [ ] CI green (`conclusion: "success"`) before reporting shipped
- [ ] Cross-surface property tests (isolation, scope, role) written when adding a new surface or before adding a new vertical module — see `references/security-property-tests.md`
- [ ] Property tests actually execute — assert minimum execution count; use in-process registry calls, not subprocess with name transforms; catch `SystemExit` separately from `Exception`
- [ ] Exempted routes in property tests have a real separate test covering the same property — not just a comment claiming "tested separately"
- [ ] Argument-dispatching handlers split into per-subcommand handlers with honest scope classification — no handler whose scope depends on a runtime argument
- [ ] DB-level triggers enforce accounting invariants (factor sums, balance constraints) — not just application-level checks
- [ ] Polymorphic link tables use TEXT for target_id — supports both integer IDs and string account codes
- [ ] Cross-company polymorphic links blocked — target_id == company_id for company targets
- [ ] SQLite table-rebuild migrations preserve dependent rows — rename dependent tables aside before DROP+rebuild, never rely on PRAGMA foreign_keys=OFF inside a transaction
- [ ] Bulk operations are atomic — pre-validate all items, single-transaction insert, no per-item commits
- [ ] Base-currency exchange rates forced to 1 — reject non-unit rates when transaction_currency == reporting_currency
- [ ] Opus 529 handled with `--fallback-model sonnet` retry — review completes even when Opus is overloaded
- [ ] Cursor API resource_exhausted handled — either retry later or Hermes builds directly with contract tests
- [ ] Dual review findings synthesized into cross-model overlap table — both reviewers' findings addressed
- [ ] Tests validating old mechanisms updated to validate new mechanisms after architecture changes
- [ ] Local installation updated after push (stash, pull, resolve, verify)
- [ ] No build artifacts committed to repo root (BRIEF.md, review diffs, review outputs)
- [ ] Idempotent/registration paths suppress duplicates in SQL (`ON CONFLICT ... DO NOTHING`), not by catching IntegrityError — PG aborts the transaction (see Red Flags — idempotent multi-step writes)
- [ ] "Exists" fast paths verify the existing object matches the request; mismatch returns an error naming the occupied resource (see Red Flags)
- [ ] Refusal errors name the remedy (flag/command), not just the cause (see Red Flags)
- [ ] Release hygiene checklist (Step 12) completed before tagging or releasing

## Release Hygiene Checklist (Step 12 — before tagging or releasing)

This is NOT engineering. It is the mechanical release hygiene that recurs every
release. Skipping it produces a tag that points at the wrong commit, version
pins that disagree with the tag, a missing CHANGELOG, and build artifacts
committed to the repo root. The user has corrected this pattern multiple times.

Run these steps after all review fixes are committed and CI is green, BEFORE
creating or moving a tag or publishing a release:

### 1. Bump ALL version pins

Search for the old version string across ALL files, not just the obvious ones:

```bash
grep -rn "0\.4\.0" plugin.yaml pyproject.toml VERSION README.md .claude-plugin/
```

Files that typically carry version pins:
- `plugin.yaml` (version field)
- `pyproject.toml` (version field)
- the entrypoint script (VERSION constant)
- `README.md` (status line)
- `.claude-plugin/plugin.json` (version field)
- `.claude-plugin/marketplace.json` (version field)
- Any `VERSION` file if one exists

Update ALL of them in one commit. The `test_release_versions_agree` test
checks internal consistency (all pins agree with each other) but does NOT
check against the git tag. You must verify manually.

### 2. Add CHANGELOG entry

Add a new `## vX.Y.Z` section at the top of `CHANGELOG.md` (below the
`# Changelog` header). Include:
- One-line summary of the release theme
- Release posture (production-ready, beta, etc.)
- Key changes grouped by feature area
- Review summary (which models reviewed, how many findings, all fixed)

### 3. Remove ALL build artifacts from the repo root

Internal AI workflow files must NEVER be committed to the repo. These include:
- `BRIEF.md`, `BRIEF_*.md`, `FIX_BRIEF_*.md` — spec/brief files for Cursor
- `codex-review.md`, `opus-review.md`, `opus-review-raw.txt` — review outputs
- `review-prompt.md`, `review.diff` — review inputs
- Any `*.diff` files generated for review

```bash
git rm BRIEF*.md FIX_BRIEF*.md *review*.md *review*.txt *review*.diff 2>/dev/null
```

If the repo has pruned these before, it will need to prune them again. The
rule is simple: nothing in the repo root that is not part of the shipped
product. Briefs and reviews go in `/tmp/` or the Hermes workspace, not the repo.

### 4. Move the tag to the final commit

If a tag was created before the hygiene commit, it now points at the wrong
commit. Delete and recreate it:

```bash
git tag -d vX.Y.Z
git tag vX.Y.Z HEAD
git push origin vX.Y.Z --force
```

If a GitHub release exists, delete and recreate it (the API rejects
`gh release edit --target` when the commitish changes):

```bash
gh release delete vX.Y.Z --yes
gh release create vX.Y.Z --prerelease --title "..." --notes "..."
```

### 5. Verify

```bash
# Tag points at the latest commit
git rev-parse vX.Y.Z          # should equal git rev-parse HEAD
# No version drift
grep -rn "0\.4\.0" .          # should return nothing (old version gone)
# No build artifacts in repo root
ls BRIEF*.md *review*.md *review*.diff 2>/dev/null  # should be empty
# CHANGELOG has the new entry
head -3 CHANGELOG.md
# CI green
gh run list --limit 1 --json conclusion -q '.[0].conclusion'
```

### Common failure modes

| Failure | What happens | When it was caught |
|---|---|---|
| Tag points at pre-hygiene commit | Release includes old version pins | An early-beta release |
| Version pins not bumped | Software self-reports 0.4.0 while tag says 0.5.0 | An early-beta release |
| No CHANGELOG entry | Users clone the repo and see no record of what changed | An early-beta release |
| Build artifacts committed | Lead clones repo and finds 530KB diff + AI review transcripts | An early-beta release (pruned twice before) |
| test_release_versions_agree passes | It checks internal consistency, not tag alignment — false confidence | An early-beta release |

## Reference Files
- `references/pitfalls-dispatch-semantics.md` — dispatch/polling/parallel/model-pin pitfall rules (split from Pitfalls)
- `references/pitfalls-fix-round-verification.md` — fix-round verification rules (split from Pitfalls)
- `references/background-build-polling.md` — polling cadence for background builds (read with `pitfalls-dispatch-semantics.md`)
- `references/rest-api-review-checklist.md` — deep REST API review checklist (routers, authz, SQL patterns)
- `references/plugin-gates-and-fix-rounds.md` — plugin ship gates and fix-round contracts, proven against adversarial reviewers (companion to `hermes-plugin-development`)

- `references/fix-brief-template.md` — fix-brief template mapping each review finding to a concrete code change; `references/feature-build-brief.md` — brief for new-capability builds dispatched against pre-written contract tests.
- `references/sqlite-migration-pitfalls.md`, `references/sqlite-wal-review-findings.md`, `references/upgrade-path-test-pattern.md`, `references/architecture-refactor-test-updates.md`, `references/scope-test-in-process-execution.md` — SQLite/state-store migration lessons from a past SQLite-migration loop (blocking data-loss bug, cross-model WAL review findings, upgrade-path test gap, test updates when architecture shifts mid-loop, in-process scope property-test patterns).
- `references/mcp-category-tool-implementation.md`, `references/mcp-design-review-patterns.md`, `references/reconciliation-review-findings.md`, `references/ci-and-repo-hygiene.md` — MCP tool-surface patterns, design-review patterns, reconciliation findings, and CI/repo-hygiene pitfalls.
- `references/data-integrity-principles.md` — distilled data-layer and migration principles (invariants, foreign keys, upgrade paths, idempotency, TEXT/Decimal money, migration fixtures, CLI contract probes, module-design residue); project records retired in the 2026-10-16 refactor.
- `references/cross-model-parallel-review.md`, `references/parallel-dual-review.md` — running two independent reviewers (Codex + Opus) in parallel and synthesizing their findings.
- `references/delegate-skills-adaptation.md` — delegate-skills port adaptation notes; `references/minified-bundle-selector-research.md` — review style against the shipped minified bundle (Android wrapper dispatches).
- Archive (kept for provenance): `references/retired-red-flags-archive.md` — red-flag rules retired from SKILL.md in the 2026-09-12 dedupe (each rule's source of truth lives in Pitfalls/Workflow).
