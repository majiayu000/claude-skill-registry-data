---
name: domain-model
description: Stress-test a plan against existing domain language, code behavior, and durable decisions. Use when the user wants DDD/domain-model grilling, glossary refinement, terminology challenges, context documentation, ADR candidates, or plan validation against a repo's language.
---

# domain-model

Run a relentless domain-modeling interview that sharpens a plan against the repo's existing language, code, and decisions. Ask one question at a time, include your recommended answer, and wait for feedback before continuing.

## Core behavior

- Walk the design tree branch by branch, resolving dependent decisions in order.
- Ask exactly one question per turn, with a recommended answer and the evidence behind it.
- If code or existing docs can answer the question, inspect them instead of asking.
- Challenge terms against the glossary or known domain language immediately.
- Sharpen vague or overloaded words into precise canonical terms.
- Stress-test relationships with concrete scenarios and edge cases.
- Cross-reference user claims with code; surface contradictions directly.
- Record terms and decisions as they crystallize instead of batching them at the end.

## Before the first question

1. Identify the target plan, Beads task, target repo, and any active alignment or contract file.
2. Read relevant harness context first:
   - `bd show <id>` for the active issue when one exists.
   - `knowledge/_shared.yaml` and the relevant `knowledge/repos/<repo>.yaml`.
   - `.tmp/work/<TASK-ID>-alignment.md` or interface contracts when provided.
3. Explore the target repo before interviewing:
   - Existing domain docs: `CONTEXT-MAP.md`, `CONTEXT.md`, `docs/adr/`, and context-local `docs/adr/`.
   - Code terms: exported types, entities, events, routes, database tables, command names, and tests.
   - Prior decisions in Beads comments, especially `design:` and `worklog:` notes.
4. Summarize the current model in two or three sentences, then ask the first unresolved question.

## Persistence

Default to Agent Forge persistence unless the target repo already has domain docs or the user asks for them.

- Prefer `knowledge/` for durable repo/domain facts that future agents should reuse.
- Use Beads comments for issue-scoped discoveries:
  - `design:` for terminology, boundaries, and decision rationale.
  - `worklog:` for session progress and investigation notes.
- When a target repo already has `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR conventions, update those files inline as terms or decisions are resolved.
- When the user explicitly requests target-repo docs, create or update `CONTEXT.md` and `docs/adr/` lazily using the reference formats.
- Do not create real domain docs just because this skill was loaded; create them only when there is resolved content to record.

See:

- `references/CONTEXT-FORMAT.md` for glossary/context structure.
- `references/ADR-FORMAT.md` for minimal ADR guidance.

## Session loop

For each unresolved branch:

1. Check whether the answer is already in code, tests, knowledge, Beads, `CONTEXT.md`, or ADRs.
2. If the answer is discoverable, report the finding and cite the evidence.
3. If the answer needs human judgment, ask one question only.
4. Include a recommended answer in the same turn:
   - Name the canonical term or boundary you recommend.
   - Explain the trade-off or invariant it protects.
   - Mention what documentation would change if accepted.
5. Wait for feedback before asking the next question.
6. When the user accepts or corrects a term or decision, record it immediately in the chosen persistence target.

## Challenge rules

### Glossary conflicts

When the user uses a term differently from existing language, stop and reconcile it:

> `CONTEXT.md` defines "Cancellation" as voiding an entire Order, but this plan uses it for removing one line item. Should the canonical term be "Line-item removal" instead?

### Fuzzy language

When a word is overloaded, propose a precise term:

> You said "account." Do you mean **Customer**, **User**, **Tenant**, or **Billing Account**? I recommend **Billing Account** because the scenario is about invoices and payment ownership.

### Concrete scenarios

Probe boundaries with examples:

> If an Order has three shipments and one shipment fails, does Billing reverse the whole Invoice or issue a partial Credit? I recommend modeling **Credit** separately from **Cancellation** so fulfillment failures do not rewrite order history.

### Code contradictions

Check claims against implementation:

> The plan says partial cancellation is allowed, but `Order.cancel()` currently cancels the whole order and tests only cover full cancellation. Which behavior is authoritative?

## ADR threshold

Offer an ADR only when all three are true:

1. The decision is hard to reverse.
2. The decision would surprise a future reader without context.
3. The decision reflects a real trade-off among viable options.

If any condition is missing, record the rationale in Beads or knowledge instead of creating an ADR.

## Done

End the session with:

- Resolved terms and decisions.
- Remaining ambiguities, each phrased as a single next question.
- Where durable context was recorded, or why nothing was written.
- Any code/documentation contradictions that still need follow-up work.
