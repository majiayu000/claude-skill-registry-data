---
name: wolf-principles
description: Wolf's 10 core principles for agent behavior and system design
version: 1.2.0
triggers:
  - "wolf principles"
  - "core principles"
  - "system guidelines"
  - "agent behavior"
  - "decision making"
---

# Wolf Principles Skill

This skill provides access to Wolf's 10 core principles that guide the design, implementation, and operation of the Wolf Agents multi-agent system. These principles have been refined over 50+ phases of real-world development.

## When to Use This Skill

- **ALWAYS** before making architectural decisions
- When justifying design choices or trade-offs
- During planning and implementation of new features
- When resolving conflicts between competing priorities
- For onboarding new team members or agents

## The 10 Core Principles

### 1. Artifact-First Development

**Principle**: All work produces durable, verifiable artifacts rather than ephemeral conversations.

**Implementation**:
- Pull Requests (PRs) are the primary unit of work and evidence
- Every change must be committed, reviewed, and merged
- Conversations and decisions are captured in issues, ADRs, and journals
- No work is considered complete without a merged artifact

**Example Application**:
```
Instead of: "I fixed the bug, it works now"
Do this: Create PR with fix, tests, and documentation of root cause
```

### 2. Role Isolation and Separation of Concerns

**Principle**: Each agent role has clearly defined responsibilities with minimal overlap and strict boundaries.

**Implementation**:
- Individual GitHub Apps per role with minimal required permissions
- Agents cannot merge their own implementations
- Clear ownership matrices and authority boundaries
- Role cards define exact scope, non-goals, and collaboration patterns

**Example Application**:
```
PM Agent: Defines requirements and acceptance criteria
Coder Agent: Implements solution meeting criteria
Reviewer Agent: Validates implementation quality
QA Agent: Verifies functionality and tests
```

### 3. Research-Before-Code

**Principle**: All implementation work must be preceded by structured research and evidence-based recommendations. This applies at **TWO levels**:
1. **Level 1 - Architectural Research** (research-agent, 2-8 hours): "Should we use this approach?"
2. **Level 2 - Documentation Lookup** (coder-agent, 2-5 minutes): "How do I use this library's current API?"

**Implementation**:

**Level 1 - Architectural Research:**
- Mandatory Research Agent analysis before any coding begins
- Structured research comments with evidence, findings, and advised solutions
- `research` label as a blocking gate for implementation
- Implementation must align with or justify deviations from research
- Time scale: 2-8 hours for feasibility, approach, and architecture decisions

**Level 2 - Documentation Lookup:**
- Use WebSearch/WebFetch for official API documentation before using libraries
- Verify syntax/patterns against authoritative sources (not model memory)
- Check for breaking changes, new features, and current best practices
- Look up version-specific documentation matching your project
- Time scale: 2-5 minutes per library (prevents "cold start" coding from memory)

**Why Two Levels:**
- **Level 1** addresses *unknown unknowns* (architectural risks, feasibility)
- **Level 2** addresses *known unknowns* (current API syntax, recent changes)
- Both prevent wasted implementation time from outdated assumptions

**Example Application**:
```
Task: Add authentication to API

Level 1 - Architectural Research (research-agent, 4 hours):
- Analyze existing auth patterns, security requirements, compliance needs
- Compare JWT vs OAuth2 vs Passport.js approaches
- Evaluate security implications, scalability, maintenance burden
- Deliver recommendation: "Use Passport.js with JWT strategy"
→ Output: ADR documenting decision and rationale

Level 2 - Documentation Lookup (coder-agent, 3 minutes):
- WebSearch "passport.js jwt strategy official documentation 2025"
- WebFetch https://www.passportjs.org/packages/passport-jwt/
- Verify: Current version is 4.0.1, check for breaking changes from 3.x
- Review: Example code for JWT verification and token extraction
→ Output: Implementation using current, verified API patterns

Result: Implementation informed by both architectural research (Level 1)
and current documentation (Level 2), avoiding both strategic and tactical errors.
```

### 4. Advisory-First Enforcement

**Principle**: New policies and constraints are tested in advisory mode before becoming hard gates.

**Implementation**:
- Shadow-mode validation for new rules and patterns
- Gradual rollout with confidence thresholds
- Evidence collection before enforcement
- Fallback and rollback mechanisms for all gates

**Example Application**:
```
New Rule: All PRs must have 90% test coverage
Phase 1: Report coverage but don't block (2 weeks)
Phase 2: Block if <70% coverage (2 weeks)
Phase 3: Enforce 90% threshold (ongoing)
```

### 5. Evidence-Based Decision Making

**Principle**: All decisions must be supported by concrete evidence and measurable outcomes.

**Implementation**:
- Performance budgets with measurement requirements
- Security scans and validation evidence
- Test coverage and quality metrics
- Documented trade-offs with quantified impacts

**Example Application**:
```
Decision: Choose between REST and GraphQL
Evidence Required:
- Latency benchmarks for typical queries
- Bundle size impact measurements
- Developer productivity metrics
- Maintenance cost analysis
```

### 6. Self-Improving Systems

**Principle**: The system continuously learns from its operations and evolves based on evidence.

**Implementation**:
- Comprehensive journaling of problems, decisions, and learnings
- Regular retrospectives and pattern identification
- Automated metrics collection and analysis
- Feedback loops from operations back to design

**Example Application**:
```
Problem: CI failures increasing
Journal: Document failure patterns
Analysis: Identify common root causes
Improvement: Add pre-commit checks for identified patterns
Measurement: Track CI failure rate reduction
```

### 7. Multi-Provider Resilience

**Principle**: The system must operate reliably across multiple AI providers with graceful fallback.

**Implementation**:
- Provider-agnostic interfaces and abstractions
- Automated failover between providers
- Rate limit awareness and throttling
- Provider-specific optimizations without vendor lock-in

**Example Application**:
```
Primary: OpenAI GPT-4 for complex reasoning
Fallback 1: Claude for continued operation
Fallback 2: Local models for basic functionality
Circuit Breaker: Automatic switching based on availability
```

### 8. GitHub-Native Integration

**Principle**: Leverage GitHub platform primitives to minimize custom infrastructure and operational overhead.

**Implementation**:
- GitHub Apps for authentication and authorization
- GitHub Actions for automation and workflows
- Issues and PRs for coordination and communication
- GitHub API for all programmatic interactions

**Example Application**:
```
Instead of: Custom task tracking system
Use: GitHub Issues with labels and milestones
Instead of: Custom CI/CD pipeline
Use: GitHub Actions with reusable workflows
```

### 9. Incremental Value Delivery

**Principle**: All work should be broken into small, independently valuable increments.

**Implementation**:
- Target 2-8 hour work increments for AI-accelerated development
- Each PR represents complete, testable functionality
- Continuous integration and deployment patterns
- Feature flags for gradual rollout

**Example Application**:
```
Feature: User Dashboard
Increment 1: Basic layout and navigation (2h)
Increment 2: User profile widget (3h)
Increment 3: Activity feed (4h)
Increment 4: Settings panel (2h)
Each increment is fully functional and deployable
```

### 10. Transparent Governance

**Principle**: All decisions, processes, and constraints must be openly documented and auditable.

**Implementation**:
- Public documentation of all policies and procedures
- Clear audit trails for all changes
- Role-based access controls with justification
- Regular governance reviews and updates

**Example Application**:
```
Decision: Change deployment frequency
Documentation: ADR with rationale
Audit Trail: Git history of decision
Review: Monthly governance meeting
Update: Adjust based on operational metrics
```

## How to Query Principles

You can ask about specific principles or search across all principles:

### Query by Number
"What is principle 5?" → Returns Evidence-Based Decision Making

### Query by Topic
"How does Wolf handle security?" → Returns relevant principles (2, 5, 7)

### Query by Implementation
"How to make decisions?" → Returns principles 3, 5, 6

### Get All Principles
"Show all principles" → Returns complete list with summaries

## Principle Conflicts Resolution

When principles appear to conflict, use this priority order:

1. **Security and Safety** (Principles 2, 7)
2. **Evidence and Quality** (Principles 3, 5, 6)
3. **Operational Efficiency** (Principles 1, 8, 9)
4. **Governance and Compliance** (Principles 4, 10)

## Integration with Other Skills

- **wolf-archetypes**: Principles inform archetype behavior
- **wolf-roles**: Each role implements relevant principles
- **wolf-governance**: Principles guide governance rules

## Scripts Available

- `query.js` - Search principles by ID, keyword, or topic
- `apply.js` - Generate principle-based recommendations for specific scenarios

## Evolution and Updates

These principles evolve based on operational evidence. Changes require:
1. Evidence collection showing insufficiency
2. Impact analysis on existing systems
3. Community review from all roles
4. Advisory-first deployment
5. Post-implementation assessment

## Red Flags - STOP

If you catch yourself thinking:

- ❌ **"This is too simple to need principles"** - Simple decisions cascade. Even trivial choices compound over time. Query principles BEFORE proceeding.
- ❌ **"I know the right approach already"** - Evidence before opinions (Principle 5). Your intuition needs validation against principles.
- ❌ **"Principles don't apply to this work type"** - ALL work has principles. Research? Use Principle 3. Bug fix? Use Principle 1. No exceptions.
- ❌ **"I'll check principles after implementation"** - Too late. Principles guide implementation, not justify it post-hoc.
- ❌ **"This conflicts with deadline pressure"** - Principles ENABLE speed by preventing rework. Skipping principles slows you down.
- ❌ **"I'm just prototyping"** - Prototypes become production (always). Use Principle 9 (incremental value) even for experiments.

**STOP. Use Skill tool to load wolf-principles BEFORE proceeding.**

## After Using This Skill

**REQUIRED NEXT STEPS:**

```
Sequential skill chain - DO NOT skip steps
```

1. **REQUIRED NEXT SKILL**: Use **wolf-archetypes** to determine behavioral archetype
   - **Why**: Principles are strategic guidance. Archetypes translate them into tactical requirements for your specific work type.
   - **Gate**: Cannot proceed to implementation without archetype selection
   - **Tool**: Use Skill tool to load wolf-archetypes

2. **REQUIRED NEXT SKILL**: Use **wolf-governance** to identify quality gates
   - **Why**: Archetypes define priorities. Governance defines acceptance criteria and Definition of Done.
   - **Gate**: Cannot claim work complete without meeting governance requirements
   - **Tool**: Use Skill tool to load wolf-governance

3. **REQUIRED NEXT SKILL**: Use **wolf-roles** to understand collaboration patterns
   - **Why**: Work rarely happens in isolation. Roles define who does what and how handoffs occur.
   - **Gate**: Cannot proceed without understanding role boundaries
   - **Tool**: Use Skill tool to load wolf-roles

**DO NOT PROCEED to implementation without completing steps 1-3.**

### Verification Checklist

Before claiming you've applied principles:

- [ ] Queried wolf-principles for relevant guidance
- [ ] Selected archetype using wolf-archetypes
- [ ] Identified quality gates using wolf-governance
- [ ] Loaded role guidance using wolf-roles
- [ ] Created artifact (PR, ADR, journal entry) documenting decisions

**Can't check all boxes? Work is incomplete. Return to this skill.**

---

*Source: docs/principles.md (lines 292-527)*
*Last Updated: 2025-11-14*
*Phase: Superpowers Skill-Chaining Enhancement v2.0.0*