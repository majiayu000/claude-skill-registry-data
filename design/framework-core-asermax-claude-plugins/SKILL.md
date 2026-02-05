---
name: framework-core
description: |
  Load when working with any katachi framework command. Provides workflow principles, status tracking conventions, and decision guidance. This skill establishes the collaborative context for all framework operations.
---

# Framework Core Skill

Core skill that establishes workflow context for all katachi framework commands.

## When to Load

All framework commands should load this skill first to establish:
- Collaborative workflow principles
- Status tracking conventions
- Scratchpad usage patterns
- Context bridging guidelines
- Decision type guidance (ADR vs DES)

## Project Templates

These templates are used when creating project structure:

**Planning documents:**
- `references/VISION-template.md` - Vision document structure
- `references/DELTAS-template.md` - Delta inventory structure (work tracking)
- `references/DEPENDENCIES-template.md` - Dependency matrix structure (delta dependencies)

**Decision documents:**
- `references/ADR-template.md` - Architecture Decision Record format
- `references/DES-template.md` - Design Pattern document format

**Feature documentation:**
- `../working-on-delta/references/feature-spec.md` - Long-lived feature specification
- `../working-on-delta/references/feature-design.md` - Long-lived feature design
- `../working-on-delta/references/feature-domain-readme.md` - Domain index template
- `../working-on-delta/references/feature-specs-readme.md` - Top-level feature index

**Delta working documents:**
- `../working-on-delta/references/delta-spec.md` - Delta specification (working doc)
- `../working-on-delta/references/delta-design.md` - Delta design (working doc)
- `../working-on-delta/references/implementation-plan.md` - Implementation plan (working doc)

**Guidance documents** (how to write each document type):
- `../working-on-delta/references/spec-template.md` - How to write delta specifications
- `../working-on-delta/references/design-template.md` - How to write design rationale
- `../working-on-delta/references/plan-template.md` - How to write implementation plans

## Decision Types Reference

Load `references/decision-types.md` when:
- Creating a new decision document (ADR or DES)
- Determining which document type to use for a pattern/choice
- Retrofitting existing decisions from code
- Teaching users about ADR vs DES distinction

This reference contains the full decision tree and examples for choosing between ADRs (one-time architectural choices) and DES (repeatable patterns).

## State Detection

Before executing any command, detect project state:

### 1. Not Initialized
**Condition:** No `docs/planning/` directory exists

**Action:**
- If no significant code exists → Offer `/katachi:init-framework`
- If code exists → Explain retrofit options

### 2. Partially Initialized
**Condition:** `docs/planning/` exists but missing VISION.md, DELTAS.md, or DEPENDENCIES.md

**Action:**
- List what's missing
- Offer to complete setup
- Show which commands to run

### 3. Fully Initialized
**Condition:** All planning files exist

**Action:**
- Proceed with normal command operation
- Show current focus from CLAUDE.md if available

### 4. Retrofit Mode
**Condition:** Code exists but no framework documentation

**Action:**
- Explain retrofit commands available
- Offer `/katachi:retrofit-spec` for existing modules
- Offer `/katachi:retrofit-decision` for existing patterns

---

## Workflow Principles

Common principles for all collaborative command workflows in this framework.

### Core Principles

#### 1. One Question at a Time

Never batch multiple questions. Wait for answer before proceeding.

**Why:** Prevents cognitive overload, maintains clear conversation flow, ensures each decision gets proper attention.

#### 2. Propose, Don't Decide

Agent proposes options, user confirms. Never add or change anything without user agreement.

**Why:** User is the architect, Claude is the implementer. Maintain this relationship throughout.

#### 3. Use AskUserQuestion for Structured Options

When presenting 2-4 distinct choices, use the AskUserQuestion tool:

- Provide clear header (max 12 chars, e.g., "Logging", "Format", "Approach")
- Write complete question text
- Add description explaining each option and its implications
- Use `multiSelect: true` if choices aren't mutually exclusive
- Examples: installation modes, logging approaches, technical choices, format options

**When to use plain text instead:**
- Open-ended questions (no predefined options)
- Single simple clarification needed
- Asking for creative input
- Yes/no questions

#### 4. Detect Gaps Proactively

Throughout the entire process:
- Surface unstated assumptions by asking about them
- Identify potential edge cases and ask user if they're relevant
- Challenge vague or incomplete answers
- Ask "what could go wrong?" and "what's missing?"
- Never fill gaps yourself - always ask the user

#### 5. Use a Scratchpad

Track state in `/tmp/<command>-state.md`:

**Commands with natural IDs:**
- For `-delta` commands, include the delta ID: `/tmp/<command>-<FEATURE-ID>-state.md`
  - `/spec-delta`: `/tmp/spec-<FEATURE-ID>-state.md`
  - `/design-delta`: `/tmp/design-<FEATURE-ID>-state.md`
  - `/plan-delta`: `/tmp/plan-<FEATURE-ID>-state.md`
  - `/implement-delta`: `/tmp/implement-<FEATURE-ID>-state.md`

**Commands without natural IDs (parallel execution support):**
- Generate unique animal-adjective ID: `/tmp/<command>-<animal-adjective>-state.md`
  - `/add-delta`: `/tmp/add-delta-<animal-adjective>-state.md`
  - `/analyze`: `/tmp/analyze-<animal-adjective>-state.md`
  - `/analyze-impact`: `/tmp/analyze-impact-<animal-adjective>-state.md`
  - `/decision`: `/tmp/decision-<animal-adjective>-state.md`
  - `/review-code`: `/tmp/review-code-<animal-adjective>-state.md`
  - Enables multiple concurrent sessions without state file conflicts
  - Keep state files after completion (don't auto-clean) for debugging/audit trail

**Commands that don't need parallel support:**
- `/vision`, `/deltas`, `/dependencies` - Sequential execution sufficient, use `/tmp/<command>-state.md`

**Commands without scratchpads:**
- `/commit`, `/record-learnings` - No scratchpad needed

**Scratchpad contents:**
- Current section/phase being worked on
- Questions asked and answered
- Gaps identified
- Topics to revisit
- Decisions made

**Why:** Prevents information loss across question rounds, maintains context during iteration.

#### 6. Bridge the Context Gap

The agent reads multiple files (specs, designs, ADRs, DES patterns) and builds comprehensive context. The user reads documents when needed but doesn't have the full picture simultaneously.

**When asking questions or explaining decisions:**
- Include diagrams (ASCII art, sequence diagrams, thread/data flows)
- Provide rich context - don't assume shared understanding
- Explain the "why" behind technical questions
- Show concrete examples, not abstract references
- Name the specific files, components, or patterns being referenced

#### 7. Research When Needed

When user shows uncertainty, research to provide informed options.

**Research triggers:**
- User says "I'm not sure" or "I don't know"
- Topic involves technical choices (models, libraries, protocols, frameworks)
- User asks "what options do I have?"
- User mentions alternatives they've tried but weren't satisfied with

Use Task tool (general-purpose agent) to research, then synthesize findings to inform questions.

### Workflow Modes

#### Information Gathering

**Use for:** Understanding requirements, clarifying scope, exploring options

**Workflow:**
- Ask one question at a time
- Wait for answer before proceeding
- Use AskUserQuestion for structured choices
- Build understanding incrementally

#### Document Creation

**Use for:** Specs, designs, plans, decisions

**Workflow:**
1. **Research phase (silent, thorough)**
   - Read spec/requirements
   - Read relevant ADRs and DES patterns
   - Explore related codebase areas if needed
   - Research official documentation for libraries/frameworks/APIs
   - Build understanding without asking upfront questions

2. **Draft proposal (with decision points)**
   - Create complete document following template
   - Base all choices on research findings
   - Note any uncertainties/assumptions clearly
   - **If choices require user input:** Use AskUserQuestion (ambiguous requirements, multiple valid approaches, trade-offs)

3. **External validation (silent)**
   - Dispatch appropriate reviewer agent
   - Agent provides structured feedback

4. **Apply validation feedback (silent, with decision points)**
   - Apply ALL recommendations automatically
   - **If applying requires a choice:** Use AskUserQuestion (multiple valid fixes, conflicts with earlier decisions)
   - Track changes for presentation

5. **Present validated document**
   - Show complete document to user
   - Include summary of applied validation fixes
   - Highlight unresolved issues
   - Invite user feedback: "What needs adjustment?"

6. **Iterate based on user feedback**
   - Apply user corrections/additions
   - Re-run validation if significant changes
   - Repeat until user approves

7. **Finalize**
   - Write document to file
   - Update status

**Key principle:** Validate before presenting, auto-apply fixes. Only use AskUserQuestion for genuine decisions (multiple valid options), not for fixes.

### Validation Best Practices

#### Use Custom Agents for Validation

Dispatch the appropriate reviewer agent for validation:

| Document Type | Reviewer Agent |
|--------------|----------------|
| Delta Spec | `katachi:spec-reviewer` |
| Delta Design | `katachi:design-reviewer` |
| Implementation Plan | `katachi:plan-reviewer` |
| Implemented Code | `katachi:code-reviewer` |
| Change Impact | `katachi:impact-analyzer` |
| Existing Code | `katachi:codebase-analyzer` |

Dispatch agents using the Task tool with appropriate `subagent_type`.

#### Validation Context

Balance fresh perspective with respecting user decisions:

**Include in validation context:**
- The artifact being validated (spec, design, code, etc.)
- Relevant templates and examples
- User's explicit decisions and constraints
- Project-wide patterns (ADRs, DES documents)

**Exclude from validation context:**
- Agent's internal reasoning and discussion history
- Intermediate drafts and iterations
- Unrelated project context

### Collaborative Process

**This is always a collaborative process:**
- Ask one question at a time
- Agent proposes, user confirms - never decide without agreement
- User makes all decisions
- Provide alternatives and trade-offs (research-backed when needed)
- Never fill gaps yourself - always ask the user
- Use AskUserQuestion for structured options (2-4 choices)
- Iterate until the user approves the final result

---

## Status Tracking

Conventions for tracking delta progress through the development workflow.

### Status Symbols

| Symbol | Meaning |
|--------|---------|
| ✗ | Not Started |
| ⧗ | In Progress |
| ✓ | Complete |

### Status Progression

Deltas progress through these stages:

```
✗ Defined         (initial state - delta in DELTAS.md)
    ↓
⧗ Spec            (/spec-delta starts)
    ↓
✓ Spec            (/spec-delta completes)
    ↓
⧗ Design          (/design-delta starts)
    ↓
✓ Design          (/design-delta completes)
    ↓
⧗ Plan            (/plan-delta starts)
    ↓
✓ Plan            (/plan-delta completes)
    ↓
⧗ Implementation  (/implement-delta starts)
    ↓
✓ Implementation  (/implement-delta completes)
```

### When to Update Status

#### At Command Start
Set status to in-progress state (⧗) for the current phase.

Example: `/spec-delta CORE-001` → set status to "⧗ Spec"

#### At Command Completion
Set status to complete state (✓) for the current phase.

Example: `/spec-delta CORE-001` finishes → set status to "✓ Spec"

### How to Update Status

Use the deltas.py script:

```bash
# Set status
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status set FEATURE-ID "STATUS"

# Examples
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status set CORE-001 "⧗ Spec"
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status set CORE-001 "✓ Spec"
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status set CORE-001 "⧗ Design"
```

### Querying Status

```bash
# List all deltas with status
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status list

# Filter by category
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status list --category CORE

# Filter by status
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status list --status "✓ Spec"

# Show detailed delta status
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py status show CORE-001
```

### Status in DELTAS.md

Status is stored in DELTAS.md as a column:

```markdown
| ID | Description | Complexity | Status |
|----|-------------|------------|--------|
| CORE-001 | Delta description | Medium | ✓ Design |
| CORE-002 | Another delta | Easy | ⧗ Spec |
```

### Ready to Implement

A delta is ready to implement when:
1. All dependencies have status "✓ Implementation" or higher
2. The delta has status "✓ Plan"

Use this command to check:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/deltas.py ready
```

---

## Task Management Protocol

Use Claude Code's task tools to track workflow progress within each command.

### Purpose

Tasks provide:
- Visibility into what the command will do (upfront planning)
- Progress tracking via spinner with activeForm text
- Clear completion state for each phase

### When to Create Tasks

Create tasks at command start, after loading skills and reading initial context. Create all tasks upfront with dependencies before beginning work.

### Task Guidelines

**Identify workflow phases:** Review the command's process steps and identify distinct phases (research, draft, validate, iterate, finalize, etc.)

**Create one task per phase:** Each phase becomes a task with:
- `subject`: Imperative action (e.g., "Research context for {ID}")
- `description`: Brief explanation of what happens in this phase
- `activeForm`: Present participle shown in spinner (e.g., "Researching context")

**Set dependencies:** Use `TaskUpdate` with `addBlockedBy` to create a chain. Phases that must complete before others are blocked.

**Include identifiers:** When working with a delta or using a scratchpad ID, include it in task subjects for clarity.

**Progress through tasks:**
1. Mark task as `in_progress` when starting the phase
2. Do the work
3. Mark task as `completed` when done
4. Move to next task

### Integration with Status Tracking

Task management complements delta status tracking:

| System | Purpose | Scope |
|--------|---------|-------|
| `deltas.py` + DELTAS.md | Delta lifecycle status | Cross-session |
| Claude Code Tasks | Workflow phase progress | Within command |

Update both at appropriate points:
- `deltas.py status set` at command start/completion (delta lifecycle)
- `TaskUpdate` as each workflow phase starts/completes (session visibility)

### Commands Without Tasks

Some simple commands may not need task tracking (single-step operations, simple extractions). Use judgment - if there are distinct phases worth tracking, create tasks.
