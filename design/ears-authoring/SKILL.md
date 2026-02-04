---
name: ears-authoring
description: EARS requirement pattern authoring. Use when writing requirements using EARS patterns (Ubiquitous, State-Driven, Event-Driven, Unwanted, Optional, Complex). Provides pattern templates, validation, and examples.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# EARS Authoring

EARS (Easy Approach to Requirements Syntax) pattern authoring for precise, unambiguous requirements.

## When to Use This Skill

**Keywords:** EARS patterns, ubiquitous requirements, state-driven requirements, event-driven requirements, unwanted behavior, optional features, complex requirements, SHALL keyword, requirement syntax

**Use this skill when:**

- Writing new requirements using EARS syntax
- Converting informal requirements to EARS format
- Validating EARS pattern correctness
- Selecting the right EARS pattern for a requirement
- Understanding EARS anti-patterns

## Quick Pattern Reference

| Pattern | Keyword | Template |
| --- | --- | --- |
| Ubiquitous | (none) | The `<entity>` SHALL `<action>` |
| State-Driven | WHILE | WHILE `<condition>`, the `<entity>` SHALL `<action>` |
| Event-Driven | WHEN | WHEN `<trigger>`, the `<entity>` SHALL `<action>` |
| Unwanted | IF...THEN | IF `<condition>`, THEN the `<entity>` SHALL `<action>` |
| Optional | WHERE | WHERE `<feature>`, the `<entity>` SHALL `<action>` |
| Complex | Multiple | Combination of patterns |

## Pattern Selection Decision Tree

**Start here: When does this requirement apply?**

1. **Always applies** (no conditions)
   → Use **Ubiquitous**: "The system SHALL..."

2. **While in a specific state**
   → Use **State-Driven**: "WHILE in maintenance mode, the system SHALL..."

3. **When something happens** (event/trigger)
   → Use **Event-Driven**: "WHEN user clicks submit, the system SHALL..."

4. **To handle unwanted behavior** (error/exception)
   → Use **Unwanted**: "IF authentication fails, THEN the system SHALL..."

5. **Only when feature is enabled** (optional/configurable)
   → Use **Optional**: "WHERE dark mode is enabled, the system SHALL..."

6. **Multiple conditions apply**
   → Use **Complex**: "WHILE active, WHEN timeout occurs, the system SHALL..."

## Pattern Details

### Ubiquitous Pattern

**Use when:** Requirement applies unconditionally, always active.

**Template:**

```text
The <entity> SHALL <action>
```

**Keywords:** None required (no WHILE, WHEN, IF, WHERE)

**Examples:**

- "The system SHALL encrypt all data at rest"
- "The API SHALL respond in JSON format"
- "The application SHALL log all user actions"

**Common Mistakes:**

- Adding unnecessary conditions when behavior is universal
- Using "should" instead of "SHALL"

### State-Driven Pattern

**Use when:** Behavior applies while system is in a particular state.

**Template:**

```text
WHILE <condition>, the <entity> SHALL <action>
```

**Keywords:** WHILE (at start)

**Examples:**

- "WHILE in maintenance mode, the system SHALL display a banner"
- "WHILE the connection is active, the system SHALL send heartbeats"
- "WHILE the user is authenticated, the system SHALL show the dashboard"

**Common Mistakes:**

- Using WHEN instead of WHILE (WHEN = event, WHILE = state)
- Describing events, not states

### Event-Driven Pattern

**Use when:** Action triggered by a specific event or user action.

**Template:**

```text
WHEN <trigger>, the <entity> SHALL <action>
```

**Keywords:** WHEN (at start)

**Examples:**

- "WHEN a user submits the form, the system SHALL validate inputs"
- "WHEN an error occurs, the system SHALL log the details"
- "WHEN the session expires, the system SHALL redirect to login"

**Common Mistakes:**

- Using WHILE instead of WHEN (WHILE = state, WHEN = event)
- Describing states, not events

### Unwanted Behavior Pattern

**Use when:** Handling exceptions, errors, or unwanted conditions.

**Template:**

```text
IF <condition>, THEN the <entity> SHALL <action>
```

**Keywords:** IF...THEN (both required)

**Examples:**

- "IF authentication fails, THEN the system SHALL lock the account"
- "IF the database is unavailable, THEN the system SHALL queue requests"
- "IF input validation fails, THEN the system SHALL display error messages"

**Common Mistakes:**

- Using IF-THEN for normal behavior (use Event-Driven instead)
- Missing THEN keyword
- Using for positive conditions (reserve for negative/unwanted)

### Optional Feature Pattern

**Use when:** Behavior depends on feature flag or configuration.

**Template:**

```text
WHERE <feature/config>, the <entity> SHALL <action>
```

**Keywords:** WHERE (at start)

**Examples:**

- "WHERE dark mode is enabled, the system SHALL use dark theme"
- "WHERE audit logging is configured, the system SHALL log access"
- "WHERE two-factor authentication is enabled, the system SHALL require OTP"

**Common Mistakes:**

- Using IF instead of WHERE (IF = unwanted, WHERE = optional)
- Describing mandatory features as optional

### Complex Pattern

**Use when:** Requirement combines multiple conditions from different patterns.

**Template:**

```text
<Pattern1>, <Pattern2>, the <entity> SHALL <action>
```

**Examples:**

- "WHILE active, WHEN timeout occurs, the system SHALL reconnect"
- "WHILE in production mode, IF error occurs, THEN the system SHALL notify ops"
- "WHERE caching is enabled, WHEN data changes, the system SHALL invalidate cache"

**Common Mistakes:**

- Using Complex when a simpler pattern suffices
- Nesting conditions too deeply (max 2 recommended)

## Writing Quality Requirements

### The SHALL Keyword

**Always use SHALL** for requirements:

- ✅ "The system SHALL validate input"
- ❌ "The system should validate input"
- ❌ "The system must validate input"
- ❌ "The system will validate input"

**Why:** SHALL indicates mandatory behavior. Other words are ambiguous.

### Active Voice

**Always use active voice:**

- ✅ "The system SHALL encrypt data"
- ❌ "Data shall be encrypted"
- ❌ "Encryption shall be performed"

### Single Requirement Per Statement

**One action per requirement:**

- ✅ "The system SHALL validate input"
- ✅ "The system SHALL log validation errors"
- ❌ "The system SHALL validate input and log errors"

### Testable Requirements

**Requirements must be testable:**

- ✅ "The system SHALL respond within 200ms"
- ❌ "The system SHALL respond quickly"
- ✅ "The system SHALL support 1000 concurrent users"
- ❌ "The system SHALL scale well"

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
| --- | --- | --- |
| "should" instead of "SHALL" | Ambiguous obligation | Use "SHALL" |
| Passive voice | Unclear actor | Use active voice |
| Multiple requirements | Untestable compound | Split into separate |
| Implementation details | Specifies "how" | Focus on "what" |
| Vague terms | Not measurable | Add specific metrics |
| Wrong pattern keyword | Semantic confusion | Match pattern to behavior |

## Validation Checklist

Before finalizing an EARS requirement:

- [ ] Uses "SHALL" (not should/must/will)
- [ ] Uses active voice (entity does action)
- [ ] Single behavior per statement
- [ ] Testable with measurable criteria
- [ ] Pattern keyword matches behavior type
- [ ] No implementation details (what, not how)

## Integration with Canonical Spec

EARS requirements map to canonical specification:

```yaml
requirements:
  - id: "REQ-001"
    text: "WHEN a user submits the form, the system SHALL validate inputs"
    priority: must
    ears_type: event-driven  # Matches pattern used
    acceptance_criteria:
      - id: "AC-001"
        given: "a user on the form page"
        when: "the user clicks submit"
        then: "the system validates all inputs"
```

## References

**Detailed Documentation:**

- [Pattern Reference](references/pattern-reference.md) - Complete pattern syntax and rules
- [Examples](references/examples.md) - Real-world examples per pattern

**Related Skills:**

- `canonical-spec-format` - Canonical specification structure
- `spec-management` - Specification workflow navigation
- `requirements-quality` - INVEST criteria and quality assessment

---

**Last Updated:** 2025-12-24

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
