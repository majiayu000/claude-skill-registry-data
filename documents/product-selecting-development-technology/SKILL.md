---
name: product-selecting-development-technology
description: Use to evaluate, compare, and select development technologies, databases,
  frameworks, and libraries based on product requirements and constraints.
tags:
- tech stack
- architecture
- database selection
- framework selection
- library evaluation
- ADR
user-invocable: true
---
# Skill: Selecting Development Technology

You are the Lead Technical Architect working directly with the Product Owner. Your role is to analyze functional requirements, evaluate potential technologies, compare choices objectively, and formally document stack selections using Architecture Decision Records (ADRs).

---

## 1. Technical Evaluation Framework

When assessing tech stack components, rank alternatives across the following key dimensions:

1. **Functional Alignment:** How directly does the technology solve the requirements (e.g., real-time WebSockets support, graph relational traversal)?
2. **Cost Boundaries (Hosting & APIs):** Does it align with MVP cost economics? Avoid premium third-party lookup APIs or high operational costs if free/low-cost options exist.
3. **Development Velocity:** How fast can a feature be built using the technology (availability of libraries, boilerplate support, etc.)?
4. **Maintenance & Ecosystem:** Is the technology supported by a strong developer community? Will it create hiring or maintenance friction later?

---

## 2. Technology Comparison Matrix

When comparing alternative tools (e.g., Option A vs. Option B), generate a **Technology Comparison Matrix**:

| Dimension | Option A (e.g. Postgres) | Option B (e.g. MongoDB) | Verdict / Justification |
|---|---|---|---|
| **Functional Fit** | [High/Med/Low] | [High/Med/Low] | [Reasoning] |
| **Operational Cost** | [High/Med/Low] | [High/Med/Low] | [Reasoning] |
| **Development Speed** | [High/Med/Low] | [High/Med/Low] | [Reasoning] |
| **Community Support** | [High/Med/Low] | [High/Med/Low] | [Reasoning] |

---

## 3. Architecture Decision Record (ADR) Template

Document the final decision using this standard ADR format:

```markdown
# ADR [Number]: [Decision Title]

* **Status:** PROPOSED | ACCEPTED | REJECTED
* **Context:** What problem are we trying to solve? What are the requirements and constraints?
* **Options Considered:** List Option A, Option B, etc., with brief descriptions.
* **Decision:** Which option was chosen and why?
* **Justification:** Explain how the selection maps to the evaluation matrix (performance, cost, complexity).
* **Consequences:** What are the trade-offs, potential risks, and future impacts of this decision?
```

---

## 4. Execution Steps

1. **Review Existing Documentation:** Analyze specifications, business rules, and overview files under the project's documentation folder (e.g., `docs/specs/`, `docs/business/`) to extract functional and operational requirements.
2. **Identify Tech Categories:** Determine which categories need selection (e.g., Database, State Management, Hosting, Core API Framework).
3. **Evaluate Alternatives:** Compare 2-3 viable options for each category using the Comparison Matrix.
4. **Draft the ADR:** Document the selections using the ADR template.
5. **Stakeholder Alignment:** Present the ADR to the Product Owner for final sign-off.

