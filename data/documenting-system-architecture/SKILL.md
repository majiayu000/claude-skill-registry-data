---
name: documenting-system-architecture
description: Synthesize subsystem catalogs and architecture diagrams into comprehensive, navigable architecture reports - codifies synthesis strategies and professional documentation patterns
---

# Documenting System Architecture

## Purpose

Synthesize subsystem catalogs and architecture diagrams into final, stakeholder-ready architecture reports that serve multiple audiences through clear structure, comprehensive navigation, and actionable findings.

## When to Use

- Coordinator delegates final report generation from validated artifacts
- Have `02-subsystem-catalog.md` and `03-diagrams.md` as inputs
- Task specifies writing to `04-final-report.md`
- Need to produce executive-readable architecture documentation
- Output represents deliverable for stakeholders

## Core Principle: Synthesis Over Concatenation

**Good reports synthesize information into insights. Poor reports concatenate source documents.**

Your goal: Create a coherent narrative with extracted patterns, concerns, and recommendations - not a copy-paste of inputs.

## Document Structure

### Required Sections

**1. Front Matter**
- Document title
- Version number
- Analysis date
- Classification (if needed)

**2. Table of Contents**
- Multi-level hierarchy (H2, H3, H4)
- Anchor links to all major sections
- Quick navigation for readers

**3. Executive Summary (2-3 paragraphs)**
- High-level system overview
- Key architectural patterns
- Major concerns and confidence assessment
- Should be readable standalone by leadership

**4. System Overview**
- Purpose and scope
- Technology stack
- System context (external dependencies)

**5. Architecture Diagrams**
- Embed all diagrams from `03-diagrams.md`
- Add contextual analysis after each diagram
- Cross-reference to subsystem catalog

**6. Subsystem Catalog**
- One detailed entry per subsystem
- Synthesize from `02-subsystem-catalog.md` (don't just copy)
- Add cross-references to diagrams and findings

**7. Key Findings**
- **Architectural Patterns**: Identified across subsystems
- **Technical Concerns**: Extracted from catalog concerns
- **Recommendations**: Actionable next steps with priorities

**8. Appendices**
- **Methodology**: How analysis was performed
- **Confidence Levels**: Rationale for confidence ratings
- **Assumptions & Limitations**: What you inferred, what's missing

## Synthesis Strategies

### Pattern Identification

**Look across subsystems for recurring patterns:**

From catalog observations:
- Subsystem A: "Dependency injection for testability"
- Subsystem B: "All external services injected"
- Subsystem C: "Injected dependencies for testing"

**Synthesize into pattern:**
```markdown
### Dependency Injection Pattern

**Observed in**: Authentication Service, API Gateway, User Service

**Description**: External dependencies are injected rather than directly instantiated, enabling test isolation and loose coupling.

**Benefits**:
- Testability: Mock dependencies in unit tests
- Flexibility: Swap implementations without code changes
- Loose coupling: Services depend on interfaces, not concrete implementations

**Trade-offs**:
- Initial complexity: Requires dependency wiring infrastructure
- Runtime overhead: Minimal (dependency resolution at startup)
```

### Concern Extraction

**Find concerns buried in catalog entries:**

Catalog entries:
- API Gateway: "Rate limiter uses in-memory storage (doesn't scale horizontally)"
- Database Layer: "Connection pool max size hardcoded (should be configurable)"
- Data Service: "Large analytics queries can cause database load spikes"

**Synthesize into findings:**
```markdown
## Technical Concerns

### 1. Rate Limiter Scalability Issue

**Severity**: Medium
**Affected Subsystem**: [API Gateway](#api-gateway)

**Issue**: In-memory rate limiting prevents horizontal scaling. If multiple gateway instances run, each maintains separate counters, allowing clients to exceed intended limits by distributing requests across instances.

**Impact**:
- Cannot scale gateway horizontally without distributed rate limiting
- Potential for rate limit bypass under load balancing
- Inconsistent rate limit enforcement

**Remediation**:
1. **Immediate** (next sprint): Document limitation, add monitoring alerts
2. **Short-term** (next quarter): Migrate to Redis-backed rate limiter
3. **Validation**: Test rate limiting with multiple gateway instances

**Priority**: High (blocks horizontal scaling)
```

### Recommendation Prioritization

Group recommendations by timeline:

```markdown
## Recommendations

### Immediate (Next Sprint)
1. **Document rate limiter limitation** in operations runbook
2. **Add monitoring** for database connection pool exhaustion
3. **Configure alerting** on Data Service query execution times > 5s

### Short-Term (Next Quarter)
4. **Migrate rate limiter** to Redis-backed distributed implementation
5. **Externalize database pool configuration** to environment variables
6. **Implement query throttling** in Data Service analytics engine

### Long-Term (6 Months)
7. **Architecture review** for caching strategy optimization
8. **Evaluate** circuit breaker effectiveness under load testing
```

## Cross-Referencing Strategy

### Bidirectional Links

**Subsystem → Diagram:**
```markdown
## Authentication Service

[...subsystem details...]

**Component Architecture**: See [Authentication Service Components](#auth-service-components) diagram

**Dependencies**: [API Gateway](#api-gateway), [Database Layer](#database-layer)
```

**Diagram → Subsystem:**
```markdown
### Authentication Service Components

[...diagram...]

**Description**: This component diagram shows internal structure of the Authentication Service. For additional operational details, see [Authentication Service](#authentication-service) in the subsystem catalog.
```

**Finding → Subsystem:**
```markdown
### Rate Limiter Scalability Issue

**Affected Subsystem**: [API Gateway](#api-gateway)

[...concern details...]
```

### Navigation Patterns

**Table of contents with anchor links:**
```markdown
## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
   - [Purpose and Scope](#purpose-and-scope)
   - [Technology Stack](#technology-stack)
3. [Architecture Diagrams](#architecture-diagrams)
   - [Level 1: Context](#level-1-context)
   - [Level 2: Container](#level-2-container)
```

## Multi-Audience Considerations

### Executive Audience

**What they need:**
- Executive summary ONLY (should be self-contained)
- High-level patterns and risks
- Business impact of concerns
- Clear recommendations with timelines

**Document design:**
- Put executive summary first
- Make it readable standalone (no forward references)
- Focus on "why this matters" over "how it works"

### Architect Audience

**What they need:**
- System overview + architecture diagrams + key findings
- Pattern analysis with trade-offs
- Dependency relationships
- Design decisions and rationale

**Document design:**
- System overview explains context
- Diagrams show structure at multiple levels
- Findings synthesize patterns and concerns
- Cross-references enable non-linear reading

### Engineer Audience

**What they need:**
- Subsystem catalog with technical details
- Component diagrams showing internal structure
- Technology stack specifics
- File references and entry points

**Document design:**
- Detailed subsystem catalog
- Component-level diagrams
- Technology stack section with versions/frameworks
- Code/file references where available

### Operations Audience

**What they need:**
- Technical concerns with remediation
- Dependency mapping
- Confidence levels (what's validated vs assumed)
- Recommendations with priorities

**Document design:**
- Technical concerns section up front
- Clear remediation steps
- Appendix with assumptions/limitations
- Prioritized recommendations

## Optional Enhancements

### Visual Aids

**Subsystem Quick Reference Table:**
```markdown
## Appendix D: Subsystem Quick Reference

| Subsystem | Location | Confidence | Key Concerns | Dependencies |
|-----------|----------|------------|--------------|--------------|
| API Gateway | /src/gateway/ | High | Rate limiter scalability | Auth, User, Data, Logging |
| Auth Service | /src/services/auth/ | High | None | Database, Cache, Logging |
| User Service | /src/services/users/ | High | None | Database, Cache, Notification |
```

**Pattern Summary Matrix:**
```markdown
## Architectural Patterns Summary

| Pattern | Subsystems Using | Benefits | Trade-offs |
|---------|------------------|----------|------------|
| Dependency Injection | Auth, Gateway, User | Testability, flexibility | Initial complexity |
| Repository Pattern | User, Data | Data access abstraction | Extra layer |
| Circuit Breaker | Gateway | Fault isolation | False positives |
```

### Reading Guide

```markdown
## How to Read This Document

**For Executives** (5 minutes):
- Read [Executive Summary](#executive-summary) only
- Optionally skim [Recommendations](#recommendations)

**For Architects** (30 minutes):
- Read [Executive Summary](#executive-summary)
- Read [System Overview](#system-overview)
- Review [Architecture Diagrams](#architecture-diagrams)
- Read [Key Findings](#key-findings)

**For Engineers** (1 hour):
- Read [System Overview](#system-overview)
- Study [Architecture Diagrams](#architecture-diagrams) (all levels)
- Read [Subsystem Catalog](#subsystem-catalog) for relevant services
- Review [Technical Concerns](#technical-concerns)

**For Operations** (45 minutes):
- Read [Executive Summary](#executive-summary)
- Study [Technical Concerns](#technical-concerns)
- Review [Recommendations](#recommendations)
- Read [Appendix C: Assumptions and Limitations](#appendix-c-assumptions-and-limitations)
```

### Glossary

```markdown
## Appendix E: Glossary

**Circuit Breaker**: Fault tolerance pattern that prevents cascading failures by temporarily blocking requests to failing services.

**Dependency Injection**: Design pattern where dependencies are provided to components rather than constructed internally, enabling testability and loose coupling.

**Repository Pattern**: Data access abstraction that separates business logic from data persistence concerns.

**Optimistic Locking**: Concurrency control technique assuming conflicts are rare, using version checks rather than locks.
```

## Success Criteria

**You succeeded when:**
- Executive summary (2-3 paragraphs) distills key information
- Table of contents provides multi-level navigation
- Cross-references (30+) enable non-linear reading
- Patterns synthesized (not just listed from catalog)
- Concerns extracted and prioritized
- Recommendations actionable with timelines
- Diagrams integrated with contextual analysis
- Appendices document methodology, confidence, assumptions
- Professional structure (document metadata, clear hierarchy)
- Written to 04-final-report.md

**You failed when:**
- Simple concatenation of source documents
- No executive summary or it requires reading full document
- Missing table of contents
- No cross-references between sections
- Patterns just copied from catalog (not synthesized)
- Concerns buried without extraction
- Recommendations vague or unprioritized
- Diagrams pasted without context
- Missing appendices

## Best Practices from Baseline Testing

### What Works

✅ **Comprehensive synthesis** - Identify patterns, extract concerns, create narrative
✅ **Professional structure** - Document metadata, TOC, clear hierarchy, appendices
✅ **Multi-level navigation** - 20+ TOC entries, 40+ cross-references
✅ **Executive summary** - Self-contained 2-3 paragraph distillation
✅ **Actionable findings** - Concerns with severity/impact/remediation, recommendations with timelines
✅ **Transparency** - Confidence levels, assumptions, limitations documented
✅ **Diagram integration** - Embedded with contextual analysis and cross-refs
✅ **Multi-audience** - Executive summary + technical depth + appendices

### Synthesis Patterns

**Pattern identification:**
- Look across multiple subsystems for recurring themes
- Group by pattern name (e.g., "Repository Pattern")
- Document which subsystems use it
- Explain benefits and trade-offs

**Concern extraction:**
- Find concerns in subsystem catalog entries
- Elevate to Key Findings section
- Add severity, impact, remediation
- Prioritize by timeline (immediate/short/long)

**Recommendation structure:**
- Group by timeline
- Specific actions (not vague suggestions)
- Validation steps
- Priority indicators

## Integration with Workflow

This skill is typically invoked as:

1. **Coordinator** completes and validates subsystem catalog
2. **Coordinator** completes and validates architecture diagrams
3. **Coordinator** writes task specification for final report
4. **YOU** read both source documents systematically
5. **YOU** synthesize patterns, extract concerns, create recommendations
6. **YOU** build professional report structure with navigation
7. **YOU** write to 04-final-report.md
8. **Validator** (optional) checks for synthesis quality, navigation, completeness

**Your role:** Transform analysis artifacts into stakeholder-ready documentation through synthesis, organization, and professional presentation.
