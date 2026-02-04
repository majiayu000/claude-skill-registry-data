---
name: synthesize-plan
description: Synthesize stakeholder requirements into unified implementation plan
allowed-tools: Bash, Read, Write, Edit
---

# Synthesize Plan Skill

**Purpose**: Read all stakeholder requirement reports (architect, tester, formatter) and synthesize them into a unified implementation plan in task.md.

**Performance**: Reduces synthesis errors, ensures all stakeholder concerns addressed

## When to Use This Skill

### ✅ Use synthesize-plan When:

- All 3 requirement reports completed (architect, tester, formatter)
- Ready to transition from REQUIREMENTS to SYNTHESIS phase
- Need to create unified implementation plan
- Want to ensure all stakeholder input incorporated

### ❌ Do NOT Use When:

- Requirement reports not yet complete
- Still in REQUIREMENTS phase (agents still working)
- Plan already exists in task.md
- Task not yet in CLASSIFIED/REQUIREMENTS state

## What This Skill Does

### 1. Validates Requirements Complete

```bash
# Checks all 3 reports exist:
- /workspace/tasks/{task}/{task}-architect-requirements.md
- /workspace/tasks/{task}/{task}-tester-requirements.md
- /workspace/tasks/{task}/{task}-formatter-requirements.md
```

### 2. Reads All Reports

```bash
# Reads and parses each report:
- Extract key architectural decisions
- Extract testing requirements
- Extract documentation/style requirements
```

### 3. Identifies Conflicts/Overlaps

```bash
# Analyzes for:
- Conflicting approaches (e.g., architect wants X, tester needs Y)
- Duplicate work (e.g., both mention same feature)
- Missing coverage (e.g., no one addressed edge case)
```

### 4. Creates Unified Plan

**CRITICAL**: Plan MUST follow Purpose → Approach → Benefits structure for user approval.

```markdown
# Implementation Plan

## Problem Statement (MANDATORY)
[2-3 sentences: What problem does this solve? Why does this task exist?]
[Users cannot evaluate a plan without understanding the problem]

## Proposed Solution (MANDATORY)
[2-3 sentences: High-level approach to solving the problem]

## Benefits (MANDATORY)
- [Concrete outcome 1]
- [Concrete outcome 2]
- [How this improves the codebase]

## Architecture
[Key decisions from architect]

## Testing Strategy
[Requirements from tester]

## Documentation & Style
[Requirements from formatter]

## Implementation Approach
[Synthesized approach addressing all concerns]

## Agents to Invoke
- architect: [specific responsibilities]
- tester: [specific responsibilities]
- formatter: [specific responsibilities]
```

### 5. Writes to task.md

```bash
# Appends plan to existing task.md
# Preserves requirements section, adds implementation plan
```

### 6. Transitions State

```bash
# Updates task.json to SYNTHESIS state
jq '.state = "SYNTHESIS" | .phase = "synthesis"' task.json > tmp.json
mv tmp.json task.json
```

## Usage

### Basic Synthesis

```bash
# After all requirement reports complete
TASK_NAME="implement-formatter-api"

/workspace/main/.claude/scripts/synthesize-plan.sh \
  --task "$TASK_NAME"
```

### With Conflict Resolution

```bash
# If conflicts detected, skill prompts for resolution
TASK_NAME="implement-formatter-api"

/workspace/main/.claude/scripts/synthesize-plan.sh \
  --task "$TASK_NAME" \
  --interactive true
```

## Synthesis Process

### Phase 1: Extract Key Points

**From Architect Report**:
- Design patterns recommended
- Module structure
- API design
- Integration points
- Dependencies

**From Tester Report**:
- Test coverage needs
- Edge cases
- Test strategy (unit/integration)
- Business logic validation
- Test data requirements

**From Formatter Report**:
- JavaDoc requirements
- Code style standards
- Naming conventions
- File organization
- Documentation structure

### Phase 2: Identify Issues

**Conflicts**:
```markdown
Example: Architect recommends singleton pattern, but tester says
it makes testing difficult. Resolution: Use dependency injection.
```

**Overlaps**:
```markdown
Example: Both architect and tester mention validation logic.
Consolidate: Architect designs validation API, tester tests it.
```

**Gaps**:
```markdown
Example: No one addressed error handling for edge case X.
Add: Include error handling requirements in plan.
```

### Phase 3: Create Implementation Plan

```markdown
## Implementation Plan

### Phase 1: Core Architecture (architect)
- Implement FormattingRule interface
- Create RuleEngine class
- Set up dependency injection

### Phase 2: Testing Infrastructure (tester)
- Create test fixtures
- Implement unit tests for FormattingRule
- Add integration tests for RuleEngine

### Phase 3: Documentation & Style (formatter)
- Add JavaDoc to all public APIs
- Document usage examples
- Ensure Checkstyle compliance

### Integration Points
- RuleEngine integrates with existing Formatter
- Test coverage target: 90%
- All code follows style-guide.md standards

### Known Issues/Decisions
- Using DI instead of singleton (improves testability)
- Error handling: Validation exceptions throw checked exceptions
```

## Workflow Integration

### Complete Synthesis Workflow

```markdown
REQUIREMENTS phase: All agents complete
  ↓
[verify-requirements-complete skill]
  ↓
All 3 reports validated
  ↓
[synthesize-plan skill] ← THIS SKILL
  ↓
Read all reports
  ↓
Identify conflicts/overlaps/gaps
  ↓
Create unified plan
  ↓
Write to task.md
  ↓
Transition to SYNTHESIS state
  ↓
[checkpoint-approval skill: Plan approval]
```

## Output Format

Script returns JSON:

```json
{
  "status": "success",
  "message": "Implementation plan synthesized successfully",
  "task_name": "implement-formatter-api",
  "reports_read": [
    "implement-formatter-api-architect-requirements.md",
    "implement-formatter-api-tester-requirements.md",
    "implement-formatter-api-formatter-requirements.md"
  ],
  "conflicts_found": 1,
  "conflicts_resolved": 1,
  "plan_sections": [
    "Problem Statement",
    "Proposed Solution",
    "Benefits",
    "Architecture",
    "Testing Strategy",
    "Documentation & Style",
    "Implementation Approach"
  ],
  "plan_file": "/workspace/tasks/implement-formatter-api/task.md",
  "new_state": "SYNTHESIS",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Conflict Resolution Strategies

### Strategy 1: Architect Wins on Design

```markdown
Conflict: Architect recommends approach A, tester prefers B
Resolution: Use A (architect's domain), ensure B's concerns addressed via tests
```

### Strategy 2: Tester Wins on Testability

```markdown
Conflict: Design choice makes testing hard
Resolution: Modify design to improve testability (tester's concern valid)
```

### Strategy 3: Formatter Enforces Standards

```markdown
Conflict: Architect's design violates style standards
Resolution: Adjust design to comply with standards (non-negotiable)
```

### Strategy 4: Escalate to User

```markdown
Conflict: Genuinely equal merit approaches
Resolution: Use AskUserQuestion to get user decision
```

## Safety Features

### Precondition Validation

- ✅ Verifies all 3 reports exist
- ✅ Checks reports non-empty
- ✅ Validates task in correct state
- ✅ Confirms task.md exists

### Synthesis Validation

- ✅ Ensures all reports read successfully
- ✅ Validates plan covers all stakeholder concerns
- ✅ Checks for unresolved conflicts
- ✅ Confirms plan written to task.md

### Error Handling

On any error:
- Reports which validation failed
- Lists missing/invalid reports
- Returns JSON with error details
- Does not transition state

## Common Synthesis Patterns

### Pattern 1: Clean Synthesis (No Conflicts)

```markdown
All stakeholders aligned:
- Architect designs API
- Tester tests API
- Formatter documents API

Plan: Sequential implementation (architect → tester → formatter)
```

### Pattern 2: Testability Adjustments

```markdown
Conflict: Architect's initial design hard to test
Resolution: Add interfaces for dependency injection
Impact: Slightly more complex, but fully testable
```

### Pattern 3: Performance vs Maintainability

```markdown
Conflict: Architect wants optimization, tester wants simple code
Resolution: Start simple (tester), profile, optimize if needed
Rationale: Premature optimization avoided
```

## Related Skills

- **verify-requirements-complete**: Validates reports before synthesis
- **checkpoint-approval**: Presents synthesized plan for approval
- **gather-requirements**: Creates reports that this skill synthesizes

## Troubleshooting

### Error: "Report missing"

```bash
# Check which reports exist
ls -la /workspace/tasks/{task}/*-requirements.md

# If missing, re-invoke corresponding agent:
# - architect-requirements.md missing → re-invoke architect
# - tester-requirements.md missing → re-invoke tester
# - formatter-requirements.md missing → re-invoke formatter
```

### Error: "Unresolved conflicts"

```bash
# Review conflict details in output
# Options:
1. Manual resolution: Edit one report to align
2. User decision: Ask user to choose approach
3. Compromise: Find middle ground that satisfies both

# After resolution, retry synthesis
```

### Error: "Plan section empty"

```bash
# One stakeholder didn't provide enough detail
# Options:
1. Re-invoke agent with more specific prompt
2. Fill in gaps based on general knowledge
3. Ask user for guidance on missing section
```

### Plan Quality Issues

```bash
# Plan exists but lacks detail or clarity
# Improve by:
1. Re-reading reports for missed details
2. Adding specific implementation steps
3. Clarifying agent responsibilities
4. Adding integration points
5. Documenting known issues/decisions
```

## Implementation Notes

The synthesize-plan script performs:

1. **Validation Phase**
   - Check task exists
   - Verify task in CLASSIFIED/REQUIREMENTS state
   - Confirm all 3 reports exist
   - Validate reports non-empty

2. **Reading Phase**
   - Read architect report
   - Read tester report
   - Read formatter report
   - Extract key points from each

3. **Analysis Phase**
   - Identify conflicts between reports
   - Find overlapping concerns
   - Detect gaps in coverage
   - Note dependencies between work

4. **Resolution Phase**
   - Apply resolution strategies
   - Escalate unresolvable conflicts
   - Document decisions made
   - Ensure all concerns addressed

5. **Writing Phase**
   - Format unified plan
   - Write to task.md (append after requirements)
   - Include all required sections
   - Document agent responsibilities

6. **Transition Phase**
   - Update task.json to SYNTHESIS state
   - Record synthesis timestamp
   - Log conflicts resolved

7. **Verification Phase**
   - Confirm plan written
   - Validate plan structure
   - Check state updated
   - Return success status
