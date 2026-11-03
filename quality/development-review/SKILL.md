---
name: development-review
description: Review a feature's code changes before merge for bugs, security issues, quality and test coverage, ending in an approve or request-changes verdict. Use when a branch or feature is finished and the user wants it checked before merging or opening a pull request. Not for mentoring feedback on code to learn from; see /coaching-code.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: development
  phase: 4
  artifact: 04-review.md
  stack-aware: true
---

# Review

Review the code changes for "$ARGUMENTS" before merging. Check for bugs, security issues, code quality, and test coverage.

See also `/coaching-code` for a scored coaching report with mentoring feedback to learn from, rather than a merge verdict.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"development-review","workflow":"development","phase":4,"project":"<project>","event":"skipped","artifact":"04-review.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Review) of the Plan-Build-Test-Ship workflow (`development`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `development` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own; this one has no gate, since it needs no earlier artifact.

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"development-review","workflow":"development","phase":4,"project":"<project>","event":"started","artifact":"04-review.md","note":""}`.

Read `.singularskills/development/<project>/02-build.md` if it exists, to understand what was built. If not available, review the current branch diff against main.

## Process

1. **Gather the changes:**
   - Read the git diff of all changed files (staged + unstaged, or branch diff vs. main)
   - Understand the scope and intent of the changes

2. **Check for bugs:**
   - Logic errors, off-by-one, null/undefined handling
   - Race conditions or state management issues
   - Missing error handling at system boundaries

3. **Check for security issues:**
   - Input validation at system boundaries (user input, external APIs)
   - No secrets, tokens, or credentials in code
   - No injection vulnerabilities (SQL, XSS, command injection)

4. **Check code quality:**
   - Naming clarity — do names describe what things do?
   - Unnecessary complexity — can anything be simplified?
   - Consistency with existing codebase patterns
   - No dead code, commented-out code, or TODO placeholders

5. **Check tests:**
   - Do tests exist for new functionality?
   - Do tests verify behavior, not implementation?
   - Are edge cases covered?

6. **Write the artifact** to `.singularskills/development/<project>/04-review.md` with sections:
   - **Summary** — what was reviewed and overall assessment
   - **Issues** — categorized by severity (critical, important, minor)
   - **Strengths** — what's well done
   - **Recommendations** — suggested improvements

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The review report written to `.singularskills/development/<project>/04-review.md`. Present a summary to the user highlighting:
- Overall assessment (approve / request changes)
- Critical issues (if any)
- Key recommendations

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"development-review","workflow":"development","phase":4,"project":"<project>","event":"finished","artifact":"04-review.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: development-review
workflow: development
phase: 4
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
