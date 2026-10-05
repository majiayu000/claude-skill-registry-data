---
name: rudder-design-first-instrumentation
description: Plans instrumentation for new features starting from product requirements before code exists. Use when building new features and need to define events as part of product definition.
allowed-tools: "Bash(rudder-cli *), Read, Write, Edit"
---

# Design-First Instrumentation

This skill guides instrumentation planning for **new features** where events are defined during product definition, before implementation begins.

## When to Use This Skill

| Scenario | Use This Skill? |
|----------|-----------------|
| Building a new feature, events not yet defined | Yes |
| Product requirements include analytics needs | Yes |
| PM and engineering collaborating on what to track | Yes |
| Existing product needs instrumentation | No — use `rudder-code-first-instrumentation` |
| Restructuring existing tracking | No — use `rudder-code-first-instrumentation` |

## The Design-First Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DESIGN-FIRST INSTRUMENTATION                      │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ 1. REQUIREMENTS │ ← What questions must the data answer?
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. EVENT DESIGN │ ← Define events (names only, no properties yet)
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. HUMAN        │ ← PM/Eng review: Are these the right events?
│    CHECKPOINT   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. PROPERTY     │ ← Define properties for approved events
│    DESIGN       │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. BUILD YAML   │ ← Create tracking plan definitions
└────────┬────────┘
         ▼
┌─────────────────┐
│ 6. IMPLEMENT    │ ← Code the feature with instrumentation
└─────────────────┘
```

## Phase 1: Requirements Gathering

Start with the questions the data must answer:

### Questions Template

```markdown
## Feature: [Feature Name]

### Business Questions
- [ ] What is the conversion rate through this feature?
- [ ] Where do users drop off?
- [ ] How long does it take users to complete the flow?
- [ ] What variations do users prefer?

### Success Metrics
- Primary: _______________
- Secondary: _______________

### Funnel Stages
1. Entry point: _______________
2. Key action: _______________
3. Completion: _______________

### Stakeholders
- PM: _______________
- Engineering: _______________
- Data/Analytics: _______________
```

## Phase 2: Event Design (Names Only)

Define events as user stories or behavioral descriptions first — **no properties yet**.

### Event Description Format

Use clear, behavioral language:

```markdown
## Events for [Feature Name]

### Event: Feature Opened
- **When:** User opens the feature for the first time in a session
- **Why track:** Measures feature discovery and initial engagement
- **Funnel position:** Entry

### Event: Configuration Started
- **When:** User begins configuring the feature
- **Why track:** Measures intent to use feature
- **Funnel position:** Middle

### Event: Configuration Completed
- **When:** User successfully completes configuration
- **Why track:** Measures successful adoption
- **Funnel position:** Completion

### Event: Configuration Failed
- **When:** User encounters an error during configuration
- **Why track:** Identifies friction points
- **Funnel position:** Error state
```

### Naming Convention

| Pattern | Example | Use For |
|---------|---------|---------|
| Feature + Action (Past Tense) | `Audience Created` | Completed actions |
| Feature + State | `Checkout Started` | State transitions |
| Object + Action | `Product Viewed` | Standard interactions |

## Phase 3: Human Checkpoint

**Critical:** Before defining properties, get alignment on events.

### Review Checklist

- [ ] Do these events answer all the business questions?
- [ ] Is the funnel complete (entry → middle → completion)?
- [ ] Are error states captured?
- [ ] Are there redundant events that can be consolidated?
- [ ] Do event names follow conventions?

### Approval Gate

```markdown
## Event Review Sign-Off

Feature: _______________
Date: _______________

Approved Events:
- [ ] Event 1: _______________
- [ ] Event 2: _______________
- [ ] Event 3: _______________

Rejected/Deferred:
- [ ] _______________

Approved by:
- PM: _______________
- Engineering: _______________
```

## Phase 4: Property Design

After events are approved, define properties for each.

### Property Design Process

For each event, ask:

1. **What context is needed to answer the business questions?**
2. **What attributes describe this action?**
3. **What will we group/filter by in dashboards?**

### Property Template

```markdown
## Event: Audience Created

### Required Properties
| Property | Type | Description | Example |
|----------|------|-------------|---------|
| audience_id | string | Unique identifier | "aud_123" |
| audience_name | string | User-provided name | "High Value Users" |
| condition_count | integer | Number of conditions | 3 |

### Optional Properties
| Property | Type | Description | Example |
|----------|------|-------------|---------|
| template_used | string | If created from template | "ecommerce-buyers" |
| creation_method | string | How it was created | "wizard" \| "manual" |

### Context (Auto-included)
- workspace_id (from session context)
- user_id (from identify)
```

### Identify Shared Patterns

Look for properties used across multiple events — these become **custom types**:

```markdown
## Shared Patterns Identified

### AudienceType (used by: Created, Updated, Deleted)
- audience_id
- audience_name
- audience_type

### ConditionType (used by: Created, Updated)
- condition_id
- condition_type
- condition_operator
```

## Phase 5: Build YAML Definitions

Convert approved designs to tracking plan YAML.

### Order of Creation

```
1. Custom Types    ← Reusable patterns identified in Phase 4
2. Properties      ← Individual property definitions
3. Categories      ← Organize events by feature/domain
4. Events          ← Reference properties and custom types
5. Tracking Plan   ← Bundle events for the source
```

### Example: Custom Type

```yaml
version: "rudder/v1"
kind: "custom-type"
metadata:
  name: "custom-types"
spec:
  name: "AudienceType"
  type: "object"
  description: "Core audience information"
  config:
    properties:
      - property: "urn:rudder:property/audience_id"
        required: true
      - property: "urn:rudder:property/audience_name"
        required: true
      - property: "urn:rudder:property/audience_type"
        required: true
```

### Example: Event

```yaml
version: "rudder/v1"
kind: "event"
metadata:
  name: "events"
spec:
  name: "Audience Created"
  description: "User successfully created a new audience"
  category: "urn:rudder:category/audiences"
  rules:
    - property: "urn:rudder:property/audience"
      required: true
      customType: "urn:rudder:custom-type/audience-type"
    - property: "urn:rudder:property/condition_count"
      required: true
    - property: "urn:rudder:property/template_used"
    - property: "urn:rudder:property/creation_method"
```

### Validate and Apply

```bash
# Validate definitions
rudder-cli validate -l ./

# Preview changes
rudder-cli apply --dry-run -l ./

# Apply to workspace
rudder-cli apply -l ./
```

## Phase 6: Implementation

With tracking plan applied, implement the feature with instrumentation.

### Implementation Checklist

- [ ] Tracking plan applied to workspace
- [ ] Events documented for developers
- [ ] Instrumentation added at correct points in code
- [ ] Context middleware configured (workspace_id)
- [ ] Tested in dev environment
- [ ] Verified events reach destination

### Code Pattern

```typescript
// Feature implementation with instrumentation
async function createAudience(config: AudienceConfig): Promise<Audience> {
  const audience = await audienceService.create(config);

  // Instrumentation
  analytics.track('Audience Created', {
    audience_id: audience.id,
    audience_name: audience.name,
    audience_type: audience.type,
    condition_count: config.conditions.length,
    template_used: config.templateId || null,
    creation_method: config.method,
  });

  return audience;
}
```

## Collaboration Patterns

### PM-Led Event Design

```
PM writes event descriptions (Phase 2)
    ↓
Engineering reviews for feasibility
    ↓
Joint checkpoint (Phase 3)
    ↓
Engineering leads property design (Phase 4)
    ↓
PM validates properties answer questions
    ↓
Engineering implements
```

### Engineering-Led with PM Input

```
Engineering drafts events based on feature spec
    ↓
PM reviews for analytics completeness
    ↓
Joint refinement
    ↓
Engineering completes properties + implementation
```

## Real-World Examples

For complete end-to-end examples including RudderStack Audiences and Transformations features, see `references/real-world-examples.md`.

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Skipping human checkpoint | Events don't answer business questions | Always get sign-off before properties |
| Properties before events | Scope creep, over-instrumentation | Define event names first, properties second |
| Too granular events | Data bloat, high costs | Use properties for variations, not separate events |
| Missing error states | Can't diagnose failures | Always include failure/error events |
| No shared patterns | Duplicate properties, inconsistency | Identify custom types early |
| Enum values don't match code | Type mismatches, glue code needed | Check existing code types before defining properties |

## Checklist

Before implementation:

- [ ] Business questions documented
- [ ] Events designed with behavioral descriptions
- [ ] Human checkpoint completed (events approved)
- [ ] Properties designed for each event
- [ ] Shared patterns extracted as custom types
- [ ] YAML definitions created
- [ ] `rudder-cli validate` passes
- [ ] Tracking plan applied to dev workspace
- [ ] Implementation plan includes instrumentation points
