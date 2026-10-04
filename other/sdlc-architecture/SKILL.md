---
name: sdlc-architecture
description: Design architecture for a TriStar feature based on approved problem specification. Produces component design, data flows, API contracts, ADRs, and implementation guidelines without writing any code.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# SDLC Architecture Skill

## Prime Directive

**"Design everything. Code nothing."**

This skill produces architectural artifacts only. No source code, no pseudocode, no implementation. Output is a design specification that a developer can implement without ambiguity.

## Arguments

- `--feature=<name>` (required) - Feature name matching the problem_spec.md artifact

## Prerequisites

- `docs/artifacts/<feature>/problem_spec.md` must exist and be approved
- `docs/ARCHITECTURE.md` must be readable for baseline architecture context

## Architecture Baseline

TriStar uses a 3-layer architecture:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Designer (Layer 1) | React 19 + Next.js 15 (frontend), FastAPI + Claude API (backend) | Marketer copilot for OfferBrief generation |
| Hub (Layer 2) | FastAPI + Redis (prod) / in-memory dict (dev) | Shared state store, offer lifecycle management |
| Scout (Layer 3) | FastAPI + context signal APIs | Real-time activation engine, context scoring |

**Azure Cloud Stack:**
- Azure App Service (frontend hosting)
- Azure Functions (backend API)
- Azure Redis Cache (Hub state store, production)
- Azure SQL Database (audit trail, persistence)
- Azure Key Vault (secrets management)
- Azure CDN (static assets)

## Process

### Phase 1: Load Problem Specification

Read `docs/artifacts/<feature>/problem_spec.md`. Extract:
- All requirements (P0, P1, P2)
- Acceptance criteria
- Layers affected
- Non-goals and constraints
- Edge cases

### Phase 2: Codebase Analysis

Scan the existing codebase:
- Read `docs/ARCHITECTURE.md` for baseline architecture
- Check `src/` directory structure for existing components
- Read `.claude/rules/` for coding standards and patterns
- Identify existing components that can be reused or extended

### Phase 3: Document Current Architecture

Map the current state of the 3-layer system as it relates to this feature:
- Which existing components are relevant?
- What data currently flows between layers?
- What state transitions exist in Hub?
- What context signals does Scout currently process?

### Phase 4: Architecture Pattern Selection

For any new architectural pattern introduced, write an Architecture Decision Record (ADR):
- Pattern name and description
- At least 2 alternatives considered
- Decision rationale
- Consequences (positive and negative)

### Phase 5: Component Design

Define every new or modified component with:
- **COMP-ID**: Unique identifier (e.g., COMP-001)
- **Name**: Descriptive name
- **Path**: Exact file path in src/ structure
- **Layer**: Designer / Hub / Scout / Shared
- **Responsibility**: Single responsibility description
- **Dependencies**: Other components it depends on
- **Interface**: Public API (function signatures, props, endpoints)

### Phase 6: Data Flow Design

Map data flows for each user journey:
- Designer -> Hub flow (offer creation, approval)
- Hub -> Scout flow (offer activation)
- End-to-end flow (objective input to notification delivery)
- Error flows (what happens when each step fails)

### Phase 7: API Contract Design

For each new or modified API endpoint:
- HTTP method and path
- Request model (Pydantic v2 BaseModel)
- Response model (Pydantic v2 BaseModel)
- Status codes and error responses
- Authentication requirements
- Rate limiting configuration

### Phase 8: Data Model Design

For each new or modified data model:
- OfferBrief schema changes (if any)
- New Pydantic v2 models
- New Zod schemas (frontend validation)
- Hub state machine changes
- Database schema changes (if any)

### Phase 9: Architecture Decision Records (ADRs)

Write one ADR per significant decision. Each ADR must include:
- **Title**: ADR-NNN: Decision title
- **Status**: Proposed
- **Context**: Why this decision is needed
- **Alternatives**: At least 2 alternatives with pros/cons
- **Decision**: Which alternative was chosen
- **Consequences**: What this means for the system

### Phase 10: Implementation Guidelines

Reference the scoped rules for implementation standards:
- `.claude/rules/react-19-standards.md` for frontend patterns
- `.claude/rules/fastapi-standards.md` for backend patterns
- `.claude/rules/code-style.md` for naming and formatting
- `.claude/rules/testing.md` for test strategy
- `.claude/rules/security.md` for security requirements

## Quality Gates

Before saving the design spec, validate:

1. **Completeness**: Every requirement from problem_spec.md is addressed by at least one component
2. **Architecture Quality**: ADRs have 2+ alternatives, 3-layer separation maintained, no Designer->Scout bypass
3. **Backward Compatibility**: Breaking changes documented with blast radius estimate
4. **Hub State Integrity**: All state transitions validated, no orphan states possible
5. **Security**: PII handling addressed, OWASP mapped, Azure Key Vault for secrets
6. **Testing**: Coverage target set, test strategy for each layer defined
7. **OfferBrief Contract**: Shared type defined with both Zod and Pydantic schemas specified

## Output

Save to: `docs/artifacts/<feature>/design_spec.md`

## Refinement Mode

If `docs/artifacts/<feature>/design_review.md` exists, this is a refinement pass:

1. Read the design review findings
2. Address every Critical and Major finding
3. Document which findings were addressed and how
4. Re-validate against quality gates
5. Save updated design_spec.md with a "Refinement Log" section

## Reference Files

- `references/architecture-process.md` - Detailed 10-phase process
- `references/architecture-quality-gates.md` - Validation criteria
- `references/tristar-patterns.md` - TriStar-specific architectural patterns
