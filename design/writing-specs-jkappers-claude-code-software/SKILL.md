---
name: writing-specs
description: Creates feature specifications capturing requirements and acceptance criteria. Use when writing specs, documenting features, or defining requirements.
---

# Spec Writing

Create specifications capturing WHAT and WHY. Do not include implementation details (those belong in technical-details.md).

## Required Sections

1. **Feature Overview** (2-3 paragraphs) - What it does, who uses it, what problem it solves

2. **Success Criteria** - Measurable outcomes defining "done"

3. **Design Goals** - Primary (must achieve) and secondary (nice to have)

4. **User Experience** (1-2 paragraphs) - How users interact, expected journey

5. **Design Rationale** (1-2 paragraphs) - Why this approach, key trade-offs

6. **Constraints and Assumptions** - Technical constraints, business assumptions

7. **Functional Requirements** (FR-N format) - Max 6-8 per spec, each specific and testable, with Given-When-Then acceptance criteria

8. **Edge Cases and Error Handling** - Unusual inputs, failure scenarios, expected behaviors

## Acceptance Criteria Format

```
- [ ] Given [context], when [action], then [expected result]
```

Include 2-4 criteria per requirement covering happy path and key failure cases.

## Exclusions

Do not include: architecture diagrams, code examples, database schemas, API signatures, development estimates, timeline references, or phase sections.

## Validation

Before completing:
- Single MVP focus (one deliverable)
- All requirements have testable criteria
- No TODO/TBD placeholders
- Edge cases documented

## Scope Check

If more than 6-8 requirements, the feature is too large. Identify 3-4 core requirements and flag the rest for a separate spec. Document in a "Scope Notes" section.

## Directory Structure

```
specs/
├── YYYY-MM-DD-feature-name/
│   ├── README.md              # Spec (WHAT and WHY)
│   └── technical-details.md   # Implementation (HOW)
└── historical/
```

## Templates

- `templates/spec-readme.md` - New spec template
- `references/spec-guide.md` - Guidelines and examples
