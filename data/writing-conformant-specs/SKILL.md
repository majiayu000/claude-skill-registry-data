---
name: writing-conformant-specs
description: This skill should be used when creating new RFC 2119-conformant specification documents, iterating on specification drafts, choosing keywords (MUST/SHOULD/MAY/MUST NOT) while writing, structuring sections, or progressively refining specifications.
---

# Writing Conformant Specifications

Guides creation and iteration of RFC 2119-conformant specifications. Supports active writing: structuring documents, choosing keywords as requirements are drafted, separating normative from informative content, and progressively refining through iteration.

## When to Use

This skill should be used when:

- Creating new specification documents from scratch
- Iterating on specification drafts to improve conformance
- Drafting requirements and choosing appropriate keywords
- Structuring specification sections
- Converting plain language to RFC 2119 format
- Separating normative requirements from informative guidance
- Progressively refining specifications section-by-section

## Instructions

### 1. Load Reference Guide

Read `references/rfc-2119-guide.md` for keyword definitions, decision tree, structure patterns, normative/informative separation patterns, validation checklist, and examples.

### 2. Support Creation and Iteration

Primary use case: Help create conformant specifications through active writing and iteration.

**Creating:** Guide structure, suggest patterns (Conformance Levels, Content Focus, Typical Content + Requirements), help draft with keywords, establish normative/informative separation, reference plan-spec.md and tasklist-spec.md examples.

**Iterating:** Convert plain language to RFC 2119 requirements, refine keyword choices, add informative labels, restructure for clarity, validate and suggest refinements.

**Quick assistance:** Answer keyword questions during writing, provide labeling guidance, clarify normative vs informative, suggest patterns, reference decision tree.

**Validation:** Check conformance when ready, identify violations with line numbers, count keywords, suggest improvements.

### 3. Iterative Writing Workflow

Support this cycle: **Draft section → Keyword requirements → Label informative content → Validate → Refine → Next section**

Provide guidance at any step. Support jumping between steps as writing progresses naturally.

### 4. Apply Decision Tree

```text
Is requirement critical for correctness/safety/core functionality?
├─ Yes → MUST / MUST NOT
└─ No → Strongly recommended for quality?
    ├─ Yes → SHOULD / SHOULD NOT
    └─ No → Completely optional?
        └─ Yes → MAY / OPTIONAL
```

Provide keyword with example in context, rationale, reference to similar usage, and consideration of what happens if not met.

### 5. Reference Common Patterns

From guide: Conformance Levels (Level 1/2/3), Content Focus (MUST/MUST NOT), Typical Content + Requirements (separation), Common Mistakes → Best Practices (educational). See `references/rfc-2119-guide.md` for detailed examples and code.

### 6. Common Workflows

**Write requirements section:** Suggest structure pattern, help draft with keywords, separate examples from requirements, validate.

**Choose keywords while drafting:** Read draft, apply decision tree, suggest keywords with rationale, show transformation, explain implications.

**Convert plain language to RFC 2119:** Identify requirements vs explanations vs examples, apply keywords, add informative labels, structure using patterns, validate.

**Structure specification:** Understand scope, suggest conformance level approach, recommend organization, reference plan-spec.md or tasklist-spec.md, provide template.

**Make draft conformant:** Identify plain imperatives → RFC keywords, unlabeled examples → informative labels, subjective terms → measurable criteria, validate, refine.

**Refine keyword strength:** Analyze context, apply decision tree (what if not met?), consider conformance implications, recommend with rationale.

### 7. Provide Actionable Guidance

**Structuring:** Section organization from patterns, templates with RFC 2119 structure, references to similar specs.

**Keywords:** Specific keyword with context example, WHY it matches criticality, before/after, what happens if violated.

**Separation:** Identify normative (requirements) vs informative (guidance/examples), exact labels ("(Informative)", "Best Practice:", "Tip:"), placement, restructure if needed.

**Iteration:** Read draft, identify improvements, prioritize (critical first), refine section-by-section, validate and iterate.

**Validation:** Run checklist, report keyword counts, list issues with fixes, assess conformance, suggest next improvements.

## Resource Structure

Self-contained with bundled resources:

- **SKILL.md** - Core instructions for creation and iteration
- **references/rfc-2119-guide.md** - Complete reference (12K): definitions, decision tree, patterns, validation checklist, examples, external resources

Load reference guide for detailed patterns and validation criteria.

---

**Support active creation and iterative refinement. Write conformant specifications correctly from the start, then progressively improve.**
