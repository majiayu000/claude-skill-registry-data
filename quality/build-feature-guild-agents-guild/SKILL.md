---
name: build-feature
description: "Full pipeline: evaluation -> spec -> implementation -> review -> QA"
user-invocable: true
workflow:
  version: 1
  steps:
    - id: evaluate
      role: advisor
      intent: "Evaluate the feature against the project vision. Identify risks, dependencies, and conflicts. Issue verdict: Approved / Rejected / Requires adjustments."
      requires: [feature-description]
      produces: [evaluation-report, verdict]
      model-tier: reasoning
    - id: design
      role: tech-lead
      intent: "Break the feature into concrete tasks with acceptance criteria. Define implementation approach: files to modify, patterns to follow, interfaces, and technical risks."
      requires: [feature-description, evaluation-report]
      produces: [task-list, acceptance-criteria, technical-plan]
      model-tier: reasoning
    - id: implement
      role: developer
      intent: "Implement the feature following the technical plan. Write unit tests. Make atomic commits."
      requires: [technical-plan, acceptance-criteria]
      produces: [implementation, test-results]
      model-tier: execution
    - id: gate-pre-review
      role: system
      intent: "Run project tests and lint. Both must pass before review."
      gate: true
      produces: [gate-pre-review-result]
    - id: checkpoint
      role: system
      intent: "Create checkpoint commit and write partial pipeline trace to spec file."
      requires: [implementation, gate-pre-review-result]
      produces: [checkpoint-commit]
      gate: true
    - id: review
      role: code-reviewer
      intent: "Review code quality, patterns, security, and test coverage. Classify findings as Blocker, Warning, or Suggestion."
      requires: [implementation, gate-pre-review-result]
      produces: [review-report]
      model-tier: reasoning
    - id: fix-review-blockers
      role: developer
      intent: "Fix blocker findings from code review. Run tests after fixing."
      requires: [review-report]
      produces: [implementation]
      model-tier: execution
    - id: qa-phase
      role: qa
      intent: "Validate acceptance criteria, test edge cases, run bugfix cycles if needed."
      requires: [acceptance-criteria, implementation]
      produces: [qa-report]
      model-tier: execution
    - id: gate-final
      role: system
      intent: "Run project tests and lint as final verification. Both must pass."
      gate: true
      produces: [final-gate-result]
    - id: completion
      role: system
      intent: "Present pipeline summary to user."
      requires: [final-gate-result, review-report, qa-report]
      produces: [pipeline-summary]
      gate: true
---

# Build Feature

Full pipeline to build a feature end-to-end with all team agents. Each phase invokes a specialized agent using the `Task` tool.

## When to use

- ANY code change with acceptance criteria or a spec — regardless of perceived size
- New features, enhancements, bug fixes with defined requirements
- Even "small" changes: if the user described what it should do, it goes through the pipeline

## When NOT to use

- Typo fixes, config tweaks, dependency bumps — changes with no behavioral spec
- CLAUDE.md updates
- When the user explicitly says "do this without guild" or "just do it"

## Usage

`/build-feature [feature description]`

## Parallel Execution: Worktree Isolation

When multiple build-feature pipelines run in parallel, each MUST use its own git worktree to avoid branch conflicts:

```bash
git worktree add .claude/worktrees/[branch-name] -b [branch-name] develop
```

All file operations within the pipeline must use the worktree directory as the working directory. After the PR is merged, clean up with:

```bash
git worktree remove .claude/worktrees/[branch-name]
```

When running a single build-feature, a simple `git checkout -b` is sufficient.

## 5-Phase Pipeline

### Progress Display

At the start of each phase, display a progress indicator to the user before any agent output:

```text
[1/5] Advisor (opus) — Evaluating feature...
[2/5] Tech Lead (opus) — Defining spec and technical approach...
[3/5] Developer (sonnet) — Implementing...
[4/5] Code Reviewer (opus) — Reviewing changes...
[5/5] QA (sonnet) — Validating acceptance criteria...
```

When the preferred model for a tier is unavailable, show the fallback with an arrow indicating what was attempted:

```text
[1/5] Advisor (sonnet ← opus) — Evaluating feature...
[3/5] Developer (haiku ← sonnet) — Implementing...
```

Display the normal format (just the model name) when the preferred model resolves successfully. Display the fallback format `(actual ← preferred)` only when a fallback was required.

Model names are resolved from the step's `model-tier` using the preferred model defined in Model Resolution (see Subagent Configuration). System/gate steps do not show a model name.

When a phase loops (review-fix or QA-review cycles), show the iteration:

```text
[4/5 · round 2] Code Reviewer (opus) — Re-reviewing after fixes...
[3/5 · round 2] Developer (sonnet) — Fixing review blockers...
```

This indicator MUST be displayed after model resolution completes but before processing the agent's response. If the preferred model fails and fallback is triggered, display the fallback notation `(actual ← preferred)` — the user sees the resolved model, never the failed attempt.

The fallback notation applies to all progress lines, including loop iterations.

### Phase 1 — Evaluation (Advisor)

**Progress:** `[1/5] Advisor (opus) — Evaluating feature...`

The model name in parentheses is always the resolved model after applying Model Resolution rules. If a fallback was used, it shows `(actual ← preferred)` instead. This applies to all phases — the `model:` values shown in each phase description are the preferred models, subject to the resolution process defined in Subagent Configuration.

**Agent:** Reads `.claude/agents/advisor.md` via Task tool with `model: "opus"`
**Input:** The feature description provided by the user
**Process:**

1. The Advisor evaluates the feature against the project vision
2. Identifies risks, dependencies, and conflicts with existing functionality
3. Issues evaluation: Approved / Rejected / Requires adjustments

**Output:** Evaluation with reasoning and identified risks
**Trace data:** Verdict (Approved/Rejected/Approved with conditions), risks identified, conditions if any
**Exit condition:** If the Advisor rejects the feature, the pipeline stops here. Inform the user of the reason and suggest adjustments if any.

### Phase 2 — Specification & Technical Approach (Tech Lead)

**Progress:** `[2/5] Tech Lead (opus) — Defining spec and technical approach...`
**Agent:** Reads `.claude/agents/tech-lead.md` via Task tool with `model: "opus"`
**Input:** The feature approved by the Advisor + their observations
**Process:**

1. The Tech Lead breaks the feature into concrete tasks with verifiable acceptance criteria
2. Defines the implementation approach: files to modify, patterns to follow, interfaces
3. Anticipates technical risks and proposes mitigations
4. Estimates effort and suggests implementation order

**Output:** Task list with acceptance criteria + technical plan with files, patterns, interfaces, and risks
**Trace data:** Tasks defined count, acceptance criteria count, key patterns identified, files to modify, technical risks

### Phase 3 — Implementation (Developer)

**Progress:** `[3/5] Developer (sonnet) — Implementing...`
**Agent:** Reads `.claude/agents/developer.md` via Task tool with `model: "sonnet"`
**Input:** Tech Lead technical plan + acceptance criteria
**Process:**

1. The Developer implements following the technical plan
2. Writes unit tests as part of the implementation
3. Makes atomic commits with descriptive messages
4. Verifies that tests pass

**Output:** Implemented code + tests + commits made
**Trace data:** Files created/modified, tests added, commits made

### Pre-Review Gate (mandatory)

Before advancing to Phase 4, run automated verification:

1. Run the project test commands (e.g., `npm test`) — if it fails, the Developer must fix before advancing
2. Run the project lint commands (e.g., `npm run lint`) — if it fails, the Developer must fix before advancing
3. Only make a checkpoint commit **after** both pass

This gate CANNOT be skipped, even if the user requested phase skipping. The specific commands are in the "CLI commands" section of CLAUDE.md.

**Trace data:** Tests pass/fail, lint pass/fail

### Phase 4 — Review (Code Reviewer)

**Progress:** `[4/5] Code Reviewer (opus) — Reviewing changes...`
**Agent:** Reads `.claude/agents/code-reviewer.md` via Task tool with `model: "opus"`
**Input:** The implemented changes (git diff)
**Process:**

1. The Code Reviewer reviews quality, patterns, security, and tests
2. Classifies findings as Blocker, Warning, or Suggestion

**Output:** Review report with classified findings
**Trace data:** Blockers count, warnings count, suggestions count, review-fix loops
**Loop condition:** If there are Blocker findings, return to **Phase 3** for the Developer to fix them. Maximum 2 review-fix iterations.

### Phase 5 — QA (delegates to /qa-cycle)

**Progress:** `[5/5] QA (sonnet) — Validating acceptance criteria...`

Runs the `/qa-cycle` skill passing the acceptance criteria as context. The qa-cycle handles:

1. Running project tests and lint
2. Validating acceptance criteria
3. Testing edge cases and error scenarios
4. Bugfix cycle if issues arise (maximum 3 cycles)

**Trace data:** Acceptance criteria verified count, bugs found, QA cycles
**Additional loop condition:** If the qa-cycle bugfix introduces significant changes, return to **Phase 4** (Review) for verification. Maximum 2 review-QA cycles.

## Checkpoint Commits

After each phase completes, create a checkpoint commit to preserve progress. This ensures work survives session interruptions.

```bash
git add -A
git commit -m "wip: [feature-name] phase N complete — [phase-name]"
```

Pattern for each phase:

- After Phase 1: `wip: [feature] phase 1 — advisor approved`
- After Phase 2: `wip: [feature] phase 2 — spec and tech approach defined`
- After Phase 3: `wip: [feature] phase 3 — implementation done` -- also write partial trace (phases 1-3) to spec and update status to `implementing`
- After Phase 4: `wip: [feature] phase 4 — review passed`
- After Phase 5: `wip: [feature] phase 5 — QA passed`

## Pipeline Trace

After pipeline completion, append a `## Pipeline Trace` section to the feature's spec file in `docs/specs/`. This provides a structured record of what happened in each phase.

### Spec file discovery

1. Search `docs/specs/` for a file whose `spec-id` frontmatter matches the feature name (kebab-case)
2. If no matching spec exists, auto-create a minimal spec file at `docs/specs/[feature-name].md`

### Auto-created spec format

When no prior council spec exists, create a minimal spec:

````markdown
---
spec-id: [feature-name]
status: implementing
date: [YYYY-MM-DD]
council-type: none (pipeline-generated)
---

# Spec: [Feature Name]

## Context

Spec auto-generated by /build-feature pipeline. No prior council session.

## Pipeline Trace

[trace content appended here]
````

### Status field updates

- At Phase 4 checkpoint: set `status: implementing`
- At pipeline completion: set `status: implemented`

### Trace section format

Append this section to the spec file:

````markdown
## Pipeline Trace

pipeline-start: [YYYY-MM-DD]
pipeline-end: [YYYY-MM-DD]
phases-completed: [N]/5
review-fix-loops: [N]
qa-cycles: [N]
final-gate: pass | fail

### Phase 1 — Evaluation

- **Verdict**: [Approved/Rejected/Approved with conditions]
- **Risks identified**: [list or "None"]

### Phase 2 — Specification & Technical Approach

- **Tasks defined**: [N]
- **Acceptance criteria**: [N]
- **Key patterns**: [list]
- **Files to modify**: [list]
- **Technical risks**: [list or "None"]
- **Estimated effort**: [summary]

### Phase 3 — Implementation

- **Files created/modified**: [list]
- **Tests added**: [N]
- **Commits**: [list of commit summaries]

### Pre-Review Gate

- **Tests**: pass | fail
- **Lint**: pass | fail

### Phase 4 — Review

- **Blockers**: [N]
- **Warnings**: [N]
- **Suggestions**: [N]
- **Review-fix loops**: [N]

### Phase 5 — QA

- **Acceptance criteria verified**: [N]/[total]
- **Bugs found**: [N]
- **QA cycles**: [N]

### Final Gate

- **Tests**: pass | fail
- **Lint**: pass | fail
- **Result**: pass | fail
````

### When to write the trace

- **Phase 3 checkpoint:** Write a partial trace covering phases 1-3 to the spec file. Set status to `implementing`. Include the spec file in the checkpoint commit.
- **Pipeline completion:** Write the complete trace (all phases) to the spec file. Set status to `implemented`. Include the spec file in the final checkpoint commit.

## Final Gate (mandatory before Completion)

Before declaring the pipeline as complete, run final verification:

1. Run project tests — if it fails, return to Phase 5 (QA/Bugfix)
2. Run project lint — if it fails, return to Phase 3 (Developer)
3. Both must pass with exit code 0

This gate is the last safety net. It CANNOT be skipped under any circumstances.

**Trace data:** Tests pass/fail, lint pass/fail, result (pass/fail)

## Completion

Upon successfully completing all phases and the final gate:

1. Write the complete Pipeline Trace to the spec file (see "Pipeline Trace" section above). Update the spec status to `implemented`. Include the spec file in the final checkpoint commit.

2. Present pipeline summary:
   - Feature implemented
   - Files modified/created
   - Tests run and result
   - Review issues resolved
   - Final QA result

3. Close the GitHub Issue (if applicable):
   - Do NOT use `Closes #N` in PR description (only works when merging to default branch)
   - After the PR is merged, run: `gh issue close N --comment "Resolved in PR #X"`

## Subagent Configuration

When spawning agents via the Task tool, use these `subagent_type` values:

| Guild Agent Role | subagent_type to use |
| --- | --- |
| advisor, tech-lead | `"general-purpose"` |
| developer, bugfix | `"general-purpose"` |
| code-reviewer, qa | `"general-purpose"` |

**IMPORTANT:** Guild agent role names (advisor, developer, etc.) are NOT valid Claude Code subagent_types. Always use `"general-purpose"` for agents that need full tool access (Read, Write, Edit, Bash, Grep, Glob, etc.). Never use `"Bash"` alone — it lacks file editing tools.

Example Task invocation:

```text
Task tool with:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: "Read .claude/agents/advisor.md and assume that role. Then: [task description]"
```

The `model` parameter is resolved from the step's `model-tier`: reasoning→`"opus"`, execution→`"sonnet"`, routine→`"haiku"`. System/gate steps run inline (no Task tool).

### Model Resolution

Each `model-tier` maps to a preferred model and a fallback:

| model-tier | Preferred | Fallback |
| --- | --- | --- |
| reasoning | opus | sonnet |
| execution | sonnet | haiku |
| routine | haiku | sonnet |

The `routine` tier falls back up to sonnet because haiku has no lower-tier fallback — sonnet serves as the universal backup.

**Resolution process:**

1. Attempt the Task tool call with the preferred model for the step's `model-tier`
2. If the call fails or is rejected (model unavailable, rate-limited, or not accessible on the current plan), retry immediately with the fallback model
3. Display the progress indicator showing which model was actually used (with fallback notation if applicable) before processing the agent's response

A single retry is sufficient. If both preferred and fallback fail, surface the error to the user and halt the pipeline.

## Example Session

```text
User: /build-feature add dark mode toggle to settings page

[1/5] Advisor (opus) — Evaluating feature...
  Approved. Low risk, aligns with UX roadmap.

[2/5] Tech Lead (sonnet ← opus) — Defining spec and technical approach...
  3 tasks defined. Use CSS variables + context provider pattern.

[3/5] Developer (sonnet) — Implementing...
  Implemented ThemeContext, toggle component, CSS vars.

[4/5] Code Reviewer (opus) — Reviewing changes...
  Passed. 1 suggestion (memoize context value).

[5/5] QA (sonnet) — Validating acceptance criteria...
  All 3 acceptance criteria verified. 0 bugs.

Feature complete. PR ready for merge.
```

In this example, opus was unavailable during Phase 2 so the Tech Lead fell back to sonnet. All other phases used their preferred model.

## Notes

- Phase skipping is ONLY allowed when the user explicitly requests it (e.g., "skip eval, go straight to implementation"). The agent must NEVER decide on its own that a task is "simple enough" to skip phases. If in doubt, run the full pipeline. Verification gates (pre-Review and final) are NEVER skipped
- The pipeline is sequential: each phase depends on the output of the previous one
- Review/QA loops have limits to prevent infinite cycles
- In v1.x, parallel pipeline execution (multiple build-features via worktrees) is best-effort and depends on the host environment supporting concurrent agents
