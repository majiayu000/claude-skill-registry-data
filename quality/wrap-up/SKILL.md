---
name: wrap-up
description: "Post-implementation quality gate. Runs automated checks (tests, lint, types), invokes /flagrare:implementation-review for the seven-check parallel review, culls every code comment in the diff that is not a trap-preventer, then performs additional SOLID and Clean Code review on any findings not covered. Use when the user says 'wrap up', 'review changes', 'check my work', 'am I done', or after completing an implementation task."
---

# Wrap-up

Validate implementation quality through automated checks and structured review.

This skill orchestrates automated tooling and the `/flagrare:implementation-review` skill, then layers additional quality checks on top.

---

## When to Use

1. User says "wrap up", "review changes", "check my work", "am I done", "did I miss anything"
2. After completing a todo item or implementation task
3. Before committing (remind the user: "Ready for wrap-up?")

---

## Workflow

### Step 1: Run Automated Checks

Detect and run the project's test, lint, and typecheck commands.

**Detection order:**

1. Check `package.json` for scripts
2. Check `build.gradle.kts` / `build.gradle` for tasks
3. Check `pyproject.toml` for tool configs
4. Check `Makefile` for targets
5. Check common config files (`.eslintrc`, `tsconfig.json`, `pytest.ini`, etc.)

**Common commands by stack:**

| Stack | Test | Lint | Typecheck |
|-------|------|------|-----------|
| Node (npm) | `npm test` | `npm run lint` | `npm run typecheck` or `npx tsc --noEmit` |
| Node (pnpm) | `pnpm test` | `pnpm lint` | `pnpm typecheck` |
| Kotlin/Gradle | `./gradlew test` | `./gradlew ktlintCheck` | (built into compiler) |
| Python | `pytest` | `ruff check .` or `flake8` | `mypy .` or `pyright` |
| Go | `go test ./...` | `golangci-lint run` | (built into compiler) |

**Execute all three, continue even if one fails:**

```bash
{test_cmd} ; {lint_cmd} ; {typecheck_cmd}
```

**Report failures clearly:**

```
## Automated Checks

| Check | Status | Issues |
|-------|--------|--------|
| Tests | PASS | - |
| Lint | FAIL | 3 errors in `src/utils.ts` |
| Types | PASS | - |
```

If any check fails, list the specific errors.

### Step 2: Invoke `/flagrare:implementation-review`

Call `/flagrare:implementation-review`. This runs seven parallel subagent checks:

1. Plan gap analysis
2. Use-case coverage
3. Missing test scenarios
4. Test philosophy (Kent Dodds Testing Trophy)
5. SOLID violations
6. Clean Code violations
7. Security (pulls in `/flagrare:security-audit`)

Checks 2-4 apply `/flagrare:testing-philosophy`, behavior over implementation and the e2e necessity floor, so test quality is owned there; don't re-litigate it in Step 4. Check 7 applies `/flagrare:security-audit`, so security is owned there; don't re-litigate it in Step 4 either.

**Wait for it to complete.** Collect all findings.

### Step 3: Comment cull

Every code comment the diff adds is deleted unless it is a trap-preventer. This step acts; it does not flag. Check 6 of `/flagrare:implementation-review` reports what-comments, this step is where the deleting happens, and it covers every comment in the diff, not only the ones Check 6 named.

Enumerate every comment in the diff: line comments, block comments, file headers, doc comments on non-public symbols, and comments in test files, which are the most common survivors. Apply this test to each one, and both halves must hold:

1. If a future reader deleted or moved the code this comment sits on, would that look like a safe cleanup?
2. Would it break something they could not see from the code, the types, or the tests?

A "no" to either half means delete. The reader is not confused without it; they are only less entertained.

Before keeping a survivor, try to make it unnecessary. A constraint that can live in a name, a test title, or an assertion message should live there instead, because those are read every time the code is, and the comment is read once. A test that must be the first render in a fresh module registry is named for that; a fixture id that has a recovery query belongs in the assertion message that fires when the fixture is gone, not in a header the reader scrolls past.

What always goes, whatever it says about itself:

- **What-comments**: restate the code below them.
- **Provenance**: "on purpose", "deliberately", "the design says", "per the ticket", "the reviewer asked". These record why the author did something, which is a fact about the author, not a constraint on the reader.
- **File headers**: "this file holds the ids the specs use", "shared helpers for X". The file name and the exports say this.
- **Citations**: tickets, TDDs, Figma frames, PR numbers, doc sections. They rot, and the reader cannot act on them.
- **Narration in tests**: "we render, then we assert". The test body is the narration.

Never trim a comment into survival. Delete it whole or keep it whole; a comment that needed shortening was not a trap-preventer, it was a long provenance note. A survivor is one or two lines, states the constraint plainly, and cites nothing.

Apply the deletions directly, without asking. Record every deletion and every survivor with its one-line justification for the Step 5 report, so the user can veto a deletion or cut a survivor. The bias is that a human reviewer will ask "does this file need all these comments?" far more often than "why is there no comment here."

### Step 4: Additional Review (gaps not covered by /flagrare:implementation-review)

After `/flagrare:implementation-review` reports, check for anything it might have missed due to scope. These are supplementary checks, not duplicates.

**Naming review:**
- Are names intention-revealing?
- Do they avoid mental mapping?
- Bad: `d`, `theList`, `hp`, `apts`
- Good: `elapsedDays`, `activeUsers`, `hoursPerTask`, `apartments`

**Function size review:**
- Are functions small (ideally under 20 lines)?
- Do they have few arguments (3 or fewer ideal)?
- Are abstraction levels consistent within a function?

**Error handling review:**
- Are exceptions used instead of error codes?
- Is error handling separated from business logic?
- Are error messages informative?

**Code smells not covered by SOLID:**
- Duplicate code across the diff
- Feature envy (method uses another object's data excessively)
- Data clumps (groups of data that always appear together)
- Primitive obsession (using primitives instead of small objects)
- Long parameter lists without grouping

### Step 5: Generate Combined Report

Merge automated check results, `/flagrare:implementation-review` findings, and supplementary review into one report:

```
## Wrap-up Report

### Automated Checks
| Check | Status |
|-------|--------|
| Tests | PASS/FAIL |
| Lint | PASS/FAIL |
| Types | PASS/FAIL |

### Implementation Review (from /flagrare:implementation-review)
[Paste the seven-check summary verbatim]

### Comment cull
- Deleted: `{file}:{line}` "{first words of the comment}"
- Kept: `{file}:{line}` "{first words}", {the invisible break it prevents}

### Supplementary Review

#### Good
- {aspect}: {what's done well}

#### Suggestions
- **{aspect}** in `{file}:{line}`: {issue}
  - Suggestion: {how to fix}

### Summary
- {N} blocking issues (must fix)
- {M} suggestions (should consider)
- Overall: Ready to commit / Needs attention
```

### Step 6: Offer Fixes

If issues were found, **close with a tool, not prose.** The Step 5 report is a large artifact; ending with a prose "Would you like me to…" frequently reads as turn-complete and stops before the user can answer (the stall pattern in [`docs/research/2026-06-11-claude-code-goal-anti-stall.md`](../../../../docs/research/2026-06-11-claude-code-goal-anti-stall.md)). Immediately after the report, issue an `AskUserQuestion` tool call with options:

- **Fix the automated check errors** (lint/type)
- **Apply the review suggestions**
- **Both** (Recommended when both surfaced findings)
- **Skip for now**

Comment deletions are not on this menu: Step 3 already applied them. If the user wants one back, they say so after reading the report.

Do not render these as a numbered prose list and wait, use the tool so the user gets buttons and the turn doesn't end ambiguously.

---

## Anti-patterns

- Don't skip automated checks. They catch things review cannot.
- Don't duplicate what `/flagrare:implementation-review` already covers. If it reported on SOLID, don't re-report the same finding.
- Don't block on advisory findings. Use judgment on what's blocking vs nice-to-have.
- Don't skip this because "the change is small". Small changes still break things.
- Don't keep a comment because it is a "why". Most whys are provenance. The only why that survives is the one whose absence lets a reader break something they cannot see.
- Don't leave comment deletions for the reviewer to request. "Does this file need all these comments?" on a PR means Step 3 was skipped.

---

## Flow position

```
[code changes complete]
     |
     v
/flagrare:wrap-up
     |--- Step 1: automated checks (tests, lint, types)
     |--- Step 2: /flagrare:implementation-review (7 parallel subagents)
     |--- Step 3: comment cull (delete by default)
     |--- Step 4: supplementary review
     |--- Step 5: combined report
     |
     v
git commit
     |
     v
/flagrare:release-check
```
