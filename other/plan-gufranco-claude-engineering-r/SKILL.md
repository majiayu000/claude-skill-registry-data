---
name: plan
description: Plan implementations, record architecture decisions, and scaffold boilerplate, with subcommands plan (default), adr, and scaffold. Creates spec folders, manages ADRs, and generates files from existing project patterns. Use when user says "plan this", "how should I implement", "design this feature", "create an ADR", "scaffold a service", "architecture decision", or needs to think through an approach before coding. For code review, use /review; for shipping, use /ship; for running tests, use /test.
argument-hint: "/plan <feature> | /plan adr new <title> | /plan scaffold <type> <name> | /plan to-issues | /plan multi-execute <task>"
allowed-tools: "Read, Grep, Glob, Write, Edit, Bash, AskUserQuestion, WebFetch, WebSearch, Agent, Skill"
sensitive: true
---

## Overview

Unified planning skill for requirements gathering, architecture decisions, and code generation.

## When to Use

- Before implementing a change that touches 3 or more files, crosses a module boundary, or carries a real trade-off.
- When a significant architecture decision needs a record, or an earlier ADR is being reversed.
- When new boilerplate has to match an existing project pattern exactly.
- After a change is merged, to fold its spec delta into `specs/current/` with `/plan archive`.
- For reviewing finished code, use `/review`; for committing and opening the PR, use `/ship`; for running the suite, use `/test`; for a one-question throwaway prototype, use `/spike`.

## Process

1. Route the invocation with the table below. An unrecognized argument is a plan description.
2. Run the matching section. Each subcommand carries its own steps and rules, and the shared Rules at the end apply to all of them.

### Subcommand Routing

| Invocation | Action |
|-----------|--------|
| `/plan` or `/plan <description>` | Create implementation plan (default) |
| `/plan adr` | List existing ADRs |
| `/plan adr new <title>` | Create a new ADR |
| `/plan adr supersede <number> <title>` | Supersede an existing ADR |
| `/plan scaffold <type> <name>` | Generate boilerplate from project patterns |
| `/plan to-issues` | Export the active spec folder's task breakdown to GitHub issues |
| `/plan multi-execute <task>` | Plan and execute under a single-writer protocol with parallel model tiers |
| `/plan archive` | Merge a completed change's spec delta into the living spec and stamp the plan folder archived |

If no subcommand is recognized, treat the argument as a plan description.

---

## plan (default)

Gather requirements, search for existing solutions, evaluate trade-offs, and produce a structured implementation plan saved to a spec folder.

### When to use

- Before implementing any feature touching 3+ files or involving architectural decisions.
- When evaluating multiple approaches.
- Before refactoring that changes module boundaries.

### Arguments

- No arguments: interactive planning mode.
- `<description>`: start planning with the given task.
- `--light`: abbreviated plan without references or trade-off analysis. Produces `plan.md` only.
- `--resume`: continue from the most recent spec folder.
- `--discover`: run a structured discovery session before planning (see Discovery Phase below).
- `--auto`: run discovery, scope review, and engineering review automatically. Surface only decisions that need human input. Skip interactive approval between phases.

### Discovery Phase (when `--discover` or `--auto` is passed)

Before step 1, run a structured discovery session. Ask these six forcing questions, one at a time:

1. **Problem.** What problem does this solve? Who has it today? How do they work around it?
2. **User.** Who is the user? What is their workflow before and after this feature?
3. **Success.** What does success look like? How will you measure it?
4. **Scope.** What is the minimum viable scope? What can be deferred?
5. **Risk.** What are the biggest risks? Technical, product, timeline.
6. **Alternatives.** What existing solutions did you consider? Why are they insufficient?

Record the answers in the spec folder's `decisions.md` under a "Discovery" heading.

**Optional research step.** If the task touches a domain with active community discussion, public competitors, or external prior art, run `/research <topic>` and link the output in the spec folder's `references.md`. The research skill enforces entity resolution, citation discipline, and confidence scoring. This step is user-initiated, not automatic. Skip when the task is purely internal.

### Scope Review (when `--auto` is passed, runs after discovery)

Challenge the scope with four lenses before proceeding to architecture:

| Lens | Question |
|------|----------|
| Expansion | What is missing that users will expect? What adjacent features add outsized value? |
| Selective expansion | Which additions have the best effort-to-impact ratio? |
| Hold | Is the scope right as-is? Does every item justify its cost? |
| Reduction | What can be cut without losing core value? What is nice-to-have masquerading as must-have? |

Present the scope review findings. In `--auto` mode, only pause for user input if the review suggests changes. If the scope is clean across all four lenses, proceed.

### Process

The steps below are enablers, not gates. Their order shows what becomes possible next, not a one-way waterfall. Discovery, scope review, alternatives, and the plan itself are revisitable at any time: if implementation reveals the design was wrong, reopen the relevant artifact and update it rather than forcing the original plan through. The dependencies exist so each step has the context the next one needs, not to lock the work.

0. **Context snapshot.** Before anything else, write `context.md` in the spec folder:

   ```markdown
   # Context Snapshot
   **Created:** <YYYY-MM-DD HH:MM GMT>

   ## Task
   <Task statement from user input, verbatim>

   ## Desired Outcome
   <What success looks like, in one sentence>

   ## Known Facts
   - <Fact from user input or codebase>

   ## Constraints
   - <Time, tech, scope, or resource constraints>

   ## Unknowns
   - <Question that blocks implementation>: owner <named person or session>, needed by <task>

   ## Codebase Touchpoints
   - <Files or modules likely to change>

   ## Branch State
   - Branch: <current branch>
   - Recent commits: <last 3 commit subjects>
   ```

   This snapshot prevents context drift in long sessions. Re-read `context.md` at the start of each phase, steps 1, 5, 8. If the task has evolved, update the snapshot before continuing.

   **When the complaint is about quality rather than a missing feature, diagnose the layer before proposing content.** A report that output is weak in some dimension reads as a request for more guidance, and writing more guidance is usually the wrong fix. Ask when each existing layer fires relative to the moment the work is produced: always-on rules fire before, on-demand standards fire only on a trigger match, review checklists fire after the artifact exists, and mechanical hooks fire at write time. Guidance that only fires after the code is written cannot change the code. Compare the dimension the user is unhappy about against a dimension they are happy about, and the difference in enforcement timing is usually the whole finding. Record the comparison in `plan.md` so the approach section follows from evidence rather than from the topic list.

1. **Clarify scope.** One question at a time. What is being built? Expected outcome? Constraints? Skip if discovery phase already covered this.

2. **Search for existing work**. The tool ordering is mandatory; stop at first match:
   1. Local codebase: `rg -i "<keyword>"`, including file names. Cover [`skills/`](../../skills), [`agents/`](../../agents), [`rules/`](../../rules), [`standards/`](../../standards), [`hooks/`](../../hooks) when the new work could land in `~/.claude/`.
   2. Open PRs: `GH_TOKEN=$(gh auth token --user <account>) gh pr list --search "<keywords>"`.
   3. Recent branches: `git branch -a --list "*<keyword>*"`.
   4. Closed PRs: `GH_TOKEN=$(gh auth token --user <account>) gh pr list --state closed --search "<keywords>"`. A closed PR often names a dead-end or a postponed approach.
   5. GitHub code search: `GH_TOKEN=$(gh auth token --user <account>) gh search code "<keywords>" --language=<lang>`.
   6. Library docs: `llms.txt` first, then official docs of the major library in the area.
   7. Package registry: `pnpm search`, `pip index versions <name>` or the PyPI page, since PyPI disabled `pip search`, `cargo search`, `gem search`.
   8. Web search: last resort, only if 1-7 turned up nothing.

   **Anti-duplication gate for skills, agents, hooks, standards, rules.** Before proposing a new file in `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/hooks/`, `~/.claude/standards/`, or `~/.claude/rules/`, run steps 1-2 against `~/.claude/` and the [`rules/index.yml`](../../rules/index.yml) on-demand entries first. Prefer extending an existing file, new subcommand, new section, new mode, over creating a new one. Justify the new file in writing when no extension fits. See [`rules/pre-flight.md`](../../rules/pre-flight.md) for the full rule.

3. **Gather references.** Identify 2-5 files following patterns the new code should match. Read them. Note structure, naming, error handling, testing.

4. **Match relevant rules.** Read [`rules/index.yml`](../../rules/index.yml). Match top 3-5 rules by triggers. Read them.

5. **Evaluate alternatives.** For non-trivial decisions, 2-3 approaches with trade-offs, risk level, and recommendation. For each:
   - **Decisive test**: smallest experiment to confirm/invalidate.
   - **Stop signal**: what result means the approach is wrong.
   - **Pivot trigger**: when to switch to next-best alternative.
   Present for approval. Suggest `/plan adr new` for significant decisions.

6. **Create spec folder** in the project workspace, per [`rules/project-workspace.md`](../../rules/project-workspace.md). The root is `<repo>/docs/` or `<repo>/.work/`, resolved by [`hooks/_lib/project_workspace.py`](../../hooks/_lib/project_workspace.py); the folder is never committed:
   ```
   <root>/plans/<YYYY-MM-DD>-<slug>/
     plan.md        (goal, approach, requirements, test seams, task breakdown, out of scope, risks, validation)
     decisions.md   (context, options, chosen with reasoning)
     references.md  (patterns, related work, applicable rules)
   ```

   For a non-trivial change, `plan.md` carries a **Requirements** section before the task breakdown. Each requirement is one observable behavior stated with a normative keyword, and each carries at least one Given/When/Then scenario. See [`rules/living-specs.md`](../../rules/living-specs.md) for the format and [`rules/normative-keywords.md`](../../rules/normative-keywords.md) for keyword strength. These requirements are the plan's acceptance criteria: each scenario maps to a row in the test traceability matrix (Gate 1) and feeds the 100% coverage gate. The `test-scenario-generator` agent reads this section when present.

   ```markdown
   ## Requirements

   ### Requirement: <one observable behavior, one MUST/SHALL/SHOULD>
   #### Scenario: <names the case>
   - GIVEN <precondition>
   - WHEN <action>
   - THEN <expected, checkable outcome>
   ```

   **Living-spec delta.** When the change touches behavior already covered by a `specs/current/` spec, `plan.md` also carries a delta section against that spec using `## ADDED Requirements`, `## MODIFIED Requirements`, and `## REMOVED Requirements`. Describe the diff, not the whole spec. If the project has no `specs/current/` yet and the change is non-trivial, seed it with only the requirements this change establishes. Full delta discipline and the triviality boundary: [`rules/living-specs.md`](../../rules/living-specs.md). This is the spec-level analogue of [`rules/surgical-edits.md`](../../rules/surgical-edits.md).

   **Ready check.** Before writing tasks, every requirement answers five questions:

   - Value: who benefits, in one sentence.
   - Acceptance: the observable condition that says it is done.
   - Failure cases: what happens on invalid input and when a dependency fails, each with its own scenario.
   - Access: who may trigger it, with a scenario for a caller who may not.
   - Size: it fits one change; otherwise split it.

   A requirement that cannot answer a question is split, or its question goes to Unknowns with a named owner. Fixing it live inside the breakdown hides the gap. Questions that do not change what gets built go to the owner and stay out of the plan.

   **Test seams.** Agree the seams before writing tasks, and present them with the plan for approval. Prefer an existing seam to a new one, and pick the highest seam that can observe the behavior; the ideal count is one. A seam nobody agreed to surfaces later as a review finding, so settle it here.

   **Task breakdown.** Every task is a vertical slice: a narrow path through every layer the change touches, schema, API, UI, and tests, that is demoable or verifiable alone and fits one fresh session. A task that ships one layer is a horizontal slice and cannot be verified until its siblings land, so rework it. Order and shape:

   - Prefactoring comes first, as its own tasks: make the change easy, then make the easy change.
   - Each task names what can be demoed after it, and a **Blocked by** list of the tasks that must finish before it starts, or `None`. A task whose blockers are all done is on the frontier and can start.
   - Each task carries a **Mode**: `HITL` when it needs a human decision or action, such as an architecture choice, a design review, or a credential, and `AFK` when an agent can finish and verify it alone. Prefer `AFK`; split a mostly autonomous task so its human step becomes its own `HITL` task. An agent queue picks only `AFK` tasks, so it never stalls waiting on a person.
   - Every acceptance criterion names an observation that is false at the base commit. A criterion already true before the work, or one only another task can satisfy, grades nothing.
   - A wide refactor, one mechanical change whose blast radius spans the codebase such as a column rename, is the exception. Sequence it expand, migrate, contract: add the new form beside the old, migrate call sites in batches sized by blast radius, each blocked by the expand, then delete the old form in a task blocked by every batch.

   ```markdown
   ## Test Seams
   - <seam>: <what it observes>, existing or new

   ## Task Breakdown

   ### 1. <task title>
   - **Demo after this:** <the behavior someone can see or run>
   - **Blocked by:** None
   - **Mode:** AFK
   - **Acceptance:**
     - [ ] <criterion>: observe <signal that is false at the base commit>

   ## Out of Scope
   - <what this change deliberately does not do, and why>
   ```

   The **Out of Scope** section is required and lists real exclusions, including the options the user refused. It is the cheapest place to catch a wrong boundary.

   **Polishing checklist**, optional. For user-facing work, `plan.md` may carry a `## Polishing` section: checks run once every task is done, which bring the delivered parts into harmony without extending scope. Typical items are consistent wording across screens, every error state reachable and readable, empty and loading states present, and keyboard paths complete. An item that adds behavior is a requirement, not polish, and moves to Requirements.

7. **Append mandatory closing gates.** Every `plan.md` task breakdown must end with these two items, in this order, as the final tasks. They are not optional. They cannot be moved earlier or removed.

   **Gate 1: Test Coverage, 100%.** Apply [`../../checklists/checklist.md`](../../checklists/checklist.md) category 8, Testing. Every file changed or directly related to the changes must reach 100% coverage across statements, branches, functions, and lines, with no exclusion directive, and every user-facing entry point and requirement scenario must have an end-to-end test. "Related" means: files that import from, are imported by, or share a data contract with a changed file. Run the coverage tool scoped to changed files. If any file is below 100%, test the behavior behind the uncovered lines, or delete or refactor code no test can reach, before proceeding.

   **Gate 2: Clean Room Verification.** Apply [`../../checklists/checklist.md`](../../checklists/checklist.md) category 50, Clean Room. Run all checks from sections A through E against every file produced by this plan. If no external sources were consulted, state that explicitly and skip. Full process and remediation steps: [`standards/clean-room.md`](../../standards/clean-room.md).

8. **Present plan.** Wait for approval.

9. **Hand off.** Confirm spec written. State first step. Suggest `/plan scaffold` if new files needed. Suggest `/plan adr` if architecture decision was made.

### Research Discipline

These rules apply during steps 2-4 and any research, spike, or exploration phase. They prevent context loss during long investigative sessions.

**2-action rule.** After every two search, read, or browse operations, persist key findings to `references.md` in the spec folder before continuing. Do not accumulate findings only in context. Multimodal content like screenshots, PDF contents, or browser output must be captured as text immediately because it does not survive context compaction.

**Read before decide.** Re-read `plan.md` before any major decision. After ~50 tool calls, the original goal drifts out of the attention window. Re-reading pushes it back in. This applies to implementation too: before starting a new phase, re-read the plan.

**Never repeat failures.** If an action failed, the next action must be different. Track every failed attempt with its error in `decisions.md` using this format:

| Attempt | What was tried | Error | Next action |
|---------|---------------|-------|-------------|
| 1 | ... | ... | ... |

Failed approaches are valuable context. Keep them visible so the model updates its beliefs rather than retrying the same path.

### 3-Strike Error Protocol

When an approach fails during planning or research:

1. **Strike 1: Diagnose and fix.** Read the error. Identify root cause. Apply a targeted fix.
2. **Strike 2: Alternative approach.** Same error? Try a different method, tool, or data source. Never repeat the exact same failing action.
3. **Strike 3: Broader rethink.** Question the assumptions behind the approach. Search for solutions. Consider updating the plan's approach entirely.
4. **After 3 strikes: Escalate.** Explain what was tried, share the specific errors, and ask for guidance. Do not continue guessing.

---

## archive

Fold a completed change's spec delta into the living spec, then stamp the plan folder archived. This is the step that keeps `specs/current/` from going stale. It owns the shared merge routine that `/ship` and `/retro` also call, so the result is identical from any entry point, per the delivery-path-consistency rule in [`rules/code-style.md`](../../rules/code-style.md).

### When to use

- After the tasks in a plan folder are implemented, verified, and merged.
- When `/ship` or `/retro` prompts to close out a change that has a `specs/current/` delta.

### Arguments

- No arguments: resolve the most recent plan folder under `<root>/plans/`, or the legacy `specs/`, that has an unmerged delta.
- `<spec-folder>`: explicit path to the plan folder to archive.
- `--dry-run`: print the merge that would happen without writing.

### Steps

1. **Resolve the plan folder** and read its `plan.md` delta sections (`ADDED`, `MODIFIED`, `REMOVED`). If the plan has no delta and no `Requirements` section, there is nothing to merge; only stamp it archived.
2. **Locate the target spec** under `specs/current/<domain>/spec.md` for each requirement. Create the domain spec if the delta is all `ADDED` and no spec exists yet.
3. **Idempotency check.** For each delta requirement, compare against the current spec. If it is already merged (ADDED requirement already present with identical text, MODIFIED already applied, REMOVED already absent), skip it and report a no-op. Re-running a completed archive must change nothing.
4. **Name the target before writing.** For every MODIFIED and REMOVED requirement, state which requirement in the current spec it replaces or deletes, per the destructive-action discipline in [`rules/code-style.md`](../../rules/code-style.md). In `--dry-run`, stop here and print the plan.
5. **Apply the merge.** ADDED appended to the domain spec, MODIFIED replaces the prior requirement in place, REMOVED deleted with the reason recorded in `decisions.md`.
6. **Stamp archived.** Add an `Archived: <YYYY-MM-DD>` line to the plan folder's `plan.md` header. The plan folder stays in place, dated and permanent; only the living spec moves forward.
7. **Report.** Table of merged requirements per domain, plus any skipped no-ops.

### Rules

- Idempotent. Re-running on an already-merged delta is a no-op, never a duplicate append.
- Never rewrite a whole spec. Apply only the delta.
- Never delete the plan folder. It records why; the living spec records what.
- The merge logic lives here. `/ship` and `/retro` invoke it, never reimplement it.

---

## adr

Create and manage Architecture Decision Records. ADRs capture context, alternatives, and reasoning behind significant technical decisions.

### When to use

- After a non-trivial architecture decision.
- When changing or reversing a previous decision.
- During planning when a decision deserves its own record.

### Subcommands

- No arguments: list existing ADRs.
- `new <title>`: create interactively.
- `supersede <number> <title>`: create new ADR that supersedes existing.
- `--status <status>`: filter by proposed/accepted/deprecated/superseded.

### Process

1. Locate the ADR directory the project already tracks, found with `git ls-files | grep -i '/adr/'`. When the project tracks none, ask the user where committed ADRs live. Never create it inside the workspace root resolved per [`rules/project-workspace.md`](../../rules/project-workspace.md): when that root is `<repo>/docs/`, a `docs/adr/` there is excluded from git and the ADR is never committed. A draft the user has not decided to publish goes to `<root>/adr/`. Files: `NNN-<slug>.md`, zero-padded.
2. For new ADRs, ask one question at a time: what decision? What problem? What alternatives?
3. Draft:

```markdown
# ADR-NNN: <Title>

**Status:** accepted
**Date:** <YYYY-MM-DD>

## Context
## Decision
## Alternatives Considered
### <Alt 1> -- pros, cons
### <Alt 2> -- pros, cons
## Consequences
### Positive
### Negative
### Risks
```

1. Show draft, incorporate feedback, write file.
2. For supersession: update original status to `superseded by ADR-NNN`, link from new ADR.
3. When `SECOND_BRAIN_VAULT` resolves to a directory, offer to mirror a pointer note into `wiki/decisions/`.

   The ADR holds the technical content and stays in the repository, which is the only place it can stay true. The vault note holds what the repository has no place for: who pushed for the decision, what the organization was worried about, which constraint was really binding, and which alternative someone will propose again in six months. It carries a `pointer` field naming the ADR and never copies its body.

   Delegate the write to `/brain capture`. A vault note that duplicates the ADR is a second source of truth and will drift; that is the failure this mirror exists to avoid, so keep it to context and a pointer.

### Rules

- ADRs are append-only. Never delete superseded ones.
- The vault mirror is a pointer plus organizational context, never a copy of the ADR body.
- At least two alternatives documented.
- Status values: proposed, accepted, deprecated, superseded by ADR-NNN.
- Title describes the decision, not the problem.

---

## to-issues

Export the active spec folder's task breakdown to GitHub issues. One issue per task.

This subcommand runs only when the user asks for it. It exports planned work the user chose to track, and it is never a way to record a problem instead of fixing it. A defect found while a change is open is fixed in that change, per [`../../rules/found-fix.md`](../../rules/found-fix.md) and [`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md).

### When to use

- After a `/plan` run, when the user has said the work will be tracked in issues.
- When handing off a plan to a teammate or queue.

### Arguments

- No arguments: read the most recent plan folder under `<root>/plans/`, or the legacy `specs/` or `.claude/specs/`.
- `<spec-folder>`: explicit path to the spec folder.
- `--label <name>`: label applied to each issue this flow opens. Repeatable.
- `--milestone <name>`: milestone to assign to every issue.
- `--dry-run`: print the issue payloads without creating them.

### Steps

1. **Resolve spec folder.** Default to the latest folder under `<root>/plans/`, then the legacy `specs/` or `.claude/specs/`.
2. **Read `plan.md`.** Parse the Task Breakdown section. Each numbered task becomes one issue, carrying its demo line, acceptance criteria, **Mode**, and **Blocked by** list.
3. **Detect platform and account.** GitHub or GitLab from `git remote get-url origin`. Map the remote owner to an account per [`standards/multi-account-cli.md`](../../standards/multi-account-cli.md) and prefix every `gh` call with `GH_TOKEN=$(gh auth token --user <account>)`. Never switch the global active account.
4. **Idempotency check.** For each task, search existing open and closed issues for the exact title. Skip if a match exists, and reuse its number for blocking edges.
5. **Build issue body.** Include: the behavior the task delivers in the project's domain language, the demo line, the acceptance criteria, and the `HITL` or `AFK` mode. Describe behavior, never code locations: no file paths, line numbers, or function names, which go stale before the issue is picked up. Never name the plan, the workspace, or a planning path, since none of them exist in a clone.
6. **Create issues in dependency order**, blockers first, so every blocking edge can name a real issue number at creation time. GitHub: `GH_TOKEN=$(gh auth token --user <account>) gh issue create --title "<title>" --body-file <tmp> --label <label> --blocked-by <n,n> --parent <n>`. `--blocked-by` sets native blocking links and `--parent` makes the issue a sub-issue when the plan came from an existing issue; both exist in `gh` 2.102.0, and `GH_TOKEN=$(gh auth token --user <account>) gh issue edit <n> --add-blocked-by <n>` repairs an edge after creation. Confirm both with `gh issue create --help`; when the installed `gh` lacks either flag, write `Blocked by #N` lines in the body instead and say so in the summary. GitLab: equivalent `glab issue create`, with `Blocked by #N` in the body.
7. **Print summary.** Table of the new issues with URLs and their blocking edges. Skipped, duplicate issues listed separately.

### Rules

- Idempotent. Re-running must not create duplicates.
- The title states the behavior the task delivers. It carries no task or phase number, which would number a workflow stage in published text.
- Order and dependencies live in the native blocking links, so the issue reads correctly with no access to the plan.
- Never create issues from a `--light` plan with no task breakdown.
- Never invoke this subcommand on your own initiative, and never to record a finding from a review, a CI run, or a verification gate.
- Never push or commit. This subcommand only writes to the issue tracker.

---

## scaffold

Generate boilerplate by reading existing project patterns. No external generators, everything derived from the codebase.

### When to use

- Creating a new endpoint, service, component, module, or model.
- When new code must match existing style.

### Arguments

`<type> <name>` where type is a project pattern: `endpoint`, `service`, `component`, `module`, `model`, `controller`, `middleware`, `hook`.

### Steps

1. Parse type and name. If missing, list available types and ask.
2. **Detect framework and find examples**, parallel: read manifest, map directory structure, search for existing examples of the type.
3. Analyze 2-3 examples: naming convention, export style, imports, code structure, test file location, TypeScript patterns.
4. Generate: main file + test file following exact patterns. Business logic the user has not specified stays out of the skeleton: the function signature, types, and a failing test name the missing behavior, with no `TODO` comment.
5. Present for approval before writing.
6. Write files. Import each new export from its own module path; never create or extend a barrel file.

### Rules

- Always read existing code to derive patterns.
- Always present for approval before writing.
- Match exact naming, export style, imports.
- Never generate without at least one example.
- Never install dependencies.
- Keep generated code minimal: a skeleton with no comments, no `TODO` markers, and no barrel exports, per [`rules/code-style.md`](../../rules/code-style.md).

---

## multi-execute

Plan and execute a feature with parallel model tiers, Opus + Sonnet + Haiku, while keeping the running Claude Code session as the **sole filesystem writer**. Subagents propose; the orchestrator integrates and writes.

### When to use

- Feature is large enough to benefit from a planner-reviewer split.
- Cost matters: route deep reasoning to Opus, broad searches to Sonnet, mechanical tasks to Haiku.
- The risk of two writers conflicting on the same files is non-trivial.

### When NOT to use

- Small change, 1-3 files. Overhead exceeds value.
- Time-critical hotfix. Use `/hotfix`.
- The task is purely deterministic, rename, format, refactor. Use `/refactor`.

### Single-Writer Invariant (NON-NEGOTIABLE)

Only the running Claude Code session writes to disk. Subagents return text. The orchestrator parses, validates, and applies.

| Role | Tools | Writes? |
|------|-------|---------|
| Orchestrator (this session) | All tools | YES |
| Planner subagent | Read, Grep, Glob, WebSearch | NO |
| Generator subagents | Read, Grep, Glob | NO |
| Reviewer subagents | Read, Grep, Glob | NO |

Subagents must be briefed with: "Return your proposed changes as unified diffs or full-file content in your response. Do NOT call Edit, Write, or MultiEdit." Violations are a wasted run.

### Process

1. **Plan with Opus.** Spawn a planner subagent, Opus tier to produce the task breakdown. Single agent, single pass.
2. **Decompose.** Keep the plan's vertical slices: each chunk is one slice, or the part of one slice that owns its files outright, and a chunk starts only when its **Blocked by** tasks are integrated. Never split work into one chunk per layer, since a layer chunk cannot be verified alone.
3. **Generate in parallel.** Spawn generator subagents, Sonnet tier at most two at a time per the Parallelism Rule. Each receives one chunk plus the file content. Returns proposed text.
4. **Review in parallel.** Spawn reviewer subagents, Sonnet tier on the proposed changes. Returns approval or rejection with rationale.
5. **Integrate.** The orchestrator applies the approved changes with Edit / Write / MultiEdit. Conflicts between proposals get re-planned, back to step 2 for the conflicting subset.
6. **Verify.** Run formatter + linter + test suite. Show output.

### Cost discipline

- Planner: Opus, 1 call.
- Generator: Sonnet, N calls where N is the number of independent chunks. Cap at 6.
- Reviewer: Sonnet, N calls matching the generators.
- Orchestrator integration: this session.

Estimate cost before running. Abort and run a simpler `/plan` flow when the cost exceeds the marginal benefit of parallelism.

### Rules

- Single-writer invariant is enforced by the briefing, not by the runtime. Audit subagent responses: if any names a write tool, discard the response.
- Generator chunks must not overlap on the same file. The decomposition step is responsible for partitioning.
- Reviewer subagents read the proposal, not the diff. Diffs hide context.
- Failed verification rolls back the orchestrator's writes, `git stash` before re-planning.

---

## Rules

- Planning is investigation, not implementation. Do not write production code during `/plan`.
- Every decision must document at least two alternatives.
- Plan folders are permanent and dated. They record WHY decisions were made. The living spec under `specs/current/` records WHAT the system does now and is maintained by `/plan archive`. See [`rules/living-specs.md`](../../rules/living-specs.md).
- The plan must reference verified file paths.
- Search for existing work before designing new solutions.
- Plan folders go in the project workspace at `<root>/plans/`, never committed, and never in `~/.claude/` unless `~/.claude` is the project. Existing folders under `specs/` or `.claude/specs/` stay readable. The living spec under `specs/current/` is project documentation and stays where the project keeps it.

## Common Rationalizations

- "The design is obvious, so the existing-work search is ceremony": step 2 runs in order and stops at the first match. A closed PR or a sibling skill often already holds the answer.
- "A little code proves the approach faster than a plan": planning writes no production code. A design question that needs running code goes to `/spike`.
- "Splitting tasks by layer is cleaner": a task that ships one layer cannot be verified until its siblings land. Rework it into a vertical slice.
- "The coverage and clean-room gates are overkill for a small plan": both gates close every `plan.md` task breakdown, in order, as the final tasks.
- "Only one approach is realistic": every decision documents at least two alternatives, each with a decisive test and a stop signal.
- "Nothing is excluded, so Out of Scope stays empty": the section lists real exclusions, including every option the user refused.

## Red Flags

- Stop and re-read `context.md` and `plan.md` when a new phase starts or about 50 tool calls have passed since the last read.
- Stop and write to `references.md` when two searches, reads, or browses have run since the last write.
- Stop and escalate with the attempt table when the third strike fails.
- Stop and reshape the task when it ships a single layer or carries an acceptance criterion already true at the base commit.
- Stop and present the plan for approval when implementation is about to start without one.

## Verification

- The plan folder exists at `<root>/plans/<YYYY-MM-DD>-<slug>/` with `context.md`, `plan.md`, `decisions.md`, and `references.md`, and git does not track it.
- A non-trivial `plan.md` carries Requirements with Given/When/Then scenarios, Test Seams, a Task Breakdown whose tasks name a demo, a Blocked by list, a `HITL` or `AFK` mode, and acceptance criteria, an Out of Scope section, and the two closing gates as the last tasks.
- Every file path the plan names exists on disk or is marked as a new file.
- `decisions.md` records at least two alternatives for every decision.
- The user approved the plan before the hand-off step.
- For `adr`, `archive`, `to-issues`, and `scaffold`, the section's own Rules hold, and a re-run of `archive` or `to-issues` changes nothing.

## Related skills

- `/design` -- Design consultation before planning UI features.
- `/review` -- Review code quality after implementing the plan.
- `/ship` -- Ship the implementation.
- `/deploy` -- Merge and deploy after shipping.
- `/assessment` -- Audit completeness after plan execution.
