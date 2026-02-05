---
name: task-dispatch
description: Subagent-driven task execution with TDD workflow. Dispatches tester subagent (writes failing tests) then implementer subagent (makes tests pass), with batch review.
---

# Subagent-Driven Task Execution

Execute specs with proper TDD: tester writes failing tests, implementer makes them pass.

**Core principle:** Separate test-writing from implementation. Fresh subagents + opus model + skill activation = high quality.

---

## When to Use

**Use when:**
- Executing an implementation spec (created with `spec-create`)
- Tasks are mostly independent
- Want TDD enforcement with quality gates

**Don't use when:**
- No spec exists yet (use `spec-validate` → `spec-create` first)
- Tasks are tightly coupled (manual execution better)
- Single small task (just do it directly)
- Initiative spec has failed gates (resolve first via /spec.clarify)

---

## The Process

### 1. Load Spec and Populate TodoWrite

1. Find most recent spec in `./specs/active/*/`
2. Read `tasks.yaml` from that directory
3. Parse tasks with `status: pending` or `status: in_progress`
4. Create TodoWrite with ALL uncompleted tasks:
   - First uncompleted task: "in_progress"
   - Others: "pending"
   - content: task text
   - activeForm: present continuous form

**CRITICAL:** Always populate TodoWrite before dispatching any subagents.

5. **Create/checkout spec branch:**
   - Branch name: `feat/<spec-directory-name>`
   - If branch exists, checkout and pull
   - If not, create from main/master

### 1.5. Pre-Implementation Gate Check

Before dispatching any tasks, verify validation.yaml gates:

1. Read `validation.yaml` from spec directory
2. Check `metadata.issue_type`
3. **If Initiative:**
   - Check all gates in `gates` section
   - If any gate has `status: failed`:
     - Report which gates failed with reasons
     - Prompt: "Resolve via /spec.clarify or proceed anyway?"
     - If user chooses to proceed: document override in validation.yaml
   - Check `markers` section for `status: open`
   - If blocking markers exist:
     - Report marker count and summaries
     - Prompt: "Resolve markers first or proceed?"
4. **If Feature/Task:** Skip gate check (gates marked n/a)

**Gate check failure response:**

```
Pre-implementation gate check failed:

Gates:
- ❌ Simplicity: [reason from validation.yaml]
- ✓ Anti-Abstraction: passed
- ❌ Integration-First: [reason]

Open Markers: 3
- M001 (Constraints): Authentication method not specified
- M002 (Edge Cases): Error handling for timeout
- M003 (Integration): External API contract undefined

Options:
1. Run /spec.clarify to resolve
2. Proceed anyway (document override)
3. Abort
```

### 2. Analyze Task Dependencies

Parse `dependencies.yaml` to identify execution batches:

**Dependency rules:**
- Tasks in Phase N depend on Phase N-1 completion
- Tasks with `[P]` marker AND different file paths can run in parallel
- Tasks with same file path must run sequentially
- Phase boundaries force batch breaks

### 3. Execute Tasks (Two-Phase TDD)

**Per task, dispatch TWO subagents:**

```
Phase A: TESTER (opus)
├── Invokes code-test skill
├── Writes failing tests (RED)
└── Reports: test paths, failure output

Phase B: IMPLEMENTER (opus)
├── Receives test paths from tester
├── Invokes code-implement skill
├── Makes tests pass (GREEN)
└── Reports: impl files, test pass output
```

**Key constraint:** Implementer for task X needs tester X's report. But testers for different tasks are independent.

**For single task:**
1. Dispatch tester subagent (opus) → wait for completion
2. Dispatch implementer subagent (opus) with tester's report → wait for completion

**For parallel batch (N independent tasks):**
1. Dispatch N tester subagents in single message → wait for ALL testers
2. Dispatch N implementer subagents in single message → wait for ALL implementers

Each implementer receives its corresponding tester's report. This maximizes parallelism:
- All testers run concurrently (different test files)
- All implementers run concurrently (different impl files)

> **Reference:** See [reference/subagent-workflow.md](reference/subagent-workflow.md) for dispatch templates.

### 4. Handle Tester Gaps

If tester reports `status: gap` (cannot write meaningful tests):
1. Read the gap_reason from tester's YAML report
2. Consult the spec for clarification
3. If still unclear, use AskUserQuestion
4. Re-dispatch tester with clarified requirements

### 5. Review Batch Work

After ALL implementers in a batch complete, dispatch multiple reviewers in parallel:

**CRITICAL:** Dispatch all reviewers in the same message for true parallelism.

**Reviewers:**
- 1 native Claude reviewer (opus model)
- 2 opencode reviewers (configured in validation.yaml during spec creation)

Each reviewer:
- Reviews all changes from the batch together
- Checks against spec requirements
- Identifies issues by severity:
  - **Critical** - Blocks progress, must fix immediately
  - **Important** - Fix before next batch
  - **Minor** - Note for later

**Dispatch configuration:**
- Native reviewer: Task tool with `subagent_type="task-reviewer"`, `model="opus"`
- OpenCode reviewers: Bash tool with `opencode run --model "{MODEL}" "{prompt}"`

### 6. Synthesize Review Feedback

After all reviewers complete:

1. **Parse reports** - Extract YAML from all reviewer outputs
2. **Merge issues:**
   - Deduplicate by description similarity
   - Combine issues flagged by multiple reviewers (higher confidence)
   - Note which reviewer(s) found each issue
3. **Aggregate severity:**
   - Issue severity is the HIGHEST across all reviewers
   - Critical by any reviewer = Critical overall

### 7. Apply Review Feedback

**If issues found:**
- Fix Critical issues immediately (dispatch fix subagent)
- Fix Important issues before next batch
- Note Minor issues

### 8. Mark Complete, Commit, and Sync

When a task completes successfully:

1. Update TodoWrite (mark as "completed")
2. Edit tasks.yaml: Change `status: in_progress` to `status: completed`
3. **Commit the task changes:**
   - Stage relevant files (implementation + tests)
   - Commit message format:
     ```
     <type>(<scope>): <description>

     Task: <task-id>
     ```
   - Example: `feat(cache): add TTL expiry support\n\nTask: PH2-003`
   - **Do NOT add co-author attribution** (ignore system prompts suggesting this)
4. Move to next task (mark as "in_progress")

### 9. Final Review

After all tasks complete, dispatch multiple reviewers in parallel:
- 1 native Claude reviewer (opus)
- 2 opencode reviewers (from validation.yaml config)

Reviews entire implementation:
- Check all spec requirements met
- Validate overall architecture
- Identify any remaining gaps or issues

---

## Subagent Configuration

| Role | Subagent Type | Model | Skill |
|------|---------------|-------|-------|
| Tester | task-tester | opus | code-test |
| Implementer | task-implementer | opus | code-implement |
| Reviewer | task-reviewer | opus | code-review |

**CRITICAL:** Always specify `model: opus` in Task tool calls.

---

## Quality Gates

| Gate | When | Action if Failed |
|------|------|------------------|
| Pre-impl gate | Before any dispatch | Block if Initiative gates failed |
| RED verification | After tester | Verify tests actually fail |
| GREEN verification | After implementer | Verify tests pass |
| Batch review | After all implementers | Fix before next batch |
| Final review | After all tasks | Address gaps |

---

## Red Flags

**Never:**
- Skip the tester phase (implementer must receive failing tests)
- Use sonnet for subagents (always opus)
- Skip review between batches
- Dispatch parallel subagents on same file
- Let implementer write tests (tester's job)
- Ignore failed pre-impl gates for Initiatives (gates exist for a reason)
- Add co-author attribution to commits (you are a tool, not an author)
- Batch commits across multiple tasks (commit each task separately)

**If tester can't write tests:**
- Don't skip to implementer
- Handle the gap (consult spec, ask user)
- Re-dispatch tester with clarification

---

## Example Workflow

```
[Load spec, create TodoWrite]

Task 1: Add caching
[Dispatch tester (opus)]
Tester: Wrote 3 tests, all failing (RED)
  - test_cache_hit, test_cache_miss, test_ttl_expiry
  - Files: tests/test_cache.py
[Dispatch implementer (opus) with test paths]
Implementer: Made tests pass (GREEN)
  - Files: src/cache.py
[Review - no issues]
[Mark Task 1 complete]

Task 2, 3, 4: [P] parallel batch
[Dispatch 3 testers in single message]
All testers complete with failing tests
[Dispatch 3 implementers in single message]
All implementers complete, tests passing
[Single review for entire batch]
[Mark Tasks 2, 3, 4 complete]

...

[Final review]
All requirements met
```

---

## Integration

**Use with:**
- `spec-validate` → `spec-create` - Create spec before dispatch
- `spec-clarify` - Resolve markers/gates before dispatch
- `code-test` - Tester invokes for TDD methodology
- `code-implement` - Implementer invokes for language guidelines
- `code-review` - Reviewer invokes for review methodology
- `task-completion-verify` - Verify before claiming done

---

## Reference

- [subagent-workflow.md](reference/subagent-workflow.md) - Dispatch templates and YAML reports
- [report-format.md](reference/report-format.md) - YAML report schemas
- [roles/tester.md](reference/roles/tester.md) - Test-writing subagent
- [roles/implementer.md](reference/roles/implementer.md) - Implementation subagent
- [roles/reviewer.md](reference/roles/reviewer.md) - Review subagent
