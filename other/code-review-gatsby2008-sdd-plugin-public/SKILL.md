---
name: code-review
description: Stack-aware code quality and security review of current branch changes
argument-hint: "[--recheck]"
allowed-tools: Bash(find .:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git cat-file:*), Bash(mkdir:*), Bash(grep:*), Bash(cat .specwork/_review/*)
---

# Code Review

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/code-review/SKILL.md`

---

## Description

Run a stack-aware quality and security review on the current branch diff.
Use Java reviewers for Spring Boot projects and UI reviewers for frontend projects.
Keep the report short and evidence-based.

---

## Modes

- `/sdd:code-review` — normal review of the current diff
- `/sdd:code-review --recheck` — compare the current diff against the previous report

---

## Flow

1. Detect branch and ticket/slug
2. Collect staged + unstaged diff
3. Abort if the diff is empty
4. Detect stack from project files
5. Verify required reviewer agents exist
6. Run test coverage check on the diff (see *Test Coverage Check* below)
7. Run the matching reviewers in parallel
8. Merge findings, dedupe overlap, assign IDs
9. Prepend the test-coverage gaps (if any) to the merged report
10. Detect pack hints from diff content (see *Pack Hints* below) and append a `## Suggested Follow-ups` section if any trigger fires
11. Write `.specwork/_review/<id>-code-review.md`
12. Print the report and ask for approval before any fixes

---

## Stack Routing

- Java (`build.gradle` or `pom.xml`): `sdd:java:quality-reviewer` + `sdd:java:security-reviewer`
- Frontend (`package.json`): `sdd:ui:quality-reviewer` + `sdd:ui:a11y-reviewer`
- If both stacks appear, prefer the stack most closely tied to the changed files
- If neither stack is clear, run a generic quality review and flag the ambiguity

---

## Test Coverage Check

Run **before** invoking reviewer agents. The check operates on the same diff and reports gaps in a `## Test Coverage` section prepended to the merged report. The check is **stack-specific**:

### Java

- Find production files in the diff: `src/main/java/**/*.java`
- For each, check whether a corresponding test file appears in the diff:
  - `<ClassName>Test.java`, `<ClassName>IntTest.java`, `<ClassName>IT.java`, `<ClassName>IntegrationTest.java`
  - Search regardless of directory (unit or `intTest` source set)
- Separate into:
  - **Modified classes** — existed before (`git cat-file -e HEAD:<file>` succeeds)
  - **New classes** — added in this diff
- Skip: DTOs (fields + getters/setters only), `*Config.java`, `*Properties.java`, constants, and any file matching `*Test*`, `*IT*`, `*IntTest*`

### Frontend

- Find production files in the diff: `src/**/*.ts` and `src/**/*.tsx`
- Exclude: `*.test.ts`, `*.test.tsx`, `*.d.ts`, `*.stories.tsx`, type-only files
- For each, check whether `<name>.test.ts` or `<name>.test.tsx` appears in the diff alongside the source file
- Separate into modified vs new using `git cat-file -e HEAD:<file>`
- Skip: type-only files (`*.d.ts`), pure style files, constants, index re-exports

### Report block

If any gap is found, render the section as:

```
## Test Coverage
⚠  Modified classes without updated tests:
     src/main/.../ConsentService.java  →  ConsentServiceTest not in diff
⚠  New classes without any test:
     src/main/.../EmailDispatcher.java →  no test found in diff
```

If no gaps: omit the section silently (do not print empty headers).

The coverage gaps are **advisory** — they do not affect the verdict (PASS / PASS WITH WARNINGS / FAIL). The reviewer agents may independently surface coverage as a finding; if they do, the deduplication step keeps the agent's finding (which has severity) over the raw advisory list.

---

## Pack Hints (Java)

After the merged report is built, grep the diff to detect areas where deeper standalone packs exist. **Do NOT load these packs into the reviewer agents** — they are large reference docs and would inflate the per-run token cost. Instead, when a trigger fires, append a `## Suggested Follow-ups` section to the merged report so the user can opt-in to a deeper manual review.

| Trigger pattern (regex on diff) | Pack to suggest |
|---|---|
| `@Entity\b\|@Repository\b\|JOIN FETCH\|@EntityGraph\|@Transactional\b\|@Query\b` | `/sdd:jpa-patterns` — N+1, fetch strategy, JPQL parameterization |
| `@Async\b\|CompletableFuture\|synchronized\b\|volatile\b\|ExecutorService\|Thread\.ofVirtual` | `/sdd:concurrency-review` — thread safety, virtual threads, async patterns |
| `@RestController\|@RequestMapping\|@(Get\|Post\|Put\|Patch\|Delete)Mapping` on added files only | `/sdd:api-contract-review` — HTTP semantics, versioning, DTO leak, request validation |
| `org\.slf4j\|@Slf4j\|MDC\.\|logback\b\|feign\.client\.config` with new logging calls | `/sdd:logging-patterns` — structured logging, PII redaction, Feign DEBUG hygiene |

Hint format in the report:
```markdown
## Suggested Follow-ups
- Diff touches `@Entity` / `@Repository` — consider `/sdd:jpa-patterns` for a deeper review (N+1, fetch strategies, query parameterization).
- Diff touches `@Async` / virtual threads — consider `/sdd:concurrency-review` for thread safety and modern patterns.
```

Omit the section if no triggers fire. Suggestions are advisory and do not affect the verdict.

These packs are also useful outside `/sdd:code-review` — they can be invoked directly at any time, and only consume tokens when the user actually chooses to load them.

For frontend stack, hint detection is a no-op until frontend packs are added.

---

## Agent Rules

Each reviewer gets:
- the full diff
- a short repo context note
- evidence-based instructions only
- no code outside the diff

If a required reviewer is missing, stop and tell the user how to install it.

---

## Report Format

Keep the report compact:

```markdown
# Code Review: <Title>

## Verdict
PASS | PASS WITH WARNINGS | FAIL

## Summary
- up to 8 bullets

## Test Coverage    <!-- omit if no gaps -->
⚠  Modified classes without updated tests:
     src/main/.../ConsentService.java  →  ConsentServiceTest not in diff

## Security Findings
| ID | Severity | File:Line | Finding |
|----|----------|-----------|---------|

## Quality Findings
| ID | Severity | File:Line | Finding |
|----|----------|-----------|---------|

## Action Plan
1. [ ] F-001 — ...
2. [ ] F-002 — ...

## Questions / Uncertainties
- ...
```

For `--recheck`, replace findings with a short status table showing resolved vs still open, then list only new findings and unresolved items.

---

## Rules

- Do not edit files until the user approves the action plan
- Do not run formatting-only changes unless they fix a cited finding
- Review only the diff
- Keep findings specific, ranked, and minimal

---

## Requirements

- Run from the active pipeline branch, or any current branch when reviewing outside SDD
- At least one staged or unstaged change must exist
- Required reviewer agents must be installed for the detected stack

---

## Related Skills

- `commit` — run after review fixes are approved
