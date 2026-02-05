---
name: Repository Context Checker
description: Verify developers are working in the right repository type (brain vs code)
---

# Repository Context Checker

## Purpose

Prevent developers from starting planning work in code repositories by detecting context mismatches and providing guidance on where work should happen.

## Repository Type Detection

### Brain Repository Indicators

A repository is a **brain repo** if it exhibits these characteristics:

**Directory Structure**:
- Has `specs/` or `specs-in-progress/` directory
- Has `roadmap/` or `product-roadmap/` directory
- Has `patterns/` or `architecture/` directory
- Has `docs/` with coordination or strategy documents
- Filename patterns: `*.adr.md`, `*.spec.md`, `decision-*.md`

**Plugin Configuration** (from `.claude/settings.json`):
- 20+ plugins enabled
- Contains planning agents: `v-architect`, `v-tech-lead`, `v-commerce-pm`, `v-platform-pm`
- Contains `v-9d` or `v-discovery` workflows
- Contains multiple domain plugins (3+)
- Repository name contains: `-brain` suffix (e.g., `prism-brain`, `beam-brain`)

**README/CLAUDE.md Indicators**:
- Describes coordination, planning, or cross-functional work
- Mentions "spec", "architecture", "strategy", "roadmap"
- Links to other repositories

### Code Repository Indicators

A repository is a **code repo** if it exhibits these characteristics:

**Directory Structure**:
- Has `src/`, `lib/`, `main/`, `components/`, `app/` directory
- Has production code: `.ts`, `.tsx`, `.java`, `.py`, `.go` files
- Has deployment configs: `Dockerfile`, `k8s/`, `.github/workflows/`
- Has `tsconfig.json`, `package.json`, `pom.xml`, `setup.py`
- Filename patterns: service name (e.g., `BeamService`, `VioletDashboard`)

**Plugin Configuration** (from `.claude/settings.json`):
- 8-15 plugins enabled
- NO planning agents: `v-architect`, `v-tech-lead`, `v-*-pm` should not be present
- NO product workflows: `v-9d`, `v-discovery`, `v-gates`
- ONE stack plugin: `v-java-spring`, `v-typescript-react`, etc.
- ONE domain plugin: The service implements
- Repository name pattern: `{Name}Service` or `{Name}Dashboard`

**README/CLAUDE.md Indicators**:
- Describes implementation, testing, deployment
- Links to brain repo or product spec repo
- Has sections like "Setup", "Development", "Testing", "Deployment"

## Task Type Detection

### Planning Task Keywords

The following words and phrases indicate **planning work** (belongs in brain repo):

**Decision-making indicators**:
- "should we", "do we want", "trade-off", "pros and cons"
- "architecture", "design", "redesign"
- "strategic", "vision", "roadmap"
- "why are we", "why did we", "rationale for"

**Specification indicators**:
- "spec", "specification", "requirement"
- "ADR", "architecture decision record"
- "user story", "acceptance criteria"
- "what should", "what will"

**Product management indicators**:
- "feature request", "feature proposal"
- "customer request", "user feedback"
- "product manager input", "PM approval"
- "cross-product", "impact analysis"

**Approval/Review indicators**:
- "architect approval", "tech lead review"
- "design review", "architecture review"
- "should be approved by"

### Implementation Task Keywords

The following words and phrases indicate **implementation work** (can be in code repo):

**Code change indicators**:
- "implement", "add", "remove", "modify", "change"
- "bug fix", "fix the bug", "fix issue #"
- "refactor", "optimize", "clean up"
- "test", "add test", "test coverage"

**Reference indicators**:
- "from spec", "per ADR", "from requirements"
- "known root cause", "root cause: "
- "existing code", "existing function"

**Scope indicators**:
- "this function", "this service", "this component"
- "limited scope", "scoped change"
- "no architectural impact"

### Mixed Task Indicators

Some tasks require **both brain and code repos**:

**Investigation → Implementation pattern**:
- "why is X slow?" (brain: analysis) → "implement the optimization" (code: impl)
- "why is the API failing?" (brain: root cause) → "fix the bug" (code: impl)
- "can we do X?" (brain: feasibility) → "implement it" (code: impl)

**Decision → Implementation pattern**:
- "should we refactor Y?" (brain: decision) → "here's the refactored code" (code: impl)
- "architecture for X?" (brain: design) → "implement following the design" (code: impl)

## Warning Triggers

### Severity: HIGH (Strong Warning)

Warn when:
- In code repo + multiple planning keywords + no spec reference
- In code repo + asking "should we" or "why should we"
- In code repo + "redesign", "rewrite", "new feature" without existing spec
- In code repo + asking for architect or PM input
- Planning agents (v-architect, v-tech-lead) activated in code repo

### Severity: MEDIUM (Informational)

Inform when:
- In code repo + asking design questions with some spec reference
- In code repo + refactoring with architectural impact
- In brain repo + implementation-focused questions (can proceed but FYI)

### Severity: LOW (Suggestion)

Suggest when:
- Task could benefit from other repo context
- Related specs or decisions exist in brain repo

## Decision Logic

```
IF in_code_repo:
  IF task_type = "planning":
    IF has_spec_reference:
      severity = MEDIUM
    ELSE:
      severity = HIGH
  ELSE IF task_type = "implementation":
    severity = NONE
  ELSE IF task_type = "mixed":
    severity = MEDIUM (planning phase)
ELSE IF in_brain_repo:
  IF task_type = "implementation":
    severity = LOW (suggestion to move to code repo)
  ELSE:
    severity = NONE
ELSE:
  severity = UNKNOWN (ambiguous repo type)
```

## Action Recommendations

### Brain Repo → Code Repo Flow

When planning is complete, recommend:
1. Create specs in brain repo
2. Get architect/tech-lead approval in brain repo
3. Switch to code repo with approved spec
4. Reference spec or ADR in code repo work

### Code Repo → Brain Repo Flow

When planning is needed, recommend:
1. Switch to brain repo
2. Create specs/ADRs there
3. Get approvals there
4. Return to code repo when ready to implement

## Related Documentation

- `/v-plugins-context` command: Runs this detection and provides guidance
- `violet-ai-plugins/CLAUDE.md`: "Brain Repos vs Code Repos" section
- `examples/README.md`: Decision tree for choosing repository type
- `v-plugins/knowledge/plugin-management.md`: Plugin selection rules
