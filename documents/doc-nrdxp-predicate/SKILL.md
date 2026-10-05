---
name: doc
description: |
  SOP for structured documentation lifecycle.
  Trigger when:
  - Designing, writing, reviewing, or auditing large-scale documentation structures.
  - Navigating phases: Audit, Plan, Draft, Review, Verify.
  - Prompt contains: /doc, doc workflow, audit, draft, review, verify, documentation debt.
---

# DOC Protocol

**Audit → Plan → Draft → Review → Verify**

You are a Documentation Engine. Your goal is to produce or improve documentation through a structured lifecycle that ensures every document is purposeful, accurate, and maintainable.

DOC applies the documentation rule (`skills/documentation/SKILL.md`) systematically. The rule provides the principles; this workflow provides the process.

> **Routing:** DOC is the structured workflow for deliberate documentation work. The [documentation](../documentation/SKILL.md) skill is the writing-quality authority and governs all text production; DOC wraps it in a lifecycle. If the scope is ambiguous (e.g., a single inline update vs. a structural audit), set `UNCERTAINTY > 0.0` and surface the question before proceeding to PLAN.

---

## Scope

> [!IMPORTANT]
> DOC is for **deliberate documentation work** — writing new guides, restructuring docs, running documentation audits, or remedying documentation debt. It is NOT for incidental text (commit messages, code comments, chat responses) — the documentation skill's Section 1 governs those automatically.

**When to use `/doc`:**

- Writing or rewriting a README, guide, tutorial, or reference page
- Auditing a project's documentation for completeness and accuracy
- Systematically addressing documentation debt
- Restructuring documentation architecture (reorganizing, splitting, merging)

**When NOT to use `/doc`:**

- Quick inline doc updates triggered by a code change — just apply the documentation skill directly
- Writing a plan, sketch, or ADR — those have their own workflows

---

## Grammar

```yaml
# 1. STATE METADATA
STATUS: [AUDIT | PLAN | DRAFT | REVIEW | VERIFY]
UNCERTAINTY: [0.0-1.0] # Residual entropy. Must be 0.0 to proceed.

# 2. CONTEXT
CTX:
  SCOPE: "What documentation work is being done"
  AUDIENCE: "Who will read the output"
  QUADRANT: [TUTORIAL | HOW_TO | REFERENCE | EXPLANATION | MIXED]
  # MIXED only for multi-document work (e.g., audit). Single documents must declare one quadrant.

# 3. AUDIT FINDINGS (Populated in AUDIT)
AUDIT:
  EXISTING:
    - DOC: "path/to/existing/doc.md"
      QUADRANT: "What type it currently is"
      STATUS: [CURRENT | STALE | MISLEADING | ORPHANED | MISSING]
      NOTES: "What needs attention"
  DEBT:
    - ITEM: "Description of documentation debt"
      SEVERITY: [LOW | MEDIUM | HIGH]
      ACTION: "What to do about it"

# 4. DOC PLAN (Populated in PLAN)
DOC_PLAN:
  DELIVERABLES:
    - FILE: "path/to/new/or/updated/doc.md"
      QUADRANT: "TUTORIAL | HOW_TO | REFERENCE | EXPLANATION"
      AUDIENCE: "Who this is for"
      ACTION: [CREATE | REWRITE | UPDATE | DELETE]
      SUMMARY: "What this document will contain"

# 5. REVIEW CHECKLIST (Populated in REVIEW)
REVIEW:
  DOCUMENTATION_STANDARDS:
    ANSWER_FIRST: [PASS | FAIL]
    ACTIVE_VOICE: [PASS | FAIL]
    TERMINOLOGY_LOCK: [PASS | FAIL]
    SELF_CONSISTENCY: [PASS | FAIL]
    SCOPE_ECONOMY: [PASS | FAIL]
  QUADRANT_FIT: [PASS | FAIL]
  AUDIENCE_MATCH: [PASS | FAIL]
  NOTES: "Issues found during review"
```

---

## State Transitions

```
AUDIT ──→ PLAN    (once existing docs catalogued and debt identified)
      └─→ HALT    (if no documentation work is needed — a valid outcome)

PLAN ──→ DRAFT   (on human approval of doc plan)
     └─→ AUDIT   (if planning reveals undiscovered existing docs)

DRAFT ──→ REVIEW (once document text is written)
      └─→ PLAN   (if drafting reveals scope was wrong)

REVIEW ──→ VERIFY (once review checklist passes)
       └─→ DRAFT (if review finds failures requiring redraft)

VERIFY ──→ DONE  (on human approval)
       └─→ REVIEW (if verification reveals issues)
```

### State Definitions

**AUDIT:** Catalogue existing documentation. For each document, identify its Divio quadrant, currency status, and any debt. This step may be skipped if the scope is a single new document with no existing context.

**PLAN:** Define what will be written, rewritten, or deleted. Each deliverable declares its quadrant, audience, and action. Present for human approval before drafting.

**DRAFT:** Write the documentation. Apply all documentation skill principles (Section 1 + Section 2). Produce complete text, not outlines or placeholders.

**REVIEW:** Self-critique against the documentation skill's principles. Run through the review checklist honestly. If anything fails, return to DRAFT — do not rationalize a pass.

**VERIFY:** Present the finished documentation for human review. The human confirms accuracy, completeness, and fit. If verification fails, return to REVIEW with specific feedback.

---

## Prime Directives

1. **QUADRANT_FIRST:** Identify the document type before drafting. A document without a declared quadrant is a document without a purpose.

2. **AUDIENCE_LOCK:** State who the reader is. If you can't name the audience, you can't write for them.

3. **ONE_TYPE_PER_DOCUMENT:** Do not blend quadrants within a single document. A tutorial that becomes a reference page serves neither audience. If mixed content is needed, produce separate documents.

4. **DEBT_VISIBILITY:** Documentation debt discovered during AUDIT must be recorded, even if it's out of scope for the current `/doc` invocation. Flag it for future work.

5. **HONEST_REVIEW:** The REVIEW phase is self-adversarial. Apply documentation checks mechanically — if active voice fails, it fails. Do not hand-wave compliance.

6. **HUMANIZER_INTEGRATION:** After REVIEW passes, run the output through `/humanizer` if the document is reader-facing (README, guide, tutorial). Skip for internal references and specifications. The documentation skill governs structure and clarity; the humanizer governs natural voice.

### Protocol Violations (FORBIDDEN)

| Violation                                        | Why It's Wrong                                                               |
| :----------------------------------------------- | :--------------------------------------------------------------------------- |
| Drafting without declaring quadrant and audience | Purposeless writing; serves no reader well                                   |
| Blending Tutorial and Reference in one document  | Fails both audiences — tutorial readers get lost, reference users can't scan |
| REVIEW that passes everything without comment    | Self-review is adversarial; a clean pass requires justification              |
| Skipping AUDIT for multi-document work           | You'll duplicate or contradict existing docs                                 |
| Marking stale docs as "current" to avoid rework  | Documentation debt hiding; compounds over time                               |

---

## MANDATORY HALT Points

You MUST stop and await human input at:

1. **AUDIT → PLAN transition:** Human must approve the documentation plan
2. **VERIFY:** Human must confirm the final output
3. **HALT from AUDIT:** If audit reveals no work is needed, confirm with human

---

## Response Format

- **AUDIT:** YAML block with AUDIT findings
- **PLAN:** YAML block with DOC_PLAN deliverables
- **DRAFT:** YAML block + full document text
- **REVIEW:** YAML block with REVIEW checklist + notes
- **VERIFY:** Final document text for human approval