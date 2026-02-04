---
name: reverse-engineer
description: Deep codebase analysis to generate 9 comprehensive documentation files. Adapts based on path choice - Greenfield extracts business logic only (tech-agnostic), Brownfield extracts business logic + technical implementation (tech-prescriptive). This is Step 2 of 6 in the reverse engineering process.
---

# Reverse Engineer (Path-Aware)

**Step 2 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 30-45 minutes
**Prerequisites:** Step 1 completed (`analysis-report.md` and path selection)
**Output:** 9 comprehensive documentation files in `docs/reverse-engineering/`

**Path-Dependent Behavior:**
- **Greenfield:** Extract business logic only (framework-agnostic)
- **Brownfield:** Extract business logic + technical implementation details

**Note:** Output is the same regardless of implementation framework (Spec Kit or BMAD). The framework choice only affects what happens at Gear 6 (handoff).

---

## When to Use This Skill

Use this skill when:
- You've completed Step 1 (Initial Analysis) with path selection
- Ready to extract comprehensive documentation from code
- Path has been chosen (greenfield or brownfield)
- Preparing to create formal specifications

**Trigger Phrases:**
- "Reverse engineer the codebase"
- "Generate comprehensive documentation"
- "Extract business logic" (greenfield)
- "Document the full implementation" (brownfield)

---

## What This Skill Does

This skill performs deep codebase analysis and generates **9 comprehensive documentation files**.

**Content adapts based on your route (greenfield vs brownfield):**

### Path A: Greenfield (Business Logic Only)
- Focus on WHAT the system does
- Avoid framework/technology specifics
- Extract user stories, business rules, workflows
- Framework-agnostic functional requirements
- Can be implemented in any tech stack

### Path B: Brownfield (Business Logic + Technical)
- Focus on WHAT and HOW
- Document exact frameworks, libraries, versions
- Extract file paths, configurations, schemas
- Prescriptive technical requirements
- Enables `/speckit.analyze` validation

**9 Documentation Files Generated:**

1. **functional-specification.md** - Business logic, requirements, user stories (+ tech details for brownfield)
2. **integration-points.md** - External services, APIs, dependencies, data flows (single source of truth)
3. **configuration-reference.md** - Config options (business-level for greenfield, all details for brownfield)
4. **data-architecture.md** - Data models, API contracts (abstract for greenfield, schemas for brownfield)
5. **operations-guide.md** - Operational needs (requirements for greenfield, current setup for brownfield)
6. **technical-debt-analysis.md** - Issues and improvements
7. **observability-requirements.md** - Monitoring needs (goals for greenfield, current state for brownfield)
8. **visual-design-system.md** - UI/UX patterns (requirements for greenfield, implementation for brownfield)
9. **test-documentation.md** - Testing requirements (targets for greenfield, current state for brownfield)

---

## Configuration Check (FIRST STEP!)

**Load state file to check detection type and route:**

```bash
# Check what kind of application we're analyzing
DETECTION_TYPE=$(cat .stackshift-state.json | jq -r '.detection_type // .path')
echo "Detection: $DETECTION_TYPE"

# Check extraction approach
ROUTE=$(cat .stackshift-state.json | jq -r '.route // .path')
echo "Route: $ROUTE"

# Check spec output location (Greenfield only)
SPEC_OUTPUT=$(cat .stackshift-state.json | jq -r '.config.spec_output_location // "."')
echo "Writing specs to: $SPEC_OUTPUT"

# Create output directories if needed
if [ "$SPEC_OUTPUT" != "." ]; then
  mkdir -p "$SPEC_OUTPUT/docs/reverse-engineering"
  mkdir -p "$SPEC_OUTPUT/.specify/memory/specifications"
fi
```

**State file structure:**
```json
{
  "detection_type": "monorepo-service",  // What kind of app
  "route": "greenfield",                  // How to spec it
  "implementation_framework": "speckit",  // speckit or bmad (affects Gear 6 only)
  "config": {
    "spec_output_location": "~/git/my-new-app",
    "build_location": "~/git/my-new-app",
    "target_stack": "Next.js 15..."
  }
}
```

**Output structure (same for all frameworks):**
```
docs/reverse-engineering/
├── functional-specification.md
├── integration-points.md
├── configuration-reference.md
├── data-architecture.md
├── operations-guide.md
├── technical-debt-analysis.md
├── observability-requirements.md
├── visual-design-system.md
└── test-documentation.md
```

**Extraction approach based on detection + route:**

| Detection Type | + Greenfield | + Brownfield |
|----------------|--------------|--------------|
| **Monorepo Service** | Business logic only (tech-agnostic) | Full implementation + shared packages (tech-prescriptive) |
| **Nx App** | Business logic only (framework-agnostic) | Full Nx/Angular implementation details |
| **Generic App** | Business logic only | Full implementation |

**How it works:**
- `detection_type` determines WHAT patterns to look for (shared packages, Nx project config, monorepo structure, etc.)
- `route` determines HOW to document them (tech-agnostic vs tech-prescriptive)

**Examples:**
- Monorepo Service + Greenfield → Extract what the service does (not React/Express specifics)
- Monorepo Service + Brownfield → Extract full Express routes, React components, shared utilities
- Nx App + Greenfield → Extract business logic (not Angular specifics)
- Nx App + Brownfield → Extract full Nx configuration, Angular components, project graph

---

## Process Overview

### Phase 1: Deep Codebase Analysis

**Approach depends on path:**

Use the Task tool with `subagent_type=stackshift:code-analyzer` (or `Explore` as fallback) to analyze:

#### 1.1 Backend Analysis
- All API endpoints (method, path, auth, params, purpose)
- Data models (schemas, types, interfaces, fields)
- Configuration (env vars, config files, settings)
- External integrations (APIs, services, databases)
- Business logic (services, utilities, algorithms)

See [operations/backend-analysis.md](operations/backend-analysis.md)

#### 1.2 Frontend Analysis
- All pages/routes (path, purpose, auth requirement)
- Components catalog (layout, form, UI components)
- State management (store structure, global state)
- API client (how frontend calls backend)
- Styling (design system, themes, component styles)

See [operations/frontend-analysis.md](operations/frontend-analysis.md)

#### 1.3 Infrastructure Analysis
- Deployment (IaC tools, configuration)
- CI/CD (pipelines, workflows)
- Hosting (cloud provider, services)
- Database (type, schema, migrations)
- Storage (object storage, file systems)

See [operations/infrastructure-analysis.md](operations/infrastructure-analysis.md)

#### 1.4 Testing Analysis
- Test files (location, framework, coverage)
- Test types (unit, integration, E2E)
- Coverage estimates (% covered)
- Test data (mocks, fixtures, seeds)

See [operations/testing-analysis.md](operations/testing-analysis.md)

### Phase 2: Generate Documentation

Create `docs/reverse-engineering/` directory and generate all 8 documentation files.

See [operations/generate-docs.md](operations/generate-docs.md) for templates and guidelines.

---

## Output Files

All 9 documentation files are written to `docs/reverse-engineering/` regardless of implementation framework choice.

---

### 1. functional-specification.md
**Focus:** Business logic, WHAT the system does (not HOW)

**Sections:**
- Executive Summary (purpose, users, value)
- Functional Requirements (FR-001, FR-002, ...)
- User Stories (P0/P1/P2/P3 priorities)
- Non-Functional Requirements (NFR-001, ...)
- Business Rules (validation, authorization, workflows)
- System Boundaries (scope, integrations)
- Success Criteria (measurable outcomes)

**Critical:** Framework-agnostic, testable, measurable

### 2. configuration-reference.md
**Complete inventory** of all configuration:
- Environment variables
- Config file options
- Feature flags
- Secrets and credentials (how managed)
- Default values

### 3. data-architecture.md
**All data models and API contracts:**
- Data models (with field types, constraints, relationships)
- API endpoints (request/response formats)
- JSON Schemas
- GraphQL schemas (if applicable)
- Database ER diagram (textual)

### 4. operations-guide.md
**How to deploy and maintain:**
- Deployment procedures
- Infrastructure overview
- Monitoring and alerting
- Backup and recovery
- Troubleshooting runbooks

### 5. technical-debt-analysis.md
**Issues and improvements:**
- Code quality issues
- Missing tests
- Security vulnerabilities
- Performance bottlenecks
- Refactoring opportunities

### 6. observability-requirements.md
**Logging, monitoring, alerting:**
- What to log (events, errors, metrics)
- Monitoring requirements (uptime, latency, errors)
- Alerting rules and thresholds
- Debugging capabilities

### 7. visual-design-system.md
**UI/UX patterns:**
- Component library
- Design tokens (colors, typography, spacing)
- Responsive breakpoints
- Accessibility standards
- User flows

### 8. test-documentation.md
**Testing requirements:**
- Test strategy
- Coverage requirements
- Test patterns and conventions
- E2E scenarios
- Performance testing

---

## Success Criteria

- ✅ `docs/reverse-engineering/` directory created
- ✅ All 9 documentation files generated
- ✅ Comprehensive coverage of all application aspects
- ✅ Framework-agnostic functional specification (for greenfield)
- ✅ Complete data model documentation
- ✅ Ready to proceed to Step 3 (Create Specifications)

---

## Next Step

Once all documentation is generated and reviewed:

**For GitHub Spec Kit** (`implementation_framework: speckit`):
- Proceed to **Step 3: Create Specifications** - Use `/stackshift.create-specs` to transform docs into `.specify/` specs

**For BMAD Method** (`implementation_framework: bmad`):
- Proceed to **Step 6: Implementation** which will hand off to BMAD's `*workflow-init`
- BMAD's PM and Architect agents will use the reverse-engineering docs as rich context
- They will collaboratively create the PRD and architecture through conversation

---

## Important Guidelines

### Framework-Agnostic Documentation

**DO:**
- Describe WHAT, not HOW
- Focus on business logic and requirements
- Use generic terms (e.g., "HTTP API" not "Express routes")

**DON'T:**
- Hard-code framework names in functional specs
- Describe implementation details in requirements
- Mix business logic with technical implementation

### Completeness

Use the Explore agent to ensure you find:
- ALL API endpoints (not just the obvious ones)
- ALL data models (including DTOs, types, interfaces)
- ALL configuration options (check multiple files)
- ALL external integrations

### Quality Standards

Each document must be:
- **Comprehensive** - Nothing important missing
- **Accurate** - Reflects actual code, not assumptions
- **Organized** - Clear sections, easy to navigate
- **Actionable** - Can be used to rebuild the system

---

## Technical Notes

- Use Task tool with `subagent_type=stackshift:code-analyzer` for path-aware extraction
- Fallback to `subagent_type=Explore` if StackShift agent not available
- Parallel analysis: Run backend, frontend, infrastructure analysis concurrently
- Use multiple rounds of exploration for complex codebases
- Cross-reference findings across different parts of the codebase
- The `stackshift:code-analyzer` agent understands greenfield vs brownfield routes automatically

---

**Remember:** This is Step 2 of 6. The documentation you generate here will be transformed into formal specifications in Step 3.
