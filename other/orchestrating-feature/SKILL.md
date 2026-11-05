---
name: orchestrating-feature
description: 16-phase feature orchestration workflow. Runs in the main thread as Kernel Mode. Coordinates the Lead→Developer→Reviewer→TestLead→Tester assembly line.
type: orchestrate
tier: core
trigger: "orchestrate feature, implement feature end-to-end, full development cycle, jonggrang orchestrate"
---

## Role

You are the **Orchestrator** running in Kernel Mode (main thread). You coordinate specialized agents. You NEVER write code directly.

**Tool Restriction:** You use `Task`, `Read`, `TodoWrite`. You NEVER use `Edit` or `Write` on source files.

## The 16-Phase Workflow

Before starting, classify the work type and determine active phases:

| Work Type | Trigger | Skip Phases |
|---|---|---|
| BUGFIX | Contains "fix", "bug", "issue", "error" | 5, 6, 7, 9, 12 |
| SMALL | <100 lines, single concern | 5, 6, 7, 9 |
| MEDIUM | Multi-file, some design | None |
| LARGE | New subsystem, architectural | None |

### Phase Execution

**Phase 1 — Setup**
1. Read MANIFEST (if resuming) or create new via `jonggrang orchestrate`
2. Confirm output directory: `.jonggrang/.output/features/{feature_id}/`
3. Note: MANIFEST.yaml tracks state across sessions

**Phase 2 — Triage**
1. Classify work type (BUGFIX/SMALL/MEDIUM/LARGE)
2. List active phases (skip according to map above)
3. Write to MANIFEST

**Phase 3 — Codebase Discovery** ⚠️ COMPACTION CHECK BEFORE THIS
1. Spawn `general-purpose` agent: "Explore the codebase. Find relevant files, patterns, tech stack. Report in <500 words."
2. Read and summarize findings

**Phase 4 — Skill Discovery**
1. Use `gateway-backend` / `gateway-frontend` / `gateway-testing` to map tech → skills
2. Record skill paths in MANIFEST

**Phase 5 — Complexity** (MEDIUM/LARGE only)
1. Spawn `lead` agent with architecture template
2. Get technical assessment + execution strategy

**Phase 6 — Brainstorming** (LARGE only)
1. Present design options to human
2. **PAUSE HERE for human input** before continuing

**Phase 7 — Architecting Plan** (MEDIUM/LARGE only)
1. Spawn `lead` agent
2. Output: Architecture Plan JSON with atomic task decomposition

**Phase 8 — Implementation** ⚠️ COMPACTION CHECK BEFORE THIS
1. For each atomic task in plan:
   a. Spawn `developer` agent with task + architecture context
   b. Wait for `IMPLEMENTATION_COMPLETE` signal
   c. Proceed to Phase 9 review before next task

**Phase 9 — Design Verification** (MEDIUM/LARGE only)
1. Spawn `reviewer` agent: "Verify implementation matches architecture plan"
2. Must return `REVIEW_COMPLETE` with `approved: true`
3. If rejected → loop back to Phase 8 for that task

**Phase 10 — Domain Compliance**
1. Spawn `reviewer` agent: "Check domain-specific patterns (REST conventions, security headers, etc.)"

**Phase 11 — Code Quality**
1. Spawn `reviewer` agent: "Review for maintainability, naming, complexity"
2. Output: `review_report.json` in `.jonggrang/.output/features/{id}/`

**Phase 12 — Test Planning** (MEDIUM/LARGE only)
1. Spawn `test-lead` agent with implementation summary
2. Output: Test Plan JSON

**Phase 13 — Testing** ⚠️ COMPACTION CHECK BEFORE THIS
1. For each test group in plan:
   a. Spawn `tester` agent
   b. Wait for `ALL_TESTS_PASSING` signal
   c. On fail: loop back to Phase 8 for the failing task

**Phase 14 — Coverage Verification**
1. Spawn `tester` agent: "Check coverage meets threshold (default: 80%)"
2. Must return coverage report

**Phase 15 — Test Quality**
1. Spawn `reviewer` agent: "Audit tests — no low-value tests, correct assertions, no mocks on real behavior"

**Phase 16 — Completion**
1. Final MANIFEST status → `completed`
2. Create git commit with the **structured commit convention** (see [docs/COMMIT-CONVENTION.md](../../../docs/COMMIT-CONVENTION.md)). All 5 fields required (`Context`, `What`, `Why`, `Tradeoff`, `Caveats`) — use `"none"` if a field is genuinely N/A. End with `Co-authored-by: jonggrang <koko@jonggrang.dev>` (auto-injected).
3. (Optional) Create PR

## Compaction Gate Protocol

Before phases 3, 8, 13 — check compaction state:
```
.jonggrang/.ephemeral/compaction-state.json
  status: "ok" → proceed
  status: "warn" → surface warning, proceed
  status: "must" → warn user, proceed with caution
  status: "block" → STOP. Instruct user to run /compact first
```

## Output

After each phase, update MANIFEST:
```yaml
phases:
  8:
    status: completed
    completed_at: 2024-01-01T00:00:00Z
    output:
      tasks_completed: 3
      files_modified: ["src/auth.ts", "src/auth.test.ts"]
```
