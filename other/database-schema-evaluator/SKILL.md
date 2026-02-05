---
name: database-schema-evaluator
description: >
  Expert evaluation of database schema designs using multi-perspective analysis.
  PROACTIVELY activate for: (1) Reviewing database schema designs, (2) Comparing 
  alternative schema approaches, (3) Identifying normalization issues, (4) Assessing 
  scalability and performance implications, (5) Evaluating data integrity constraints,
  (6) Analyzing schema evolution capabilities.
  
  Triggers: "evaluate database schema", "review db design", "assess data model",
  "compare schema approaches", "check normalization", "database design review",
  "analyze table structure", "review ER diagram", "evaluate data architecture"
---

# Database Schema Evaluator

Comprehensive evaluation of database schema designs using expert panel analysis from multiple technical perspectives.

## When to Use

### Ideal Use Cases
- Reviewing schema designs before production deployment
- Comparing multiple schema approaches for a new system
- Assessing existing schema for refactoring needs
- Evaluating schema scalability for growth
- Identifying potential performance bottlenecks
- Checking compliance with normalization principles
- Reviewing data integrity and constraint design

### Anti-Patterns
- Trivial single-table designs
- Schema with no business context provided
- Purely academic exercises without real requirements
- Schemas already in production with extensive data

## Workflow

### Phase 1: Schema Analysis & Context Gathering

**Purpose:** Understand the schema structure, business requirements, and evaluation scope.

**Actions:**
1. Parse schema definition (DDL, ER diagram, or description)
2. Identify key entities, relationships, and constraints
3. Document business requirements and use cases
4. Note expected data volumes and access patterns
5. Identify specific evaluation concerns if provided

**Output Template:**
```yaml
schema_context:
  entities: [list of main tables/collections]
  relationships: [1:1, 1:N, N:M relationships]
  constraints: [PKs, FKs, unique, check constraints]
  indexes: [existing or proposed indexes]
  business_domain: [domain context]
  scale_expectations:
    initial_volume: [expected records]
    growth_rate: [expected growth]
    read_write_ratio: [expected ratio]
  specific_concerns: [any highlighted areas]
```

### Phase 2: Expert Panel Assembly

**Purpose:** Instantiate domain experts with relevant database perspectives.

**Expert Personas:**

1. **Data Architect**
   - Focus: Overall design patterns, normalization, data modeling best practices
   - Expertise: ER modeling, normalization forms (1NF-5NF, BCNF), denormalization tradeoffs
   - Evaluates: Structural integrity, design patterns, anti-patterns

2. **Performance Engineer**
   - Focus: Query optimization, indexing strategy, scalability
   - Expertise: Query execution plans, index design, partitioning, sharding
   - Evaluates: Access patterns, join complexity, index coverage, bottlenecks

3. **Data Integrity Guardian**
   - Focus: Constraints, validation rules, referential integrity
   - Expertise: ACID properties, constraint design, cascade rules, data quality
   - Evaluates: Constraint completeness, orphan prevention, data consistency

4. **Evolution Strategist**
   - Focus: Schema migration, backward compatibility, extensibility
   - Expertise: Schema versioning, migration patterns, API stability
   - Evaluates: Change flexibility, migration complexity, future-proofing

5. **Operations Specialist**
   - Focus: Backup/recovery, maintenance, monitoring
   - Expertise: Backup strategies, maintenance windows, operational complexity
   - Evaluates: Operational overhead, recovery scenarios, maintenance burden

### Phase 3: Multi-Lens Evaluation

**Purpose:** Each expert evaluates the schema from their specialized perspective.

**Evaluation Framework:**

```yaml
expert_evaluation:
  expert: [Expert Name]
  perspective: [Their focus area]
  
  strengths:
    - [Specific strength with rationale]
    - [Another strength with example]
  
  concerns:
    - issue: [Specific concern]
      severity: [critical|high|medium|low]
      rationale: [Why this matters]
      recommendation: [How to address]
  
  opportunities:
    - [Improvement opportunity]
    - [Optimization suggestion]
  
  risk_assessment:
    - risk: [Potential future problem]
      likelihood: [high|medium|low]
      impact: [high|medium|low]
      mitigation: [Suggested approach]
  
  score: [0-10 from this perspective]
  confidence: [0-1 confidence in assessment]
```

**Evaluation Criteria by Expert:**

| Expert | Primary Criteria | Secondary Criteria |
|--------|-----------------|-------------------|
| Data Architect | Normalization level, Design patterns | Naming conventions, Documentation |
| Performance Engineer | Index efficiency, Query complexity | Join paths, Denormalization benefits |
| Data Integrity Guardian | Constraint coverage, Referential integrity | Validation rules, Orphan prevention |
| Evolution Strategist | Migration simplicity, Extensibility | Backward compatibility, Version strategy |
| Operations Specialist | Backup feasibility, Maintenance overhead | Monitoring capability, Recovery time |

### Phase 4: Cross-Expert Deliberation

**Purpose:** Synthesize perspectives and identify consensus/conflicts.

**Deliberation Process:**
1. Identify areas of expert agreement (reinforced findings)
2. Surface conflicting assessments (tradeoff points)
3. Evaluate interdependencies between concerns
4. Prioritize issues based on business context
5. Generate unified recommendations

**Conflict Resolution Matrix:**
```yaml
conflicts:
  - conflict: [Description of disagreement]
    expert_1: [Position and rationale]
    expert_2: [Alternative position]
    resolution: [Recommended approach considering tradeoffs]
    business_impact: [What this means for the system]
```

### Phase 5: Comprehensive Scoring

**Purpose:** Generate quantitative assessment across dimensions.

**Scoring Dimensions:**

| Dimension | Weight | Factors |
|-----------|--------|---------|
| Correctness | 25% | Normalization, integrity, consistency |
| Performance | 20% | Query efficiency, scalability potential |
| Maintainability | 20% | Clarity, documentation, operational simplicity |
| Flexibility | 15% | Extensibility, migration paths |
| Robustness | 10% | Error handling, constraint coverage |
| Security | 10% | Access control, audit capability |

**Scoring Algorithm:**
```
dimension_score = Σ(expert_score × expert_weight) / Σ(expert_weights)
overall_score = Σ(dimension_score × dimension_weight)
confidence = min(expert_confidences) × consensus_factor
```

### Phase 6: Final Report Generation

**Purpose:** Deliver actionable evaluation with clear recommendations.

## Output Format

```markdown
# Database Schema Evaluation Report

## Executive Summary
- **Overall Score:** [X/10]
- **Confidence:** [X%]
- **Recommendation:** [APPROVE|APPROVE_WITH_CONDITIONS|REVISE|REJECT]
- **Key Strengths:** [Top 3 strengths]
- **Critical Issues:** [Top 3 concerns if any]

## Schema Overview
[Brief description of schema purpose and structure]

## Expert Evaluations

### Data Architecture Assessment
[Data Architect findings]
- **Score:** X/10
- **Key Findings:** [Bullets]

### Performance Analysis
[Performance Engineer findings]
- **Score:** X/10
- **Key Findings:** [Bullets]

### Data Integrity Review
[Data Integrity Guardian findings]
- **Score:** X/10
- **Key Findings:** [Bullets]

### Evolution Capability
[Evolution Strategist findings]
- **Score:** X/10
- **Key Findings:** [Bullets]

### Operational Assessment
[Operations Specialist findings]
- **Score:** X/10
- **Key Findings:** [Bullets]

## Consolidated Findings

### Strengths
1. [Major strength with supporting expert consensus]
2. [Another strength]

### Critical Issues
1. **[Issue Name]**
   - Severity: [Critical/High/Medium/Low]
   - Impact: [Description]
   - Recommendation: [Specific action]

### Improvement Opportunities
1. [Opportunity with expected benefit]
2. [Another opportunity]

## Tradeoff Analysis
[Discussion of key design tradeoffs and recommendations]

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [Strategy] |

## Recommendations

### Immediate Actions
1. [Required change before deployment]
2. [Another critical change]

### Short-term Improvements (1-3 months)
1. [Important but not blocking]

### Long-term Considerations (3+ months)
1. [Future optimization]

## Detailed Scoring Matrix

| Dimension | Score | Weight | Weighted Score | Notes |
|-----------|-------|--------|---------------|-------|
| Correctness | X/10 | 25% | X.XX | [Key factors] |
| Performance | X/10 | 20% | X.XX | [Key factors] |
| Maintainability | X/10 | 20% | X.XX | [Key factors] |
| Flexibility | X/10 | 15% | X.XX | [Key factors] |
| Robustness | X/10 | 10% | X.XX | [Key factors] |
| Security | X/10 | 10% | X.XX | [Key factors] |
| **Total** | **X/10** | **100%** | **X.XX** | |

## Appendices

### A. Specific Technical Recommendations
[Detailed technical suggestions with examples]

### B. Alternative Approaches Considered
[If multiple schemas were compared]

### C. References and Best Practices
[Relevant design patterns, articles, or standards]
```

## Parameters

| Parameter | Default | Options | Description |
|-----------|---------|---------|-------------|
| `evaluation_depth` | comprehensive | quick, standard, comprehensive | Level of analysis detail |
| `focus_areas` | all | performance, integrity, normalization, operations | Specific areas to emphasize |
| `database_type` | relational | relational, document, graph, timeseries | Database paradigm |
| `include_alternatives` | false | true, false | Generate alternative schema suggestions |
| `comparison_mode` | single | single, multiple | Evaluate one or compare multiple schemas |

## Quality Gates

- [ ] All five expert perspectives documented
- [ ] Minimum 3 strengths and 3 concerns identified
- [ ] Scoring completed across all dimensions
- [ ] Concrete recommendations provided
- [ ] Tradeoffs explicitly discussed
- [ ] Risk assessment includes mitigation strategies
- [ ] Output includes confidence levels
- [ ] Business context considered in recommendations

## Example Invocations

### Example 1: Single Schema Review
```yaml
request: Evaluate this e-commerce database schema
params:
  evaluation_depth: comprehensive
  focus_areas: [performance, normalization]
  database_type: relational

output: Full evaluation report with performance focus
```

### Example 2: Schema Comparison
```yaml
request: Compare normalized vs denormalized inventory schemas
params:
  comparison_mode: multiple
  focus_areas: [performance, maintainability]
  
output: Comparative analysis with tradeoff matrix
```

### Example 3: Migration Assessment
```yaml
request: Evaluate schema for microservices migration
params:
  focus_areas: [operations, flexibility]
  include_alternatives: true
  
output: Evaluation with migration-focused recommendations
```

## Integration Points

**Inputs From:**
- Schema definition files (DDL, JSON, YAML)
- ER diagrams or visual representations
- Requirements documents
- Performance benchmarks

**Outputs To:**
- Architecture decision records
- Implementation planning
- Performance optimization workflows
- Migration strategies

## Advanced Techniques Used

From `@core/technique-taxonomy.yaml`:
- **Parallel Processing:** Multi-persona simulation for expert panel
- **Unbiased Reasoning:** Conflict management matrix for balanced view
- **Perfect Recall:** Cross-referencing all constraints and relationships
- **Probabilistic Modeling:** Risk likelihood and impact assessment
- **Meta-Cognitive:** Expert confidence calibration

This skill leverages the cognitive advantages of:
- Holding multiple expert perspectives simultaneously
- Maintaining complete schema context without forgetting
- Unbiased evaluation across competing design philosophies
- Systematic coverage of all evaluation dimensions