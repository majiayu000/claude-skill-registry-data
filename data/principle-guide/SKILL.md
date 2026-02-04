---
name: principle-guide
description: Guide decision-making using principles and trade-off analysis frameworks. Use when making technical decisions, evaluating alternatives, designing solutions, or choosing between options. Helps establish lasting principles.
allowed-tools: Read
model: inherit
---

# Principle-based Decision Making

Guide systematic decision-making and establish principles that automate future decisions.

## Core Philosophy: "Decide How to Decide"

Instead of making individual decisions repeatedly, establish **principles** that automate future decisions.

### The Problem

Your day is filled with decisions:
- Which technology to use?
- How to structure this code?
- What approach to take?

**But**: Most decisions you make shouldn't require your judgment every time.

### The Solution

**One principle can guide a thousand decisions.**

```
❌ Repeated Decision: "Should we use library X?"
   (Asked every time a new library is needed)

✅ Principle Established: "Use libraries with:
   - 1000+ GitHub stars
   - Active maintenance (commit in last 3 months)
   - Compatible license (MIT/Apache2)
   - Clear documentation"
   (Applies to all future library choices automatically)
```

### Leverage

| Short-term Decision | Long-term Principle |
|---------------------|---------------------|
| "What should this variable be named?" | "Naming convention: camelCase for variables, PascalCase for classes" |
| "What should this API return?" | "API design principle: Always return consistent format {data, error, meta}" |
| "How to refactor this code?" | "Refactoring principle: Refactor when complexity >10 or duplication >3" |

**One decision → Thousand judgments automated**

## When to Use This Skill

### Technical Decisions
- Choosing technologies (database, framework, library)
- Architectural patterns (monolith vs microservices)
- Infrastructure decisions (cloud provider, deployment strategy)
- Build vs buy decisions

### Design Decisions
- API design choices
- Data model design
- Performance vs maintainability trade-offs
- Flexibility vs simplicity trade-offs

### Process Decisions
- Development workflow
- Testing strategy
- Deployment process
- Code review standards

## Decision Process (6 Steps)

### Step 1: Define Decision Context

**Questions to answer**:
- What decision needs to be made?
- Why is this decision necessary?
- What constraints exist?
- Who is affected?
- What is the expected lifespan?

**Template**:
```markdown
## Decision Context

**Decision**: [What we need to decide]
**Why**: [Problem or opportunity]
**Constraints**:
- Budget: [amount]
- Timeline: [deadline]
- Resources: [team, skills]
- Compliance: [regulations]

**Stakeholders**: [who is affected]
**Lifespan**: [how long this matters]
```

### Step 2: Identify Alternatives

List all viable options (minimum 2, ideally 3-5):

```markdown
## Alternatives

1. **Option A**: [name and brief description]
2. **Option B**: [name and brief description]
3. **Option C**: [name and brief description]
4. **Status Quo**: [do nothing / keep current]
```

**Example**:
```
1. PostgreSQL (RDBMS with ACID)
2. MongoDB (Document store, flexible schema)
3. DynamoDB (Managed NoSQL, AWS-specific)
4. Status Quo (Current MySQL setup)
```

### Step 3: Define Evaluation Criteria

Common criteria:
- **Performance**: Latency, throughput, scalability
- **Maintainability**: Code clarity, team familiarity
- **Cost**: Initial + ongoing
- **Time to market**: Development + learning curve
- **Risk**: Technical debt, vendor lock-in
- **Flexibility**: Extensibility, customization

**Assign weights**: High (3), Medium (2), Low (1)

```markdown
## Evaluation Criteria

| Criterion | Weight | Why Important |
|-----------|--------|---------------|
| Performance | High | Customer SLA: <200ms response |
| Maintainability | High | Team of 5 must maintain |
| Cost | Medium | Budget: $5K/month |
| Time to market | High | 2-month deadline |
```

### Step 4: Score Each Alternative

Score 0-10 for each criterion with rationale.

```markdown
## Trade-off Analysis

| Criterion | Weight | PostgreSQL | MongoDB | DynamoDB |
|-----------|--------|-----------|---------|----------|
| Performance | High (3) | 8/10 | 6/10 | 9/10 |
| Maintainability | High (3) | 6/10 | 9/10 | 5/10 |
| Cost | Medium (2) | 7/10 | 5/10 | 6/10 |
| Time to market | High (3) | 8/10 | 7/10 | 9/10 |

**Weighted Scores**:
- PostgreSQL: (8×3 + 6×3 + 7×2 + 8×3) / (3+3+2+3) = 7.3
- MongoDB: (6×3 + 9×3 + 5×2 + 7×3) / 11 = 6.8
- DynamoDB: (9×3 + 5×3 + 6×2 + 9×3) / 11 = 7.5
```

### Step 5: Document Reasoning

For each score, explain why:

```markdown
## Detailed Evaluation

### PostgreSQL

**Performance: 8/10**
- Handles 10K writes/sec (requirement: 5K)
- P95 latency 50ms (requirement: <200ms)
- Proven at scale

**Maintainability: 6/10**
- Team has 3 years experience ✅
- Mature ecosystem ✅
- BUT: Complex replication setup
- BUT: Requires DBA expertise

**Cost: 7/10**
- RDS: $1200/mo + backups $300/mo = $1500/mo
- Over budget ($1000/mo) but justified by reliability

[Continue for all criteria...]
```

### Step 6: Make Recommendation

```markdown
## Recommendation

**Recommended**: PostgreSQL

**Rationale**:
1. Meets critical performance requirements with margin
2. Team familiarity reduces implementation risk
3. Cost overrun ($500/mo) justified by:
   - Reduced downtime risk (current: $5K/incident)
   - Faster development (saves 1 month = $50K labor)
4. ACID compliance critical for financial data

**Trade-offs Accepted**:
- Higher cost than alternatives
- More complex operations
- **Mitigation**: Train 2 team members on PostgreSQL

**Next Steps**:
1. Prototype with RDS PostgreSQL (1 week)
2. Load testing with production data
3. Team training on best practices
4. Final decision by [date]
```

## Establishing Principles

If this decision represents a broader pattern, establish a principle:

### Principle Template

```markdown
## Principle: [Short, Memorable Name]

**Context**: [When does this apply?]

**Statement**: [Clear, actionable principle]

**Rationale**: [Why this principle exists]

**Application**:
1. [How to apply in practice]
2. [Decision criteria]

**Examples**:

✅ **Good**: [Concrete example following principle]
❌ **Bad**: [Concrete example violating principle]

**Exceptions**: [When NOT to apply]

**Related Principles**: [Other relevant principles]
```

### Example Principle

```markdown
## Principle: Database Selection for OLTP

**Context**: Choosing database for transactional workloads with ACID requirements

**Statement**: Use PostgreSQL as default unless specific requirements dictate otherwise

**Rationale**:
- Team expertise (5 years experience)
- ACID compliance
- Proven at scale
- Rich ecosystem
- Avoid decision fatigue

**Application**:
1. Start with PostgreSQL
2. Switch only if:
   - Write throughput >50K/sec → Cassandra
   - Document-heavy, flexible schema → MongoDB
   - Time-series data → TimescaleDB
   - Simple key-value → Redis

**Examples**:

✅ **Good**: User service needs ACID + complex joins → PostgreSQL
❌ **Bad**: Analytics with time-series data → Should use TimescaleDB

**Exceptions**:
- Greenfield project with no ACID requirements
- Team has no PostgreSQL experience
- Graph queries needed → Neo4j

**Related Principles**:
- "Choose boring technology"
- "Optimize for team expertise"
```

## Built-in Decision Frameworks

See [FRAMEWORKS.md](FRAMEWORKS.md) for detailed templates.

### 1. Trade-off Analysis Framework

Systematically compare alternatives with weighted criteria.

### 2. Build vs Buy Framework

Decision tree for build vs buy decisions:
- Core competency check
- Solution availability check
- Cost-benefit analysis

### 3. Technology Adoption Framework

Evaluate new technologies:
- Maturity assessment (community, maintenance, stability)
- Risk assessment
- Adoption readiness

### 4. Performance vs Maintainability Framework

Guide for optimization decisions:
- When to optimize (user-facing, high-scale, revenue-critical)
- When to keep simple (internal, low-traffic, acceptable performance)

### 5. Risk Assessment Framework

Quantify and prioritize risks:
- Risk matrix (probability × impact)
- Mitigation plans
- Residual risk calculation

## Common Decision Patterns

### Pattern 1: Technology Choice

1. Check if principle exists
2. Apply principle criteria
3. Document exception if needed
4. Make decision
5. Record in ADR

### Pattern 2: Build vs Buy

1. Core competency check
2. Solution availability
3. Cost-benefit analysis (including opportunity cost)
4. Risk assessment
5. Decision + ADR

### Pattern 3: Performance Optimization

1. Measure current state
2. Identify bottleneck
3. Calculate impact vs effort
4. Decide: optimize now vs defer
5. If optimize, isolate complexity
6. Document rationale

## Integration with Other Skills

- **doc-templates**: Use ADR template to document decisions
- **document-quality**: Reviews decision documentation
- **tech-doc-reviewer**: Validates decision quality

After making a decision, document it:
```
Use doc-templates skill to create an ADR for this decision
```

## Example Scenarios

### Scenario 1: Database Choice

**User**: "I'm choosing between PostgreSQL and MongoDB for a new service"

**Skill response**:
```
Let's use the decision framework to guide this choice.

## Step 1: Decision Context
What are your requirements?
- ACID compliance needed?
- Query complexity (simple key-value vs complex joins)?
- Expected scale (reads/writes per second)?
- Team expertise?

## Step 2: Evaluation Criteria
Based on typical database decisions, key criteria:
- ACID compliance (if needed)
- Query capabilities
- Scale requirements
- Team expertise
- Operational complexity

[Guide through steps 3-6...]
```

### Scenario 2: Build Custom Auth vs Auth0

**User**: "Should we build custom authentication or use Auth0?"

**Skill response**:
```
This is a classic Build vs Buy decision. Let's apply the framework:

## Core Competency Check
- Is authentication your core business value? [ ] Yes [ ] No
- Does custom auth provide competitive advantage? [ ] Yes [ ] No
- Do you have deep security expertise in-house? [ ] Yes [ ] No

If mostly "No", lean toward Buy (Auth0).

## Available Solutions
| Solution | Pros | Cons | Cost |
|----------|------|------|------|
| Auth0 | Proven security, low maintenance | Vendor lock-in | $200/mo |
| AWS Cognito | AWS integration, cheap | Limited features | $50/mo |
| Build Custom | Full control | High maintenance, security risk | $50K initial + $10K/mo |

[Continue analysis...]

## Recommendation
**Buy** (Auth0) because:
- Not core competency (unless you're an auth company)
- Security-critical (don't build yourself)
- Cost justified by reduced risk
```

## Principles Library (Built-in)

Common principles for quick reference:

### Technical Principles

**Choose Boring Technology**
- Use proven, well-understood tech
- Innovation tokens: Spend wisely (max 3 per project)

**Optimize for Team Expertise**
- Choose what team knows unless compelling reason
- Consider hiring difficulty and learning curve

**Measure Before Optimizing**
- Profile first, optimize second
- Target P95/P99, not average

**Fail Fast, Fail Loudly**
- Explicit error handling
- No silent failures
- Log context, not just messages

### Process Principles

**Test First**
- Write failing test before implementation
- Refactor only when tests are green

**Review Everything**
- No code reaches production without review
- Review for clarity, not just correctness

**Automate Toil**
- If done >3 times, automate
- Invest 10% time in automation

### Architecture Principles

**Loose Coupling, High Cohesion**
- Minimize dependencies between modules
- Group related functionality

**Data at Rest, Logic in Code**
- Store data, not behavior
- Avoid storing derived values (unless caching)

**Explicit Over Implicit**
- Make dependencies obvious
- Configuration over convention (when clarity matters)

## Success Criteria

A well-guided decision includes:
- Clear context and constraints
- Multiple alternatives with trade-offs
- Explicit criteria and weights
- Scored comparison with rationale
- Recommendation with reasoning
- (Optional) Principle for future automation

## Next Steps

After making a decision:
1. Document in ADR using `doc-templates`
2. Establish principle if pattern emerges
3. Share with team for feedback
4. Review after 3-6 months
