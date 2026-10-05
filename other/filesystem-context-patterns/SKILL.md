---
name: filesystem-context-patterns
description: Use the filesystem as a first-class context management tool for AI agent sessions. Covers scratch pads, plan persistence, sub-agent communication, dynamic.
---

# Filesystem Context Patterns

Specialized expertise in using the filesystem to extend, persist, and share agent context beyond the conversation window. The filesystem is the most reliable mechanism for managing state across long sessions, between agents, and across session boundaries.

## When to Use This Skill

Use this skill for:

- Tool outputs exceeding ~2,000 tokens (write to file instead of keeping in context)
- Tasks spanning multiple turns or sessions
- Multi-agent coordination requiring shared state
- Loading skills or configuration on demand
- Persisting plans, decisions, or analysis results
- Agent self-improvement through instruction updates

**Trigger phrases**: "write to file", "save context", "share between agents", "persist state", "scratch pad", "session file", "agent communication", "dynamic loading", "filesystem patterns"

## What This Skill Does

Provides filesystem-based context management including:

- **Scratch Pad**: Writing intermediate results to files to free context space
- **Plan Persistence**: Storing plans that survive context resets
- **Sub-Agent Communication**: File-based message passing between agents
- **Dynamic Skill Loading**: Loading relevant skills on demand
- **Terminal Persistence**: Capturing terminal output for later reference
- **Self-Modification**: Agents updating their own instructions based on learnings

## Instructions

### Step 1: Select the Appropriate Pattern

**Pattern Selection Guide**:

| Situation | Pattern | Example |
|-----------|---------|---------|
| Large tool output that has been consumed | **Scratch Pad** | Write codebase analysis to file, reference path |
| Plan or design that must survive context resets | **Plan Persistence** | Store implementation plan in `tasks/plan.md` |
| Multiple agents need to share findings | **Sub-Agent Communication** | Agent A writes results to shared workspace |
| Too many skills loaded at session start | **Dynamic Skill Loading** | Load compliance skills only when audit is needed |
| Need to reference terminal output later | **Terminal Persistence** | Pipe build output to `tasks/build-log.txt` |
| Agent discovers a pattern to remember | **Self-Modification** | Update AGENTS.md or memory files |

### Step 2: Scratch Pad Pattern

**Purpose**: Offload large intermediate results from context to filesystem, keeping only a compact reference in the conversation.

**When to use**: After generating or reading content larger than ~2,000 tokens that has been analyzed but may be needed for reference later.

**Implementation**:

```markdown
## Scratch Pad Workflow

1. Agent generates or reads large content
2. Agent writes content to a scratch file:
   - Path: `tasks/scratch/[descriptive-name].md`
   - Include a header with purpose and timestamp
3. Agent states a compact summary in conversation
4. Later: agent re-reads the scratch file if needed

## File Naming Convention
tasks/scratch/
├── analysis-auth-module.md      # Codebase analysis results
├── search-results-user-api.md   # Search output saved for reference
├── diff-before-refactor.md      # Saved diff for comparison
└── tool-output-build-log.md     # Captured command output
```

**Template for scratch files**:

```markdown
## Scratch: [Descriptive Title]
**Created**: [timestamp]
**Purpose**: [Why this was saved]
**Referenced by**: [What task/step uses this]

---

[Content]
```

**Key rule**: Always include a one-line summary in the conversation after writing the scratch file. The summary should contain enough information to decide whether to re-read the file.

### Step 3: Plan Persistence Pattern

**Purpose**: Store structured plans in files so they survive context resets, session boundaries, and can be shared between agents.

**When to use**: Before starting any multi-step implementation; whenever a plan is approved.

**Implementation**:

```markdown
## Plan Persistence Workflow

1. Create plan following the plan-before-code methodology
2. Write plan to: `tasks/plan-[feature-name].md`
3. Reference the plan file path throughout implementation
4. Update the plan file as steps complete (mark items done)
5. At session handoff, the plan file IS the continuity document

## Plan File Structure
tasks/
├── plan-auth-refactor.md        # Active implementation plan
├── plan-api-redesign.md         # Another active plan
├── completed/                   # Finished plans (for reference)
│   └── plan-db-migration.md
└── handoff-2026-02-24.md        # Session handoff document
```

**Integration with `plan-before-code`**: The plan file created in the planning phase becomes the source of truth throughout implementation. Instead of relying on the agent to "remember" the plan, have it re-read the file at each major step.

```
"Re-read tasks/plan-auth-refactor.md and proceed with the next
uncompleted step."
```

### Step 4: Sub-Agent Communication Pattern

**Purpose**: Enable multiple agents to share state through filesystem rather than conversation context, avoiding the "telephone game" of context handoffs.

**When to use**: Multi-agent workflows, parallel research tasks, any situation where one agent's output feeds another agent's input.

**Implementation**:

```markdown
## Sub-Agent Communication Workspace

tasks/agents/
├── shared/                       # Shared read-write space
│   ├── findings.md              # Accumulated research findings
│   ├── decisions.md             # Decisions log (append-only)
│   └── file-inventory.md       # List of all files under work
├── agent-research/              # Research agent's workspace
│   ├── output.md               # Research results
│   └── status.md               # Current status
├── agent-implementation/        # Implementation agent's workspace
│   ├── output.md               # Implementation results
│   └── status.md               # Current status
└── orchestrator/                # Orchestrator's coordination files
    ├── task-assignments.md      # Who is doing what
    └── integration-plan.md     # How to merge results
```

**Communication Protocol**:

1. **Orchestrator** writes task assignments to `tasks/agents/orchestrator/task-assignments.md`
2. **Each agent** reads its assignment, performs work, writes results to its workspace
3. **Each agent** updates `shared/findings.md` with key discoveries (append-only)
4. **Orchestrator** reads all agent outputs and integrates

**Critical rules**:
- `shared/` files are append-only (agents add, never overwrite)
- Each agent has its own workspace (no cross-agent writes)
- Status files enable progress monitoring without reading full outputs
- Use structured formats (Markdown with consistent headers) for machine-readable content

### Step 5: Dynamic Skill Loading Pattern

**Purpose**: Load skills and configuration on demand to keep the initial context lean and focused.

**When to use**: When the full skill catalog would consume too much context; when switching between task types mid-session.

**Implementation**:

```markdown
## Dynamic Skill Loading Workflow

1. Start session with minimal context (core workflow skills only)
2. When a specific capability is needed:
   - Read the relevant SKILL.md file
   - Apply its instructions to the current task
   - The skill content enters context naturally through the file read
3. When switching to a different task type:
   - Read the new skill file
   - The previous skill's content naturally ages out of active attention

## Skill Discovery Paths
~/.codex/skills/                  # Global skills (installed by DevAI-Hub)
$CODEX_HOME/skills/                    # Project-specific skills
catalog/skills/[category]/[name]/ # Skill catalog (development reference)
```

**Loading triggers**:
- Security review needed → Read `security-review/SKILL.md`
- Compliance check needed → Read relevant `compliance/[framework]/SKILL.md`
- Performance optimization → Read `performance-review/SKILL.md`

**Key principle**: Do not pre-load all skills. Let the task determine which skills are relevant, and load them just-in-time.

### Step 6: Terminal Persistence Pattern

**Purpose**: Capture terminal output (build logs, test results, command output) to files for later reference and analysis.

**When to use**: When command output is large, when you need to compare outputs across runs, or when test results need analysis.

**Implementation**:

```markdown
## Terminal Persistence Workflow

1. Run command and capture output:
   - Write output to: `tasks/logs/[command]-[timestamp].txt`
   - Or use shell redirection: `npm test > tasks/logs/test-run.txt 2>&1`

2. Summarize the output in conversation:
   - "Tests: 45 passed, 3 failed. Details in tasks/logs/test-run.txt"

3. When analysis is needed:
   - Read the log file
   - Focus on specific sections (errors, warnings)
   - Write analysis to scratch pad

## Log File Organization
tasks/logs/
├── build-2026-02-24.txt         # Build output
├── test-run-latest.txt          # Most recent test run
├── lint-output.txt              # Linter results
└── deploy-staging.txt           # Deployment log
```

### Step 7: Self-Modification Pattern

**Purpose**: Enable agents to update their own instructions based on discoveries made during sessions, creating a feedback loop that improves future sessions.

**When to use**: When the agent discovers a project convention, a gotcha, or a pattern that should persist across sessions.

**Implementation**:

```markdown
## Self-Modification Targets

1. **AGENTS.md** (project-level):
   - Add discovered conventions: "All API routes use camelCase"
   - Add gotchas: "The auth module requires Node 18+"
   - Add workflow preferences: "Always run lint before commit"

2. **Memory files** (~/.codex/projects/[project]/memory/):
   - Store project-specific patterns
   - Record debugging insights
   - Track architectural decisions

3. **Skill files** (for skill developers):
   - Update skill instructions based on real-world usage
   - Add new patterns discovered through practice
   - Refine trigger phrases based on actual invocations

## Self-Modification Protocol
1. Agent discovers a pattern or convention
2. Agent verifies the pattern (check 2-3 examples in the codebase)
3. Agent proposes the update to the user
4. On approval: agent writes to the appropriate file
5. Future sessions benefit from the persisted knowledge
```

**Safety guidelines**:
- Always verify patterns against multiple examples before persisting
- Propose changes to the user before writing to AGENTS.md
- Memory files can be updated more freely (they are advisory, not directive)
- Never overwrite existing instructions without user approval

## Best Practices

- **Name files descriptively**: `analysis-auth-module.md` not `output.md`
- **Include timestamps**: Files without dates become stale unknowingly
- **Clean up scratch files**: Delete or archive after the task completes
- **Append, don't overwrite**: For shared files, append new entries rather than replacing
- **Reference paths explicitly**: "See tasks/plan.md" is clearer than "see the plan file"
- **Structured formats**: Use Markdown with consistent headers so agents can parse content
- **One purpose per file**: A plan file, a findings file, and a decisions file are better than one giant file

## Common Patterns

### Pattern 1: Session State File

**Situation**: Long session needs checkpointing to prevent context loss.

**Solution**: Maintain a running state file that gets updated at each major milestone:
```
tasks/session-state.md:
- Current task and status
- Files modified (running list)
- Decisions made (append-only)
- Next steps (updated each milestone)
```

### Pattern 2: Multi-Agent Workspace

**Situation**: Parallel research agents exploring different parts of the codebase.

**Solution**: Use the sub-agent communication workspace (Step 4) with:
- Each agent has its own output directory
- Shared findings file for cross-agent discovery
- Orchestrator integration plan for merging results

### Pattern 3: Progressive Skill Loading

**Situation**: A code review task that starts with architecture analysis, then moves to security, then performance.

**Solution**: Load skills progressively as each phase begins:
1. Start: Read `context-analysis/SKILL.md`
2. Phase 2: Read `security-review/SKILL.md`
3. Phase 3: Read `performance-review/SKILL.md`
4. Final: Read `final-report/SKILL.md`

Each skill enters context fresh, at the point of maximum attention.

## Quality Checklist

- [ ] Appropriate pattern selected for the situation
- [ ] Files named descriptively with timestamps where relevant
- [ ] Summaries provided in conversation after writing to files
- [ ] Shared files use append-only protocol
- [ ] Scratch files cleaned up after task completion
- [ ] Self-modification changes reviewed before persisting
- [ ] File paths referenced explicitly in conversation

## Related Skills

- `context-manager` - Context fundamentals and attention budget management
- `context-compression` - Compression techniques that use filesystem patterns
- `plan-before-code` - Planning methodology (plans should be file-persisted)
- `task-coordinator` - Task coordination that benefits from file-based state

---

**Version**: 1.0.0
**Last Updated**: February 2026
**Author**: DevAI-Hub
**Attribution**: Adapted from [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) (MIT License)


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
