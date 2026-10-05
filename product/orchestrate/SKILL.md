---
description: "Orchestrator for parallel Linear Issue implementation. Analyze milestones and dependencies, then delegate implementation to sub-agents in optimal order and concurrency"
user-invokable: true
---

# /orchestrate

An orchestration skill that understands milestones, analyzes dependencies, and delegates implementation of multiple Linear Issues to sub-agents.

## Arguments

- `/orchestrate` — Analyze active milestones and suggest the next Issues to implement
- `/orchestrate <Issue ID> [Issue ID...]` — Implement specified Issues considering dependencies
- `/orchestrate milestone <name>` — Implement Issues in the specified milestone in dependency order
- `/orchestrate status` — Show all milestone progress + running sub-agent status

---

## Steps

### Phase 0: Product Understanding — Milestone and Current State Overview

**Do this first on every run.** The orchestrator first adopts the product owner's perspective.

#### 0-1. Fetch All External Context (Parallel)

Launch all of the following **in a single parallel batch** (5 calls total):

- `mcp__linear-server__list_milestones(project=yorishiro-proxy)`
- `mcp__linear-server__get_document(id=d413edd7-d296-433a-ab94-11d4dd57d883)` (roadmap)
- `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=started)`
- `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=backlog)`
- `mcp__linear-server__list_issues(team=Usk6666, project=yorishiro-proxy, state=unstarted)`

#### 0-2. Process Fetched Data

From the milestone list, classify progress:

- `progress == 100` → Complete
- `0 < progress < 100` → Active (in progress)
- `progress == 0` → Not started

From the roadmap document, extract:

- **Product goal**: What is being built and for whom
- **Milestone structure**: The goal and delivered value of each milestone
- **Inter-milestone dependencies**: Which milestone depends on which
- **Issue ordering within milestones**: Natural implementation order of Issues within each milestone
- **Technical decisions**: Design decisions already made (storage choice, protocol strategy, etc.)

Group fetched Issues by `projectMilestone` field.
**Do not fetch completed Issues.** Use milestone progress + roadmap Issue table to track completion status.
Only fetch specific completed Issues individually with `get_issue(id)` when needed for building dependency context.

> **Note**: Codebase state checks (file existence, type verification) are deferred to Phase 1-1
> where they can be done precisely for the specific dependencies that matter.

#### 0-3. Generate Current State Summary

Present a concise milestone-based summary to the user:

```markdown
## Project State Analysis

### Milestone Progress
| Milestone | Progress | Remaining |
|-----------|----------|-----------|
| M1: Foundation | 100% | — |
| M2: MCP Interface v2 | 79% | 3 issues |  ← ACTIVE
| M3: Active Testing | 0% | N issues |
| M4: Multi-Protocol | 0% | N issues |
| M5: Production Ready | 0% | N issues |

### Active: M2 — MCP Interface v2
| ID | Title | Status | Priority |
|----|-------|--------|----------|
| USK-79 | ... | Backlog | High |
| ...
```

---

### Phase 1: Dependency Analysis and Execution Plan

#### 1-1. Build Dependency Graph Between Issues

Analyze the following dependencies from milestone structure and Issue descriptions:

**Inter-milestone dependencies** (dynamic analysis based on roadmap):
- Read dependency information from the milestone sections of the roadmap document
- Determine dependency satisfaction from milestone progress (`progress == 100` → satisfied)
- Do not start Issues in a milestone whose prerequisite milestone is not complete

**Intra-milestone dependencies** (inferred from Issue content):
Fetch each Issue's description with `mcp__linear-server__get_issue` and determine dependencies from these perspectives:

1. **Data dependency**: Issue A creates types/interfaces that Issue B uses
2. **Functional dependency**: Issue A's functionality must work before Issue B can be tested
3. **Integration dependency**: There is an Issue C that combines the outputs of Issues A and B

Also refer to Linear's `blockedBy` / `blocks` fields, but if not set,
infer dependency relationships from the roadmap's Issue ordering and Issue content.

When a dependency is identified, **verify it against the actual codebase** (e.g., check that
the expected file/type/interface exists with Glob or Grep). This replaces the former Phase 0
codebase check with targeted, dependency-driven verification.

#### 1-2. Identify Parallel Execution Groups

Derive groups of Issues (parallel execution batches) that can be run simultaneously from the dependency graph.

**Conditions for parallel execution:**
- No mutual dependencies
- Primarily modify different packages/files (low conflict risk)
- Issues from the same milestone or from milestones whose dependencies are satisfied

#### 1-3. Present Execution Plan

Present the plan to the user in the following format and get approval:

```markdown
## Execution Plan

### Target Milestone: M2 — MCP Interface v2

### Batch 1 (Parallel Execution)
| Issue | Title | Branch | Reason |
|-------|-------|--------|--------|
| USK-XX | ... | feat/USK-XX-xxx | No dependencies |
| USK-YY | ... | feat/USK-YY-yyy | No dependencies |

### Batch 2 (After Batch 1, Parallel Execution)
| Issue | Title | Branch | Dependencies |
|-------|-------|--------|-------------|
| USK-AA | ... | feat/USK-AA-aaa | USK-XX |

### Concurrency: Max 2 (Batch 1) → Sequential (Batch 2)
### Estimated PRs: 3
```

---

### Phase 1.5: Per-Issue Design Review (Parallel)

Run a pre-implementation design review for each Issue in the upcoming batch — in parallel, read-only.
This catches ambiguity, principle violations, and pattern-match false positives **before** any
implementer agent starts coding. Especially important for ad-hoc Issues filed from test-stage
findings (e.g., bug reports surfaced during e2e or manual verification), which did not pass
through `/project plan` milestone planning and therefore have no upstream design vetting.

The design-reviewer Agent template is the same one used by `/implement` Step 4 and
`/project plan` Greenfield Mode — see `.claude/agents/design-reviewer.md`. This phase mirrors
that invocation pattern so all three skills stay in sync.

#### 1.5-1. Skip Rules

Skip the design review for an Issue when **all** of the following are true:

- No new public types and no interface changes
- No more than a single call site touched
- Test-only, docstring-only, or comment-only change

Record the skip reason in the Phase 1-3 plan you presented to the user, alongside the
Issue row. When in doubt, do not skip — design review is read-only and cheap relative to
discovering a wrong approach during implementation.

#### 1.5-2. Launch Design Reviewers in Parallel

For each non-skipped Issue in the upcoming batch, launch a design-reviewer Agent in parallel
(single message, multiple Task calls):

```
Task(
  description="Design review: <Issue ID>",
  subagent_type="general-purpose",
  isolation="worktree",
  prompt=<composed from .claude/agents/design-reviewer.md>
)
```

**Placeholder values** (mirrors `/implement` Step 4 invocation — keep in sync):

| Placeholder | Value |
|---|---|
| `{{SCOPE_DESCRIPTION}}` | Issue title + description + tentative file actions (new / modified) inferred from the Issue body |
| `{{SPEC_REFERENCES}}` | Paths to relevant spec/design docs. Cite specific sections (`docs/rfc/envelope.md §3.3`), not whole files. For data-path Issues, always include `docs/rfc/envelope.md`. |
| `{{PACKAGES_TO_SURVEY}}` | Packages the Issue creates, modifies, or depends on |
| `{{COMPLETED_CONTEXT}}` | The `{{DEPENDENCY_CONTEXT}}` you already built in Phase 1 (outputs of completed dependency Issues — types, interfaces, file paths) |
| `{{PRODUCT_IDENTITY}}` | Read from `.claude/skills/review-gate/SKILL.md` Phase 1-4 "Product context" block — single source of truth |
| `{{PRINCIPLES}}` | The **MITM Implementation Principles** list from `CLAUDE.md`, quoted verbatim — all items, not a fixed count (the list grows; do not hardcode a number here) |

**Concurrency**: same cap as the implementer batch (max 3 from Notes). If the upcoming batch
has more than 3 Issues, run design reviews in sub-batches matching the implementer parallel
groups.

#### 1.5-3. Process Each `DESIGN_REVIEW_RESULT`

Each design-reviewer Agent returns a structured `DESIGN_REVIEW_RESULT` (see
`.claude/agents/design-reviewer.md` Step 5 for the format). Triage per Issue:

| Outcome | Action |
|---|---|
| All resolved + fitness PASS | Fold the **Resolved** table and **Boundary Survey Summary** into `{{DESIGN_REVIEW_CONTEXT}}` for the implementer (see Phase 2-1). Proceed to Phase 2 for this Issue. |
| Unresolved items exist | **Pause orchestrate**. Present only the unresolved questions to the user with the agent's proposed answers and trade-offs. After user input, fold both resolved + user-resolved decisions into `{{DESIGN_REVIEW_CONTEXT}}`. Do not re-ask resolved questions. |
| Fitness check FAIL | **Pause orchestrate**. Report scope adjustment recommendations. Ask the user whether to (a) adjust the Issue scope and re-run design review, (b) split the Issue per Phase 2-2-A, or (c) drop this Issue from the batch. Do not launch the implementer for this Issue until the fitness failure is resolved. |
| Step 3.5 says "Defense-in-depth" or "Pattern-match false positive" | Surface the classification to the user and request an explicit decision: proceed / defer with re-open trigger / close as not-applicable. The default for these classifications is **not** to implement — see CLAUDE.md MITM Principle #6. |

If multiple Issues in the batch produce unresolved/fitness-fail results, batch the user
prompts together (one message per orchestrate run, not one per Issue) to avoid pause-fatigue.

#### 1.5-4. Cleanup Tracking

Record each design-reviewer's `agentId` (from the Task tool return value). Phase 3-3
worktree cleanup will remove these worktrees alongside the implementer worktrees.

---

### Phase 2: Sub-Agent Launch and Management

#### 2-1. Per-Batch Execution

Based on the plan, launch sub-agents per batch.
**Launch Issues within a batch in parallel; execute between batches sequentially.**

Task tool settings for each Issue:

- `subagent_type`: `"general-purpose"`
- `isolation`: `"worktree"` — Each sub-agent works in an independent git worktree
- `description`: Short description including the Issue ID (e.g., `"Implement USK-30"`)
- `prompt`: Read the `.claude/agents/implementer.md` prompt template, replace placeholders with actual values, and pass it

**Placeholder list:**
- `{{ISSUE_ID}}` → Issue ID (e.g., `USK-30`)
- `{{ISSUE_TITLE}}` → Issue title
- `{{ISSUE_DESCRIPTION}}` → Issue description (Markdown)
- `{{ISSUE_LABELS}}` → Comma-separated label names
- `{{BRANCH_NAME}}` → Branch name (e.g., `feat/USK-30-http-handler`)
- `{{BRANCH_TYPE}}` → `feat` / `fix` / `chore`
- `{{PRODUCT_CONTEXT}}` → Product context built in Phase 0 (described below)
- `{{DEPENDENCY_CONTEXT}}` → Dependency context for this Issue (described below)
- `{{DESIGN_REVIEW_CONTEXT}}` → Design review findings folded in from Phase 1.5 (described below). For Issues that skipped Phase 1.5, set to a one-line note stating the skip reason (e.g., `"Skipped: test-only change"`).

**Building `{{PRODUCT_CONTEXT}}`:**

The static product/security context (architecture, data path packages, threat model) lives in **`/review-gate` SKILL.md Phase 1-4** as the single source of truth. Sub-agents already read `CLAUDE.md`, which covers conventions and package layout. Do **not** duplicate either source here — only add milestone-specific and Issue-specific context on top:

```
Current milestone: <Milestone name>
Goal: <milestone description>
Progress: <progress>%
This Issue is part of <Milestone name>, and <description of Issue's position>.

Relevant design decisions:
- <Technical decisions related to this Issue, derived from the roadmap>
```

**Building `{{DEPENDENCY_CONTEXT}}`:**

Concretely describe the outputs of completed Issues that this Issue depends on.
Helps sub-agents understand "what already exists" so they can integrate correctly.

If there are no dependencies:
```
This Issue has no preceding dependencies. Foundational type definitions and interfaces are
already defined in the scaffolding. See the package layout in CLAUDE.md.
```

If there are dependencies:
```
This Issue depends on the outputs of the following completed Issues:

### USK-XX: <title>
- Package: internal/connector/
- Provided type: `PeekConn` (net.Conn wrapper with Peek method)
- Usage: Create PeekConn in Listener.handleConn and pass to Detector
- Key files: internal/connector/detect.go

### USK-YY: <title>
- Package: internal/session/
- Provided interface: `Store` (Save, Get, List, Delete methods)
- Usage: Inject Store into HTTP handler constructor
- Key files: internal/session/store.go, internal/session/sqlite_store.go
```

Gather dependency context information from the PRs and actual codebase of completed Issues.
Including specific type names, method signatures, and file paths lets sub-agents
integrate accurately with existing code.

**Building `{{DESIGN_REVIEW_CONTEXT}}`:**

For Issues that ran through Phase 1.5, fold the design-reviewer's `DESIGN_REVIEW_RESULT` into a
condensed block the implementer can act on:

```
## Design Review Findings (Phase 1.5)

### Boundary Survey
<2-4 line summary of key types/interfaces/data flows the agent discovered>

### Resolved Decisions
| # | Question | Answer | Source |
|---|----------|--------|--------|
| 1 | ... | ... | RFC §X.Y / Principle #N / Sibling: <pkg> |

### Decisions Confirmed by User (if any)
| # | Question | Decision | Notes |
|---|----------|----------|-------|

### Fitness Check
PASS — all 6 MITM Principles upheld.
```

For Issues skipped per Phase 1.5-1, set `{{DESIGN_REVIEW_CONTEXT}}` to:

```
Design review skipped — <skip reason>. Implement directly per Issue description.
```

**Branch name determination rules:**
- Issue labels or title contains "bug" / "fix" → `fix/`
- Otherwise → `feat/`
- Branch name: `<type>/<issue-id>-<short-desc>` (kebab-case from Issue title, max 40 chars)

**Prompt construction steps:**
1. Read `.claude/agents/implementer.md` with the Read tool
2. Extract the code block inside the `## Prompt Body` section
3. Replace placeholders with actual values
4. Pass the replaced string as the `prompt` parameter to the Task tool

#### 2-2. Wait for Batch Completion and Launch Next Batch

When all sub-agents in a batch have completed:

1. **Validate results**: Confirm success/failure of each sub-agent
2. **Merge decision for successful PRs**: If the next batch depends on a PR,
   ask the user "Would you like to merge this PR before proceeding to the next batch?"
3. **Update main**: If merged, the next batch's sub-agents work from the latest main
4. **Handle failures**: Determine whether a failed Issue blocks subsequent batches
   - If a blocker: Try to fix it, or exclude the blocked Issue from subsequent batches
   - If not a blocker: Continue with subsequent batches and address the failed Issue later
   - If the sub-agent reports "scope is materially larger than spec implies": apply the **Split Oversized Issue** procedure (see 2-2-A below) instead of retrying.
5. **Verify main-clone branch**: Run `git branch --show-current` and `git worktree list` in the main clone. Sub-agents' Edit-tool race occasionally lands edits in the main clone; if main is off-base, switch back with `git checkout <base> && git pull --rebase origin <base>` before launching the next batch.
6. **Launch next batch**: Proceed to the next batch once the above is complete

#### 2-2-A. Split Oversized Issue

Trust the sub-agent's bottom-up scope reassessment when it has actually attempted the work — the agent estimates from compile errors and test ripples, which is grounded; the design review estimates from documentation and is sometimes optimistic. Do **not** push harder; split.

**Red flags during planning that suggest oversize** — if any of these were true at plan time, the issue was already too big:

- Multiple unrelated decision axes (e.g., "delete vs migrate" on more than one feature)
- Plan invokes a "may briefly break green within the PR" exemption
- Test fixture migration count > 20 sites
- Multiple new packages must be created
- A single file edit is projected to exceed 200 lines

**Salvage and split**:

1. Push the partial work as `wip/<original-issue-id>-partial-salvage` (single commit, descriptive message tagging what is salvageable and what is **not**). Stash-only is fragile — a worktree cleanup can lose it.
2. Re-read the user direction. The sub-agent may have misinterpreted (e.g., treated "delete X" as "migrate X"). Do not propagate the misinterpretation into the split.
3. Create N follow-up issues. Each split issue body must include:
   - Pointer to the salvage branch + commit SHA
   - Explicit "take vs ignore from salvage" list (the salvage often contains contradictory partial work)
   - Single-source-of-truth design citation (link the design-review answers, not the original Linear body which is now superseded)
   - `blockedBy` chain so Linear shows the order
4. Update the parent issue (do **not** close it). It becomes the "final cleanup + audit" PR after splits land. Set `blockedBy` to the new split issues. Move state back to `Backlog`.
5. Cleanup discipline: remove only the worktrees this session launched, via the canonical snippet in `CLAUDE.md` → Worktree Cleanup. `--force --force` is required to override locks (a failed sub-agent may have left lock files). Do not bulk-delete other sessions' worktrees.

#### 2-3. Parallel Launch Example

```
# Batch 1: Launch in parallel
Call multiple Task tools in the same message:
Task(description="Implement USK-XX", subagent_type="general-purpose", isolation="worktree", prompt=<prompt>)
Task(description="Implement USK-YY", subagent_type="general-purpose", isolation="worktree", prompt=<prompt>)

# Wait for Batch 1 to complete → validate results → PR merge decision

# Batch 2: Launch in parallel
Task(description="Implement USK-AA", subagent_type="general-purpose", isolation="worktree", prompt=<prompt>)
Task(description="Implement USK-BB", subagent_type="general-purpose", isolation="worktree", prompt=<prompt>)
```

---

### Phase 2.5: Review Gate

Run review gates in the background for PRs that succeeded in the batch.
Launch the entire review gate as a background Agent per PR so the orchestrator is not blocked.

#### 2.5-1. Identify Review Targets

Target Issues where a PR was created in the batch. Skip failed Issues (no PR).

#### 2.5-2. Launch Background Review Gate

Delegate the entire review → Fix → re-review cycle for each PR to **one background Agent**.
The orchestrator can proceed to the next batch preparation (merge decisions, etc.) without waiting for results.

Launch the following Agent for each PR with `run_in_background: true`:

```
Agent(
  description="Review gate PR #<N>",
  subagent_type="general-purpose",
  run_in_background=true,
  prompt=<review gate prompt>
)
```

**No `isolation` here, deliberately.** This agent launches other agents and touches no files
itself — it reads the PR through `gh` and delegates all code access to the reviewers and fixers
it spawns, which ARE isolated. Isolating it would make those children nest at
`agent-<parent>/.claude/worktrees/agent-<child>`; because `.claude/worktrees/` is gitignored,
removing the parent then leaves an unregistered husk directory that only `rm` can reclaim. Tell
the agent explicitly that it is running in the caller's checkout and must not check out a branch,
fetch into it, or edit/stage/commit anything there.

**Review Gate Prompt Content:**

The prompt passed to the Agent should instruct it to execute the `/review-gate` flow.
Read `.claude/skills/review-gate/SKILL.md` and include its full content in the prompt,
along with:
- PR number, branch name, Issue ID
- Product context, security context
- Content of agent templates (`.claude/agents/code-reviewer.md`, `.claude/agents/security-reviewer.md`, `.claude/agents/fixer.md`)

> **Single Source of Truth**: The review gate flow is defined in `/review-gate` SKILL.md.
> Do not duplicate the flow steps here. Always read the SKILL.md at prompt construction time
> to ensure the latest version is used.

**Expected Output Format:**

The Review Gate Agent must return results in this format:

```
REVIEW_GATE_RESULT:
  pr_number: <N>
  code_review: APPROVED | CHANGES_REQUESTED
  security_review: APPROVED | CHANGES_REQUESTED
  final_verdict: APPROVED | ESCALATED
  fix_rounds: 0 | 1 | 2
  low_fix_only: true | false
  unresolved_findings: [...]
  agent_ids: [<all sub-agent IDs launched>]
```

#### 2.5-3. Collect Review Results

When a background Agent sends a completion notification, parse and record the results.
If a merge decision is needed (the next batch depends on it), wait for that PR's review to complete.

#### 2.5-4. Concurrency Strategy

| Scenario | Strategy | Concurrent Agents |
|----------|----------|------------------|
| N PRs in a batch | Launch review gates for all PRs as background simultaneously | N |
| Inside each review gate | Code + Security in parallel | 2 |
| During Fix | Fixer 1 agent only (exclusive within review gate Agent) | 1 |

#### 2.5-5. Recording Review Results

Record each PR's review result in the following format for aggregation in Phase 3:

```
pr_review_results[PR number] = {
  code_review: APPROVED | CHANGES_REQUESTED,
  security_review: APPROVED | CHANGES_REQUESTED,
  final_verdict: APPROVED | ESCALATED,
  fix_rounds: 0 | 1 | 2,
  low_fix_only: true | false,
  unresolved_findings: [...]
}
```

#### 2.5-6. Linear Status Integration

| Event | Linear Comment |
|-------|---------------|
| Review starts | "PR #N created. Automated review starting." |
| Review passes | "PR #N: Code Review APPROVED, Security Review APPROVED" |
| LOW Fix applied | "PR #N: APPROVED with LOW findings. Applying fixes." |
| Fix cycle starts | "PR #N: Review found issues. Fix round N starting." |
| Passes after Fix | "PR #N: All findings resolved after N fix round(s)." |
| Escalation | "PR #N: ESCALATION - N unresolved findings after 2 fix rounds." |

Post comments to Issues using `mcp__linear-server__create_comment`.
Linear comments are posted inside the review gate Agent.

#### 2.5-7. Handling Escalations

If there are escalated PRs:
- Continue processing other PRs in the batch
- Report unresolved finding details to the user and request manual intervention
- Leave subsequent batch execution to the user's judgment (depending on whether it is a blocker)

---

### Phase 3: Aggregate and Report Results

#### 3-1. Overall Summary

After all batches complete, aggregate results by milestone:

```markdown
## Implementation Results Summary

### Milestone: M2 — MCP Interface v2

#### Batch 1
| Issue | Title | Status | PR | Tests | Code Review | Security Review | Fix Rounds |
|-------|-------|--------|----|-------|-------------|----------------|---------|------------|
| USK-XX | ... | Success | #4 | 8 passed | APPROVED | APPROVED | 0 |
| USK-YY | ... | Success | #5 | 12 passed | APPROVED | Fix→APPROVED | 1 |

#### Batch 2
| Issue | Title | Status | PR | Tests | Code Review | Security Review | Fix Rounds |
|-------|-------|--------|----|-------|-------------|----------------|---------|------------|
| USK-AA | ... | Success | #6 | 5 passed | APPROVED | APPROVED | 0 |
| USK-BB | ... | Failed | — | 2 failed | — | — | — |

### Failed Issues
- **USK-BB**: ... — Test failure
  - Worktree: `/path/to/worktree` (can be checked manually)
  - Recommended: Check error logs, manually fix, or re-run

### Escalated Issues (Review not passed)
- **USK-ZZ**: ... — N unresolved findings in Security Review
  - Recommended: Manual review and fix

### Milestone Completion Status
This batch run has brought M2 to 100%.
Next milestone: M3 (Active Testing)
Continue with `/orchestrate milestone M3`.
```

If the milestone is not complete, report remaining Issues and suggest next actions.

#### 3-2. Issue Status Updates

- Implementation success + review passed: Update status to "In Review"
- Implementation success + review escalated: Update to "In Review" and record unresolved findings in comments
- Implementation failed: Keep "In Progress" and record error details with `mcp__linear-server__create_comment`

#### 3-3. Worktree Cleanup

The Claude Code Task tool does not auto-delete worktrees when they have changes after completion.
The orchestrator (caller) explicitly deletes them.

**Important**: To prevent accidentally destroying worktrees actively in use by other sessions,
do not bulk-delete. **Only target the worktrees of sub-agents you launched.**

**Steps:**

1. Record agent IDs from each Task call result in Phase 1.5 (design-reviewer) and Phase 2 (implementer)
   (the `agentId` field in the Task tool return value)
2. In addition to the Phase 2.5 review gate Agent's agent ID,
   also collect the `agent_ids` list in the review gate Agent's output (IDs of sub-agents it launched internally)
3. After all batches and review cycles complete, run the following for each recorded agent ID
   (design-reviewer + implementer + review-gate + nested fixer/code-reviewer/security-reviewer IDs):

Write those IDs one per line to a file and run the canonical cleanup snippet against it.

> Use the canonical cleanup snippet in `CLAUDE.md` → **Agent Isolation Strategy → Worktree
> Cleanup**. Do not construct `.claude/worktrees/agent-<id>` from an ID (a nested sub-agent's
> worktree lives inside its parent's, so the path does not exist and the remove silently
> no-ops), use `--force --force` (a single `--force` fails on a locked worktree), and never
> select paths with `grep -F -f` (this machine's `grep` is ugrep: an empty pattern file matches
> every line).

Because the review-gate Agent is launched **without** isolation (2.5-2), the reviewer and fixer
worktrees it creates are flat siblings of the ones this phase created — there is no nesting to
unwind. The snippet resolves real paths anyway, so it stays correct if that ever changes.

- Delete all worktrees you launched regardless of success/failure (changes are pushed to remote)
- Debug information for failed Issues is accessible via Linear comments and `git checkout <branch-name>`
- `git worktree remove` only deletes the directory; branches and commits are preserved

#### 3-4. Suggest Next Steps

Suggest the next executable milestone/batch.

---

## Dependency Analysis Guidelines

### Inter-Milestone Dependencies (Dynamic analysis based on roadmap)

Read the dependency information from the milestone sections of the roadmap document
and determine dependency satisfaction from milestone progress.

- `progress == 100` → Dependency satisfied. Can proceed to subsequent milestone Issues
- `0 < progress < 100` → Partially satisfied. May be able to proceed depending on remaining Issue content
- `progress == 0` → Not satisfied. Prerequisite milestone goes first

### Intra-Milestone Dependency Inference Rules

1. **Infrastructure/utility Issues go first**: Foundational items like buffered readers and storage layers
2. **Handlers/business logic in the middle**: Logic built on top of the foundation
3. **Integration/combining Issues later**: Issues that connect multiple components go after dependencies are ready
4. **E2E tests/integration tests last**: After all components are in place
5. **MCP tool definitions after corresponding internal implementations**: Expose tools after the internal API is finalized

### Criteria for Parallel Execution

**Can run in parallel:**
- Primarily modify different packages (e.g., `internal/connector/` and `internal/layer/`)
- Implement a common interface but do not call each other
- Tests do not depend on each other's implementations

**Must run sequentially:**
- Issue B imports types or interfaces generated by Issue A
- Issue B's tests assume Issue A's implementation
- Issue B modifies the same part of a file changed by Issue A

---

## Notes

- Maximum concurrent executions: up to 3 Issues (due to resource constraints)
- Always load the latest roadmap (do not cache)
- Do not implement across milestones as a general rule (proceed to the next after the previous milestone's PRs are merged)
- Each sub-agent operates completely independently — no cross-references
- Linear Issue status updates are the orchestrator's responsibility (sub-agents do not do this)
- If you are not confident in the dependency analysis result, confirm with the user
