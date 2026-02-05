---
name: propose-feature-design
description: Create or update feature technical design document with architecture and implementation guidance
---

# Propose Feature Design Skill

## Purpose

Create a technical design document that guides implementation. This provides architecture, patterns, and design decisions without writing the actual code.

## When to Use

- Feature concept and requirements exist
- Ready to plan the implementation approach
- Need to document architecture and design patterns

## Prerequisites

- Feature concept exists in `docs/features/NNNN-feature-name/concept.md`
- Requirements exist in `docs/features/NNNN-feature-name/requirements.md`
- User understands the technical approach

## Procedure

### 1. Verify Prerequisites Exist

```bash
# Check that concept and requirements exist
ls ./docs/features/NNNN-feature-name/concept.md
ls ./docs/features/NNNN-feature-name/requirements.md
```

If either doesn't exist, complete those steps first.

### 2. Check for Idea Honing Document

```bash
ls ./planning/NNNN-feature-name/idea-honing.md 2>/dev/null
```

If it exists, review it for design insights and technical considerations discussed during idea honing.

### 3. Copy Design Template

```bash
cp ./docs/features/0000-templates/design.md ./docs/features/NNNN-feature-name/
```

### 4. Fill in Overview

Write a high-level description of the architecture and design approach. Reference the concept and requirements.

### 5. Identify Critical Constraints

For each key operation, ask:
- What would be a WRONG way to implement this?
- What performance characteristics are required?
- What invariants must hold?

Fill in the Critical Constraints table with:
- **ID**: CC-1, CC-2, etc.
- **Constraint**: What MUST be done a specific way
- **Rationale**: Why (performance, correctness, security)
- **Anti-pattern**: The wrong approach to reject in review

This is the most important section for preventing implementation mistakes.
Be specific—vague constraints don't help.

### 6. Define Architecture

Describe the overall structure:
- Component relationships
- Data flow
- Layer responsibilities
- Integration points

Use simple diagrams with ASCII art if helpful.

### 7. Define Domain Model

Specify the core types and operations:

**Types**
- Purpose and role
- Key properties
- Validation rules
- Relationships to other types

**Operations**
- Function signatures (conceptual)
- What they do
- Key behaviors
- Invariants (what must always be true)

### 8. Define Module Structure

Show how code should be organized:
- Directory structure
- Module responsibilities
- File organization
- Separation of concerns

**Module size limit**: This project enforces a 550-line limit per module (see `scripts/lint_loc.py`).
When designing modules, consider whether a component might exceed this limit.
If so, plan the internal decomposition upfront—split by capability (e.g., `builder.rs`, `searcher.rs`), not by artifact type.
The linter's output includes refactoring guidance if limits are exceeded.

**Keep impl blocks together**: All `impl` blocks for a type should live in one file.
Scattering impl blocks across files makes it hard for readers (and AI) to get a complete picture of what a type does.
If a type's implementation is too large, delegate to helper functions or internal component types rather than splitting the impl block itself.

```rust
// ✅ Good: single impl block delegates to helpers
impl KnowledgeIndex {
    pub fn build(&self, path: &Path) -> Result<()> {
        self.builder.build(path)  // delegates to internal component
    }
}

// ❌ Bad: impl blocks split across files
// facade/mod.rs: impl KnowledgeIndex { fn new() ... }
// facade/build.rs: impl KnowledgeIndex { fn build() ... }
// facade/search.rs: impl KnowledgeIndex { fn search() ... }
```

### 9. Document Design Patterns

Describe relevant patterns and why they apply:
- Which patterns to use
- How they fit the problem
- Implementation guidance

### 10. Document Design Decisions

For significant choices between alternatives, add entries to the Design Decisions section:
- What was decided
- What alternatives were considered
- Why this option was chosen
- What it implies for implementation

This creates a record that helps implementors understand the reasoning.

### 11. Add Implementation Guidance

Key considerations for implementors:
- Reference Critical Constraints by ID
- Performance considerations
- Testing approach
- Edge cases to handle

### 12. Keep Code Minimal

Remember:
- Use minimal illustrative code
- Focus on architecture and decisions
- Guide implementors, don't implement
- Reference requirements by ID when relevant

## Validation

Verify the design document:

```bash
# Check file exists
ls ./docs/features/NNNN-feature-name/design.md

# Verify it has content
head -50 ./docs/features/NNNN-feature-name/design.md
```

## Common Issues

**Too much code**: If there are large code blocks, remove them and focus on guidance.

**Too abstract**: If the design is vague, add concrete type names and module structure.

**Missing architecture**: Ensure the overall structure is clear before diving into details.

**Not referencing requirements**: Link design decisions back to specific requirement IDs.

## Next Steps

After creating the design:
1. Review with implementors for feasibility
2. Refine based on feedback
3. Once design is solid, create test plan using `propose-feature-test-plan` skill
4. Then create implementation plan using `propose-implementation-plan` skill
