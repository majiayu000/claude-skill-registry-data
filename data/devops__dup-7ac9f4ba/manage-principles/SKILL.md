---
name: manage-principles
description: Manage and update project Constitution. Use when (1) Constitution violation detected during implementation, (2) proposing new architectural principle, (3) templates need sync after Constitution update, (4) reviewing project architecture rules.
tools: [Read, Write, Edit]
location: project
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: manage-principles 호출 - {작업 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# manage-principles Skill

**Purpose**: Project Constitution management with violation detection and template synchronization

## When to Use

Agents should invoke this skill when:

- Constitution violation detected during implementation
- New development pattern needs to be codified
- Existing principle requires clarification or update
- Team standard conflicts with Constitution
- User explicitly requests Constitution changes

## Quick Start

### 1. Analyze Current State

```bash
# Read Constitution
cat .specify/memory/constitution.md
```

### 2. Detect Context Type

| Type | Description | Action |
|------|-------------|--------|
| **Violation** | Code conflicts with principle | Fix code OR amend |
| **Gap** | Pattern not covered | Draft new principle |
| **Clarification** | Principle ambiguous | Add clarifying language |
| **Update** | Principle needs refinement | Show before/after |

### 3. Propose & Apply

1. Generate proposal with rationale
2. Present for user approval
3. Update Constitution with version bump
4. Synchronize dependent templates
5. Validate consistency

## Usage Examples

```javascript
// Violation detected
skill: constitution({ type: "violation", principle: "VII", context: "RPC uses 'as unknown as Type'" });

// New pattern needs codification
skill: constitution({ type: "gap", proposal: "Add error boundary principle" });

// Clarification needed
skill: constitution({ type: "clarification", principle: "II", question: "SSR-First for admin panels?" });
```

## Principle Categories

| Category | Principles | Amendment |
|----------|------------|-----------|
| **NON-NEGOTIABLE** | I, II, III, VII, VIII | Requires strong rationale |
| **FLEXIBLE** | IV, V, VI, IX | Exceptions with justification |

## Dependencies

- `.specify/memory/constitution.md` - Primary source
- `.claude/commands/help.md` - User-facing guide
- `.claude/commands/speckit.*.md` - Template references

## Related Skills

- `verify` - Uses Constitution for validation
- `implement` - Follows Constitution principles
- `spec` - References Constitution in planning

## References

For detailed documentation, see:

- [Amendment Process](references/amendment-process.md) - 5-phase workflow, violation handling
- [Principles Guide](references/principles-guide.md) - Structure, categories, versioning
- [Output Format](references/output-format.md) - Report templates, examples, error handling
