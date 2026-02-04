---
name: pm-assistant
description: Product Owner assistance for ticket refinement, epic breakdown, dependency analysis, and backlog management across multiple project management systems. Use this skill when working with tickets to create, analyze, propose amendments, or generate discussion questions. Supports Linear, Local Markdown, Jira, GitHub Issues, and other PM systems through extensible connectors.
---

# PM Assistant Skill

## Overview

This skill enables Product Owner workflows across multiple project management systems:
- Create and refine tickets with proper structure and acceptance criteria
- Analyze tickets for gaps, clarity, completeness, and dependencies
- Break down epics into actionable sub-tickets
- Generate meaningful refinement session questions
- Propose amendments based on conversation context

The skill automatically detects which PM system the project uses (Linear, Local Markdown, Jira, GitHub, etc.) and applies the appropriate connector to query and mutate data. All analysis patterns and refinement workflows are system-agnostic and work consistently across platforms.

## Getting Started: PM System Detection

Before starting any work, the skill automatically establishes the PM system context:

### 1. PM System Detection

The skill detects which PM system the project uses by:
1. **Checking for MCP servers** - Is Linear, Jira, GitHub, or other PM connector available?
2. **Checking CLAUDE.md** - Does the project declare a PM system explicitly?
3. **Checking for docs/tickets directory** - Does Local Markdown tickets directory exist?
4. **Using AskUserQuestion tool** - If detection is ambiguous (see "Using AskUserQuestion for User Input" section)

### 2. PM System Configuration

Configure the PM system in **CLAUDE.md** file in your project root:

**Example for Linear**:
```markdown
# CLAUDE.md

## Project Management
- **System**: Linear
- **Team Prefix**: PROD
- **Project**: Backend Services
```

**Example for Jira**:
```markdown
# CLAUDE.md

## Project Management
- **System**: Jira
- **Instance**: https://company.atlassian.net
- **Project**: BACKEND
```

**Example for Local Markdown**:
```markdown
# CLAUDE.md

## Project Management
- **System**: Local-Markdown
- **Directory**: docs/tickets
```

### 3. Connector-Specific Discovery

Once the PM system is detected, the skill loads the appropriate connector from `connectors/` (e.g., `connectors/linear.md`, `connectors/local-markdown.md`, `connectors/jira.md`). The connector handles:
- Finding team/project context specific to that system
- Discovering available workspaces, teams, or projects
- Using AskUserQuestion tool if multiple options exist (see "Using AskUserQuestion for User Input" section)

This ensures all operations are scoped to the correct workspace for the detected PM system.

## Core Capabilities

### 1. Create Tickets from Conversation

**Scenario**: "Create a ticket for this feature with acceptance criteria" or "Based on the conversation transcript create epic with tickets/ticket"

**Process**:
1. Extract requirements from conversation context
2. Use ticket template from `assets/ticket_template.md`
3. Structure as simple or complex ticket based on scope
4. Apply appropriate type labels (Feature, Bug, Enhancement, etc.)
5. Present proposal to user for review
6. **Use AskUserQuestion tool for confirmation**: Wait for explicit approval before proceeding
7. **After user confirms**: Create ticket using the loaded PM connector
8. Report created ticket with ID and link

**Guidelines**:
- Refer to `references/ticket_structure_guide.md` for formatting standards
- Use `connectors/{system}.md` for PM system-specific API details
- Include acceptance criteria for complex work
- Flag open questions when scope is unclear
- Suggest dependencies if work relates to existing tickets

### 2. Propose Ticket Amendments

**Scenario**: "Are there any wrong assumptions in the ticket?" or "Based on the conversation transcript suggest adjustments to epic XXX-123"

**Process**:
1. Fetch existing ticket/epic using the loaded PM connector
2. Analyze current state (description, acceptance criteria, scope)
3. Cross-reference with provided context (code, conversation, etc.)
4. Use patterns from `references/analysis_patterns.md` to identify:
   - Assumption mismatches
   - Scope gaps or overreach
   - Missing edge cases or error handling
   - Outdated requirements
5. Present proposed changes:
   - "Current state" (quote from ticket)
   - "Suggested changes" (with rationale)
   - "Questions for team" (if needed)
6. **Use AskUserQuestion tool for confirmation**: Wait for explicit approval before proceeding
7. **After user confirms**: Update ticket using the loaded PM connector
8. Report changes applied

**Guidelines**:
- Be specific: quote the problematic text
- Explain the "why" behind each suggested change
- Distinguish between critical (must fix) and nice-to-have improvements
- Use AskUserQuestion tool if context is ambiguous or requires clarification

### 3. Analyze Tickets for Quality

**Scenario**: "Review existing Linear tickets for completeness, clarity, dependencies, open questions" for range AIA-100 through AIA-110

**Process**:
1. Fetch all tickets in range using the loaded PM connector with appropriate filters
2. For each ticket, evaluate against criteria:
   - **Clarity**: Title, description, acceptance criteria
   - **Completeness**: All required fields, edge cases covered
   - **Dependencies**: Blocks/Blocked-by relationships identified
   - **Open questions**: Uncertainties flagged
3. Use `references/analysis_patterns.md` Pattern 4 for systematic evaluation
4. Compile findings:
   - Strong tickets (ready for development)
   - Needs work (specific improvements recommended)
   - Needs breakdown (too large)
   - Blocked (waiting on decisions)
5. Present report with:
   - Summary per ticket
   - Recommended actions
   - Highest-priority refinements needed

**Guidelines**:
- Use consistent evaluation structure
- Highlight both strengths and issues
- Provide specific, actionable recommendations
- Flag patterns across multiple tickets (e.g., all missing error handling)

### 4. Identify Gaps in Epic Coverage

**Scenario**: "Identify gaps in the planned tickets for epic XXX-123"

**Process**:
1. Fetch epic using the loaded PM connector
2. Query subtickets using the connector's hierarchy query (e.g., filter `parent:"XXX-123"`)
3. Analyze epic scope vs. ticket coverage using `references/analysis_patterns.md` Pattern 1:
   - Frontend/UI components
   - Backend services and APIs
   - Testing and QA work
   - Documentation and knowledge base
   - Deployment or infrastructure
   - Edge cases and error scenarios
4. Present findings:
   - Identified gaps with context
   - Suggested new tickets for each gap
   - Estimated scope per gap
5. **Use AskUserQuestion tool for confirmation**: Present options to create all tickets, select specific ones, or review proposals first
6. **After user confirms**: Create tickets using the loaded PM connector

**Guidelines**:
- Be thorough but realistic (not everything needs a separate ticket)
- Group related gaps (e.g., multiple API endpoints in one ticket)
- Consider team's estimation approach when scoping gaps
- Link new tickets to epic as subtickets

### 5. Analyze Dependencies and Suggest Parallelization

**Scenario**: User asks about dependencies between tickets or how to parallelize work

**Process**:
1. Fetch relevant tickets and analyze relationships
2. Use `references/analysis_patterns.md` Pattern 3:
   - Extract explicit Blocks/Blocked-by relationships
   - Identify implicit dependencies
   - Find critical path (work that must complete first)
   - Group by parallelizable tracks
3. Present parallelization strategy:
   - Work that can happen simultaneously
   - Critical path dependencies
   - Recommended team allocation
4. Suggest implementation sequence

**Guidelines**:
- Consider frontend/backend can often run in parallel if API contract is clear
- Testing can often run alongside implementation if setup is clear
- Documentation can start early with skeleton/outline
- Infrastructure work often critical path

### 6. Generate Refinement Session Questions

**Scenario**: "Generate questions for the next refinement session for tickets XXX-100 through XXX-110"

**Process**:
1. Fetch ticket range using the loaded PM connector with appropriate filters
2. Analyze each ticket for uncertainty patterns:
   - Missing acceptance criteria
   - Ambiguous requirements
   - Unknown trade-offs
   - Implicit assumptions
   - Unclear edge cases
3. Use `references/refinement_session_guide.md` and `references/analysis_patterns.md` Pattern 5
4. Generate questions organized by:
   - **Critical blockers**: Must resolve first
   - **Design/Technical questions**: Needed before building
   - **Edge cases**: Clarify completeness
   - **Dependencies**: Identify coordination needs
   - **Success metrics**: Define what "done" means
5. Present as structured question set with:
   - Target audience (Product, Engineering, Design)
   - Why the question matters
   - Suggested answers or options

**Guidelines**:
- Prioritize high-impact questions first
- Frame as open-ended (not leading)
- Group related questions by theme
- Note interdependencies between questions
- Suggest time-boxing for discussion

## Analysis Patterns and Templates

### Reference Materials

**For ticket structure standards**:
- `references/ticket_structure_guide.md` - Detailed standards, templates, red flags
- `assets/ticket_template.md` - Practical templates for simple/complex/bug/epic tickets

**For analysis workflows**:
- `references/analysis_patterns.md` - Detailed patterns for gaps, assumptions, dependencies, clarity, refinement
- `connectors/{system}.md` - PM system-specific tool reference:
  - `connectors/linear.md` - Linear MCP API reference
  - `connectors/local-markdown.md` - Local Markdown connector documentation
    - `connectors/local-markdown/setup.md` - Setup instructions

**For refinement sessions**:
- `references/refinement_session_guide.md` - Question generation, facilitation, templates

### When to Use Each Analysis Pattern

| Pattern | Trigger Question | Reference |
|---------|------------------|-----------|
| Gap Identification | "Identify gaps in epic XXX" | `analysis_patterns.md` Pattern 1 |
| Assumption Mismatch | "Are there wrong assumptions?" | `analysis_patterns.md` Pattern 2 |
| Dependency Analysis | "What are dependencies?" | `analysis_patterns.md` Pattern 3 |
| Quality Review | "Review tickets for completeness" | `analysis_patterns.md` Pattern 4 |
| Refinement Questions | "Generate questions for session" | `analysis_patterns.md` Pattern 5, `refinement_session_guide.md` |
| Epic Adjustment | "Suggest adjustments to epic" | `analysis_patterns.md` Pattern 6 |

## Workflow: Create and Propose

All creation and amendment operations follow this pattern:

### Step 1: Gather Context
- User provides requirements (conversation, transcript, existing ticket)
- Establish team/project scope if not already known
- Fetch existing data if modifying

### Step 2: Analyze and Draft
- Use appropriate patterns from `references/analysis_patterns.md`
- Follow structure from `references/ticket_structure_guide.md` or templates
- Draft ticket/amendment with complete context

### Step 3: Present for Review
- Show "current state" and "proposed state" for amendments
- Show "proposed ticket" for new tickets
- Include rationale for each decision
- Use AskUserQuestion tool if clarification is needed

### Step 4: Wait for Confirmation
- **Use AskUserQuestion tool** to get explicit user confirmation before proceeding
- **Do not proceed** until user confirms via the tool response
- Offer to adjust draft if user suggests changes
- Re-present adjusted version and confirm again using AskUserQuestion

### Step 5: Apply Changes
- Use the loaded PM connector to create/update
- Call connector-specific create/update functions
- Include team/project context in all operations (per connector requirements)

### Step 6: Report Results
- Confirm what was created/updated
- Provide ticket ID and Link (if available)
- Ask: "What would you like to do next?"

## Best Practices

### PM System and Project Scoping
- **Always detect** the PM system (MCP server, CLAUDE.md, or use AskUserQuestion tool)
- **Check CLAUDE.md** in project directory for explicit system configuration
- **Load the correct connector** for the detected system
- **Discover team/project context** using the connector's discovery functions
- **Use AskUserQuestion tool** if multiple teams/projects found and context is ambiguous
- **Filter all queries** to correct team and project per the connector's requirements

### Ticket Quality
- Read `references/ticket_structure_guide.md` for quality standards
- Ensure titles are specific and action-oriented
- Include acceptance criteria for complex work
- Flag open questions when scope is unclear
- Link dependencies explicitly

### Analysis Completeness
- Quote specific text when identifying issues
- Explain the "why" behind recommendations
- Distinguish between facts (what's written) and inferences
- Flag assumptions clearly
- Suggest options with trade-offs when multiple paths exist

### User Confirmation Protocol
- Always show proposals before applying
- **Use AskUserQuestion tool** to get explicit user confirmation with clear options
- Wait for confirmation response from the tool before proceeding
- Never assume approval
- Offer revision if user suggests changes
- Re-present for approval after revisions (using AskUserQuestion again)

### PM Connector Usage
- Refer to `connectors/{system}.md` for complete tool reference for the detected system
- Use filters appropriately (per the connector's query syntax)
- Handle errors gracefully (following connector-specific error handling guidance)
- Respect rate limits and batch operations when possible

## Using AskUserQuestion for User Input

When user input is required during workflow execution, use the **AskUserQuestion** tool to present structured options. This ensures clear, actionable choices and reduces ambiguity.

### When to Use AskUserQuestion

Use the tool for:
1. **PM system/project detection** - When multiple teams or projects exist and context is ambiguous
2. **Clarifying questions during analysis** - When requirements, scope, or context needs clarification
3. **Confirmation before actions** - Before creating or updating tickets in the PM system

Do NOT use for:
- Open-ended conversational follow-ups ("What would you like to do next?")
- Refinement session questions (those are for human facilitators)

### Example 1: PM System Detection (Multiple Teams Available)

**Scenario**: Multiple Linear teams found, need to determine which one to use.

```
Use AskUserQuestion tool with:
{
  "questions": [{
    "question": "Multiple Linear teams found in your workspace. Which team should I use for this project?",
    "header": "Team Selection",
    "multiSelect": false,
    "options": [
      {
        "label": "PROD - Product Team",
        "description": "Main product development team (15 active issues)"
      },
      {
        "label": "ENG - Engineering Platform",
        "description": "Infrastructure and platform team (8 active issues)"
      },
      {
        "label": "DESIGN - Design System",
        "description": "Design system and component library team (5 active issues)"
      }
    ]
  }]
}
```

### Example 2: Clarifying Requirements During Analysis

**Scenario**: Analyzing a ticket but scope is ambiguous between two interpretations.

```
Use AskUserQuestion tool with:
{
  "questions": [{
    "question": "The ticket mentions 'email notifications' but doesn't specify the scope. What should be included?",
    "header": "Scope",
    "multiSelect": true,
    "options": [
      {
        "label": "Digest emails",
        "description": "Scheduled summary emails sent daily/weekly"
      },
      {
        "label": "Real-time notifications",
        "description": "Immediate emails when events occur"
      },
      {
        "label": "Transactional emails",
        "description": "System-triggered emails (password reset, confirmations)"
      }
    ]
  }]
}
```

### Example 3: Confirming Before Creating Tickets

**Scenario**: Identified 3 gaps in epic coverage, ready to create tickets.

```
Use AskUserQuestion tool with:
{
  "questions": [{
    "question": "I've identified 3 missing tickets for the email digest epic. Should I create them?",
    "header": "Create Tickets",
    "multiSelect": false,
    "options": [
      {
        "label": "Create all 3 tickets",
        "description": "Create tickets for: UI preferences component, end-to-end testing, and scheduled job setup"
      },
      {
        "label": "Show me the proposals first",
        "description": "Present detailed ticket proposals for review before creating"
      },
      {
        "label": "Create only high-priority ones",
        "description": "Create tickets for UI component and testing, defer infrastructure work"
      }
    ]
  }]
}
```

### Guidelines for Effective Questions

**Structure**:
- Use clear, specific question text
- Provide 2-4 options (not just yes/no when possible)
- Include descriptions explaining what each option means
- Use `multiSelect: true` only when choices are not mutually exclusive

**Headers**:
- Keep short (max 12 chars): "Team", "Scope", "Approach", "Confirm"
- Describes the decision type

**Options**:
- Label: Concise choice (1-5 words)
- Description: Explain implications or what happens if chosen
