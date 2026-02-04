---
name: flow-architect
description: Guide architectural decisions and PLAN.md updates using Flow framework. Use when user discusses "architecture", "how should we architect", "design patterns", "how should we structure", "how do we structure", "technology choice", "should we use", "DO/DON'T rules", "update architecture", or wants to update Architecture section in PLAN.md. Helps document architectural decisions, update DO/DON'T guidelines, define scope boundaries, and record technology choices during brainstorming.
---

# Flow Architect

Help users make and document architectural decisions using Flow framework projects. This Skill activates during brainstorming when design patterns, technology choices, or system structure need to be captured in PLAN.md.

## When to Use This Skill

Activate when the user discusses architecture:
- "How should we architect this?"
- "What's the best structure for..."
- "Should we use [pattern/library/approach]?"
- "Update the architecture section"
- "Add a DO/DON'T rule"
- "What technology should we choose?"
- "Document this design decision"
- "Define the scope boundaries"

## Architecture Philosophy

**Flow's Core Principle**: Document architectural decisions during brainstorming, not during implementation. PLAN.md preserves design rationale for future reference.

**Key Sections in PLAN.md**:
- **Architecture**: High-level system structure, component boundaries, data flow
- **DO/DON'T Guidelines**: Discovered patterns and anti-patterns with rationale
- **Scope**: What's in V1 vs future versions, boundaries and constraints

**When to Update**:
- Major architectural decision made
- Pattern discovered that should be followed consistently
- Technology choice finalized
- Scope boundary clarified
- Anti-pattern identified

## PLAN.md Architecture Section

### What Goes in Architecture

**High-level Structure**:
- System components and their relationships
- Module boundaries and responsibilities
- Data flow between components
- Integration points (external APIs, services, databases)
- Key design patterns being used

**Example Architecture Section**:
```markdown
## Architecture

### System Structure

**Core Components**:
- **PaymentProcessor**: Orchestrates payment flow, handles retries
- **StripeClient**: Wrapper around Stripe SDK, manages API calls
- **ErrorMapper**: Translates Stripe errors to domain errors
- **RetryPolicy**: Configurable backoff and retry logic

**Data Flow**:
```
User → PaymentProcessor → StripeClient → Stripe API
         ↓ (on error)
    ErrorMapper → RetryPolicy → StripeClient (retry)
```

**Integration Points**:
- Stripe API v2024-10 (payment processing)
- Webhook endpoint (payment status updates)
- Database (transaction log)
```

### What Doesn't Go in Architecture

**Avoid These**:
- ❌ Implementation details (specific line numbers, code snippets)
- ❌ Completed work (belongs in task notes)
- ❌ Bugs and fixes (belongs in iteration notes)
- ❌ Speculation about future features (keep focused on V1)

## DO/DON'T Guidelines

### When to Add Guidelines

**Add a guideline when you discover**:
- A pattern that should be followed consistently
- An anti-pattern that should be avoided
- A constraint from the technology/platform
- A design decision with specific rationale

**DO NOT add guidelines for**:
- Obvious best practices (don't state "write tests")
- One-off decisions (not patterns)
- Implementation details (belongs in code comments)
- Preferences without rationale

### Guideline Structure

**Format**:
```markdown
### DO: [Action]

**Rationale**: [Why this pattern works]

**Example**:
```[language]
// Good approach
```

**Anti-pattern**:
```[language]
// What to avoid
```
```

**Real Example**:
```markdown
### DO: Use RetryPolicy for all Stripe API calls

**Rationale**: Stripe API has transient failures (rate limits, network issues). Retry logic with exponential backoff prevents user-facing errors.

**Example**:
```typescript
const result = await retryPolicy.execute(() =>
  stripe.createCharge({ amount, currency })
);
```

**Anti-pattern**:
```typescript
// Don't call Stripe directly without retry
const result = await stripe.createCharge({ amount, currency });
```
```

### DON'T: [Anti-pattern]

**Rationale**: [Why this causes problems]

**Impact**: [Consequences of ignoring this]

**Example**:
```markdown
### DON'T: Retry permanently failed payments

**Rationale**: Permanent failures (invalid card, insufficient funds) will never succeed. Retrying wastes resources and delays error feedback to user.

**Impact**:
- User waits longer for error message
- Unnecessary load on Stripe API
- Potential rate limit violations

**How to Identify Permanent Failures**:
- Stripe error codes: `card_declined`, `insufficient_funds`, `invalid_card`
- Use ErrorMapper to classify errors
```

## Technology Choices

### When to Document Technology Decisions

**Document when you choose**:
- External library or framework
- Design pattern (e.g., Repository pattern, Strategy pattern)
- Architecture style (e.g., layered, hexagonal, microservices)
- Third-party service (e.g., Stripe, Twilio, SendGrid)

### Technology Choice Format

```markdown
## Technology Choices

### [Component/Area]: [Technology]

**Decision**: Using [technology/pattern] for [purpose]

**Rationale**:
- [Reason 1: why this choice]
- [Reason 2: advantage over alternatives]
- [Reason 3: fits project constraints]

**Alternatives Considered**:
- [Alternative 1]: [Why not chosen]
- [Alternative 2]: [Why not chosen]

**Trade-offs**:
- ✅ Pros: [advantages]
- ❌ Cons: [disadvantages]
- ⚖️ Acceptable for V1: [why trade-offs are OK]
```

**Example**:
```markdown
### Retry Logic: Custom Implementation

**Decision**: Building custom retry policy instead of using Stripe SDK built-in retry

**Rationale**:
- Stripe SDK v12 doesn't expose retry configuration
- Need fine-grained control over backoff timing
- Want to distinguish transient vs permanent errors

**Alternatives Considered**:
- Stripe SDK built-in retry: Not customizable enough
- Generic retry library (async-retry): Doesn't understand Stripe error semantics

**Trade-offs**:
- ✅ Pros: Full control, testable, Stripe-aware
- ❌ Cons: More code to maintain
- ⚖️ Acceptable for V1: Retry logic is isolated in RetryPolicy class
```

## Scope Boundaries

### Defining Scope

**V1 Scope** (what's included):
- Core functionality needed for first release
- Must-have features
- Blocking dependencies

**V2/V3 Scope** (what's deferred):
- Nice-to-have features
- Optimizations
- Edge cases
- Advanced features

### Scope Section Format

```markdown
## Scope

### V1 - MVP (Current)

**In Scope**:
- [Core feature 1]
- [Core feature 2]
- [Core feature 3]

**Out of Scope** (defer to V2):
- [Enhancement 1]: [Why deferred]
- [Enhancement 2]: [Why deferred]

**Constraints**:
- [Constraint 1]: [Impact on design]
- [Constraint 2]: [Impact on design]
```

**Example**:
```markdown
## Scope

### V1 - MVP (Current)

**In Scope**:
- Payment processing (charge credit cards)
- Basic retry logic (transient failures only)
- Error mapping (Stripe errors → domain errors)
- Transaction logging

**Out of Scope** (defer to V2):
- Refunds: Not needed for initial launch
- Subscription billing: Future business model
- Multi-currency: US only for V1
- Webhook verification: Will add when scaling

**Constraints**:
- Stripe API v2024-10 (latest stable)
- TypeScript 5.x (project standard)
- Must handle 100 req/sec (growth expectation)
```

## Updating PLAN.md During Brainstorming

### Workflow

1. **Read current PLAN.md**:
   - Check existing Architecture section
   - Review current DO/DON'T guidelines
   - Understand scope boundaries

2. **Discuss with user**:
   - Present architectural options clearly
   - Explain trade-offs for each approach
   - Reference existing patterns in codebase

3. **Update PLAN.md** (after user decides):
   - Add/update Architecture section
   - Add new DO/DON'T guidelines
   - Document technology choices
   - Clarify scope boundaries

4. **Reference in task file**:
   - Link to PLAN.md sections in task notes
   - Don't duplicate content in task files

### Subject Resolution Type B

Architectural decisions are often **Type B subjects** in brainstorming:
- **Type B**: Documentation-only updates (no code)
- Resolved by updating PLAN.md
- No action items needed
- Marked resolved when PLAN.md updated

**Example Type B Subject**:
```markdown
### Subject 2: Define Retry Strategy

**Status**: ✅ RESOLVED (Type B - Documentation)

**Question**: What retry strategy should we use for Stripe API calls?

**Decision**: Exponential backoff with jitter (1s, 2s, 4s, 8s, 16s max)

**Rationale**:
- Prevents thundering herd problem (jitter)
- Standard for API rate limiting
- Stripe recommends exponential backoff

**PLAN.md Updated**:
- Added "Retry Logic" to Architecture section
- Added "DO: Use RetryPolicy for all Stripe calls" guideline
- Documented RetryPolicy configuration in Technology Choices
```

## Common Architecture Patterns

### Pattern: Layered Architecture

```
Presentation Layer (API endpoints, controllers)
    ↓
Business Layer (services, domain logic)
    ↓
Data Layer (repositories, database access)
    ↓
External Layer (third-party APIs)
```

**When to use**: Clear separation of concerns, traditional web apps

### Pattern: Wrapper/Adapter

**When to use**: Integrating with external service, need to control interface

**Example**:
```markdown
### StripeClient Wrapper

**Purpose**: Wrap Stripe SDK to add retry logic and error mapping

**Benefits**:
- Isolates Stripe-specific code
- Single place for retry configuration
- Easier to test (can mock wrapper)
- Can swap Stripe for different provider

**Structure**:
```typescript
class StripeClient {
  constructor(
    private stripe: Stripe,
    private retryPolicy: RetryPolicy,
    private errorMapper: ErrorMapper
  ) {}

  async createCharge(params: ChargeParams): Promise<Charge> {
    return this.retryPolicy.execute(async () => {
      try {
        return await this.stripe.charges.create(params);
      } catch (error) {
        throw this.errorMapper.map(error);
      }
    });
  }
}
```
```

### Pattern: Strategy Pattern

**When to use**: Multiple algorithms for same operation, chosen at runtime

**Example**: RetryPolicy with different backoff strategies (linear, exponential, custom)

## Interaction with Other Flow Skills

**Planning Stage** (flow-planner Skill):
- `/flow-brainstorm-start` - Begin architectural discussion
- `/flow-brainstorm-subject` - Add design decision to discuss

**Architecture Stage** (This Skill):
- Discuss architectural options ← YOU ARE HERE
- Update PLAN.md with decisions ← YOU ARE HERE
- Resolve Type B subjects (documentation)

**Implementation Stage** (flow-implementer Skill):
- `/flow-implement-start` - Build based on architecture
- Reference PLAN.md architecture during coding

## Detailed Guidance

For comprehensive patterns, examples, and templates, see **[PLAN_UPDATES.md](PLAN_UPDATES.md)**:

- **When to Update PLAN.md**: Type B subjects, workflows, timing guidance
- **Architecture vs Scope**: Detailed distinction with decision tree and examples
- **DO/DON'T Examples**: 4 comprehensive patterns with full code (API integration, error handling, configuration, testing)
- **Technology Choice Templates**: Complete documentation format with 2 real examples
- **Keeping PLAN.md Focused**: What to include/avoid, red flags, how to slim down

## References

- **PLAN.md Structure**: DEVELOPMENT_FRAMEWORK.md lines 2363-2560
- **Brainstorming Pattern**: DEVELOPMENT_FRAMEWORK.md lines 1167-1797
- **Subject Resolution Type B**: DEVELOPMENT_FRAMEWORK.md lines 1247-1268
- **DO/DON'T Guidelines**: Include rationale and examples, avoid speculation

## Key Reminders

**Before suggesting architecture changes**:
- [ ] Read current PLAN.md Architecture section
- [ ] Understand existing patterns in codebase
- [ ] Present multiple options with trade-offs
- [ ] Let user make final decision

**After user decides**:
- [ ] Update PLAN.md with decision
- [ ] Add DO/DON'T if pattern emerges
- [ ] Document technology choice with rationale
- [ ] Resolve brainstorming subject (Type B)

**Keep PLAN.md focused**:
- High-level decisions, not implementation details
- Rationale, not speculation
- Patterns, not one-off choices
- V1 scope, defer V2/V3 discussions
