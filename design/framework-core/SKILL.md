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
- `references/VISION-template.md` - Vision document structure
- `references/FEATURES-template.md` - Feature inventory structure
- `references/DEPENDENCIES-template.md` - Dependency matrix structure
- `references/BACKLOG-template.md` - Backlog for bugs, ideas, improvements, tech-debt, questions
- `references/ADR-template.md` - Architecture Decision Record format
- `references/DES-template.md` - Design Pattern document format

## Decision Types Reference

Load `references/decision-types.md` when:
- Creating a new decision document (ADR or DES)
- Determining which document type to use for a pattern/choice
- Retrofitting existing decisions from code
- Teaching users about ADR vs DES distinction

This reference contains the full decision tree and examples for choosing between ADRs (one-time architectural choices) and DES (repeatable patterns).

## Backlog System

The backlog tracks items not ready for full feature treatment:
- **Bugs** (BUG-) - Issues to fix via `/review-code`
- **Ideas** (IDEA-) - May be promoted to features via `/add-feature`
- **Improvements** (IMP-) - Enhancements to fix via `/review-code`
- **Tech Debt** (DEBT-) - Cleanup items via `/review-code`
- **Questions** (Q-) - Resolve via `/decision`

Use `${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py` for management:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py list      # List open items
python ${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py show ID   # Show item details
python ${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py add TYPE "TITLE" --priority N
python ${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py fix ID    # Mark as fixed
python ${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py promote ID --feature FEATURE-ID
```

Priority scale: 1=critical, 2=high, 3=medium, 4=low, 5=someday

## State Detection

Before executing any command, detect project state:

### 1. Not Initialized
**Condition:** No `planning/` directory exists

**Action:**
- If no significant code exists → Offer `/katachi:init-framework`
- If code exists → Explain retrofit options

### 2. Partially Initialized
**Condition:** `planning/` exists but missing VISION.md, FEATURES.md, or DEPENDENCIES.md

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
- For `-feature` commands, include the feature ID: `/tmp/<command>-<FEATURE-ID>-state.md`
  - `/spec-feature`: `/tmp/spec-<FEATURE-ID>-state.md`
  - `/design-feature`: `/tmp/design-<FEATURE-ID>-state.md`
  - `/plan-feature`: `/tmp/plan-<FEATURE-ID>-state.md`
  - `/implement-feature`: `/tmp/implement-<FEATURE-ID>-state.md`

**Commands without natural IDs (parallel execution support):**
- Generate unique animal-adjective ID: `/tmp/<command>-<animal-adjective>-state.md`
  - `/add-feature`: `/tmp/add-feature-<animal-adjective>-state.md`
  - `/analyze`: `/tmp/analyze-<animal-adjective>-state.md`
  - `/analyze-impact`: `/tmp/analyze-impact-<animal-adjective>-state.md`
  - `/decision`: `/tmp/decision-<animal-adjective>-state.md`
  - `/review-code`: `/tmp/review-code-<animal-adjective>-state.md`
  - Enables multiple concurrent sessions without state file conflicts
  - Keep state files after completion (don't auto-clean) for debugging/audit trail

**Commands that don't need parallel support:**
- `/vision`, `/features`, `/dependencies` - Sequential execution sufficient, use `/tmp/<command>-state.md`

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

2. **Draft proposal**
   - Create complete document following template
   - Base all choices on research findings
   - Note any uncertainties/assumptions clearly

3. **Present for review**
   - Show complete proposal to user
   - Highlight uncertainties and ask about them
   - Invite user feedback: "What needs adjustment?"

4. **Iterate**
   - Apply user corrections/additions
   - Re-present updated sections if significant changes
   - Repeat until user approves

5. **Finalize**
   - Apply any validation step (if command includes it)
   - Write document to file

**Key principle:** Always draft first, no upfront questions. Questions happen during review phase.

### Validation Best Practices

#### Use Custom Agents for Validation

Dispatch the appropriate reviewer agent for validation:

| Document Type | Reviewer Agent |
|--------------|----------------|
| Feature Spec | `katachi:spec-reviewer` |
| Feature Design | `katachi:design-reviewer` |
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

Conventions for tracking feature progress through the development workflow.

### Status Symbols

| Symbol | Meaning |
|--------|---------|
| ✗ | Not Started |
| ⧗ | In Progress |
| ✓ | Complete |

### Status Progression

Features progress through these phases:

```
✗ Defined         (initial state - feature in FEATURES.md)
    ↓
⧗ Spec            (/spec-feature starts)
    ↓
✓ Spec            (/spec-feature completes)
    ↓
⧗ Design          (/design-feature starts)
    ↓
✓ Design          (/design-feature completes)
    ↓
⧗ Plan            (/plan-feature starts)
    ↓
✓ Plan            (/plan-feature completes)
    ↓
⧗ Implementation  (/implement-feature starts)
    ↓
✓ Implementation  (/implement-feature completes)
```

### When to Update Status

#### At Command Start
Set status to in-progress state (⧗) for the current phase.

Example: `/spec-feature CORE-001` → set status to "⧗ Spec"

#### At Command Completion
Set status to complete state (✓) for the current phase.

Example: `/spec-feature CORE-001` finishes → set status to "✓ Spec"

### How to Update Status

Use the features.py script:

```bash
# Set status
python scripts/features.py status set FEATURE-ID "STATUS"

# Examples
python scripts/features.py status set CORE-001 "⧗ Spec"
python scripts/features.py status set CORE-001 "✓ Spec"
python scripts/features.py status set CORE-001 "⧗ Design"
```

### Querying Status

```bash
# List all features with status
python scripts/features.py status list

# Filter by phase
python scripts/features.py status list --phase 1

# Filter by category
python scripts/features.py status list --category CORE

# Filter by status
python scripts/features.py status list --status "✓ Spec"

# Show detailed feature status
python scripts/features.py status show CORE-001
```

### Status in FEATURES.md

Status is stored in FEATURES.md as a column:

```markdown
| ID | Description | Complexity | Status |
|----|-------------|------------|--------|
| CORE-001 | Feature description | Medium | ✓ Design |
| CORE-002 | Another feature | Easy | ⧗ Spec |
```

### Ready to Implement

A feature is ready to implement when:
1. All dependencies have status "✓ Implementation" or higher
2. The feature has status "✓ Plan"

Use this command to check:
```bash
python scripts/features.py ready
```
