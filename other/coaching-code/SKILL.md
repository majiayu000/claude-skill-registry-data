---
name: coaching-code
description: Review code as a senior engineer would — SOLID, clean code, security, performance, database and testing — in a scored coaching report with top suggestions. Use when the user wants mentoring feedback on a file or module they wrote to learn how to make it better. Not for a pre-merge review of a feature; see /development-review.
metadata:
  argument-hint: "<file-or-topic> [--skip-checks]"
  stack-aware: true
---

# Code Coaching

Review "$ARGUMENTS" through the lens of a senior software engineer. Provide mentorship feedback on code quality, architecture patterns, security, performance, and testing.

See also `/development-review` for a pre-merge approve/request-changes verdict on a feature's changes, rather than mentoring feedback to learn from.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Derive `<project>` from the argument by taking its basename without extension and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"coaching-code","workflow":"coaching","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

## Prerequisites

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

None — this is a utility skill that can run anytime.

## Process

1. **Read the target:**
   - Read the source code files specified in "$ARGUMENTS"
   - If it's a directory, read the key files
   - Understand the context: what does this code do?

2. **Read reference material:**
   - Read `references/code-principles.md` for engineering principles
   - Read `references/feedback-format.md` for output structure

3. **Evaluate against engineering principles:**
   - **SOLID:** Single responsibility, open/closed, Liskov, interface segregation, dependency inversion
   - **Clean code:** Naming clarity, function size, abstraction levels, self-documenting code
   - **DRY/YAGNI/KISS:** Appropriate abstraction level, no premature optimization
   - **Security:** Input validation, injection prevention, secrets management, auth patterns
   - **Performance:** N+1 queries, appropriate data structures, caching, lazy loading
   - **Database:** Normalization, indexing, query patterns, transactions
   - **Testing:** Coverage, behavior vs. implementation testing, test quality
   - **Error handling:** Appropriate error types, no swallowed errors, graceful degradation

4. **Write the coaching report** to `.singularskills/coaching/<project>/code-review.md` following the feedback format.

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The code coaching report written to `.singularskills/coaching/<project>/code-review.md`. Present the score and top 3 suggestions to the user.
