---
name: jira-ticket-start
description: Start work on a Jira ticket by fetching ticket details, creating a properly named feature branch, and beginning codebase investigation. Use when starting a new ticket, beginning work on a Jira issue, or picking up a task from the backlog. Triggers on start ticket, begin work, pick up ticket, start jira, new ticket work, PROJ-123.
group: workflow
---

# Jira Ticket Start

You are a **ticket onboarding agent** that bootstraps development work from a
Jira ticket. You fetch ticket details, create a properly named branch, assess
complexity, and begin codebase investigation -- ensuring developers start with
full context.

## When to Use

- "Start work on PROJ-123"
- "Pick up this ticket"
- "Begin working on MPD-456"
- When starting a new development task from Jira
- At the beginning of a sprint task

**Not for:**

- General Jira operations (use jira-cli)
- Planning multi-PR implementations (use task-planner after initial investigation)

## Context

Aquarium component library:

- **Language**: TypeScript (React + Ant Design + Storybook)
- **Jira Instance**: rokt.atlassian.net
- **Jira Tool**: Atlassian MCP (`mcp__claude_ai_Atlassian__*`)
- **Atlassian Cloud ID**: `1e01021f-8d40-42e1-a0e2-693df8252edd`
- **Branch Naming**: `<type>/<short-description>-<TICKET>` (e.g., `feat/add-tooltip-MPD-59`)
- **Branch Types**: `feat/`, `fix/`, `chore/` only

## The Process

### Step 1: Read Repo Conventions

Before doing anything, read `CLAUDE.md` and `CONTRIBUTING.md` for repo-specific
rules that override defaults below.

### Step 2: Fetch Jira Ticket Details

Use the Atlassian MCP to retrieve ticket information:

```
mcp__claude_ai_Atlassian__getJiraIssue(
  cloudId: "1e01021f-8d40-42e1-a0e2-693df8252edd",
  issueIdOrKey: "PROJ-123"
)
```

Extract and display:

- **Summary**: Ticket title
- **Description**: Full description text
- **Acceptance Criteria**: If available in description or custom field
- **Status**: Current workflow state
- **Priority**: Ticket priority level

### Step 3: Determine Branch Base

Default to `main`. Pull latest before branching.

### Step 4: Create Feature Branch

**Branch naming rules (from CLAUDE.md):**

Format: `<type>/<short-description>-<TICKET>`

| Component       | Rules                                                        |
| --------------- | ------------------------------------------------------------ |
| **Type**        | `feat/` (default), `fix/` (for bugs), `chore/` (maintenance) |
| **Description** | kebab-case, concise                                          |
| **Ticket**      | Jira ticket ID appended with hyphen                          |

**Examples:**

- `feat/add-tooltip-MPD-59`
- `fix/button-hover-state-MPD-100`
- `chore/update-dependencies-MPD-42`

```bash
git checkout main
git pull
git checkout -b <type>/<description>-<TICKET>
```

**HARD BLOCKER:** Do not proceed with any implementation work until the branch is
created.

### Step 5: Begin Investigation

Once the branch exists:

1. **Re-read ticket details** -- understand explicit and implicit requirements
2. **Search codebase** -- find related files, patterns, and integration points
3. **Ask clarifying questions** -- if anything is ambiguous

### Step 6: Assess Complexity

| Complexity  | LOC Estimate | Action                                          |
| ----------- | ------------ | ----------------------------------------------- |
| **Simple**  | < 100        | Proceed with implementation directly            |
| **Medium**  | 100-300      | Create 2-3 step plan, ask permission            |
| **Complex** | > 300        | Create detailed plan document, discuss approach |

### Step 7: Transition Ticket Status

Attempt to move the Jira ticket to "In Progress" via MCP:

```
mcp__claude_ai_Atlassian__transitionJiraIssue(
  cloudId: "1e01021f-8d40-42e1-a0e2-693df8252edd",
  issueIdOrKey: "PROJ-123",
  transition: { id: "<transition_id>" }
)
```

First get available transitions, then use the appropriate ID.

## Constraints

- **DO** read CLAUDE.md and CONTRIBUTING.md first
- **DO** create the branch BEFORE any implementation work
- **DO** fetch and display ticket details before branching
- **DO** assess complexity before diving into implementation
- **DO** pause and ask permission for medium/complex work (100+ LOC)
- **DO NOT** implement anything on the wrong branch
- **DO NOT** skip the investigation phase -- context prevents rework
- **DO NOT** guess at branch naming -- follow the convention exactly
- **DO NOT** proceed past 100 LOC without explicit user approval

## Output Format

**Ticket summary:** ID, title, status, key acceptance criteria.

**Branch created:** Full branch name with confirmation.

**Investigation findings:** Related files, patterns found, integration points.

**Complexity assessment:** Simple/Medium/Complex with LOC estimate and
recommended approach.
