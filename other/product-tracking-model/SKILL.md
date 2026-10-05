---
name: product-tracking-model
description: "Model a product before telemetry work by defining users, value moments, entities, lifecycle states, and decision questions. Use when asked to map a product for analytics, define what a product does, prepare a tracking model, or establish a telemetry foundation. Turkish triggers: ürün analitik veri modeli, event taksonomisi, kimlik ve property sözleşmesi."
---

# Product Tracking: Model

Create a compact product model that makes later telemetry decisions traceable. Do not select an analytics vendor, add SDKs, or send data.

## Workflow

1. Read only the product materials and repository areas the user put in scope.
2. Separate confirmed facts from assumptions. Ask only for facts that materially change the model.
3. Define:
   - primary user roles and accountable organizations;
   - the smallest meaningful value moment;
   - core entities and their stable relationships;
   - lifecycle states, permissions, and meaningful transitions;
   - product questions that evidence should answer.
4. Identify sensitive fields. Prefer pseudonymous identifiers and data minimization; do not include secrets, free-form user content, regulated data, or unnecessary identifiers in telemetry.
5. Produce a reviewable model before designing events.

## Deliverable

Use this structure in conversation or, when the user requests project artifacts, propose `.telemetry/product-model.md`:

```text
Product outcome
Users and organizations
Core value moment
Entities and relationships
Lifecycle states and transitions
Decision questions
Known unknowns and privacy boundaries
```

## Quality bar

- Every proposed event later must map to a decision question or value moment.
- Do not turn every click into a product event.
- Mark inference clearly; never pretend a codebase proves product intent.
- Hand off to `product-tracking-audit` for current reality or `product-tracking-plan` for the target design.
