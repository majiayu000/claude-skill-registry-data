---
name: metis-gap-analysis
description: "Pre-plan gap analysis for hidden intentions and edge cases. Use before delivering plans to catch missing elements."
context: fork
globs: []
alwaysApply: false
---

# Metis Gap Analysis — Pre-Plan Validation

Use this skill to analyze implementation plans BEFORE they are delivered to the user. Catches what the planner missed: hidden intentions, ambiguities, missing criteria, over-engineering, and edge cases.

Named after Metis, the Titaness of wisdom and deep thought — she forces externalization of implicit knowledge.

---

## The Core Principle

> **The plan author has ADHD working memory. Force the gaps into the open.**

When Athena generates a plan, implicit knowledge never makes it onto the page. Metis catches these gaps before the user approves the plan.

---

## When to Run

Metis runs **AFTER** Athena generates the plan, **BEFORE** delivering to the user for approval.

```
Athena generates plan
  ↓
Metis analyzes (this skill)
  ↓
Gaps injected into plan
  ↓
Athena revises plan with gaps addressed
  ↓
Plan delivered to user for approval
```

---

## Gap Categories

### 1. Hidden Intentions

What the user wanted but didn't say:

| Signal | Question to Ask |
|--------|----------------|
| Vague scope ("improve performance") | "What metric defines 'improved'? Latency? Throughput? Memory?" |
| No rollback mentioned | "What's the rollback strategy if this breaks?" |
| No migration path | "How do we migrate existing data?" |
| No monitoring mentioned | "How will we know if this works in production?" |

### 2. Ambiguities

Terms that could derail implementation:

| Signal | Question to Ask |
|--------|----------------|
| "Fast", "scalable", "robust" | "Define the target: <100ms? 10k req/s? 99.9% uptime?" |
| "Following existing patterns" | "Which pattern? There are 3 different auth patterns in the codebase." |
| "When ready", "as needed" | "What triggers readiness? What's the threshold?" |
| No scope boundaries | "What is explicitly OUT of scope?" |

### 3. Missing Acceptance Criteria

How to know it worked:

| Signal | Question to Ask |
|--------|----------------|
| No test strategy | "What tests verify this works?" |
| No success metrics | "What does 'done' look like?" |
| No verification steps | "How does the user verify this in production?" |
| No error scenarios | "What happens when X fails?" |

### 4. AI Slop Patterns

Over-engineering and scope creep:

| Signal | Action |
|--------|--------|
| 10+ phases for a simple feature | "Can this be done in 3-5 phases?" |
| Abstract interfaces for single impl | "Do we need this abstraction?" |
| "Future-proof" without current need | "YAGNI — remove unless needed now" |
| Unnecessary microservices | "Can this be a module instead?" |

### 5. Edge Cases

What wasn't covered:

| Signal | Question to Ask |
|--------|----------------|
| No error handling plan | "What happens on timeout? Network failure? Invalid input?" |
| No rate limiting | "What if this endpoint is hammered?" |
| No pagination for lists | "What if there are 1M records?" |
| No cache invalidation | "When does the cache stale?" |

---

## Output Format

When gaps are found, inject into the plan:

```markdown
## ⚠️ Gaps Identified (Metis Analysis)

### Hidden Intentions
- [ ] User said "improve performance" but didn't specify target metric
  → Recommendation: Define target (e.g., <200ms p95 latency)

### Ambiguities
- [ ] "Following existing patterns" — codebase has 3 different patterns
  → Recommendation: Specify which pattern (e.g., Repository pattern from users/)

### Missing Acceptance Criteria
- [ ] No test strategy defined
  → Recommendation: Add test requirements per phase

### AI Slop Patterns
- [ ] 8 phases for a simple CRUD feature
  → Recommendation: Consolidate to 3-4 phases

### Edge Cases
- [ ] No error handling for database connection failure
  → Recommendation: Add retry + fallback strategy
```

---

## Clearance Checklist

Before declaring a plan complete, verify:

- [ ] Core objective is clearly defined
- [ ] Scope boundaries are established (what's IN and OUT)
- [ ] No critical ambiguities remain
- [ ] Technical approach is decided
- [ ] Test strategy is confirmed
- [ ] Rollback strategy exists
- [ ] Acceptance criteria are measurable
- [ ] Edge cases are addressed

If ANY item is unchecked → inject the gap into the plan.

---

## Integration with Athena

Athena should run Metis analysis as a sub-step:

```
1. Athena generates initial plan
2. Athena applies Metis Gap Analysis (this skill)
3. Athena revises plan to address gaps
4. Athena delivers revised plan to user
```

This is NOT a separate agent — it's a skill that Athena applies to her own plan before delivery.
