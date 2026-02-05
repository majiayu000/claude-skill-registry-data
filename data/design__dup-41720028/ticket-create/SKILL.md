---
name: ticket-create
description: "Interactive Atomic Ticket design and creation tool following Single Responsibility Principle. Use when: (1) Creating new tickets for development tasks, (2) Breaking down complex requirements into atomic tickets, (3) Creating tickets from test failures, (4) Batch creating multiple tickets from requirements description. Each ticket must have exactly one Action + one Target."
---

# Ticket Create

Interactive Atomic Ticket design and creation tool - guides users to design tickets following Single Responsibility Principle.

## Core Principle

**Atomic Ticket = One Action + One Target (Single Responsibility)**

Every ticket must pass the four validation checks:

1. **Semantic Check**: Can express as "verb + single target"?
2. **Modification Reason Check**: Only one reason would cause modification?
3. **Acceptance Consistency**: All acceptance criteria point to same target?
4. **Dependency Independence**: No circular dependencies if split?

## Prohibited Evaluation Methods

**NEVER use these metrics to determine if splitting is needed**:
- Time estimates (30 minutes, 1 hour)
- Lines of code (50 lines, 100 lines)
- File count (2 files, 5 files)
- Test count (5 tests, 10 tests)

**ONLY use the four Single Responsibility checks above.**

## File Format

**v3.0 (Frontmatter Edition)**: Tickets are stored as Markdown files with YAML frontmatter.

### Storage Location

```text
docs/work-logs/v{VERSION}/tickets/{ticket_id}.md
```

**Example**:
```text
docs/work-logs/v0.16.0/tickets/0.16.0-W1-001.md
```

### File Structure

```yaml
---
# === Identification ===
ticket_id: "0.16.0-W1-001"
version: "0.16.0"
wave: 1

# === Single Responsibility ===
action: "Implement"
target: "startScan() method"

# === Execution ===
agent: "parsley-flutter-developer"

# === 5W1H Design ===
who: "parsley-flutter-developer"
what: "Implement startScan() method"
when: "Phase 3 start"
where: "lib/infrastructure/"
why: "Enable barcode scanning"
how: "Use mobile_scanner package"

# === Acceptance Criteria ===
acceptance:
  - Task implementation complete
  - Related tests pass
  - No code quality warnings

# === Related Files ===
files:
  - lib/infrastructure/scanner_service.dart

# === Dependencies ===
dependencies: []

# === Status Tracking ===
status: "pending"
assigned: false
started_at: null
completed_at: null
---

# Execution Log

## Task Summary

Implement startScan() method

---

## Problem Analysis

<!-- To be filled by executing agent -->

---

## Solution

<!-- To be filled by executing agent -->

---

## Test Results

<!-- To be filled by executing agent -->

---

## Completion Info

**Completion Time**: (pending)
**Executing Agent**: parsley-flutter-developer
**Review Status**: pending
```

---

## Interactive Flow

### Step 1: Requirement Collection

```text
Claude: Please describe the task you want to complete:
```

Wait for user input.

### Step 2: Responsibility Analysis

Analyze user requirement and identify independent responsibilities:

```text
Claude: I identified the following independent responsibilities:
1. [Responsibility 1]
2. [Responsibility 2]
...

Each responsibility will become an independent Atomic Ticket.
```

### Step 3: Single Responsibility Check

For each identified responsibility, perform four checks:

```text
Claude: Responsibility 1 "[description]" Single Responsibility Check:
✅ Semantic: Can express as "[verb] + [target]"
✅ Modification Reason: Only "[reason]" would cause modification
✅ Acceptance Consistency: All criteria point to [target]
✅ Dependency Independence: No circular dependencies
→ Meets Atomic Ticket standard
```

If not passing, suggest further splitting:

```text
Claude: ⚠️ Responsibility 2 "[description]" needs further splitting:
❌ Modification Reason: Has two modification reasons
   - Reason A: [description]
   - Reason B: [description]
→ Suggest splitting into:
   - Ticket A: [verb] [target A]
   - Ticket B: [verb] [target B]
```

### Step 4: Ticket Creation Confirmation

```text
Claude: Suggest creating the following Atomic Tickets:

| ID | Action | Target | Agent |
|----|--------|--------|-------|
| {VERSION}-W1-001 | Implement | startScan() method | parsley |
| {VERSION}-W1-002 | Implement | stopScan() method | parsley |

Confirm creation? (Y/n)
```

### Step 5: Create Ticket Files

After confirmation, create Markdown files for each Ticket.

Run:
```bash
uv run .claude/hooks/ticket-creator.py create \
  --version "0.16.0" \
  --wave 1 \
  --seq 1 \
  --action "Implement" \
  --target "startScan() method" \
  --agent "parsley-flutter-developer"
```

**Output**:
```text
✅ Created Ticket: 0.16.0-W1-001
   Location: docs/work-logs/v0.16.0/tickets/0.16.0-W1-001.md
```

---

## Available Commands

### Interactive Mode (Default)

```bash
/ticket-create
```

Guided Q&A to create Tickets step by step.

### Batch Mode

```bash
/ticket-create batch --description "requirement description"
```

Auto-identify responsibilities from description and batch create Tickets.

### From Test Failures

```bash
/ticket-create from-tests
```

Auto-create fix Tickets from latest test results (one Ticket per failing test).

### Initialize Version Directory

```bash
uv run .claude/hooks/ticket-creator.py init 0.16.0
```

Creates version directory and tickets subdirectory.

### List Tickets

```bash
uv run .claude/hooks/ticket-creator.py list --version 0.16.0
```

Lists all tickets in the specified version.

### Show Ticket Details

```bash
uv run .claude/hooks/ticket-creator.py show --id 0.16.0-W1-001
```

Displays full ticket information including 5W1H.

---

## Ticket ID Format

```text
{Version}-W{Wave}-{Seq}
```

**Examples**:
- `0.16.0-W1-001` - v0.16.0, Wave 1, Ticket 1
- `0.16.0-W2-003` - v0.16.0, Wave 2, Ticket 3

### Wave Definition (Dependency Layers)

| Wave | Meaning | Can Execute |
|------|---------|-------------|
| W1 | No dependencies | Immediately, in parallel |
| W2 | Depends on some W1 tickets | After W1 dependencies complete |
| W3 | Depends on some W2 tickets | After W2 dependencies complete |

**Wave Assignment Rule**: Tickets with no dependencies → W1, tickets depending on W1 → W2, etc.

---

## Naming Conventions

**Action (Verb)**:
- `Implement` - Create new feature
- `Fix` - Correct error
- `Add` - Add test or documentation
- `Refactor` - Improve structure
- `Remove` - Delete feature
- `Update` - Modify existing content

**Target (Noun)**:
- Specific method: `startScan() method`
- Specific class: `ISBNValidator class`
- Specific test: `ISBNValidator.validate() test`
- Specific file: `ticket-create SKILL.md`

## Common Mistakes

| Wrong | Problem | Correct |
|-------|---------|---------|
| Implement scanning and offline support | Two targets | Split into two Tickets |
| Fix all ISBN tests | Multiple targets | One Ticket per test |
| Refactor and optimize SearchService | Two actions | Split into two Tickets |

---

## Status Tracking

Status is tracked via frontmatter fields in each Ticket file.

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "pending", "in_progress", "completed" |
| `assigned` | boolean | Whether someone has claimed the ticket |
| `started_at` | datetime | When work started (ISO 8601) |
| `completed_at` | datetime | When work completed (ISO 8601) |

Use `/ticket-track` commands to update status:
- `claim` - Mark as in progress
- `complete` - Mark as completed
- `release` - Release back to pending

---

## Related Skills

- `/ticket-track` - Track and update Ticket status

## Resources

### Scripts
- `.claude/hooks/ticket-creator.py` - Main creation script
- `.claude/hooks/frontmatter_parser.py` - Frontmatter parsing module

### Templates
- `.claude/templates/ticket.md.template` - Ticket file template

### References
- `.claude/methodologies/atomic-ticket-methodology.md` - Full Single Responsibility methodology
- `.claude/methodologies/frontmatter-ticket-tracking-methodology.md` - Frontmatter tracking methodology
