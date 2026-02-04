---
name: ground-truth-template
description: Generic ground truth documentation template for creating verifiable reference skills. Auto-invoke when user requests ground truth skill creation, validation criteria framework, or canonical documentation templates. Do NOT load during actual ground truth usage (use project-specific skills instead).
allowed-tools: [Grep]
version: 1.0.0
category: Templates
tags: [template, ground-truth, validation, reference-data]
last-updated: 2025-10-20
---

# Ground Truth Documentation Template

## Purpose
This template guides the creation of ground truth skills - verifiable, canonical reference documentation that provides definitive facts, definitions, and validation criteria. Replace all `[PLACEHOLDER]` values with actual verified information.

## SKILL.md Frontmatter Template

```yaml
---
name: [project]-[domain]-ground-truth
description: Ground truth documentation for [PROJECT_NAME] [DOMAIN] providing canonical definitions, verified facts, and validation criteria. Auto-invoke when user discusses [TOPIC_1], [TOPIC_2], or validates [VALIDATION_SCENARIO]. Do NOT load for general [DOMAIN] discussions without [PROJECT_NAME] context.
allowed-tools: []
version: 1.0.0
category: Ground Truth
tags: [[project], [domain], reference, validation]
source: [CANONICAL_SOURCE_URL_OR_LOCATION]
verified-date: [YYYY-MM-DD]
next-review: [YYYY-MM-DD]
---
```

**Description Engineering Guidance**:

✅ **DO** include:
- Specific topics covered (definitions, metrics, processes)
- Validation scenarios where ground truth applies
- Canonical source attribution
- Version or release reference if applicable

❌ **DON'T** use:
- Generic descriptions ("Provides information about...")
- No source attribution
- No scope boundaries (will load for irrelevant discussions)

**Example Good Description**:
```
Ground truth documentation for Phoenix payment processing providing canonical transaction states, error codes, and retry policies. Auto-invoke when user discusses payment flows, error handling, or validates transaction logic. Do NOT load for general payment discussions outside Phoenix.
```

## Ground Truth Content Structure

### 1. Canonical Definitions

**Purpose**: Single source of truth for terms, concepts, and classifications

#### Term: `[TERM_NAME]`

**Definition**: `[PRECISE_CANONICAL_DEFINITION]`

**Source**: `[AUTHORITATIVE_SOURCE]` (verified `[DATE]`)

**Related Terms**:
- `[RELATED_TERM_1]`: `[BRIEF_DEFINITION]`
- `[RELATED_TERM_2]`: `[BRIEF_DEFINITION]`

**Anti-Patterns** (What this is NOT):
- ❌ `[COMMON_MISCONCEPTION_1]`
- ❌ `[COMMON_MISCONCEPTION_2]`

**Example Usage**:
```
[CODE_EXAMPLE_OR_REAL_WORLD_USAGE]
```

### 2. Verified Facts & Metrics

**Purpose**: Quantifiable, verifiable information with sources

#### Fact Category: `[CATEGORY_NAME]`

| Metric/Fact | Value | Source | Verified Date |
|-------------|-------|--------|---------------|
| `[METRIC_1]` | `[VALUE]` `[UNIT]` | `[SOURCE_LINK]` | `[YYYY-MM-DD]` |
| `[METRIC_2]` | `[VALUE]` `[UNIT]` | `[SOURCE_LINK]` | `[YYYY-MM-DD]` |
| `[METRIC_3]` | `[VALUE]` `[UNIT]` | `[SOURCE_LINK]` | `[YYYY-MM-DD]` |

**Calculation Method** (if applicable):
```
[FORMULA_OR_CALCULATION_METHODOLOGY]
```

**Freshness Policy**:
- **Update Frequency**: `[DAILY/WEEKLY/MONTHLY/QUARTERLY]`
- **Staleness Threshold**: Data older than `[TIME_PERIOD]` requires reverification
- **Last Verified**: `[YYYY-MM-DD]`

### 3. Canonical Processes & States

**Purpose**: Definitive workflows, state machines, and process flows

#### Process: `[PROCESS_NAME]`

**States**:
```
[STATE_1] → [STATE_2] → [STATE_3] → [FINAL_STATE]
```

**State Transitions**:

| From State | Event/Trigger | To State | Constraints |
|------------|---------------|----------|-------------|
| `[STATE_1]` | `[EVENT_1]` | `[STATE_2]` | `[CONDITION]` |
| `[STATE_2]` | `[EVENT_2]` | `[STATE_3]` | `[CONDITION]` |
| `[STATE_3]` | `[EVENT_3]` | `[FINAL_STATE]` | `[CONDITION]` |

**Error States**:
- `[ERROR_STATE_1]`: Triggered by `[ERROR_CONDITION]` → Recovery: `[RECOVERY_PROCESS]`
- `[ERROR_STATE_2]`: Triggered by `[ERROR_CONDITION]` → Recovery: `[RECOVERY_PROCESS]`

**Source**: `[TECHNICAL_SPEC_LINK_OR_DOC]` (version `[VERSION]`, dated `[DATE]`)

### 4. Validation Criteria

**Purpose**: Definitive rules for validating implementations, data, or behaviors

#### Validation Domain: `[DOMAIN_NAME]`

**Required Properties**:
```yaml
- Property: [PROPERTY_1]
  Type: [DATA_TYPE]
  Constraints: [VALIDATION_RULES]
  Example Valid: [VALID_EXAMPLE]
  Example Invalid: [INVALID_EXAMPLE]

- Property: [PROPERTY_2]
  Type: [DATA_TYPE]
  Constraints: [VALIDATION_RULES]
  Example Valid: [VALID_EXAMPLE]
  Example Invalid: [INVALID_EXAMPLE]
```

**Business Rules**:
1. `[RULE_1]`: `[DETAILED_DESCRIPTION]`
   - **Valid Example**: `[EXAMPLE]`
   - **Invalid Example**: `[COUNTER_EXAMPLE]`

2. `[RULE_2]`: `[DETAILED_DESCRIPTION]`
   - **Valid Example**: `[EXAMPLE]`
   - **Invalid Example**: `[COUNTER_EXAMPLE]`

**Validation Test Cases** (Reference):
```
Test ID: [TEST_ID]
Description: [WHAT_IS_BEING_TESTED]
Input: [TEST_INPUT]
Expected Output: [EXPECTED_RESULT]
Source: [TEST_SPEC_LOCATION]
```

### 5. Error Codes & Messages

**Purpose**: Canonical error taxonomy with meanings and resolutions

#### Error Category: `[CATEGORY]`

| Error Code | Error Name | Meaning | Resolution | Severity |
|------------|------------|---------|------------|----------|
| `[CODE_1]` | `[NAME]` | `[DESCRIPTION]` | `[FIX_STEPS]` | `[CRITICAL/HIGH/MEDIUM/LOW]` |
| `[CODE_2]` | `[NAME]` | `[DESCRIPTION]` | `[FIX_STEPS]` | `[CRITICAL/HIGH/MEDIUM/LOW]` |

**Error Code Format**:
```
Pattern: [REGEX_PATTERN_OR_FORMAT]
Example: [EXAMPLE_ERROR_CODE]
```

### 6. Reference Data & Enumerations

**Purpose**: Canonical lists, enumerations, and classification schemes

#### Enumeration: `[ENUM_NAME]`

| Value | Display Name | Description | Deprecated? |
|-------|--------------|-------------|-------------|
| `[VALUE_1]` | `[DISPLAY_1]` | `[DESCRIPTION]` | No |
| `[VALUE_2]` | `[DISPLAY_2]` | `[DESCRIPTION]` | No |
| `[VALUE_3]` | `[DISPLAY_3]` | `[DESCRIPTION]` | ⚠️ Yes (since `[DATE]`) |

**Source**: `[API_SPEC_OR_SCHEMA_LOCATION]`

## Validation Checklist

Before finalizing ground truth skill, verify:

**Content Quality**:
- [ ] All `[PLACEHOLDERS]` replaced with actual verified values
- [ ] Zero PII (no names, emails, phone numbers)
- [ ] Zero business-confidential metrics (use relative values or omit)
- [ ] All facts sourced and dated
- [ ] All definitions from canonical sources

**Source Attribution**:
- [ ] Every fact has a source reference
- [ ] Source links are accessible (internal docs, public APIs, etc.)
- [ ] Verification dates included
- [ ] Next review date set (freshness policy)

**Validation Quality**:
- [ ] Examples include both valid and invalid cases
- [ ] Business rules are unambiguous
- [ ] Error codes are complete and current
- [ ] State transitions are comprehensive

**Metadata & Tracking**:
- [ ] `source` field in frontmatter points to canonical documentation
- [ ] `verified-date` is current
- [ ] `next-review` date set based on freshness policy
- [ ] `allowed-tools: []` set (ground truth is read-only reference)
- [ ] Category and tags aid discovery

**Security & Scope**:
- [ ] File location matches scope (project ground truth in `.claude/skills/projects/[name]/ground-truth/`)
- [ ] No sensitive implementation details exposed
- [ ] Reviewed by subject matter expert

## Usage Examples

**Creating New Ground Truth Skill**:
```
User: "Create a ground truth skill for Phoenix payment error codes"

Claude: [Loads this template skill, uses structure to create Phoenix-specific ground truth]
```

**Validating Implementation**:
```
User: "Is this transaction state valid according to ground truth?"

Claude: [Loads project ground truth skill, checks against canonical state definitions]
```

**Do NOT Use This Template For**:
- Actual ground truth reference (use project-specific skills instead)
- Stakeholder information (use stakeholder template)
- Product roadmaps (use product template - roadmaps change frequently)
- Opinion or subjective content (ground truth is objective, verifiable facts only)

## Freshness & Maintenance

**Update Triggers**:
- New product release with API changes
- Schema version updates
- Error code additions or changes
- Process flow modifications
- Quarterly review (minimum)

**Staleness Warning**:
If `next-review` date has passed, skill should display:
```
⚠️ STALE GROUND TRUTH: Last verified [DATE], review overdue by [DAYS] days.
Please reverify before relying on this information.
```

**Version Control**:
- Track changes in git with descriptive commit messages
- Reference source documentation version in commits
- Update `version` field using semantic versioning (1.0.0 → 1.1.0 for additions)

---

**Template Source**: Phase 2 requirements + validation framework
**Template Version**: 1.0.0
**Last Updated**: 2025-10-20
**Validation**: Ready for Phase 2 implementation
