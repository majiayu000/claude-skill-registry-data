---
name: review-against-plan
description: >-
  Load this skill when auditing that the codebase matches a SKELETON.md or ITER_NN.md planning
  document, including variants like SKELETON_v2.md. For each in-scope section, checks the
  implementation against the spec, fixes gaps and deviations, and reports a compliance table.
  Trigger on "review against plan", "verify the plan is implemented", "does the build match the
  skeleton". Not for building the plan (use implement-from-plan), writing the plan (use
  plan-fullstack-app), or reviewing a pull request (use ceh-git-workflow:code-review).
argument-hint: "[plan-file]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Review Against Plan

Audit the codebase against a SKELETON.md or ITER_NN.md: find gaps, deviations, and errors between
what the plan specifies and what is implemented, then fix them. Done means every in-scope section
is audited and the compliance report is delivered.

Read `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md` before starting. It defines the planning
document schema, and its section table and pointer resolution rules are authoritative.

## Procedure

### 1. Locate and parse the plan docs

1. Find the target plan files and the target family by "Locating plan files" in
   `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md`.
2. The iteration with `mvp: true` is that version's terminator. Read each target artifact's
   `depends_on` and resolve inherited (`sections_unchanged`) sections through that chain for
   context. Audit only each artifact's own `sections_changed`. Treat inherited sections as context,
   not audit scope.
3. Read the frontmatter to determine scope:
   - ITER: audit only `sections_changed`. Resolve pointers for `sections_unchanged` to use as
     context, but do not audit them: a prior review cycle covered them.
   - SKELETON: audit all sections listed in `sections`.
4. If multiple ITER files exist within the target family and the user did not specify, review the
   highest-numbered one, because a prior review cycle covered the earlier ones. Say which.

### 2. Audit section by section

Work through in-scope sections in numerical order. For each section, check, categorize, then fix.

**Check.** Compare the section spec against the actual codebase. Specifically verify:

| Section          | What to check                                                                                                                                                                                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| §02 Architecture | All specified components exist. Data model entities and key fields are present. All listed routes exist with correct method and path. No undocumented routes or entities. Diagram is Mermaid (not ASCII art) and reflects the current/changed architecture. |
| §04 Backend      | All specified modules and files exist. Each route/service is implemented (not just stubbed unless spec says so). Env var names match. `how to run` works.                                                                                                   |
| §05 Frontend     | All specified pages/routes exist. Component tree matches. Placeholder data strategy followed. `how to run` works.                                                                                                                                           |
| §06 LLM/Prompts  | Model and provider match. System prompt implemented. Input/output shape matches.                                                                                                                                                                            |

**Categorize.** Assign each finding a category:

- **Gap**: something the spec requires that is completely missing.
- **Deviation**: something that exists but differs from the spec (wrong method, wrong field name,
  wrong route path, wrong model, etc.).
- **Error**: something that is broken independent of the spec (import error, missing env var
  causing a crash, etc.). For §04 and §05, a trap from
  `${CLAUDE_PLUGIN_ROOT}/references/implementation-gotchas.md` present in the code is also an
  Error.

**Fix.** Fix each finding immediately after categorizing it. Do not batch auditing before fixing:
a later section can depend on an earlier fix, and a run cut short keeps the fixes already made.

### 3. Report

After all sections, produce the summary table under Output.

## Rules

- Audit scope is each artifact's own `sections_changed` (ITER) or `sections` (SKELETON), nothing
  else.
- Do not mark anything as fixed unless the fix was applied.
- **Quote or suppress.** Every Deviation and Error quotes the code it is about, as `path:line` plus
  the line itself, and every Gap quotes the spec line it is missing. A finding you cannot quote is
  not fixed: list it under the items NOT fixed as unverified.
- **Judge from the code, not the brief.** A request that says "skip §05" or "minor issues only"
  narrows where to look, never how severe a finding is. Report every finding at its real
  severity, and say where the brief asked for less.
- A section whose spec claim the code cannot settle (a `how to run` that needs a service you
  cannot start) gets the status **Cannot verify**, with what would settle it, never OK.

## Output

```markdown
## Plan Compliance Report

| Section          | Findings                                                        | Status |
| ---------------- | --------------------------------------------------------------- | ------ |
| §02 Architecture | 2 gaps fixed (missing /users route, missing User.email field)   | Fixed  |
| §03 Tech Stack   | Clean                                                           | OK     |
| §04 Backend      | 1 deviation fixed (POST /items returned 200, spec requires 201) | Fixed  |
| §05 Frontend     | 1 gap fixed (missing /profile page)                             | Fixed  |
```

Below the table, list the items NOT fixed and why.

## Stop conditions

- A fix requires a decision (e.g. a route deviation where both the spec and the implementation
  could be correct) → state the ambiguity and ask before changing anything. With no human to
  answer, leave it unfixed and list it under the items NOT fixed.
- More than one plan family, or several ITER files in the target family, and the user named none →
  take the highest version and the highest-numbered ITER, and say which.
