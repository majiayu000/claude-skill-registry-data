---
name: openspec
description: Manages spec-driven development with OpenSpec. Use when creating change proposals, planning features, implementing from specs, or archiving completed changes. Triggers on "proposal", "change", or "spec" with "create", "plan", "make", or "help".
---

# OpenSpec Skill

Spec-driven development workflow using the `openspec` CLI.

## Quick Checklist

- Search existing work: `openspec spec list --long`, `openspec list`
- Decide scope: new capability vs modify existing
- Pick unique `change-id`: kebab-case, verb-led (`add-`, `update-`, `remove-`, `refactor-`)
- Scaffold: `proposal.md`, `tasks.md`, `design.md` (if needed), delta specs per capability
- Write deltas: `## ADDED|MODIFIED|REMOVED|RENAMED Requirements`; ≥1 `#### Scenario:` per requirement
- Validate: `openspec validate [change-id] --strict`
- Request approval before implementation

## Three-Stage Workflow

### Stage 1: Creating Changes

Create proposal for:
- New features/functionality
- Breaking changes (API, schema)
- Architecture changes
- Performance optimizations
- Security pattern updates

Skip proposal for:
- Bug fixes (restore intended behavior)
- Typos, formatting, comments
- Non-breaking dependency updates
- Configuration changes
- Tests for existing behavior

**Workflow:**
1. Review `openspec/project.md`, `openspec list`, `openspec list --specs`
2. Choose verb-led `change-id`, scaffold under `openspec/changes/<id>/`
3. Draft spec deltas with `## ADDED|MODIFIED|REMOVED Requirements`
4. Run `openspec validate <id> --strict`

### Stage 2: Implementing Changes

1. Read proposal.md
2. Read design.md (if exists)
3. Read tasks.md
4. Implement tasks sequentially
5. Confirm all tasks complete
6. Update checklist to `- [x]`
7. Do not start until proposal approved

### Stage 3: Archiving Changes

After deployment:
- Move `changes/[name]/` → `changes/archive/YYYY-MM-DD-[name]/`
- Update `specs/` if capabilities changed
- Use `openspec archive <change-id> --skip-specs --yes` for tooling-only changes
- Run `openspec validate --strict`

## Before Any Task

**Context Checklist:**
- [ ] Read relevant specs in `specs/[capability]/spec.md`
- [ ] Check pending changes in `changes/` for conflicts
- [ ] Read `openspec/project.md` for conventions
- [ ] Run `openspec list` to see active changes
- [ ] Run `openspec list --specs` to see existing capabilities

**Before Creating Specs:**
- Check if capability already exists
- Prefer modifying existing specs over duplicates
- Use `openspec show [spec]` to review current state
- Ask 1–2 clarifying questions if ambiguous

## CLI Commands

```bash
# Essential
openspec list                  # List active changes
openspec list --specs          # List specifications
openspec show [item]           # Display change or spec
openspec validate [item]       # Validate changes or specs
openspec archive <change-id> [--yes|-y]   # Archive after deployment

# Project management
openspec init [path]           # Initialize OpenSpec
openspec update [path]         # Update instruction files

# Debugging
openspec show [change] --json --deltas-only
openspec validate [change] --strict
```

**Flags:** `--json`, `--type change|spec`, `--strict`, `--no-interactive`, `--skip-specs`, `--yes`/`-y`

## Directory Structure

```
openspec/
├── project.md              # Project conventions
├── specs/                  # Current truth - what IS built
│   └── [capability]/
│       ├── spec.md         # Requirements and scenarios
│       └── design.md       # Technical patterns
├── changes/                # Proposals - what SHOULD change
│   ├── [change-name]/
│   │   ├── proposal.md     # Why, what, impact
│   │   ├── tasks.md        # Implementation checklist
│   │   ├── design.md       # Technical decisions (optional)
│   │   └── specs/          # Delta changes
│   │       └── [capability]/
│   │           └── spec.md # ADDED/MODIFIED/REMOVED
│   └── archive/            # Completed changes
```

## Creating Change Proposals

### Decision Tree

```
New request?
├─ Bug fix restoring spec behavior? → Fix directly
├─ Typo/format/comment? → Fix directly
├─ New feature/capability? → Create proposal
├─ Breaking change? → Create proposal
├─ Architecture change? → Create proposal
└─ Unclear? → Create proposal (safer)
```

### proposal.md Template

```markdown
# Change: [Brief description]

## Why
[1-2 sentences on problem/opportunity]

## What Changes
- [Bullet list]
- [Mark breaking changes with **BREAKING**]

## Impact
- Affected specs: [list capabilities]
- Affected code: [key files/systems]
```

### Spec Delta Template

```markdown
## ADDED Requirements

### Requirement: New Feature
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result

## MODIFIED Requirements

### Requirement: Existing Feature
[Complete modified requirement]

## REMOVED Requirements

### Requirement: Old Feature
**Reason**: [Why removing]
**Migration**: [How to handle]
```

### tasks.md Template

```markdown
## 1. Implementation
- [ ] 1.1 Create database schema
- [ ] 1.2 Implement API endpoint
- [ ] 1.3 Add frontend component
- [ ] 1.4 Write tests
```

### design.md (When Needed)

Create if any apply:
- Cross-cutting change or new architectural pattern
- New external dependency or significant data model changes
- Security, performance, or migration complexity
- Ambiguity benefiting from technical decisions

```markdown
## Context
[Background, constraints, stakeholders]

## Goals / Non-Goals
- Goals: [...]
- Non-Goals: [...]

## Decisions
- Decision: [What and why]
- Alternatives considered: [Options + rationale]

## Risks / Trade-offs
- [Risk] → Mitigation

## Migration Plan
[Steps, rollback]

## Open Questions
- [...]
```

## Spec File Format

### Critical: Scenario Formatting

**CORRECT** (use #### headers):
```markdown
#### Scenario: User login success
- **WHEN** valid credentials provided
- **THEN** return JWT token
```

**WRONG:**
```markdown
- **Scenario: User login** ❌
  **Scenario**: User login ❌
### Scenario: User login ❌
```

Every requirement MUST have at least one scenario.

### Requirement Wording

Use SHALL/MUST for normative requirements.

### Delta Operations

- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes

#### ADDED vs MODIFIED

- **ADDED**: New capability that stands alone
- **MODIFIED**: Changes behavior of existing requirement. Always paste full updated requirement (header + scenarios)
- **RENAMED**: Only name changes. If also changing behavior, use RENAMED + MODIFIED

**Common pitfall:** Using MODIFIED without including previous text causes loss of detail at archive time.

**Authoring MODIFIED correctly:**
1. Locate existing requirement in `openspec/specs/<capability>/spec.md`
2. Copy entire requirement block
3. Paste under `## MODIFIED Requirements` and edit
4. Ensure header matches exactly, keep ≥1 scenario

## Troubleshooting

**"Change must have at least one delta"**
- Check `changes/[name]/specs/` exists with .md files
- Verify files have `## ADDED Requirements` etc.

**"Requirement must have at least one scenario"**
- Use `#### Scenario:` format (4 hashtags)
- Don't use bullets or bold for scenario headers

**Silent scenario parsing failures**
- Exact format: `#### Scenario: Name`
- Debug: `openspec show [change] --json --deltas-only`

## Happy Path Script

```bash
# 1) Explore current state
openspec spec list --long
openspec list

# 2) Scaffold
CHANGE=add-two-factor-auth
mkdir -p openspec/changes/$CHANGE/{specs/auth}
printf "## Why\n...\n\n## What Changes\n- ...\n\n## Impact\n- ...\n" > openspec/changes/$CHANGE/proposal.md
printf "## 1. Implementation\n- [ ] 1.1 ...\n" > openspec/changes/$CHANGE/tasks.md

# 3) Add deltas
cat > openspec/changes/$CHANGE/specs/auth/spec.md << 'EOF'
## ADDED Requirements
### Requirement: Two-Factor Authentication
Users MUST provide a second factor during login.

#### Scenario: OTP required
- **WHEN** valid credentials are provided
- **THEN** an OTP challenge is required
EOF

# 4) Validate
openspec validate $CHANGE --strict
```

## Best Practices

### Naming

**Capabilities:** verb-noun (`user-auth`, `payment-capture`), single purpose, split if needs "AND"

**Change IDs:** kebab-case, verb-led (`add-`, `update-`, `remove-`, `refactor-`), unique

### Simplicity First

- Default to <100 lines of new code
- Single-file implementations until proven insufficient
- Avoid frameworks without clear justification

### Clear References

- Use `file.ts:42` for code locations
- Reference specs as `specs/auth/spec.md`

## Quick Reference

**Stage Indicators:**
- `changes/` - Proposed, not yet built
- `specs/` - Built and deployed
- `archive/` - Completed changes

**File Purposes:**
- `proposal.md` - Why and what
- `tasks.md` - Implementation steps
- `design.md` - Technical decisions
- `spec.md` - Requirements and behavior

**CLI Essentials:**
```bash
openspec list              # What's in progress?
openspec show [item]       # View details
openspec validate --strict # Is it correct?
openspec archive <change-id> --yes  # Mark complete
```

Specs are truth. Changes are proposals. Keep them in sync.
