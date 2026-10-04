---
name: quality-lint
description: Run + audit AICP's linters (ruff for Python code, tools/lint.py for wiki pages) — classify violations, decide what to fix now vs defer as technical debt, and apply fixes. Distinct from feature-test (correctness) and quality-coverage (gaps); this skill is about code + content hygiene. Loads when the operator says "lint", "check style", "audit code style", "clean up ruff violations".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# quality-lint

Audits AICP's lint surface across two lint domains: **Python code** (via ruff)
and **wiki pages** (via `tools/lint.py`). The two domains are related but
separate — a clean AICP project passes both. This skill generates the audit,
classifies violations, and batches fixes.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "lint", "check style", "ruff audit", "clean up lint violations", "wiki lint audit", "code style check"
- **Pre-release gate**: before a milestone ships, confirm lint is clean
- **Periodic hygiene cycle**: weekly or per-release — lint drifts silently between commits
- **After onboarding a new contributor**: new code may introduce new violations; audit surfaces them
- **Post-refactor check**: refactor-* skills may have introduced lint regressions; confirm clean
- **CI failure investigation**: CI reports lint failure; this skill decides whether to fix or defer

Do NOT load when:

- A specific test is failing (load `systematic-debugging` or `feature-test`)
- Coverage is the concern, not style (load `quality-coverage`)
- Architecture is the concern, not style (load `architecture-review` or `quality-audit`)
- The lint tool itself needs setup (load `foundation-testing` for pytest + coverage; ruff is a Python dependency)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Run both linters, capture the baseline

**Trigger**: skill loaded; operator wants an audit.

**Process**:

1. Run ruff on AICP Python code:

   ```bash
   ruff check aicp/ tests/ tools/ --output-format=concise 2>&1 | tee /tmp/ruff-audit.log
   ruff format --check aicp/ tests/ tools/ 2>&1 | tee /tmp/ruff-format-audit.log
   ```

   Capture exit codes and violation counts per rule (ruff groups violations by rule code E/F/W/PL/etc.).

2. Run the wiki lint:

   ```bash
   python3 -m tools.lint --include-inbox 2>&1 | tee /tmp/wiki-lint-audit.log
   ```

   Capture: total pages linted, errors, warnings, per-error types.

3. Write a baseline snapshot at `wiki/decisions/00_inbox/lint-audit-<date>.md` (type=reference). Include:

   - Total violations per lint domain (ruff code, ruff format, wiki)
   - Top 5 rule codes by frequency (ruff) + top 3 error types (wiki)
   - Before-state test count (so fixes don't regress tests)

**Quality bar (Operation 1 done when)**:

- [ ] Both linters ran with fresh output (not cached from a prior session)
- [ ] Exit codes captured per linter
- [ ] Per-rule/per-error breakdowns in the baseline
- [ ] Test count captured (prevents "fixed lint, broke tests" silent regression)
- [ ] Baseline written to `wiki/decisions/00_inbox/lint-audit-<date>.md`

### Operation 2: Classify violations by fix strategy

**Trigger**: Operation 1 baseline captured.

**Process**:

1. For each ruff violation class, classify the fix strategy:
   - **Auto-fix safe** — `ruff check --fix` handles it without behavior change (import ordering I001, unused imports F401 for names the tool can't verify elsewhere, trailing whitespace W291, etc.). Batch with a single fix command.
   - **Auto-fix risky** — `ruff check --fix` could rewrite semantics (unused-argument F841 that's actually used via kwargs, noqa comments that hide real bugs). Fix manually with review.
   - **Legit violation** — the code genuinely should change (e.g., E721 `type(x) == int` should be `isinstance(x, int)`). Fix and re-verify.
   - **Known exception** — the code is correct and ruff is wrong (regex tests, CLI magic, generated code). Add `# noqa: <CODE>` with a brief why-comment.
   - **Defer as debt** — legitimate but out of scope right now (e.g., large file's complexity rules). File as a separate refactor task.

2. For wiki lint errors, classify by fix:
   - **Missing required field** — add to frontmatter (content preservation, metadata add).
   - **Invalid enum value** — pick from allowed set (semantic fix, review needed).
   - **Missing Summary** — write a 30+ word summary (content authoring, not cosmetic).
   - **Title/H1 mismatch** — pick one and align the other (semantic choice).
   - **No relationships** — may be a structural page (index, log) where relationships aren't required. Check against the page type's expectations.

3. Extend the baseline page with the classification table:

   ```markdown
   | Violation | Count | Strategy | Notes |
   |-----------|-------|----------|-------|
   | ruff E501 (line too long) | 23 | auto-fix safe | ruff format handles |
   | ruff F841 (unused arg) | 5 | manual review | 3 real dead args, 2 kwargs-used |
   | wiki missing_summary | 2 | content authoring | log entries need summaries |
   ```

**Quality bar (Operation 2 done when)**:

- [ ] Every violation class has a strategy tag
- [ ] Auto-fix-safe vs manual vs noqa vs defer explicitly called for each class
- [ ] Wiki error categories classified (some are structural, not fixable)

### Operation 3: Apply fixes in batches

**Trigger**: Operation 2 classification complete; operator approved the fix batch.

**Process**:

1. **Auto-fix safe batch first**: `ruff check --fix --select <safe-codes> aicp/ tests/ tools/`. Re-run the full suite: `pytest tests/ --tb=short`. If tests pass, commit: `style(<scope>): ruff auto-fix <codes>`.

2. **Format pass**: `ruff format aicp/ tests/ tools/`. Re-run tests. Commit: `style(<scope>): ruff format`.

3. **Manual-review batch**: work through violations one-by-one in a focused batch (10-20 at a time). For each: read context, decide (fix / noqa / defer), apply. Re-run tests after each 5 fixes to catch regressions early. Commits: one per logical batch, not one per fix.

4. **Wiki lint fixes**: for each wiki error, apply the fix type identified in Operation 2. Re-run `python3 -m tools.lint` after each fix batch.

5. **Deferred items**: for each "defer as debt" violation, create a follow-up task in `wiki/backlog/tasks/` with specific file/line references. Don't lose the deferral — an unfiled deferral is a silent regression.

**Quality bar (Operation 3 done when)**:

- [ ] Auto-fix + format batches landed with passing tests after each
- [ ] Manual review batch applied in reviewable commits (not one giant commit)
- [ ] Every deferred violation has a follow-up task in backlog
- [ ] Full suite passes: `pytest tests/ --tb=short` exit 0
- [ ] Wiki lint passes: `tools/lint.py` exit 0

### Operation 4: Update the audit page + contribute patterns

**Trigger**: Operation 3 fixes landed.

**Process**:

1. Re-open the audit page. Record:
   - Before/after counts per lint domain
   - Fixes applied (per strategy: auto-fix N, format N, manual N, noqa N)
   - Deferrals (count + follow-up task IDs)
   - Test count confirms no regression
2. If the audit surfaced a SYSTEMIC pattern (e.g., "unused-imports consistently come from test files that were reorganized; add a CI check that fails on new unused imports in tests/"), contribute back to second brain: `gateway contribute --type lesson --title "..."`.
3. Consider: should the audit frequency increase (more drift than expected) or decrease (clean project — less audit value)? Update `pm-status-report` recommendation accordingly.
4. Lint the audit page: `tools/lint.py wiki/decisions/00_inbox/lint-audit-<date>.md`.

**Quality bar (Operation 4 done when)**:

- [ ] Before/after counts per lint domain
- [ ] Fix distribution per strategy
- [ ] All deferrals have follow-up task IDs
- [ ] Test count confirmed unchanged or increased
- [ ] Systemic pattern (if any) contributed as lesson
- [ ] Audit page lint passes

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Blindly auto-fixing everything (ruff --fix --unsafe-fixes risk)

The temptation: `ruff check --fix --unsafe-fixes aicp/ tests/ tools/` — clears many violations in one shot. But `--unsafe-fixes` includes changes that ALTER BEHAVIOR (e.g., rewriting `type(x) == T` to `isinstance(x, T)` can change subclass handling). A single command that "cleaned everything" may have silently broken semantics.

**Detection**: did you use `--unsafe-fixes`? Did you run the full test suite AFTER the fix, with ZERO failures, AND confirm the test count didn't decrease?

**The rule**: default to `ruff check --fix` WITHOUT `--unsafe-fixes`. Unsafe fixes get the manual-review batch (Operation 3 step 3). Never apply unsafe auto-fixes and commit without human eyes on the diff.

### Gotcha 2: Adding noqa to silence a real bug (rule-gaming)

A ruff rule flags something. Reading the code, it's not obvious why. Tempting to add `# noqa: <CODE>` and move on. But if the rule flagged a real issue (e.g., F821 unreachable-import because a module was deleted), silencing it hides the bug.

**Detection**: did you READ the code the rule flagged and understand why the rule fired? Or did you add noqa because the rule was annoying?

**The rule**: every `# noqa: <CODE>` needs a comment explaining WHY the rule is wrong for this code. If you can't explain, the rule is probably right — fix the code, don't silence it.

### Gotcha 3: Fixing lint without running tests (semantic regression)

A manual-review batch changes code. Tests don't run. The lint fix happened to change behavior (e.g., removed a "dead" argument that was actually consumed via `**kwargs`). Silent regression.

**Detection**: did the manual-review batch land with a test run proving the suite still passed (count unchanged)?

**The rule**: per Operation 3 — re-run tests after EACH 5-fix batch. Regressions caught in a 5-fix window are easy to bisect. A 50-fix commit that broke tests is a nightmare.

### Gotcha 4: Losing deferrals (unfiled "later" items)

A violation is "out of scope right now, defer." The fix for THIS skill pass is "skip it." Tempting to leave the deferral in the chat and move on. Per Quality Standards anti-pattern: this is "documentation theater" — the appearance of triaging without the operational change.

**Detection**: the audit page mentions "deferred N violations" but no corresponding tasks exist in `wiki/backlog/tasks/`.

**The rule**: every deferred violation has a follow-up task file. The task has specific file:line references so future work can find the exact spots.

### Gotcha 5: Wiki-lint fixes that paper over real quality issues

A wiki page fails `missing_summary` because the Summary is "TBD" (two words, fails the 30-word minimum). Tempting to pad it to 30 words with fluff. But the page genuinely has no summary yet — padding hides that fact.

**Detection**: did you ADD substantive content to meet the word count, or pad with generic phrasing?

**The rule**: if a wiki page has no real summary, the fix is "author the summary properly" (often out of scope for a lint pass — file as content authoring task). Don't pad to satisfy the metric. Per Quality Standards "gaming the number" anti-pattern: compliance theater.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact this skill produces:

- **Lint audit page**: see `wiki/decisions/00_inbox/coverage-audit-<date>.md` (from `quality-coverage` skill) — same reference-page shape
- **Real ruff configuration**: see `pyproject.toml` for AICP's ruff configuration (rules enabled, line length, Python version target)

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP's lint is `ruff check + ruff format` for Python (not pylint, not flake8) and `tools/lint.py` for wiki pages (not markdownlint — AICP-specific schema validation). Using a different Python linter would require AGENTS.md + CLAUDE.md + domain-profile updates + CI config — do not switch casually.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| quality-coverage | coverage audit (tests missing paths) | Different quality axis (coverage vs style) |
| quality-audit | broader quality review (architecture + patterns + hygiene) | Encompasses lint as one dimension; this skill is the lint-specific deep dive |
| quality-debt | technical debt tracking | Deferrals from this skill feed into quality-debt's inventory |
| foundation-testing | setting up ruff + pytest initially | Pre-audit; this skill runs against configured tooling |
| feature-test | per-feature testing | Includes running lint as a gate; this skill is suite-wide lint audit |
| refactor-* skills | structural code changes | May introduce lint regressions this skill catches |
