---
name: zoom-out
description: Step back from a narrow code section and place it in its system context. Reads the file, traces callers and callees, identifies the module boundary, names the architectural role, and surfaces hidden coupling. Use when user says "zoom out", "what is this", "where does this fit", "give me context on this code", "what calls this", or feels lost in unfamiliar code. For line-by-line code review, use /review; for debugging, use /investigate; for onboarding to a whole repo, use /onboard.
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: "/zoom-out src/billing/invoice.ts:42 [--depth 3]"
---

## Overview

Perspective shift. The user is staring at a function, file, or module and cannot see the system around it. This skill widens the lens until the role of the code is clear, then stops.

## When to Use

- The user says "zoom out", "what is this", "where does this fit", "give me context on this code", or "what calls this".
- The user names one file or one line and cannot say which module owns it or who calls it.

For line-by-line review, use `/review`; for a bug hunt, use `/investigate`; for whole-repository orientation, use `/onboard`.

## Arguments

- `<path>` or `<path>:<line>`: the file or location to zoom out from. Required.
- `--depth <n>`: how many hops outward to trace. Default 2, max 4. Higher depth burns context fast.

## Process

### 1. Read the target

Read the full file at `<path>`. If a line number is given, read 30 lines around it. Identify:
- The primary export or symbol at the location.
- Other exports in the same file.
- Imports from inside the project versus from third-party packages.

### 2. Trace inward (callees)

For each function the target calls, locate its definition. Note:
- Which module it lives in.
- Whether it is pure or has side effects such as I/O, network, database, or global state.
- Whether it is project code or library code.

Stop at depth 1 unless `--depth` is higher.

### 3. Trace outward (callers)

Grep the project for usages of the target's exports. For each caller:
- Which module imports it.
- The shape of the call site, one-shot, loop, retry, conditional.
- Whether the caller is a route handler, a job, a CLI entry, a test, or another internal module.

### 4. Identify the module boundary

Group the files touched in steps 2 and 3 by directory and by responsibility. State:
- Which module the target belongs to.
- Which neighboring modules it talks to.
- Whether the boundary looks intentional or accidental such as cross-cutting imports, circular references, or leaky abstractions.

### 5. Name the architectural role

Pick the closest match from this list. Add a one-line justification.

| Role | Signal |
|------|--------|
| Domain logic | Pure functions, no I/O, expresses business rules |
| Application service | Orchestrates domain calls and infrastructure, no business rules |
| Adapter | Translates between an external system and the domain |
| Controller / route handler | Sits at the HTTP, queue, or CLI boundary |
| Repository | Persists or retrieves domain objects |
| Utility | Stateless helper used across modules |
| Configuration | Loads, validates, or exposes config |
| Entry point | Wires the system at startup |

If the target spans more than one role, that is itself a finding. Surface it.

### 6. Surface hidden coupling

List anything that would surprise a new contributor:
- Side effects at module load time. See the "No side effects at module level" bullet under "Fundamentals" in [`standards/code-style.md`](../../standards/code-style.md).
- Shared mutable state.
- Implicit ordering requirements between callers.
- Logic that depends on environment variables read deep in the call stack.
- Type assertions that hide a contract violation.

### 7. Output

Produce a single report. No file edits. Format:

```markdown
# Zoom-out: <path>

## What it is
One paragraph. Primary purpose, surface area, dependencies.

## Role
<role from the table>. Justification: <one line>.

## Callers (depth N)
- file:line - <one line>
- file:line - <one line>

## Callees (depth N)
- file:line - <one line>
- file:line - <one line>

## Module boundary
- Lives in: <module>
- Talks to: <neighbor modules>
- Boundary health: clean / leaky / circular / cross-cutting

## Hidden coupling
- <finding> at file:line
- <finding> at file:line

## Suggested next reads
- file:line - reason
- file:line - reason
```

## Rules

- This skill never edits code. It produces a report only.
- Cap depth at 4. Beyond that, the report stops being a zoom-out and becomes a survey.
- Cite every claim with `file:line`. No abstract statements about "the architecture".
- If the role does not match the table, say so explicitly. Do not invent a category.
- Stop after the report. Do not propose refactors. Use `/refactor` for that.

## Common Rationalizations

- "The file name says what it does": a name is a claim. The callers in step 3 show the role the code actually plays.
- "Depth 4 gives a fuller picture": past depth 4 the report turns into a survey, and the role of the target gets lost in it.
- "It is close enough to Application service": a near match hides the finding. Say the role does not fit the table and describe what it does.
- "The coupling is obvious, no need to cite it": every hidden-coupling item carries a `file:line` so the reader can check it in one step.

## Red Flags

- Stop and run the caller grep when the Callers list is empty and the target has exports.
- Stop and cite the location when a claim in the report carries no `file:line`.
- Stop at the report when the next step you are drafting is an edit or a refactor proposal.
- Stop and narrow `--depth` when the traced file count passes what fits in one report.

## Verification

- The report has every heading from the step 7 template.
- Every caller, callee, and hidden-coupling line cites `file:line`.
- The role names one table entry with a justification, or says plainly that none fits.
- No file was modified during the run.

## Related skills

- `/onboard` for whole-repo orientation.
- `/explain` for line-level explanation of a block.
- `/refactor` after the zoom-out reveals a structural problem.
- `/investigate` when the goal is finding a bug, not understanding the structure.
