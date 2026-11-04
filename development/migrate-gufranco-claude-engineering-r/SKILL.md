---
name: migrate
description: Migrate a framework or library, or upgrade a major version, along the official migration path with one tested commit per step.
disable-model-invocation: true
argument-hint: "/migrate jest vitest | /migrate react 19 | /migrate node 22"
allowed-tools: "Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch, AskUserQuestion"
sensitive: true
---

## Overview

Framework and library migration assistant. Applies changes incrementally with a separate commit per step and full test runs between steps, so any step can be rolled back independently.

## When to Use

- Replacing one library or framework with another across the codebase, such as Express to Fastify or Jest to Vitest.
- Upgrading a dependency or runtime across a major version with breaking changes.
- For planning a migration without executing it, use `/plan`; for a single-call API rename inside one module, use `/refactor`.

## Invocation

| Invocation | Action |
|-----------|--------|
| `/migrate <from> <to>` | Migrate from one library/framework to another |
| `/migrate <library> <version>` | Upgrade a library to a specific major version |

Examples:
- `/migrate express fastify`
- `/migrate jest vitest`
- `/migrate react 19`
- `/migrate node 22`
- `/migrate typescript 5.5`

---

## Steps

1. **Detect current state.** Analyze the current usage of the source library or framework:
   - Read the manifest file to find the current version.
   - Search the codebase for import statements and usage patterns.
   - Count affected files: `grep -r "import.*from '<source>'" --include="*.ts" --include="*.tsx" | wc -l`
   - Identify configuration files specific to the source.
   - List plugins, extensions, or addons that depend on the source.

2. **Research the migration path.** Gather migration guidance:
   - Check for official migration guides from the target library or framework.
   - Identify breaking changes between the source and target versions.
   - Map source APIs to target equivalents.
   - Identify features with no direct equivalent that require redesign.

3. **Generate migration plan.** Create a step-by-step plan:

   | Step | Description | Risk | Rollback |
   |------|------------|------|----------|
   | 1 | Install target, keep source as fallback | Low | Remove target from dependencies |
   | 2 | Migrate configuration files | Medium | Restore config from git |
   | 3 | Migrate utility and helper modules | Low | Revert commit |
   | 4 | Migrate core application code | High | Revert commit |
   | 5 | Migrate test files | Medium | Revert commit |
   | 6 | Remove source dependency | Low | Re-add to manifest |
   | 7 | Clean up: remove compatibility shims | Low | Revert commit |

   Present the plan and wait for approval before proceeding.

4. **Execute each step.** For every step in the plan:
   a. Make the code changes for this step only.
   b. Run the formatter.
   c. Run the linter. Fix any new warnings.
   d. Run the type checker. Fix any new errors.
   e. Run the full test suite. If tests fail because of the migration, fix them as part of this step.
   f. Run the build. Verify zero errors.
   g. Commit with a descriptive message: `refactor(<scope>): migrate <component> from <source> to <target>`.
   h. Report the step result before proceeding to the next.

5. **Verify final state.** After all steps complete:
   - Confirm the source library is no longer in the dependency manifest.
   - Confirm no import statements reference the source.
   - Run the full test suite one final time.
   - Run the build one final time.
   - Report the migration summary.

### Output per step

```
## Step <N>/<total>: <description>

**Files changed:** <count>
**Tests:** <passed>/<total>, <failed> failures
**Build:** pass/fail
**Commit:** <hash> <message>
```

### Final output

```
## Migration Complete

**Source:** <library@version>
**Target:** <library@version>
**Steps completed:** <N>/<total>
**Total files changed:** <count>
**Total commits:** <count>

### Verification
- [ ] Source removed from dependencies
- [ ] No source imports remain
- [ ] All tests pass
- [ ] Build succeeds
- [ ] No linter warnings

### Breaking Changes Applied
| Change | Files affected | How resolved |
|--------|---------------|-------------|
| <API change> | <count> | <approach taken> |

### Manual Follow-up
- <Any items requiring manual verification or testing>
```

## Rules

- Never execute without presenting the plan first. Wait for approval.
- Each step must be a separate commit. Never batch multiple migration steps into one commit.
- Run the full test suite after every step, not just affected tests.
- If a step fails tests and the fix is non-trivial, stop and report. Do not continue with a broken intermediate state.
- When the source and target have different paradigms, do not force a 1:1 mapping. Redesign the affected code to be idiomatic in the target.
- Preserve all existing test coverage. Migration must not reduce the test count or coverage percentage.
- Do not add the target library without checking if it is already a dependency.
- Follow [`../../rules/code-style.md`](../../rules/code-style.md) dependency evaluation criteria when the migration involves choosing between alternatives.
- Prefix every `gh` or `glab` command with the appropriate token per [`standards/github-accounts.md`](../../standards/github-accounts.md) or [`standards/gitlab-accounts.md`](../../standards/gitlab-accounts.md).

## Common Rationalizations

- "A 1:1 API mapping is faster than a redesign": when the paradigms differ, the mapped code fights the target. Rewrite the affected code in the target's idiom.
- "Configuration and helpers are small, one commit covers both steps": one commit per plan step keeps each step revertible alone.
- "The affected tests pass, the full suite can run at the end": a break caught three steps late cannot be pinned to its step. Run the full suite after every step.
- "The old test has no target equivalent, dropping it keeps the migration moving": the test count and coverage stay at or above the baseline. Port the test.
- "The remaining failures will clear up in the next step": the intermediate state stays green. Stop and report instead of carrying a broken step forward.

## Red Flags

- Stop and present the plan when execution is about to start without the user's approval.
- Stop and report when a step's test failures need a non-trivial fix.
- Stop and redesign when a source feature has no target equivalent and a compatibility shim is the only mapping on offer.
- Stop and read the manifest when the target is about to be added, since it can already be a dependency.
- Stop and restore coverage when the test count or coverage after a step is lower than before it.

## Verification

- The source library is absent from the dependency manifest, and a search for its imports returns zero matches.
- The full test suite and the build pass after the last step, and the linter reports zero warnings.
- `git log` shows one commit per plan step, each with the `refactor(<scope>): migrate` subject.
- The test count and coverage are equal to or above their values before the first migration step.
- The Migration Complete report lists every breaking change applied and every manual follow-up.

## Related skills

- `/plan` -- Plan the migration without executing it.
- `/audit` -- Check for vulnerabilities in the target library before migrating.
- `/test` -- Run the test suite independently.
- `/ship commit` -- Commit migration steps.
- `/review` -- Review the migration diff.
