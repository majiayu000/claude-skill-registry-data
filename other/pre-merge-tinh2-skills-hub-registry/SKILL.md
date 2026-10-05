---
name: pre-merge
description: "One-command PR gate that runs four passes over exactly the changed surface — code review (correctness then simplification), security (injection, authz, secrets, dependency diff), tests (run the suite and flag untested changed lines)."
version: "2.0.1"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous merge gatekeeper. Do NOT ask the user questions; run all applicable passes and render one verdict. Speed comes from scoping every pass to the diff, never from skipping a pass.

TARGET: $ARGUMENTS
If arguments give a PR number, check it out with `gh pr checkout <n>` first. If they give a base branch, diff against it. If empty, gate the current branch against the auto-detected base.

=== PRE-FLIGHT ===

1. Git repo required (`git rev-parse --git-dir`); otherwise STOP: "pre-merge gates a git branch; none found."
2. Detect base branch (origin/HEAD symbolic ref, else main/master/develop). Compute `MB=$(git merge-base HEAD <base>)`. If HEAD == MB (no changes): STOP with verdict `MERGE (empty diff — nothing to gate)`.
3. Build the changed-file inventory with `git diff --name-status $MB..HEAD`. Classify each file:
   - source | test | config/CI | dependency manifest or lockfile | docs
   - UI: components/templates/styles/screens, detected by extension and path (`.tsx`, `.jsx`, `.vue`, `.svelte`, `_screen.dart`, `.html`, `.css`)
   - generated: skip entirely (lockfile content is read only by the dependency-diff check)
4. Detect the test command and any lint/typecheck commands from package scripts, Makefile, CI config. Record what exists; missing gates are reported as coverage gaps, not silently ignored.
5. Uncommitted changes present: include them in the gated surface (`git diff $MB` instead of `$MB..HEAD`) and note "gated tree includes uncommitted work".

=== PHASE 1: CODE REVIEW PASS (changed surface only) ===

1. Read every changed source file in full (context matters), but raise findings ONLY on changed or directly-affected lines.
2. Correctness sweep:
   - Logic errors, inverted conditions, off-by-one boundaries.
   - Unhandled null/empty/error paths on changed lines.
   - Broken error propagation: swallowed exceptions, catch-and-continue, missing awaits.
   - Concurrency and ordering hazards introduced by the change.
   - Contract breaks for existing callers of modified functions — grep the callers and check each one.
3. Simplification sweep (after correctness, never instead of it):
   - Duplication introduced by this diff of code that already exists in the project.
   - Dead code added (unreachable branches, unused exports).
   - Needless abstraction or complexity that a stdlib or existing project utility already covers.
4. Record each finding: PASS-tag R#, severity (BLOCKER = wrong behavior or broken caller; NIT = works but should improve), file:line, one-line evidence, concrete fix.

VALIDATION: every changed source file has been read; findings list (possibly empty) recorded with the per-file coverage list.
FALLBACK: diff too large to read fully (>~5000 changed lines): gate the riskiest files first (source > config > UI > docs), report exact coverage ("reviewed 34/61 files"), and cap the verdict at MERGE-WITH-NITS — an unread diff can never earn a clean MERGE.

=== PHASE 2: SECURITY PASS (changed surface only) ===

1. Injection: any changed line where external input reaches SQL/NoSQL/shell/eval/HTML/template without parameterization or encoding.
2. Authz: new or modified endpoints, routes, handlers, or DB rules — verify an auth check exists and matches siblings; flag IDOR patterns (object fetched by user-supplied ID without ownership check).
3. Secrets: scan the DIFF TEXT (`git diff $MB..HEAD`) for keys, tokens, passwords, private keys, connection strings — including in deleted lines (a removed secret is still leaked in history: flag for rotation).
4. Dependency diff: if manifests/lockfiles changed, list added/upgraded packages; check each addition for typosquat-ish names and run the ecosystem's audit (`npm audit`, `pip-audit`, `cargo audit`) if the tool is present. New Critical/High vulns introduced by the diff = BLOCKER.
5. Findings tagged S#, severity (BLOCKER = exploitable or leaked secret; NIT = hardening), file:line, fix.

VALIDATION: all four checks executed or explicitly n/a (e.g. "no dependency changes").
FALLBACK: audit tool absent: report "dependency vulns unchecked — <tool> not installed" as a coverage gap; do not fabricate a clean result.

=== PHASE 3: TEST PASS ===

1. Run the full suite with the detected command. Record pass/fail counts and any failures with output excerpts. Any failing test that passes on the base branch = BLOCKER T#.
2. Untested-changed-lines check: for each changed source file, find its tests (path convention, same-name test file, grep for the symbol names in test dirs). Changed public functions/branches with no test exercising them get a T# finding: BLOCKER if the change is behavioral logic in non-trivial code paths, NIT for trivial/presentational changes.
3. If a coverage tool is configured, run it scoped to changed files for line-level evidence; otherwise use the symbol-grep method and say so.

VALIDATION: suite executed (or "no test suite" recorded as a standing finding), untested-changes list produced.
FALLBACK: suite is too slow (>10 min estimate) : run the test files related to changed code plus any smoke/fast target, and report the narrowed scope; a narrowed test pass caps the verdict at MERGE-WITH-NITS.

=== PHASE 4: A11Y PASS (only if UI files changed) ===

1. Skip cleanly with "no UI files changed" if the Phase 0 inventory has no UI files.
2. Static checks on changed UI code:
   - Images/icons without alt text or a semantic label.
   - Interactive elements that are not native buttons/links and lack role + tabindex + keyboard handling.
   - Form inputs without associated labels (for/id, aria-label, or wrapping label).
   - Color values introduced without a contrast-checkable pairing — flag for manual contrast check.
   - Focus traps and removed focus outlines (outline: none without a replacement).
   - Touch targets below ~44-48px where sizes are explicit in the diff.
   - Missing Semantics wrappers on interactive Flutter widgets.
3. Findings tagged A#: BLOCKER = unusable by keyboard/screen reader (e.g. click-div with no role/tabindex on a primary action); NIT = degraded experience.

VALIDATION: every changed UI file checked or pass skipped with reason.
FALLBACK: framework's a11y idioms unknown: apply the WAI-ARIA-level checks (labels, roles, keyboard) which are framework-independent, and note the limitation.

=== PHASE 5: VERDICT ===

Aggregate: any BLOCKER anywhere -> BLOCK. No blockers but any NIT or any coverage gap/cap from fallbacks -> MERGE-WITH-NITS. Otherwise -> MERGE. Never soften a BLOCKER into a nit because the fix is easy; easy fixes make BLOCK cheap to resolve.

=== OUTPUT ===

Emit exactly one verdict block, nothing after it:

```
==================== PRE-MERGE VERDICT ====================
VERDICT: MERGE | MERGE-WITH-NITS | BLOCK
Branch: <branch> vs <base> (<n> files, +<a>/-<d>)
Passes: review OK|n findings, security OK|n, tests <p>/<t> pass, a11y OK|n|skipped(no UI)
Coverage gaps: <none | list>

BLOCKING FINDINGS
1. [S2] <title> — <file>:<line>
   Fix: <one concrete action>
(...numbered, grouped blockers first)

NITS
n. [R4] <title> — <file>:<line> — Fix: <action>
===========================================================
```

=== SELF-REVIEW ===

Score 1-5: Complete (all four passes ran or skipped with stated reason), Robust (every finding re-checked against the actual file before the verdict — no stale or duplicate findings), Clean (verdict block parseable, findings numbered, no finding without file:line). Any score < 4: fix before emitting the verdict; if unfixable, add it to Coverage gaps.

=== LEARNINGS CAPTURE ===

Append to ~/.claude/skills/pre-merge/LEARNINGS.md: date + repo + verdict, diff size, pass durations, false-positive findings the user pushed back on (if known), suggested patch to this skill, verdict [Smooth/Minor friction/Major friction].

=== STRICT RULES ===

1. Exactly one verdict per run; never emit two candidate verdicts or a hedge.
2. Every finding carries file:line and a concrete fix; a finding you cannot locate precisely gets dropped or re-verified, not published vaguely.
3. Never scan beyond the changed surface for findings (whole-repo problems are out of scope), but always read enough surrounding context to judge the change.
4. Never skip a pass silently; skips require a stated reason in the Passes line.
5. A fallback-narrowed run (unread files, narrowed tests) can never produce a clean MERGE.
6. Never fix code in this skill — it gates; remediation belongs to review-and-fix.
7. Deleted secrets are still findings (history + rotation), not resolved issues.
