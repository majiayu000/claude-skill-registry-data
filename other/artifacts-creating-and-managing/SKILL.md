---
name: artifacts-creating-and-managing
description: |
  Creates and manages project artifacts (research, spikes, analysis, plans) using templated scripts.
  Use when asked to "create an ADR", "research topic", "spike investigation", "implementation plan", or "create analysis".
  Provides standardized structure, naming conventions, and helper scripts for artifact organization.
allowed-tools: Read, Write, Bash, Glob, Edit
---

# Artifacts: Creating and Managing

## Quick Start

**Create an ADR:**
```bash
python .claude/skills/artifacts-creating-and-managing/scripts/create_adr.py \
  --title "Use Event Sourcing" \
  --status proposed \
  --context "Need audit trail for compliance"
```

**Create a Research Topic:**
```bash
python .claude/skills/artifacts-creating-and-managing/scripts/create_research_topic.py \
  --topic "GraphQL vs REST" \
  --objective "Choose API architecture" \
  --questions "Performance?" "Tooling?"
```

**Create an Implementation Plan:**
```bash
python .claude/skills/artifacts-creating-and-managing/scripts/create_implementation_plan.py \
  --feature "User Auth" \
  --overview "Add OAuth2 support" \
  --steps "Configure provider" "Implement tokens" "Add tests"
```

## Purpose

Standardizes how artifacts are created and organized within `.claude/artifacts/` directory. Artifacts are temporary work products that support development but don't belong in version control or permanent documentation.

## When to Use Artifacts

**Use artifacts when:**
- Conducting research ("research GraphQL libraries")
- Creating spikes ("spike on authentication approaches")
- Writing analysis ("analyze performance bottlenecks")
- Documenting decisions (ADRs)
- Planning implementations
- Capturing session notes
- Recording investigation results

**Don't use artifacts for:**
- Permanent documentation (use `docs/` instead)
- Source code (use `src/` instead)
- Tests (use `tests/` instead)
- Configuration (use config files)

## Directory Structure

```
.claude/artifacts/
├── YYYY-MM-DD/                    # Date-based organization
│   ├── research/                  # Research topics
│   │   └── topic-name.md
│   ├── spikes/                    # Technical spikes
│   │   └── spike-name.md
│   ├── analysis/                  # Code/architecture analysis
│   │   └── analysis-name.md
│   ├── plans/                     # Implementation plans
│   │   └── plan-name.md
│   ├── sessions/                  # Session notes
│   │   └── session-name.md
│   └── adr/                       # Architecture Decision Records
│       └── NNN-decision-name.md
└── completed/                     # Archived artifacts
    └── adr/
        └── NNN-decision-name.md
```

## File Naming Conventions

**Research topics:**
```
.claude/artifacts/YYYY-MM-DD/research/topic-name.md
Example: .claude/artifacts/2025-12-24/research/graphql-libraries.md
```

**Spikes:**
```
.claude/artifacts/YYYY-MM-DD/spikes/spike-name.md
Example: .claude/artifacts/2025-12-24/spikes/oauth2-integration.md
```

**Analysis:**
```
.claude/artifacts/YYYY-MM-DD/analysis/analysis-name.md
Example: .claude/artifacts/2025-12-24/analysis/performance-bottlenecks.md
```

**Implementation plans:**
```
.claude/artifacts/YYYY-MM-DD/plans/feature-name-plan.md
Example: .claude/artifacts/2025-12-24/plans/user-authentication-plan.md
```

**ADRs:**
```
.claude/artifacts/YYYY-MM-DD/adr/NNN-decision-title.md
Example: .claude/artifacts/2025-12-24/adr/001-use-event-sourcing.md
```

## Core Rules

1. **Date-based organization** - All artifacts under `YYYY-MM-DD/` directory
2. **Kebab-case names** - Use hyphens, lowercase, no spaces
3. **Category folders** - research/, spikes/, analysis/, plans/, adr/
4. **Markdown format** - All artifacts are .md files
5. **Templated creation** - Use helper scripts for consistency
6. **Completion tracking** - Move to `completed/` when done

## Category Definitions

### Research
**Purpose:** Investigate libraries, tools, or approaches

**Template:**
```markdown
# Research: [Topic]

## Objective
[What you're researching and why]

## Questions
1. [Question 1]
2. [Question 2]

## Findings
[Research results]

## Recommendation
[Conclusion]
```

**Example usage:** "Research GraphQL client libraries for React"

### Spikes
**Purpose:** Time-boxed technical investigation

**Template:**
```markdown
# Spike: [Investigation]

## Goal
[What you're trying to prove/learn]

## Approach
[How you'll investigate]

## Results
[What you discovered]

## Decision
[Next steps based on results]
```

**Example usage:** "Spike on OAuth2 integration with existing auth system"

### Analysis
**Purpose:** Investigate existing code/architecture

**Template:**
```markdown
# Analysis: [Subject]

## Scope
[What's being analyzed]

## Findings
[Issues/observations]

## Recommendations
[Proposed changes]
```

**Example usage:** "Analyze performance bottlenecks in API handlers"

### Plans
**Purpose:** Document implementation approach

**Template:**
```markdown
# Implementation Plan: [Feature]

## Overview
[Feature description]

## Steps
1. [Step 1]
2. [Step 2]

## Testing Strategy
[How to verify]

## Risks
[Potential issues]
```

**Example usage:** "Plan implementation of two-factor authentication"

### ADRs (Architecture Decision Records)
**Purpose:** Document architectural decisions

**Template:**
```markdown
# ADR NNN: [Decision Title]

## Status
[proposed | accepted | deprecated | superseded]

## Context
[Why this decision is needed]

## Decision
[What we decided]

## Consequences
[Positive and negative outcomes]
```

**Example usage:** "ADR 001: Use Event Sourcing for Audit Trail"

## Helper Scripts

All scripts located in `.claude/skills/artifacts-creating-and-managing/scripts/`:

### create_adr.py
```bash
python create_adr.py \
  --title "Use PostgreSQL" \
  --status proposed \
  --context "Need relational database for complex queries"
```

**Required:** --title, --status, --context
**Optional:** --decision, --consequences

### create_research_topic.py
```bash
python create_research_topic.py \
  --topic "GraphQL vs REST" \
  --objective "Choose API architecture" \
  --questions "Performance?" "Developer experience?"
```

**Required:** --topic, --objective
**Optional:** --questions (multiple)

### create_spike.py
```bash
python create_spike.py \
  --name "OAuth Integration" \
  --goal "Prove OAuth2 works with current system" \
  --timebox "4 hours"
```

**Required:** --name, --goal
**Optional:** --timebox, --approach

### create_analysis.py
```bash
python create_analysis.py \
  --subject "API Performance" \
  --scope "Handler response times"
```

**Required:** --subject
**Optional:** --scope

### create_implementation_plan.py
```bash
python create_implementation_plan.py \
  --feature "2FA Authentication" \
  --overview "Add two-factor auth using TOTP" \
  --steps "Add TOTP library" "Create setup flow" "Add verification"
```

**Required:** --feature, --overview
**Optional:** --steps (multiple), --risks

## Integration Pattern

**Typical workflow:**

1. **Create artifact:**
   ```bash
   python scripts/create_research_topic.py --topic "Caching Strategies"
   ```

2. **Work on artifact:**
   - Add findings, analysis, or decisions
   - Reference code, documentation, or other artifacts
   - Update as investigation progresses

3. **Complete artifact:**
   - Mark as complete (status: accepted/completed)
   - Move to `completed/` if ADR
   - Reference in code or documentation
   - Archive or delete if temporary

4. **Cross-reference:**
   - Link from code comments: `// See: .claude/artifacts/2025-12-24/research/caching.md`
   - Link from documentation: `docs/` references artifacts
   - Link between artifacts: Related ADRs reference each other

## Examples

### Example 1: Research Library

**User:** "Research libraries for state management in React"

**Workflow:**
```bash
# 1. Create research artifact
python create_research_topic.py \
  --topic "React State Management Libraries" \
  --objective "Choose state library for new features" \
  --questions "Performance?" "Learning curve?" "TypeScript support?"

# 2. Conduct research (add to artifact)
# - Compare Redux, Zustand, Jotai, Recoil
# - Test performance benchmarks
# - Review documentation quality

# 3. Document findings in artifact
# 4. Make recommendation
```

**Output:** `.claude/artifacts/2025-12-24/research/react-state-management.md`

### Example 2: Create ADR for Technology Choice

**User:** "Document decision to use PostgreSQL"

**Workflow:**
```bash
# 1. Create ADR
python create_adr.py \
  --title "Use PostgreSQL for Primary Database" \
  --status proposed \
  --context "Need relational database with JSONB support"

# 2. Add decision details to artifact
# 3. Document consequences
# 4. Change status to accepted
# 5. Move to completed/adr/ when implemented
```

**Output:** `.claude/artifacts/2025-12-24/adr/001-use-postgresql.md`

### Example 3: Implementation Plan

**User:** "Plan implementation of user authentication"

**Workflow:**
```bash
# 1. Create plan
python create_implementation_plan.py \
  --feature "User Authentication" \
  --overview "Add OAuth2 and JWT-based auth" \
  --steps "Add auth library" "Create login flow" "Add JWT middleware" "Write tests"

# 2. Add testing strategy
# 3. Document risks
# 4. Use plan to guide implementation
```

**Output:** `.claude/artifacts/2025-12-24/plans/user-authentication-plan.md`

## Expected Outcomes

### Successful Artifact Creation

```
✅ Artifact Created

Type: Research Topic
Path: .claude/artifacts/2025-12-24/research/graphql-libraries.md
Status: In Progress

Next Steps:
1. Add research findings
2. Document recommendations
3. Reference in implementation plan
```

### Completed Artifact

```
✅ Artifact Completed

Type: ADR
Path: .claude/artifacts/completed/adr/001-use-postgresql.md
Status: Accepted
Date: 2025-12-24

Outcome:
- Decision documented
- Rationale captured
- Consequences listed
- Referenced in: src/database/README.md
```

## Supporting Files

- **[templates/](templates/)** - Markdown templates:
  - adr-template.md
  - research-template.md
  - spike-template.md
  - analysis-template.md
  - plan-template.md

- **[scripts/](scripts/)** - Helper scripts:
  - create_adr.py
  - create_research_topic.py
  - create_spike.py
  - create_analysis.py
  - create_implementation_plan.py
  - list_artifacts.py (find all artifacts)
  - archive_artifact.py (move to completed/)

## Best Practices

1. **Use templates** - Scripts ensure consistency
2. **Date organization** - Easy to find recent artifacts
3. **Descriptive names** - Clear purpose from filename
4. **Complete artifacts** - Don't leave them half-finished
5. **Cross-reference** - Link artifacts to code/docs
6. **Archive when done** - Move completed ADRs to `completed/`
7. **Delete temporary artifacts** - Don't accumulate unnecessary files
8. **Update status** - Keep artifact status current

## Red Flags to Avoid

1. **Creating artifacts in wrong location** - Always use `.claude/artifacts/`
2. **Skipping date folder** - All artifacts under `YYYY-MM-DD/`
3. **Mixed case names** - Use kebab-case consistently
4. **No category folder** - Put in research/, spikes/, etc.
5. **Creating without template** - Use helper scripts
6. **Leaving artifacts incomplete** - Finish or delete
7. **Not archiving ADRs** - Move completed ADRs to `completed/`
8. **Creating permanent docs as artifacts** - Use `docs/` for permanent documentation

---

**Key principle:** Artifacts are temporary work products with standardized structure. They support development but aren't permanent documentation.

**Remember:** Use helper scripts for consistency, organize by date, and archive/delete when complete.
