---
name: prd-review-challenger
description: "Critical review of PRDs, feature specs, and product decision documents — acts as a devil's advocate to surface weak assumptions, missing requirements, implementation risks, and logical gaps. Use when a PM or team lead wants to stress-test a document before team review, validate a spec before development starts, or identify what's missing in a product decision. Triggers RU: «проверь PRD», «разбери спецификацию», «найди дыры в PRD». Triggers EN: 'review my PRD', 'challenge my spec', 'find holes in my PRD', 'critique my feature spec'. Do not use for writing or rewriting PRDs."
version: 1.0.0
---

# Skill: prd-review-challenger

Acts as a devil's advocate for PRDs, feature specs, and product decisions. Surfaces
weak spots, hidden assumptions, logical gaps, and overlooked risks — before the
document goes to the team or into development.

---

## Triggers

**Russian:** «проверь PRD», «разбери спецификацию», «найди дыры в PRD», «покритикуй спецификацию», «ревью PRD», «challenger для PRD», «что упущено в спецификации».
**English:** "review my PRD", "challenge my spec",
"find holes in my PRD", "critique my feature spec", "stress-test my PRD",
"what's missing in my spec"

---

## Language Detection

Detect the language of the input document — respond in that language.
If a different language is explicitly requested, use it.

---

## Input

**Required:** text of a PRD, feature spec, or product decision description
(pasted directly into the conversation or provided as a file).

**Optional:** context that sharpens the critique:
- product target audience
- project stage (0→1, scaling, redesign)
- strategic constraints (timeline, tech stack, budget)
- the angle that matters most right now (UX, technical complexity, business risks)

## Output

A structured review report with five sections:

1. Weak spots and hidden assumptions
2. Open questions — what the PRD doesn't answer
3. Implementation and UX risks
4. Alternative approaches to consider
5. Completeness checklist with rating

---

## Instructions

### Step 1 — Accept the Document and Assess Its Type

Receive the document text. Identify the document type:

| Document type | Action |
|--------------|--------|
| Full PRD / feature spec | Proceed to Step 2 |
| Too short (< 3 paragraphs) | State: "The document is too short for a full review — I'll give feedback on what's available and list what's structurally missing" |
| Technical document (not a PRD) | Apply the same critical approach; open with: "This is a technical document, not a PRD — I'll review it as a specification" |
| Request to write a PRD | Decline: this skill critiques, it does not create. Suggest `product-management:write-spec` |

### Step 2 — Completeness Checklist

Assess whether each component is present. This provides the structural foundation
for the critique in Steps 3–4.

Mark each item: present (✓), absent (✗), partial (△), not applicable (—).

**For PRDs and feature specs:**

- Problem and its scope (problem statement + evidence)
- Target audience / personas
- User stories or usage scenarios
- Acceptance criteria (measurable definition of done)
- Edge cases and non-standard scenarios
- Success metrics (how we'll know the feature works)
- Out of scope (what we explicitly are not doing)
- Technical constraints and dependencies
- Rollback / plan B on failure
- Impact on other parts of the product

**For technical documents (design doc, architecture doc, migration plan) —
replace non-applicable items:**

- Problem and its scope (applicable)
- Owner and reviewers (instead of "Target audience")
- Failure scenarios and boundary states (instead of "User stories")
- Success criteria / test plan (instead of "Acceptance criteria")
- Infrastructure edge cases (applicable)
- Performance metrics and observability (instead of "Feature metrics")
- Out of scope (applicable)
- Dependencies and preconditions (applicable)
- Rollback plan (applicable)
- Impact on adjacent systems (instead of "Product impact")

Mark "—" only when an item is objectively inapplicable to the document type.
A missing item is a finding for the critique — not just a formality.

### Step 3 — Four-Axis Critique

Produce the critique as four sections. Each section must contain specific
observations with references to the document (direct quote or section reference).
Do not give generic feedback ("needs better description") — give specifics
("section X states Y, but does not explain Z").

**Section 1: Weak spots and hidden assumptions**
Find statements treated as facts that have not been validated or justified.
Format: "The document assumes [X] — but this has not been proven / verified /
conflicts with [Y]."

**Section 2: Open questions**
List questions the document doesn't answer but engineers or designers will
definitely ask. Format: "What happens if [scenario]?",
"How does the system behave when [condition]?"

**Section 3: Implementation and UX risks**
Identify two types of risks:
- Technical: non-obvious complexity, dependencies, performance, security
- UX: non-obvious behavior for the user, friction, interface edge cases

For each risk: description + potential consequence if left unaddressed.

**Section 4: Alternative approaches**
Propose 2–3 alternatives to the chosen approach — not to replace it, but to
confirm the decision is deliberate. Format: "Alternative: [description] —
trade-off: [upside] vs [downside]."

### Step 4 — Final Output

Close with two blocks:

**Completeness assessment** — the checklist from Step 2 as a table:
component, status (✓/✗/△/—), brief comment on missing items.

**Top 3 priorities** — the three most critical gaps to close before development
starts. Format: numbered list, one sentence per item.

---

## Constraints

- Does not write or rewrite PRDs — critique only
- Has no domain knowledge about the specific product without provided context
- Does not replace review with actual stakeholders, engineers, and designers
- Does not provide legal, financial, or technical expert assessments without
  relevant context
- If the PRD is confidential (NDA, internal), the user takes responsibility
  for sharing the content
