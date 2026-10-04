---
name: ralph-orchestrator
description: Orchestrates the full Ralph autonomous agent pipeline from requirements gathering to execution. Use when building new features, platforms, or complex tasks that need structured development through spec-interview, PRD generation, and autonomous implementation.
model: claude-opus-4-5
---

<objective>
Orchestrate the complete Ralph pipeline for autonomous feature development:

1. **spec-interview** → Gather comprehensive requirements through guided discovery
2. **generate-prd** → Create actionable Product Requirements Document
3. **ralph-convert-prd** → Transform PRD into atomic user stories (prd.json)
4. **Subagent execution** → Spawn ralph-coder/ralph-tester subagents via Task tool

This skill coordinates these tools while keeping you in control at decision points.
</objective>

<essential_principles>

<principle name="CRITICAL_never_implement_directly">
**NEVER implement user stories yourself.** The orchestrator's ONLY job is to:
1. Run spec-interview, generate-prd, ralph-convert-prd skills
2. Spawn ralph-coder and ralph-tester subagents via the Task tool to execute stories
3. Manage prd.json state, git operations (commit/merge), and progress tracking

**ALL code implementation MUST happen through subagents** — ralph-coder implements production code, ralph-tester writes tests and verifies. You are the orchestrator, NOT the implementer. Do not write code, create files, modify source files, or make any project changes directly.

If you catch yourself about to write code or modify project files: **STOP. Spawn a subagent instead.**
</principle>

<principle name="CRITICAL_stop_on_errors">
**STOP and ask the user for instructions** whenever:
- A subagent returns a failed result
- A pre-execution check fails (invalid prd.json, missing files, dirty git state)
- A merge conflict occurs during worktree merge
- Any unexpected error occurs during the pipeline
- You are unsure about any decision

**Do NOT** try to fix issues yourself, retry automatically, or continue past errors. Present the error clearly to the user and wait for their instructions.
</principle>

<principle name="parallel_batch_execution">
Stories with no dependencies between them run in parallel. The orchestrator:
1. Groups independent stories into batches
2. Spawns multiple ralph-coder subagents simultaneously (each in its own worktree)
3. After coders complete, spawns ralph-tester subagents in parallel (in the same worktrees)
4. Merges successful worktree branches to main sequentially
5. Updates prd.json and moves to the next batch

This maximizes throughput while maintaining correct dependency ordering.
</principle>

<principle name="two_phase_pipeline">
Each story goes through a two-phase pipeline:
- **Phase 1: Code** — ralph-coder (or matched project agent) implements production code + docs
- **Phase 2: Test** — ralph-tester (or matched project agent) writes tests + runs verification

Separation gives each agent a focused context window. The orchestrator wraps ANY agent with Ralph context (story spec, return format, constraints) so even non-Ralph agents integrate seamlessly.
</principle>

<principle name="orchestrator_owns_state">
**The orchestrator owns all state:**
- **prd.json** — only the orchestrator reads/writes story status. Agents return JSON results, orchestrator updates prd.json. This prevents race conditions during parallel execution.
- **Git operations** — only the orchestrator commits and merges. Neither coder nor tester commits. Orchestrator commits only after tester confirms all verification passes.
- **Worktree lifecycle** — orchestrator creates worktrees (via Task isolation), merges branches, and manages cleanup.
</principle>

<principle name="agent_discovery">
The orchestrator **prefers existing project/user agents** over defaults. At startup:
1. Scan `.claude/agents/*.md` and `~/.claude/agents/*.md`
2. Match agents to storyTypes by description keywords
3. Fall back to ralph-coder/ralph-tester when no better match exists

This lets users configure best-practice agents for their stack, and Ralph automatically uses them.
</principle>

<principle name="shared_knowledge">
Both coder and tester agents update `tasks/common_knowledge.md` with patterns, conventions, gotchas, and architectural decisions they discover. The orchestrator reads this file between batches to:
- Pass accumulated knowledge to subsequent subagent prompts
- Detect actionable discoveries (e.g., manual steps needed, environment issues)
- Make informed routing decisions for upcoming stories

Both agents also update the `docs/` folder with documentation about new features, APIs, test setup, and architecture changes. The `tasks/test-log.md` and `tasks/review-notes.md` files are updated by tester agents with test registries and improvement recommendations.
</principle>

<principle name="fresh_context_per_story">
Each subagent runs with a fresh context for each story. Memory persists only through:
- Git history (committed code in worktrees)
- tasks/progress.txt (learnings between iterations)
- tasks/prd.json (story status tracking)
- tasks/common_knowledge.md (shared patterns and conventions across stories)
- tasks/test-log.md (test registry across stories)
- tasks/review-notes.md (improvement recommendations across stories)

**Never assume agents "remember" previous stories — but they CAN read shared knowledge files.**
</principle>

<principle name="atomic_stories">
Each user story MUST be completable in ONE context window.

**Right-sized:**
- Add a database column
- Create a UI component
- Update a server action
- Implement a filter

**Too large (will fail):**
- Build entire dashboard
- Add authentication system
- Refactor entire API
</principle>

<principle name="real_verification">
Every story must be verified with **real runtime checks** — not just that it compiles.

- **API stories**: curl endpoints with real data, check response codes and bodies
- **UI stories**: Playwright e2e tests that navigate and interact with real UI
- **Database stories**: Run migrations, query DB directly to confirm schema
- **Infra stories**: Health checks, config validation, service startup

Static checks (typecheck, lint) are baseline. Runtime validation is required.
</principle>

<principle name="quality_gates">
All checks must pass before the orchestrator commits:
- Story-specific verification commands pass (real runtime checks)
- **Full test suite passes** (unit + integration + e2e) — no regressions allowed
- TypeCheck passes
- UI verified via Playwright (for frontend stories)

After each story, the tester runs ALL existing tests (via `testCommands` in prd.json root) to catch regressions. A story is NOT done until the entire test suite passes.
</principle>

<principle name="status_tracking">
Stories use structured status tracking:
- `"pending"` → not started
- `"in_progress"` → being worked on by subagents
- `"done"` → verified, committed, and merged to main
- `"failed"` → attempted but verification failed
- `"blocked"` → dependencies not met

Stories track `attempts` / `maxAttempts` to prevent infinite retries on broken stories.
</principle>

<principle name="user_control_points">
You approve at each stage:
1. After spec-interview → Review SPEC.md
2. After generate-prd → Review PRD
3. After ralph-convert-prd → Review prd.json stories
4. Before execution → Confirm ready to execute
5. Between batches → View progress (if issues arise)

Don't rush. Bad requirements = wasted iterations.
</principle>

</essential_principles>

<prd_json_schema>
```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description]",
  "testCommands": {
    "unit": "npm test",
    "integration": "npm run test:integration",
    "e2e": "npx playwright test",
    "typecheck": "npm run typecheck"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "storyType": "backend | frontend | database | api | infra | test",
      "acceptanceCriteria": ["Specific criterion 1", "Typecheck passes"],
      "verificationCommands": [
        { "command": "npm run typecheck", "expect": "exit_code:0" },
        { "command": "curl -s http://localhost:3000/api/...", "expect": "contains:expected" }
      ],
      "status": "pending",
      "priority": 1,
      "attempts": 0,
      "maxAttempts": 3,
      "notes": "",
      "blockedBy": [],
      "docsToUpdate": ["README.md", "docs/api.md"],
      "completedAt": null,
      "lastAttemptLog": ""
    }
  ]
}
```

**Expect matchers for verificationCommands:**
- `exit_code:0` — command exits with code 0
- `exit_code:N` — command exits with specific code N
- `contains:STRING` — stdout contains STRING
- `not_empty` — stdout is non-empty
- `matches:REGEX` — stdout matches regex pattern
</prd_json_schema>

<intake>
What would you like to do?

1. **Full pipeline** - Start from scratch (spec → PRD → prd.json → execute)
2. **Continue from PRD** - Already have PRD, convert and execute
3. **Execute only** - Already have prd.json, run Ralph
4. **Check status** - View current prd.json progress

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "full", "start", "new feature" | `workflows/full-pipeline.md` |
| 2, "continue", "have PRD", "convert" | `workflows/from-prd.md` |
| 3, "execute", "run ralph", "have prd.json" | `workflows/execute-only.md` |
| 4, "status", "check", "progress" | `workflows/check-status.md` |

**After reading the workflow, follow it exactly.**
</routing>

<quick_reference>

**Key Files:**
| File | Purpose |
|------|---------|
| SPEC.md | Comprehensive requirements from spec-interview |
| tasks/prd-*.md | Product Requirements Document |
| tasks/prd.json | Atomic user stories for Ralph |
| tasks/progress.txt | Learnings between iterations |
| tasks/test-log.md | Registry of all tests created per story (updated by tester agents) |
| tasks/review-notes.md | Improvement recommendations after each story (updated by tester agents) |
| tasks/common_knowledge.md | Shared knowledge base — patterns, conventions, gotchas discovered across stories (updated by both coder and tester agents, read by orchestrator between batches) |
| docs/ | Project documentation — updated by both coder and tester agents with new features, APIs, test setup, etc. |

**Agents:**
| Agent | Role | Fallback |
|-------|------|----------|
| ralph-coder | Implements production code + docs for one story | Default coder when no project-specific agent matches |
| ralph-tester | Writes tests + runs verification for one story | Default tester when no project-specific agent matches |
| Project agents | Discovered from .claude/agents/ and ~/.claude/agents/ | Matched to storyTypes by description keywords |

**Execution model:**
```
BATCH 1 (independent stories):
  Phase 1: Task(coder, US-001, worktree) + Task(coder, US-005, worktree)  ← parallel
  Phase 2: Task(tester, US-001) + Task(tester, US-005)                    ← parallel
  Merge: US-001 → main, US-005 → main                                    ← sequential

BATCH 2 (stories that depended on BATCH 1):
  Phase 1: Task(coder, US-002, worktree) + Task(coder, US-003, worktree)
  Phase 2: Task(tester, US-002) + Task(tester, US-003)
  Merge: US-002 → main, US-003 → main
```

**Commands:**
```bash
# Check story status
cat tasks/prd.json | jq '.userStories[] | {id, title, status, attempts}'

# View learnings
cat tasks/progress.txt

# View test registry
cat tasks/test-log.md

# View review notes
cat tasks/review-notes.md
```

</quick_reference>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| full-pipeline.md | Complete flow: spec → PRD → prd.json → execute |
| from-prd.md | Convert existing PRD and execute |
| execute-only.md | Run Ralph on existing prd.json |
| check-status.md | View current progress |
</workflows_index>

<success_criteria>
Pipeline is complete when:
- [ ] Requirements gathered through spec-interview (including verification environment)
- [ ] PRD created with verifiable acceptance criteria
- [ ] prd.json has atomic stories with storyType, verificationCommands, and blockedBy
- [ ] All stories have `status: "done"` in prd.json
- [ ] All verification commands passed (real runtime checks, not just typecheck)
- [ ] Code committed and merged to main via worktree branches
</success_criteria>
