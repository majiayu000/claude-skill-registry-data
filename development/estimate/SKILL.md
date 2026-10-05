---
name: estimate
description: "Analyzes a task or GitHub issue and provides effort estimation broken into subtasks with T-shirt sizing, risk assessment, and dependency mapping. Use for sprint planning or before committing to deadlines."
argument-hint: "[task description or issue number]"
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git log*)
---

# Effort Estimation

## Context
!`gh issue view $1 2>/dev/null || echo "Provide a task description or issue number"`

---

## Estimation Process

### Step 1: Scope Analysis
1. Read the task/issue description carefully
2. Search the codebase to understand current state
3. Identify all files, modules, and systems that would be affected
4. Check for existing implementations that can be reused

### Step 2: Task Breakdown
Decompose the work into subtasks. For each subtask:

| Subtask | Files Affected | Size | Confidence |
|---------|---------------|------|------------|
| ... | ... | S/M/L/XL | High/Med/Low |

**Size Guide:**
- **S (Small)**: < 2 hours — single file change, straightforward logic
- **M (Medium)**: 2-6 hours — multiple files, some complexity, needs tests
- **L (Large)**: 1-2 days — cross-module changes, new patterns, significant testing
- **XL (Extra Large)**: 3-5 days — architectural changes, new infrastructure, coordination needed

### Step 3: Risk Assessment
Identify risks that could expand the estimate:

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ... | High/Med/Low | +S/+M/+L | ... |

Common risks:
- Unclear requirements → ask clarifying questions first
- Legacy code with no tests → add time for writing tests
- External dependencies → add time for integration
- Database migrations → add time for rollback planning
- API changes → add time for consumer coordination

### Step 4: Dependencies
List any blockers or prerequisites:
- Other issues that must be completed first
- External services or APIs that must be available
- Team members who need to be consulted
- Infrastructure or access requirements

### Step 5: Total Estimate

| Scenario | Estimate | Assumption |
|----------|----------|------------|
| **Best case** | ... | Everything goes smoothly, no surprises |
| **Likely case** | ... | Normal amount of debugging and iteration |
| **Worst case** | ... | Major risks materialize |

---

## Rules
- Be honest — over-optimistic estimates hurt more than conservative ones
- Include testing and review time in estimates
- Flag any assumptions you're making
- If the task is too vague to estimate, say so and list the questions that need answers
