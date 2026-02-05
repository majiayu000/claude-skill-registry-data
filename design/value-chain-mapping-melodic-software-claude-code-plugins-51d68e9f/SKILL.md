---
name: value-chain-mapping
description: Map value chains from user needs to underlying components
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Value Chain Mapping Skill

Map value chains from user needs to underlying components as the foundation for Wardley Maps.

## When to Use This Skill

Use this skill when:

- **Value Chain Mapping tasks** - Working on map value chains from user needs to underlying components
- **Planning or design** - Need guidance on Value Chain Mapping approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Documentation-First Approach

Before mapping value chains:

1. **Invoke `docs-management` skill** for value chain patterns
2. **Verify mapping methodology** via MCP servers (perplexity)
3. **Base guidance on Wardley's value chain decomposition**

## Value Chain Fundamentals

```text
Value Chain = Components Linked by Dependencies

User Need
    │
    ▼
┌─────────────────┐
│ Component A     │ ◄── Visible to user
└────────┬────────┘
         │ depends on
         ▼
┌─────────────────┐
│ Component B     │ ◄── Less visible
└────────┬────────┘
         │ depends on
         ▼
┌─────────────────┐
│ Component C     │ ◄── Invisible to user
└─────────────────┘

Key Principles:
- Start with user need (anchor)
- Work backwards to dependencies
- Higher = more visible to user
- Lower = more invisible (infrastructure)
```

## Step 1: Identify the Anchor (User Need)

### Good vs Bad Anchors

```text
GOOD ANCHORS (Needs):
✓ "I need to communicate with my team"
✓ "I need to process customer payments"
✓ "I need to deploy software reliably"
✓ "I need to understand customer behavior"
✓ "I need to manage my finances"

BAD ANCHORS (Solutions):
✗ "I need Slack"
✗ "I need Stripe"
✗ "I need Kubernetes"
✗ "I need Google Analytics"
✗ "I need QuickBooks"

Test: Can the need be satisfied multiple ways?
If tied to specific solution, you have a solution, not a need.
```

### Anchor Identification Questions

```text
Finding User Needs:

WHO Questions:
- Who is the user?
- Who benefits from this?
- Who are we serving?

WHAT Questions:
- What outcome do they want?
- What problem are they solving?
- What value do they receive?

WHY Questions:
- Why do they need this?
- Why does this matter to them?
- Why would they pay for this?

Test Questions:
- Is this a capability or a solution?
- Could this be satisfied differently?
- What's the underlying job-to-be-done?
```

## Step 2: Decompose Into Components

### Decomposition Method

```text
Decomposition Process:

Start: User Need
Ask: "What is required to satisfy this need?"
Answer: List of components (first level)

For Each Component:
Ask: "What does THIS depend on?"
Answer: List of sub-components (next level)

Repeat until you reach:
- Commodities (electricity, bandwidth)
- Standard services (cloud compute)
- Well-known infrastructure

Stop When:
- Component is truly commodity
- Further decomposition adds no strategic value
- You've reached common industry infrastructure
```

### Component Identification Checklist

```text
For Each Potential Component:

□ Is it a capability (not just an activity)?
□ Does it provide value to something above it?
□ Can it evolve independently?
□ Does it have identifiable evolution stage?
□ Can you point to who/what provides it?

Component Boundaries:
- Should be cohesive (single responsibility)
- Should have clear interfaces
- Should be manageable units
- Should be meaningfully different from siblings
```

## Step 3: Establish Dependencies

### Dependency Types

```text
Dependency Relationships:

REQUIRES (Hard Dependency)
Component A ───► Component B
"A cannot function without B"

Example: API Service ───► Database

USES (Soft Dependency)
Component A - - ► Component B
"A uses B but could use alternatives"

Example: Application - - ► Logging Service

ENABLES (Reverse Dependency)
Component A ◄─── Component B
"B enables/enhances A"

Example: Analytics ◄─── User Interface
```

### Dependency Rules

```text
Dependency Principles:

1. DIRECTION
   - Dependencies flow DOWN the value chain
   - Higher components depend on lower components
   - Users are at the top, infrastructure at bottom

2. VISIBILITY CORRELATION
   - Components closer to user need = more visible
   - Components further from user = less visible
   - Dependency depth ≈ invisibility

3. MULTIPLE DEPENDENCIES
   - Components can depend on multiple others
   - Creates complexity in the chain
   - Watch for critical path dependencies

4. CIRCULAR DEPENDENCIES
   - Should be rare/avoided
   - May indicate poor decomposition
   - Can create analysis paralysis
```

## Step 4: Validate the Chain

### Validation Checklist

```text
Value Chain Validation:

COMPLETENESS
□ Does chain start with user need?
□ Are all critical dependencies captured?
□ Does chain reach commodity level?
□ No orphan components (disconnected)?

ACCURACY
□ Do dependencies reflect reality?
□ Is visibility ordering correct?
□ Are component boundaries appropriate?
□ Does it match how work actually flows?

USEFULNESS
□ Is granularity appropriate for purpose?
□ Can you position components on evolution axis?
□ Does it reveal strategic insights?
□ Can decisions be made from this chain?
```

### Common Validation Issues

```text
Problems to Watch For:

TOO SHALLOW
Symptom: Few levels, large components
Fix: Ask "what does this depend on?" more times

TOO DEEP
Symptom: Many levels, trivial components
Fix: Consolidate components, focus on strategic items

MISSING COMPONENTS
Symptom: Gaps in dependencies, magic jumps
Fix: Trace the actual work/data flow

SOLUTION BIAS
Symptom: Components are products, not capabilities
Fix: Reframe as "what capability does this provide?"

ACTIVITY CONFUSION
Symptom: Components are verbs, not nouns
Fix: Activities are not components; capabilities are
```

## Value Chain Patterns

### Common Patterns

```text
Standard Value Chain Shapes:

LINEAR CHAIN
User Need
    │
    ▼
[A] → [B] → [C] → [D]
Simple, sequential dependencies

BRANCHING CHAIN
User Need
    │
    ├──► [A] → [C]
    │          ↓
    └──► [B] → [D] → [E]
Multiple paths to satisfy need

CONVERGING CHAIN
User Need
    │
[A]─┴─[B]
    │
    ▼
   [C]
    │
   [D]
Multiple components feeding one

PLATFORM CHAIN
User Need
    │
    ▼
   [A]
    │
┌───┼───┐
▼   ▼   ▼
[B][C][D]
    │
    ▼
  [Platform]
Common platform underneath
```

### Domain-Specific Examples

```text
E-COMMERCE VALUE CHAIN:

User Need: "Buy products online"
    │
    ├── Product Discovery
    │       ├── Search
    │       ├── Catalog
    │       └── Recommendations
    │
    ├── Shopping Experience
    │       ├── Cart
    │       ├── Wishlist
    │       └── Pricing
    │
    ├── Checkout
    │       ├── Payment Processing
    │       ├── Tax Calculation
    │       └── Address Validation
    │
    └── Fulfillment
            ├── Inventory
            ├── Shipping
            └── Notifications
                    │
                    ▼
            [Cloud Infrastructure]
```

```text
SAAS APPLICATION VALUE CHAIN:

User Need: "Manage projects collaboratively"
    │
    ├── User Management
    │       ├── Authentication
    │       ├── Authorization
    │       └── Identity Provider
    │
    ├── Project Management
    │       ├── Task Tracking
    │       ├── Timeline/Gantt
    │       └── Resource Allocation
    │
    ├── Collaboration
    │       ├── Real-time Sync
    │       ├── Notifications
    │       └── Comments/Chat
    │
    └── Reporting
            ├── Analytics
            ├── Dashboards
            └── Export
                    │
                    ▼
            [Database] [Compute] [Storage]
```

## Value Chain Documentation Template

````markdown
# Value Chain: [Domain/Context]

## User Need
[The anchor - what users actually need]

## Users
- [Primary user persona]
- [Secondary user persona]

## Value Chain Diagram

```text
[ASCII diagram of value chain]
```

## Component Inventory

| ID | Component | Description | Depends On | Visibility |
|----|-----------|-------------|------------|------------|
| 1 | [Name] | [What it does] | - | High |
| 2 | [Name] | [What it does] | 1 | Medium |
| 3 | [Name] | [What it does] | 2 | Low |

## Dependency Matrix

|   | C1 | C2 | C3 | C4 |
|---|----|----|----|----|
| C1 | - | | | |
| C2 | X | - | | |
| C3 | | X | - | |
| C4 | | X | X | - |

## Critical Path

[Which dependencies are most critical]

## Assumptions

- [Assumption about user need]
- [Assumption about components]

## Open Questions

- [What needs further investigation]

## Next Steps

- [ ] Validate with users
- [ ] Position on evolution axis
- [ ] Identify strategic opportunities

````

## Visibility Assessment

### Y-Axis Positioning Guide

| Visibility Level | Characteristics | Examples |
|------------------|-----------------|----------|
| **0.90-1.00** | Direct user interaction | UI, Customer Portal |
| **0.75-0.89** | User-aware features | Notifications, Search |
| **0.50-0.74** | Application services | Business Logic, APIs |
| **0.25-0.49** | Platform services | Auth, Messaging, Cache |
| **0.10-0.24** | Infrastructure | Database, Compute, Storage |
| **0.00-0.09** | Utilities | Power, Network, Physical |

### Visibility Questions

```text
Assessing Visibility:

HIGH VISIBILITY (Near User):
- Does the user directly interact with this?
- Does the user know this exists?
- Is this a selling point to users?

MEDIUM VISIBILITY:
- Does this affect user experience directly?
- Would users notice if it failed?
- Is this mentioned in user documentation?

LOW VISIBILITY:
- Is this purely technical infrastructure?
- Could you swap this without users knowing?
- Is this industry-standard plumbing?
```

## Workflow

When mapping value chains:

1. **Define Scope**: What are we mapping? For what purpose?
2. **Identify Anchor**: What is the user need?
3. **List First-Level Components**: What directly satisfies the need?
4. **Decompose Recursively**: What does each component depend on?
5. **Draw Dependencies**: Connect components with dependency arrows
6. **Validate Chain**: Check completeness, accuracy, usefulness
7. **Assess Visibility**: Position components on Y-axis
8. **Document**: Capture components, dependencies, assumptions
9. **Prepare for Evolution**: Ready to add X-axis positioning

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
