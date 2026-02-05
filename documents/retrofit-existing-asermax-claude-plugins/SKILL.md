---
name: retrofit-existing
description: |
  Load when retrofitting framework documentation to existing code. Supports creating specs and decisions from implementations, enabling gradual framework adoption for existing projects.
---

# Retrofit Existing Skill

Create framework documentation from existing code.

## When to Load

Load this skill for:
- `/katachi:retrofit-spec <path>` - Create spec from existing code
- `/katachi:retrofit-design <ID>` - Create design from existing code (with integrated decision discovery)
- `/katachi:retrofit-decision <topic>` - Document existing decisions

## Philosophy

Most projects don't start with perfect planning. The framework should:
- Meet projects where they are
- Enable gradual documentation
- Preserve existing knowledge
- Not require starting over

## Retrofit Spec Workflow

### 1. Identify Target

User provides file or module path:
- Single file: `/path/to/module.py`
- Directory: `/path/to/module/`
- Module name: `authentication`

### 2. Dispatch Codebase Analyzer

```python
Task(
    subagent_type="katachi:codebase-analyzer",
    prompt=f"""
Analyze this code to create a feature specification.

## Analysis Type
spec

## Target
{file_path}

## Project Context
{vision_content if exists else "No VISION.md found"}

Infer requirements and create a draft spec document.
"""
)
```

### 3. Present Draft Spec

Show the inferred spec to user:
- Highlight assumptions made
- Note areas of uncertainty
- Ask: "What needs adjustment?"

### 4. Iterate

User provides corrections:
- Clarify user story
- Adjust acceptance criteria
- Add missing scenarios
- Correct misunderstandings

### 5. Assign Feature ID

Once spec is approved:
- Determine appropriate category
- Assign next available ID
- Ask user to confirm

### 6. Integrate into Framework

Add feature to FEATURES.md:

```bash
python scripts/features.py deps add-feature RETRO-001
```

Mark as already implemented:

```bash
python scripts/features.py status set RETRO-001 "✓ Implementation"
```

### 7. Update Dependencies

Ask about dependencies:
- "Does this feature depend on others?"
- "Do other features depend on this?"

Update matrix accordingly:

```bash
python scripts/features.py deps add-dep RETRO-001 CORE-001
```

### 8. Save Spec

Write spec to `specs/RETRO-001.md`

Note the retrofit source:

```markdown
## Status
Retrofit from existing code: `/path/to/original/code`
```

## Retrofit Decision Workflow

### 1. Identify Decision

User describes the pattern or choice:
- "We use JWT for authentication"
- "All services follow the repository pattern"
- "Errors are handled with custom exception types"

### 2. Dispatch Codebase Analyzer

```python
Task(
    subagent_type="katachi:codebase-analyzer",
    prompt=f"""
Analyze the codebase to document this decision.

## Analysis Type
decision

## Topic
{decision_description}

## Project Context
{vision_content if exists else "No VISION.md found"}

Infer the pattern/choice and create a draft ADR or DES document.
"""
)
```

### 3. Determine Document Type

Based on analysis, determine if this is:
- **ADR**: One-time architectural choice (technology, approach)
- **DES**: Repeatable pattern (how we do X)

Present recommendation to user with rationale.

### 4. Present Draft

Show the inferred ADR or DES:
- Context extracted from code
- Alternatives inferred (what wasn't chosen)
- Consequences observed

### 5. Iterate

User provides corrections:
- Clarify the context
- Add alternatives considered
- Correct consequences
- Add missing details

### 6. Assign ID

Determine next available ID:
- ADR: Check existing ADRs, assign next number
- DES: Check existing DES, assign next number

### 7. Update Index

Add to appropriate README:
- `docs/architecture/README.md` for ADR
- `docs/design/README.md` for DES

### 8. Save Document

Write to appropriate location:
- `docs/architecture/ADR-XXX-title.md`
- `docs/design/DES-XXX-title.md`

---

## Retrofit Design Workflow

Create design documentation from existing code with integrated decision discovery.

### 1. Verify Prerequisites

- Feature must have a retrofitted spec (`specs/FEATURE-ID.md`)
- Status should be "✓ Implementation" (code exists)

### 2. Dispatch Codebase Analyzer

```python
Task(
    subagent_type="katachi:codebase-analyzer",
    prompt=f"""
Analyze this code to create a design document.

## Analysis Type
design

## Retrofitted Spec
{spec_content}

## Implementation Code
{code_content}

## Project Context
{vision_content if exists else "No VISION.md found"}

Create a draft design document and identify undocumented decisions.
"""
)
```

### 3. Present Draft Design

Show the inferred design:
- Problem context extracted from code
- Design overview from architecture
- Modeling from code structure
- Data flow from execution paths
- Key decisions (flagged for ADR/DES)

### 4. Integrated Decision Discovery

For each flagged decision in Key Decisions:
- Present ADR/DES recommendation to user
- If user agrees, spawn retrofit-decision inline
- Capture the created ADR/DES reference
- Update design to reference new decisions

Example interaction:
```
"I identified these undocumented decisions:

1. **JWT for authentication** (architectural choice)
   Recommendation: Create ADR

2. **Repository pattern** (repeatable pattern)
   Recommendation: Create DES

Which should become formal documents?"
```

### 5. Iterate

User provides corrections:
- Clarify context
- Adjust modeling
- Add missing data flows
- Correct decision rationale

### 6. Validate

Dispatch `katachi:design-reviewer`:
- Review for completeness
- Check pattern alignment
- Identify missing elements

### 7. Save Design

Write to `designs/FEATURE-ID.md`
Include retrofit note with:
- Source code path (from spec)
- Decisions created during retrofit
- Assumptions made

---

## Migration Strategies

Detailed patterns for adopting the framework in existing projects.

### Strategy 1: Vision-First (Top-Down)

For projects with clear direction but undocumented:

1. Create VISION.md from existing understanding
2. Extract FEATURES.md from vision
3. Map existing code to features
4. Retrofit specs for implemented features
5. Mark implemented features as complete

### Strategy 2: Code-First (Bottom-Up)

For projects with existing code but unclear direction:

1. Retrofit specs for key modules (`/katachi:retrofit-spec`)
2. Retrofit designs with integrated decision discovery (`/katachi:retrofit-design`)
   - ADR/DES patterns are discovered and documented automatically during this step
3. Identify feature groupings
4. Create FEATURES.md from retrofitted specs
5. Synthesize VISION.md from features

**Note:** Steps 1 and 2 are done per-module. The retrofit-design command
chains naturally after retrofit-spec and handles decision discovery inline,
eliminating the need for a separate retrofit-decision pass for most decisions.

### Strategy 3: Hybrid

For projects with some documentation:

1. Inventory existing documentation
2. Gap analysis: what's missing?
3. Retrofit missing pieces
4. Integrate into framework structure

---

## Inventory First

Before retrofitting, take inventory:

### Documentation Inventory

| Document Type | Location | Status |
|--------------|----------|--------|
| README | /README.md | Exists, outdated |
| Architecture docs | /docs/arch/ | Partial |
| API documentation | /docs/api/ | Complete |
| Decision records | None | Missing |

### Code Inventory

| Module | Purpose | Tests | Documentation |
|--------|---------|-------|---------------|
| auth | Authentication | Yes | Partial |
| api | REST endpoints | Yes | OpenAPI |
| core | Business logic | Partial | None |
| db | Data layer | Yes | None |

---

## Migration Path: Small Project

For projects with < 20 modules:

### Week 1: Foundation
1. Create minimal VISION.md
2. Create FEATURES.md with top-level modules as features
3. Mark all as "✓ Implementation" (already built)

### Week 2: Critical Decisions
1. Identify 3-5 key architectural decisions
2. Retrofit ADRs for each
3. Create docs/architecture/ structure

### Week 3: Key Patterns
1. Identify 3-5 repeating patterns
2. Retrofit DES for each
3. Create docs/design/ structure

### Ongoing: Gradual Enhancement
1. Retrofit specs when touching modules
2. Add decisions when making changes
3. Document patterns as they emerge

---

## Migration Path: Large Project

For projects with 20+ modules:

### Phase 1: Skeleton (1-2 days)
1. Create VISION.md with high-level scope
2. Create FEATURES.md with module categories only
3. Create empty DEPENDENCIES.md structure
4. Create index files for docs/

### Phase 2: Critical Path (1 week)
1. Identify 5 most critical modules
2. Retrofit specs for critical modules
3. Retrofit decisions for core architecture
4. Map dependencies for critical path

### Phase 3: Expand (ongoing)
1. Add features as modules are touched
2. Retrofit specs before making changes
3. Document decisions when discovered
4. Build dependency matrix incrementally

---

## Handling Existing Documentation

### README.md

**Don't delete** - It serves different purpose.

**Extract to VISION.md:**
- Project description → Problem statement
- Goals → Core requirements
- Architecture overview → Reference to ADRs

**Keep in README:**
- Getting started
- Installation
- Quick usage examples

### Existing Decisions

If project has decision records:

1. **Compatible format**: Move to docs/architecture/ADR-XXX.md
2. **Different format**: Create ADR referencing original
3. **Scattered decisions**: Consolidate into ADRs

### API Documentation

Keep separate - different purpose:
- OpenAPI/Swagger → API reference
- Feature specs → Behavior requirements

Cross-reference:
```markdown
## Dependencies
- API: See OpenAPI spec at /docs/api/openapi.yaml
```

---

## Retrofit Templates

### Spec Retrofit Header

```markdown
# [Feature Name]

## Status
Retrofit from existing code: `path/to/module`
Date: YYYY-MM-DD

## User Story
[Inferred from code behavior]
```

### ADR Retrofit Header

```markdown
# ADR-XXX: [Title]

## Status
Retrofit from existing implementation
Date: YYYY-MM-DD

## Context
[Inferred from code patterns and comments]
```

---

## Common Challenges

### Challenge: No Clear Feature Boundaries

**Solution:**
- Start with directory structure as features
- Refine as understanding grows
- Don't try to be perfect initially

### Challenge: Undocumented Decisions

**Solution:**
- Interview team members
- Check git history for major changes
- Look for comments explaining "why"
- Mark assumptions clearly

### Challenge: Inconsistent Patterns

**Solution:**
- Document current state (not ideal state)
- Create DES with "current" and "recommended"
- Gradually migrate during regular work

### Challenge: Too Much to Document

**Solution:**
- Only retrofit what you touch
- Prioritize critical paths
- Accept partial coverage
- Document as you go

---

## Success Criteria

Framework adoption is successful when:

1. **New work follows framework** - Specs before code
2. **Changes update docs** - Existing docs stay current
3. **Decisions are captured** - New choices become ADRs
4. **Patterns are documented** - Repeated code becomes DES
5. **Team uses it** - Not just one person

---

## Anti-Patterns

### Documentation Sprint

**Don't:** Try to document everything at once
**Do:** Document incrementally with regular work

### Perfect History

**Don't:** Try to reconstruct all past decisions
**Do:** Document from now forward, retrofit as needed

### Forced Fit

**Don't:** Force existing code into rigid categories
**Do:** Adapt categories to fit the project

### Ceremony Overload

**Don't:** Require full spec/design/plan for bug fixes
**Do:** Scale documentation to task size
