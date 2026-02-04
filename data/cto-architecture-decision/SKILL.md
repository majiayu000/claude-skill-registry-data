---
name: cto-architecture-decision
description: Expert methodology for making and documenting critical architectural decisions using ADRs, trade-off analysis, migration planning, and technical debt management.
---

# CTO Architecture Decision Skill

## Purpose

This skill provides a systematic approach to making critical architectural and technology decisions. Use it to evaluate options, document decisions through Architecture Decision Records (ADRs), plan migrations, and manage technical debt strategically.

## When to Use

Trigger this skill when you need to:

- Make major technology decisions (database selection, framework choice, cloud provider)
- Document architectural decisions for team alignment
- Evaluate build vs buy options
- Plan technical migrations or refactoring
- Assess and prioritize technical debt
- Compare architecture patterns (monolith vs microservices, event-driven, etc.)
- Evaluate vendor or open-source solutions

## Core Methodology

Follow this systematic decision-making process:

### Phase 1: Frame the Decision

1. **Define the Problem**

   - What are we trying to achieve?
   - What constraints do we have? (timeline, budget, team skills, existing systems)
   - What's the cost of not deciding or deciding wrong?
   - Who are the stakeholders?

2. **Identify Options**

   - Brainstorm 3-5 potential solutions
   - Include "do nothing" as an option when appropriate
   - Consider hybrid approaches
   - Don't prematurely eliminate options

3. **Define Evaluation Criteria**
   - Use `references/frameworks/decision-criteria-framework.md` to select criteria
   - Common criteria: performance, scalability, cost, team expertise, time to implement, maintainability, security, vendor lock-in
   - Weight criteria by importance (not all criteria are equal)

### Phase 2: Evaluate Options

1. **Research Each Option**

   - Technical capabilities and limitations
   - Cost structure (initial + ongoing)
   - Learning curve and team fit
   - Community support and ecosystem
   - Long-term viability and roadmap

2. **Score Against Criteria**

   - Use quantitative scoring when possible (1-10 scale)
   - Document assumptions for each score
   - Consider risk factors and uncertainties
   - Use templates from `references/templates/trade-off-matrix.md`

3. **Identify Trade-offs**
   - What do you gain with each option?
   - What do you give up?
   - Are trade-offs acceptable given context?

### Phase 3: Make and Document Decision

1. **Make the Decision**

   - Review scores and trade-offs
   - Consider "reversibility" - can we change our mind later?
   - Validate with key stakeholders
   - Choose the option that best fits context

2. **Create Architecture Decision Record (ADR)**

   - Use template from `references/templates/adr-template.md`
   - Document: context, decision, consequences, alternatives considered
   - Include date, status (proposed/accepted/deprecated/superseded)
   - Store in version control for team access

3. **Create Implementation Plan**
   - Break decision into actionable steps
   - Identify risks and mitigation strategies
   - Define success criteria and rollback plan
   - Assign owners and timeline

## Key Principles

- **Context is King**: The right decision depends on your specific situation (team size, stage, constraints)
- **Document Why, Not Just What**: Future teams need to understand the reasoning
- **Embrace Reversibility**: Favor decisions that can be changed if needed
- **Quantify When Possible**: Use data and scoring over gut feelings
- **Consider Total Cost of Ownership**: Look beyond initial cost to maintenance, scaling, team time
- **Value Team Alignment**: A good decision with team buy-in beats a perfect decision with resistance

## Bundled Resources

**Frameworks** (`references/frameworks/`):

- `decision-criteria-framework.md` - Comprehensive evaluation criteria for different decision types
- `architecture-patterns.md` - Common patterns with pros/cons (microservices, event-driven, serverless, etc.)
- `technical-debt-assessment.md` - Framework for quantifying and prioritizing technical debt
- `migration-strategies.md` - Approaches for major migrations (strangler fig, big bang, phased)

**Templates** (`references/templates/`):

- `adr-template.md` - Standard Architecture Decision Record format
- `trade-off-matrix.md` - Structured comparison of options
- `migration-plan-template.md` - Step-by-step migration planning
- `build-vs-buy-analysis.md` - Framework for build vs buy decisions
- `rfc-template.md` - Request for Comments format for collaborative decision-making

**Examples** (`references/examples/`):

- Real-world ADRs for common decisions (database selection, microservices adoption, cloud provider)
- Migration plans from successful transformations
- Technical debt assessments with ROI calculations

## Usage Patterns

**Example 1**: User says "Should we move from PostgreSQL to MongoDB?"

→ Frame decision: What problem are we solving? Current pain points?
→ Define criteria: Query patterns, scalability needs, team expertise, migration cost
→ Score both options + alternatives (keep PostgreSQL but optimize, use both)
→ Create ADR documenting decision and trade-offs
→ If migrating, generate migration plan with risk mitigation

**Example 2**: User says "We need to evaluate our technical debt"

→ Load `references/frameworks/technical-debt-assessment.md`
→ Categorize debt: performance, security, maintainability, scalability
→ Score by impact (business risk) and effort (time/cost to fix)
→ Prioritize using impact/effort matrix
→ Create remediation roadmap with phased approach

**Example 3**: User says "Help us decide between building or buying a feature"

→ Use `references/templates/build-vs-buy-analysis.md`
→ Evaluate: development cost, time to market, ongoing maintenance, flexibility, vendor risk
→ Calculate Total Cost of Ownership for both options
→ Consider strategic fit and competitive advantage
→ Document decision in ADR format

**Example 4**: User says "We're considering microservices. Is it right for us?"

→ Load `references/frameworks/architecture-patterns.md`
→ Assess current context: team size, complexity, deployment frequency, organizational structure
→ Compare monolith vs microservices vs modular monolith
→ Identify trade-offs specific to the situation
→ Create ADR with recommendation and implementation roadmap if appropriate

## Decision Types Coverage

**Technology Selection**:

- Databases (SQL vs NoSQL, specific products)
- Programming languages and frameworks
- Cloud providers (AWS, GCP, Azure)
- Infrastructure tools (Kubernetes, serverless, VMs)
- Monitoring and observability tools

**Architecture Patterns**:

- Monolith vs microservices vs modular monolith
- Event-driven architecture
- Serverless architecture
- API design (REST, GraphQL, gRPC)
- Data architecture (centralized vs distributed)

**Migration Decisions**:

- Database migrations
- Cloud migrations (on-prem to cloud, cloud to cloud)
- Framework upgrades
- Architecture transformations

**Build vs Buy**:

- Feature development vs third-party solution
- Open source vs commercial tools
- In-house platform vs managed service

## Writing Style

All outputs should be:

- **Data-driven**: Use concrete scoring and comparisons
- **Balanced**: Present options fairly without bias
- **Actionable**: Provide clear recommendations with next steps
- **Contextual**: Adapt advice to company stage, team size, constraints
- **Future-aware**: Consider long-term implications and reversibility

---

**Version**: 1.0.0
**Author**: Rinaldo Festa
**Philosophy**: Make better technical decisions through systematic evaluation and clear documentation
