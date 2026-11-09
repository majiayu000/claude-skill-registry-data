---
name: auto-fix-loop
description: This skill should be used when the user asks to "review and fix PR", "review-pr-loop", "auto-fix PR issues", "review and correct everything", "fix all PR review issues", "keep reviewing until clean", "auto-review loop", "review-fix cycle", "review and fix everything automatically", or wants an autonomous review-fix-review cycle that automatically corrects all actionable bugs and suggestions, commits each fix, re-runs review, and loops until clean without asking for confirmation.
---

# Autonomous PR Review-Fix Loop

**Preflight:** run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"` as the first
action. A non-zero exit stops the skill: print its output verbatim and do nothing else.

Run `/pr-review-toolkit:review-pr` in a loop. Fix issues. Re-run the review.
Keep looping. **ONLY TWO EXIT CONDITIONS EXIST:**

1. **The review found ZERO issues** (no Critical, no Important, no Suggestions — completely clean)
2. **5 passes reached** (safety limit)

**NOTHING ELSE stops the loop.** Not "all remaining are SKIP". Not "only suggestions left".
Not "fixes were applied". After EVERY pass where fixes were applied, you MUST re-run the
review to check if the fixes introduced new issues. After EVERY pass where issues were
found but skipped, increment the pass counter and re-run. The loop runs until one of
the two exit conditions is met.

## Loop State: the `mcp__pr-review__loop` tool

When `mcp__pr-review__loop` is in your tool list, the loop's state lives in it,
not in your memory: the pass counter, the seen findings and the fix log survive a
long run that way. Call it at each of these points, with `action` and its fields:

| When | Call | It answers |
| --- | --- | --- |
| Step 1, once, after Step 1.5 | `{"action": "start", "test_command": "<TEST_COMMAND or empty>"}` | pass 0 |
| Step 2, before every review | `{"action": "begin_pass"}` | the pass number, or `exit: max_passes` with the summary |
| Step 4, after every review | `{"action": "findings", "keys": ["<file>::<one-line summary>", ...]}`, one key per finding, an empty list when the review found nothing | `exit: clean` with the summary, or which keys are `new` and which were `seen` |
| Step 5, after each fix commit | `{"action": "fixed", "key": "<key>", "sha": "<short sha>", "description": "<fix>"}` | the fix count |
| Step 6, after a revert | `{"action": "reverted", "key": "<key>", "sha": "<reverted sha>"}` | the sha it marked |
| Step 7 | `{"action": "status"}` | passes, exit reason, fixes and reverts for the summary |

The answer that carries an `exit` ends with one more line, `record: <path>` or
`record: none — <why>`: the review record the loop left for the github plugin's
ready guard, or the reason it left none. It never changes the exit. Step 7 prints it.

Treat a `seen` key exactly as the algorithm treats `seen_issues`: SKIP it. When an
answer carries `exit`, go to Step 7 with that reason and render the summary from
the answer, not from memory. While the loop runs, a stop before either exit
condition is refused once with the pass it stands at: go back to Step 2. Any
prompt the user types, or an interrupted turn, ends that hold.

When the tool is not listed, keep the same state yourself, as the algorithm below
spells it out.

## Loop Algorithm (MANDATORY — follow exactly)

```
pass_count = 0
seen_issues = set()
fix_log = []
TEST_COMMAND = discover_test_command()  # see Step 1.5 — once, before the loop

LOOP:
  pass_count += 1

  # EXIT CHECK 1: safety limit
  if pass_count > 5:
      display exit summary
      STOP

  # Run review
  results = invoke /pr-review-toolkit:review-pr all

  # EXIT CHECK 2: completely clean
  if results has ZERO findings (no Critical, no Important, no Suggestions):
      display "CLEAN — no issues found"
      STOP

  # There ARE findings — process them
  for each finding:
      if finding is in seen_issues:
          mark as SKIP (already attempted)
          continue
      if finding is ACTIONABLE (Critical or Important with clear fix):
          read file, apply fix, commit, add to seen_issues
      else:
          mark as SKIP (suggestion/ambiguous)

  # Run tests after fixes — but only if a real test command was found.
  # TEST_COMMAND == UNDETERMINED is not a failing test run: it means there is
  # nothing to run, and that must never trigger a revert.
  if TEST_COMMAND != UNDETERMINED:
      if TEST_COMMAND fails:
          revert last commit, add to seen_issues

  # MANDATORY: go back to LOOP — do NOT stop here
  # Even if all findings were SKIP, the pass counter increments
  # and we re-run the review. The review might find NEW issues
  # that weren't visible before, or confirm the code is clean.
  goto LOOP
```

**CRITICAL RULE:** After applying fixes, you MUST re-run the review. You cannot
assume the fixes are correct. You cannot assume no new issues were introduced.
The ONLY way to confirm "clean" is to run the review and get zero findings.

## What to Auto-Fix (no user confirmation needed)

**Always fix — issues labeled Critical or Important by review agents:**
- Bugs: logic errors, null handling, race conditions, security issues
- CLAUDE.md violations: explicit rule breaches detected by code-reviewer
- Silent failures: empty catch blocks, swallowed errors, missing logging
- Comment inaccuracies: factually wrong comments, outdated documentation
- Type design issues: missing invariant checks, weak encapsulation with clear fix
- Test defects: missing critical assertions, incorrect test logic
- Code simplification: redundant code, unnecessary complexity with clear simplification

**SKIP but do NOT stop the loop:**
- Architecture/design choices requiring broader context
- Issues where the "fix" is ambiguous or has multiple valid approaches
- Suggestions that would change public API or behavior significantly
- Style preferences not backed by CLAUDE.md rules
- Issues already in `seen_issues` (fix was attempted and either failed or reappeared)

## Step-by-Step Protocol

### Step 1: Initialize

```
- Identify changed files via `git diff --name-only` (or full codebase if user requests)
- Set pass_count = 0
- Set MAX_PASSES = 5
- Initialize seen_issues = set()
- Initialize fix_log = []
- Determine TEST_COMMAND (see Step 1.5) — once, before entering the loop
- Display: "Starting review-fix loop (max 5 passes)"
```

### Step 1.5: Determine the Test Command (once, before the loop)

**This plugin targets many repositories, most of them not Python.** `python -m pytest tests/ -x -q`
is a Python-project assumption, not a universal fact. In a Vue, PHP, Go, or Rust
repo that command is simply absent: it exits non-zero because the shell
cannot find `pytest`, not because a test failed — and treating that as a
failing test run means Step 6 reverts a good commit every single pass and
reports it as an ordinary loop iteration. **A missing test runner must never
look like a failing test.**

Discover the command instead of assuming it, in this order:

1. **The project's own documented convention wins.** Look for an explicit
   test command in `CLAUDE.md`, `README.md`, or `package.json`/`composer.json`
   scripts (a `"test"` entry). If one is documented, use it verbatim.
2. **Otherwise, detect from project files** (first match wins):

   | Found in the repo                                          | Command                  |
   | ----------------------------------------------------------- | ------------------------ |
   | `package.json` with a `"test"` script, `yarn.lock` present  | `yarn test`               |
   | `package.json` with a `"test"` script, `pnpm-lock.yaml`     | `pnpm test`               |
   | `package.json` with a `"test"` script (npm otherwise)       | `npm test`                |
   | `composer.json` with a `"test"` script                       | `composer test`           |
   | `phpunit.xml` or `phpunit.xml.dist`                          | `vendor/bin/phpunit`      |
   | `pyproject.toml` (`[tool.pytest...]`), `pytest.ini`, or `setup.cfg` (`[tool:pytest]`) | `python -m pytest` |
   | `Gemfile` referencing `rspec`                                | `bundle exec rspec`       |
   | `go.mod`                                                     | `go test ./...`           |
   | `Cargo.toml`                                                 | `cargo test`              |
   | `Makefile` with a `test:` target                             | `make test`               |

3. **If nothing above matches, `TEST_COMMAND = UNDETERMINED`.** Tell the user
   once, on the first pass only: "No test command could be determined for
   this project — proceeding without a test gate. Fixes will be committed
   without automated verification." Do not ask for confirmation; this is
   informational, not a stop condition.

Run this discovery exactly once per invocation of the skill, before Step 2,
and reuse the result for every pass — do not re-detect on each loop
iteration, and do not fall back to `pytest` at any point if detection finds
nothing.

**If the detected command itself is unusable** (e.g. the interpreter or
binary is not on `PATH` — a "command not found" exit, not a test failure),
treat that the same as `UNDETERMINED` for the rest of the run: warn the user
once and stop gating on tests, rather than reverting every subsequent pass
because the tool to run tests does not exist.

### Step 2: Increment pass counter and check safety limit

```
pass_count += 1
if pass_count > MAX_PASSES:
    → go to Step 7 (Exit Summary)
Display: "PASS {pass_count} — Running review..."
```

### Step 3: Run review

Invoke the review using the Skill tool or by launching review agents directly:
- Launch code-reviewer and silent-failure-hunter in parallel (minimum)
- Optionally add comment-analyzer, pr-test-analyzer, code-simplifier

Wait for ALL agents to complete. Aggregate results.

### Step 4: Check for clean exit

Count ALL findings across all agents (Critical + Important + Suggestions). The
loop computes the verdict from each agent's closing findings block.

**If total findings == 0:**
→ go to Step 7 (Exit Summary) with exit_reason = "clean"

**If total findings > 0:**
→ go to Step 5 (Apply Fixes)

### Step 5: Apply fixes

For each finding, in order of severity (Critical first):

1. Build dedup key: `(file_path, issue_summary)`
2. If key in `seen_issues` → SKIP, continue to next
3. If finding is ACTIONABLE (Critical/Important with clear fix):
   - Read the affected file
   - Apply the fix using Edit tool
   - Verify no syntax errors
   - Stage and commit: `git add <file> && git commit -m "<message>"`
   - Add to `seen_issues`
   - Append to `fix_log`
4. If finding is NOT actionable (Suggestion/ambiguous):
   - Add to `seen_issues` (so we don't re-evaluate it next pass)
   - Note it for the exit summary

**Do NOT ask for confirmation.** Fix and commit autonomously.
**Do NOT exit after fixing.** Proceed to Step 6.

### Step 6: Run tests and loop back

**If `TEST_COMMAND == UNDETERMINED`** (Step 1.5 found nothing to run): skip
testing entirely for this pass. This is not a failure — do not revert
anything on this basis, and do not re-attempt discovery mid-loop.

**Otherwise, run `TEST_COMMAND`.**

If it exits non-zero because the tests themselves failed:
- Revert: `git revert HEAD --no-edit`
- Add the reverted issue to `seen_issues`
- Do NOT exit — continue

If it exits non-zero because the command itself could not run (interpreter
or binary not found, not a test assertion failure): do not revert — that is
an absence-of-tooling signal, not a failing test. Warn the user once, set
`TEST_COMMAND = UNDETERMINED` for the remainder of this run, and continue.

**MANDATORY: Go back to Step 2.** Do not stop. Do not display a summary.
Do not ask the user anything. Go directly to Step 2.

### Step 7: Exit Summary (ONLY reached from Step 2 or Step 4)

Display:

```markdown
## Review-Fix Loop Complete

**Passes:** {pass_count}
**Total fixes committed:** {fix_count}
**Exit reason:** {clean | max_passes}

### Fixes Applied
- {commit_hash}: {fix description}
- ...

### Skipped Issues (if any)
- {issue description} — Reason: {suggestion/ambiguous/already_attempted}

{the `record:` line of the exit answer, verbatim}
```

The last line is the `record:` line the answer that carried `exit` ended with, copied
as it stands, whether it names a path or says `none — <why>`. When the tool was not
listed, or the exit answer carried no such line, print `record: none — the loop tool
is not available`.

## Commit Convention

Follow the project's commit convention from CLAUDE.md (e.g., `fix(<scope>): description`).
If no convention, default to `fix: {description}`.
Never include `Co-Authored-By`, Claude, Anthropic, or AI references.

## Integration with Review Agents

| Agent | What it finds | Auto-fixable? |
|-------|--------------|---------------|
| code-reviewer | Bugs, CLAUDE.md violations, quality issues | Yes (Critical/Important) |
| silent-failure-hunter | Empty catches, swallowed errors, bad fallbacks | Yes |
| comment-analyzer | Inaccurate/outdated comments | Yes |
| pr-test-analyzer | Missing test coverage, weak assertions | Partially (clear gaps only) |
| type-design-analyzer | Weak invariants, poor encapsulation | Partially (clear fix only) |
| code-simplifier | Redundant code, unnecessary complexity | Yes |
