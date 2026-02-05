---
name: parallel-coordinator
description: Coordinate parallel agent execution using ACE Framework for LiveMetro React Native development. Use when implementing features with 3+ independent subtasks (UI + API + Firebase + Tests).
type: workflow
priority: high
version: 2.0
based_on: Anthropic Multi-Agent Research System (https://www.anthropic.com/engineering/multi-agent-research-system)
---

# Parallel Agent Coordinator

## Purpose

Coordinate parallel execution of specialist agents using the **ACE (Autonomous Cognitive Entity) Framework** for safe, efficient multi-agent development.

## When to Use

### Use When:
- Feature implementation with 3+ independent subtasks
- Multi-layer work (UI + API + Firebase + Tests)
- Performance optimization across multiple files
- Different file types that can be developed simultaneously

### Don't Use When:
- Sequential dependencies (task B requires task A's output)
- Same file modifications
- Single, focused task (one component/function)
- Simple refactoring

---

## Effort Scaling (Anthropic Pattern)

**Critical Decision**: Determine appropriate resource allocation BEFORE spawning agents.

See [effort-scaling.md](../../agents/shared/effort-scaling.md) for complete guide including:
- Complexity matrix (Trivial → Complex)
- Decision flowchart
- Token economics
- Agent selection guide

**Quick Reference**:
| Complexity | Agents | When to Use |
|------------|--------|-------------|
| Trivial | 0 | Typo, single line |
| Simple | 1 | One component/function |
| Moderate | 2-3 | UI + API + Tests |
| Complex | 5+ | System-wide changes |

---

## Task Delegation Template

**Critical**: Every subagent MUST receive all four elements to prevent duplicated work and gaps.

### Delegation Format

```markdown
## Task: {task_name}

### Objective
{Clear, specific goal statement}
- What success looks like
- Measurable outcome

### Output Format
{Expected deliverable structure}
- File paths and naming: `src/components/{Feature}/index.tsx`
- Code style: TypeScript strict, path aliases
- Documentation: JSDoc for public APIs

### Tools & Sources
{Resources to use}
- Skills to invoke: `react-native-development`
- Reference files: `src/components/ExistingComponent.tsx`
- APIs: Seoul Metro API documentation

### Task Boundaries (DO NOT)
{Explicit exclusions to prevent overlap}
- DO NOT modify files in: `src/services/`
- DO NOT implement: API calls (backend agent handles)
- DO NOT test: (test agent handles)
- WAIT FOR: `backend-integration-specialist` types before starting
```

### Real Example

```markdown
## Task: Create StationInfoCard Component

### Objective
Create a reusable card component displaying station information including:
- Station name with line color indicator
- Distance from user (optional)
- Tap handler for navigation

### Output Format
- File: `.temp/agent_workspaces/mobile-ui/proposals/StationInfoCard.tsx`
- Props interface exported
- memo() wrapper for performance
- Accessibility labels included

### Tools & Sources
- Invoke: `react-native-development` skill
- Reference: `src/components/train/StationCard.tsx` (existing pattern)
- Types: `src/models/station.ts`

### Task Boundaries (DO NOT)
- DO NOT fetch station data (backend handles)
- DO NOT implement navigation logic (screen handles)
- DO NOT write tests (test-automation handles)
- DO NOT modify existing StationCard
```

---

## Iteration Loop (Anthropic Pattern)

Multi-agent workflows rarely complete in one round. Use iterative refinement:

```
ITERATION PROTOCOL:

1. INITIAL DELEGATION
   └── Spawn subagents with clear boundaries

2. COLLECT RESULTS
   └── Read from .temp/agent_workspaces/*/proposals/

3. EVALUATE COMPLETENESS
   ├── All requirements addressed?
   ├── Quality gates pass?
   └── Integration conflicts?

4. IF GAPS FOUND
   ├── Identify specific gaps
   ├── Create targeted follow-up tasks
   └── Spawn additional subagents (narrow scope)

5. MERGE & VALIDATE
   ├── Integrate to src/
   ├── Run quality checks
   └── Spawn quality-validator

6. REPEAT IF NEEDED
   └── Continue until all gaps closed
```

### Gap Detection Checklist

After subagent completion, check:
- [ ] All files from task description created?
- [ ] Types match between backend and UI?
- [ ] Tests exist for new functionality?
- [ ] No TypeScript errors?
- [ ] No ESLint errors?
- [ ] Coverage threshold met?

### Follow-up Task Example

```markdown
## Follow-up: Missing Error Handling

### Context
Initial StationInfoCard implementation complete but missing:
- Error state when station data unavailable
- Loading skeleton while data fetches

### Objective
Add error and loading states to StationInfoCard

### Output Format
- Update existing file in proposals/
- Add LoadingState and ErrorState sub-components

### Task Boundaries
- ONLY modify StationInfoCard.tsx
- DO NOT change prop interface
```

---

## ACE Framework Overview

### Layer 1: Ethical Clearance

**Before any parallel execution, verify**:
- [ ] User privacy respected (no indefinite tracking)
- [ ] API rate limits honored (Seoul API: 30s minimum)
- [ ] App stability maintained
- [ ] Data integrity preserved

**Ethical Veto Power**: Any agent detecting violation → IMMEDIATE ABORT

### Layer 2: Global Strategy

Define strategic context:
```json
{
  "user_goal": "[Problem we're solving]",
  "success_criteria": [
    "iOS and Android functionality",
    "TypeScript strict compliance",
    "Test coverage >75%",
    "Performance: <300ms response"
  ],
  "constraints": [
    "Seoul API rate limits (30s)",
    "Optimize Firebase reads",
    "No breaking changes"
  ]
}
```

### Layer 3: Agent Capability Matching

| Agent | Strengths (>0.80) | Weaknesses (<0.50) |
|-------|-------------------|---------------------|
| **mobile-ui** | React Native (0.95), TypeScript (0.90), Navigation (0.90) | Native modules (0.30), Backend (0.40) |
| **backend-integration** | Firebase (0.95), Seoul API (0.90), Data sync (0.90) | UI design (0.40), Animations (0.30) |
| **performance-optimizer** | React optimization (0.90), Memory leaks (0.85) | New features (0.50), UI (0.45) |
| **test-automation** | Jest (0.95), RTL (0.90), Coverage (0.90) | Feature impl (0.40), UI design (0.35) |

**Matching Rule**: If agent confidence < 0.70 → Agent should DECLINE

### Layer 4: Task Decomposition

**Standard Pattern**:
```json
{
  "subtasks": [
    {
      "id": "task_1",
      "agent": "backend-integration-specialist",
      "task": "API/Firebase integration",
      "output": "src/services/[feature]/[service].ts",
      "workspace": ".temp/agent_workspaces/backend-integration/",
      "dependencies": [],
      "skill": "api-integration OR firebase-integration"
    },
    {
      "id": "task_2",
      "agent": "mobile-ui-specialist",
      "task": "UI components and screens",
      "output": "src/screens/[Screen].tsx",
      "workspace": ".temp/agent_workspaces/mobile-ui/",
      "dependencies": ["task_1"],
      "skill": "react-native-development"
    },
    {
      "id": "task_3",
      "agent": "test-automation-specialist",
      "task": "Test coverage",
      "output": "**/__tests__/[feature].test.ts",
      "workspace": ".temp/agent_workspaces/test-automation/",
      "dependencies": ["task_1", "task_2"],
      "skill": "test-automation"
    }
  ]
}
```

**Execution Flow**:
```
1. Create workspace directories for each agent
2. Invoke Task tool for each agent with appropriate skill
3. Monitor progress via metadata.json (every 30s)
4. Collect proposals from .temp/agent_workspaces/*/proposals/
5. Integrate to src/ after validation
```

**Dynamic Reallocation Triggers**:
- Agent blocked for >2x estimated time
- Agent reports capability mismatch
- Task complexity underestimated

### Layer 5: File Locks & Workspace Isolation

**CRITICAL**: Secondary agents can ONLY write to their workspaces

| Agent | Read Access | Write Access |
|-------|-------------|--------------|
| **Primary** | All files | src/**, .temp/** |
| **mobile-ui** | All files | .temp/agent_workspaces/mobile-ui/** ONLY |
| **backend-integration** | All files | .temp/agent_workspaces/backend-integration/** ONLY |
| **performance-optimizer** | All files | .temp/agent_workspaces/performance-optimizer/** ONLY |
| **test-automation** | All files | .temp/agent_workspaces/test-automation/** ONLY |

**Lock File Location**: `.temp/coordination/locks/`

**Conflict Resolution**: If overlapping edits detected:
1. Move both versions to `.temp/integration/conflicts/`
2. Primary reviews diff
3. Options: Accept A, Accept B, Manual merge

### Layer 6: Skill Invocation

| Task Type | Required Skill |
|-----------|---------------|
| React Native UI | `react-native-development` |
| Push notifications | `notification-system` |
| Seoul API | `api-integration` |
| Firebase | `firebase-integration` |
| Tests | `test-automation` |

**Tool Usage**:
```typescript
// GOOD: Agent writes to own workspace
Write(.temp/agent_workspaces/mobile-ui/proposals/StationCard.tsx)

// BAD: Agent writes to src/ directly (DENIED)
Write(src/components/train/StationCard.tsx)

// GOOD: Agent reads from src/ for reference
Read(src/components/train/ExistingComponent.tsx)
```

---

## Best Practices

### 1. Clear Task Boundaries
- **Do**: Assign distinct file outputs to each agent
- **Don't**: Have multiple agents modify the same file

### 2. Explicit Dependencies
- **Do**: Define clear dependency order (backend → UI → tests)
- **Don't**: Create circular dependencies

### 3. Regular Progress Updates
- **Do**: Agents update metadata.json every 30s
- **Don't**: Long silent periods

### 4. Skill Invocation
- **Do**: Invoke appropriate skill before starting work
- **Don't**: Skip skill guidelines

### 5. Workspace Discipline
- **Do**: Write only to assigned workspace
- **Don't**: Attempt to write directly to src/

---

## Quick Reference

### Directory Structure
```
.temp/
├── agent_workspaces/
│   ├── mobile-ui/
│   │   ├── drafts/
│   │   ├── proposals/
│   │   └── metadata.json
│   ├── backend-integration/
│   ├── performance-optimizer/
│   └── test-automation/
├── coordination/
│   ├── locks/
│   ├── tasks/
│   └── status/
└── integration/
    ├── checkpoints/
    └── conflicts/
```

### Agent Metadata Format
```json
{
  "agent_id": "mobile-ui-specialist",
  "status": "working|blocked|completed|failed",
  "progress": 0-100,
  "current_task": "description",
  "files_modified": [],
  "last_updated": "ISO timestamp"
}
```

### Validation Commands
```bash
npm run type-check  # Must pass (zero errors)
npm run lint        # Must pass (zero errors)
npm test --coverage # Must pass (>75% coverage)
```

---

## Summary

This skill enables:
- Coordinate 2-5 specialist agents in parallel
- Apply effort scaling (Trivial → Complex)
- Use structured delegation templates
- Iterate until all gaps closed
- Achieve up to 90% time reduction (Anthropic benchmark)
- Maintain code quality (TypeScript strict, 75%+ coverage)
- Prevent conflicts through workspace isolation
- Save context via external memory system

**Remember**:
- **Scale Appropriately**: Don't spawn 5 agents for a typo fix
- **Delegate Clearly**: Use the 4-part template every time
- **Iterate**: One round rarely catches everything
- Multi-agent uses ~15x more tokens than single-agent

---

## Available Agents

| Agent | Role | Model |
|-------|------|-------|
| `lead-orchestrator` | Coordination, effort scaling | opus |
| `mobile-ui-specialist` | UI components, screens | sonnet |
| `backend-integration-specialist` | Firebase, Seoul API | sonnet |
| `performance-optimizer` | Memory, render optimization | sonnet |
| `test-automation-specialist` | Jest tests, coverage | sonnet |
| `quality-validator` | Final review, validation | haiku |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `external-memory` | Context persistence |
| `agent-observability` | Decision tracing |
| `agent-improvement` | Self-improvement loop |

---

## Reference Documentation

For detailed procedures, see [references/operations-guide.md](references/operations-guide.md):
- Validation Gates (pre/mid/post execution)
- Emergency Abort Procedure
- Integration Workflow
- Monitoring & Debugging commands
- Complete Example walkthrough

External Reference:
- [Anthropic Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)

---

**Version**: 2.0 | **Last Updated**: 2025-01-04
