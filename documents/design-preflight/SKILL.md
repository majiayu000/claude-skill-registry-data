---
name: design-preflight
description: Use only when explicitly requested with $design-preflight, through design-preflight-with-docs, or through the full github-issue-delivery or azure-devops-work-item-delivery workflow before implementation, to examine hard-to-change design decisions, durable architecture, compatibility assumptions, and one-way-door risks.
---

# Design Preflight

Run a controlled `grilling` pass before design or implementation. Keep the interface small and the default lightweight.

A user's explicit request for `design-preflight-with-docs`, the full
`github-issue-delivery` workflow, or the full `azure-devops-work-item-delivery`
workflow delegates this preflight. A caller must forward the request and issue
or Work Item context; a reference to this skill alone is insufficient.

## Required Sub-Skill

**REQUIRED SUB-SKILL:** Use `grilling`.

This skill is a wrapper, not a replacement. Use `grilling` as the questioning engine and provide it with the brief below.

In every mode except `open`, inherit its fact-finding, recommended answers, and dependency-aware rounds. This wrapper overrides its exhaustive question scope, question budget, recommendation baseline, and completion rules with the rules below. In `open`, use `grilling` unchanged.

## Public Interface

| Invocation | Meaning |
|---|---|
| `$design-preflight` | Same as `durable`. |
| `$design-preflight durable` | Target-design stance: recommend the best end state for current requirements. |
| `$design-preflight conservative` | Preserve-current stance: recommend the smallest change that keeps existing behavior working. |
| `$design-preflight quick` | Blocker-only modifier. Combine with a stance (`conservative quick`); alone it uses `durable`. |
| `$design-preflight open` | Raw `grilling`; do not apply this skill's filtering. |

Treat unknown words as context hints, not CLI errors. Natural-language limits like "3 questions max" or "blockers only" are upper bounds.

## Stances

The stance sets the **baseline**: the default every recommendation and every unasked decision falls back to.

### durable

Default. Use when the design should move toward the best target, typically during active development.

Internal brief: `focus=one-way-door decisions`, `budget=5 soft`, `threshold=high`, `compatibility=not assumed`, `baseline=target design`.

The target design is the design you would choose for the current requirements if starting now. Recommend from it, not from the current structure. "Simplest" means the simplest end state, not the smallest diff. Within real constraints, prefer long-term maintainability, clear responsibilities and boundaries, and a single coherent model. Accept justified short-term migration work when it reduces long-term architectural debt. Base the design on current requirements and evidenced future constraints; add abstractions or extension points only for evidenced needs.

Do not assume backward compatibility is required. Treat compatibility as real only when the user, public contract, stored data, external integration, rollout plan, or operational reality makes it real. When such evidence appears, honor it and note in the handoff that `conservative` may fit this target.

Prefer questions that reveal whether to:

- make a breaking change now instead of adding a compatibility shim
- migrate or replace an old data model instead of supporting two models indefinitely
- create a cleaner boundary instead of matching the current structure
- remove or rename an awkward interface before it spreads
- accept short-term migration work to avoid long-term architectural debt

Refactoring and migration agreed in the preflight are part of the requested change, not unrelated refactors.

### conservative

Use when existing behavior is relied upon, typically for systems in operation.

Internal brief: `focus=one-way-door decisions`, `budget=5 soft`, `threshold=high`, `compatibility=assumed`, `baseline=current structure`.

Treat existing behavior, public contracts, stored data, and external integrations as compatibility constraints. Recommend the smallest change that fits the current structure and conventions. Propose a breaking change, migration, or boundary change only when the requirement cannot be met within the current structure, and ask before adopting it. Record target-design improvements as follow-up proposals; keep them out of the implementation.

Prefer questions that reveal whether:

- an assumed constraint has real dependents, or can be relaxed
- the change needs a migration, feature flag, or staged rollout
- a breaking change is unavoidable, and how to version or announce it
- an awkward existing interface must be extended rather than replaced

### quick

A modifier on either stance for when the user wants only blockers.

Internal brief: the stance's brief with `focus=blocker-level one-way-door decisions`, `budget=3 hard`, `threshold=blocker-only`.

Ask only questions where a wrong default is likely to force rework, migration, or a visible contract change.

### open

Use raw `grilling`. Do not impose this skill's one-way-door filter, stance, or question budget.

## Brief To Give Grilling

In every mode except `open`, start the `grilling` session with this brief, adding the selected stance's internal brief and baseline paragraph:

```text
This is a design preflight, not an open-ended interview.

Ask only questions whose answers affect hard-to-change design decisions.
Apply the selected mode's question budget across the whole session, not per round.
For each question, state the one-way door it affects and the cost if the default proves wrong.
Stop early if no question clears the bar.

Prioritize one-way-door risks: public contracts, data models, architecture boundaries, dependency direction, migration cost, rollout constraints, operational assumptions, security boundaries, and long-term maintenance cost.

Base every recommended answer on the stance's baseline.
Give each recommended answer a one-line reason. When viewpoints favor different answers, name each viewpoint and the answer it favors, such as short-term smallest change versus long-term maintainability, then give the overall recommendation from the stance's baseline and why.
When the evidence supports no recommendation, say so in place of one.
For durable: recommend from the target design and challenge compatibility-preserving defaults; ask whether compatibility is a real constraint or merely an assumed safe choice.
For conservative: recommend from the current structure and challenge changes that break existing behavior; ask whether a break is truly required.
```

## Question Bar

Ask only when the answer would materially change:

- public interfaces, contracts, data formats, or persisted schemas
- migration path, compatibility policy, or rollout constraints
- module boundaries, ownership, extension points, or dependency direction
- security, privacy, deployment, or operational assumptions
- long-term maintainability versus compatibility tradeoffs

Do not ask about:

- internal names or small implementation tactics
- reversible UI copy or local layout details
- test organization unless it affects public behavior or architecture
- preferences already covered by project conventions

## Question Budget and Completion

In every mode except `open`:

- Carry forward the user's stated preferences and settled decisions. Reopen them only when new evidence or a contradiction materially affects the design.
- In `durable` and `conservative`, aim for at most 5 questions. If high-impact, hard-to-change decisions remain unresolved, briefly explain why further questions are needed and ask only those questions.
- In `quick`, ask at most 3 questions. Explicit user limits are hard caps in every mode. Count separately answerable decisions separately; do not bundle them to evade a cap.
- Stop when no unresolved decision meets the selected question bar. Do not exhaust branches outside that scope. Settle decisions below the bar from the stance's baseline and repo conventions, and state the material ones as assumptions.
- If a hard cap leaves a high-impact decision unresolved, summarize it and its implications. Continue only work that does not depend on it; do not silently choose an answer or treat the cap as approval.
- Replace `grilling`'s blanket final confirmation with a brief handoff, then proceed within the user's already authorized scope. Still obtain any independently required approval. A request for preflight alone does not authorize implementation.

## Draft for a coordinator

When a delivery coordinator asks for a draft, the drafter cannot ask the user;
the coordinator holds the dialogue. Apply the selected mode's question bar,
budget, and recommendation rules as if asking, but return the questions instead
of asking them. Give each question the one-way door it affects, the cost if the
default proves wrong, its options, the recommended answer with its reason and
viewpoints, and the questions whose answers it depends on. Add the direction and
assumptions for decisions below the bar. A drafted recommendation is not an
accepted decision; do not proceed on it.

The coordinator asks the questions under the same budget and returns the user's
answers. When an answer changes a dependent question, revise that question
before the coordinator asks it. With the answers settled, give the handoff
under Output and proceed within the authorized scope.

## Output

In every mode except `open`, briefly summarize the stance, chosen direction, compatibility constraints to preserve, agreed breaking changes or migration work, remaining material assumptions or unresolved decisions, and, in `conservative`, target-design follow-up proposals. Omit empty categories. Keep this in the conversation unless a durable document is requested or required by repo conventions.

If no question clears the bar, say so briefly and give the applicable direction and assumptions without requiring an extra confirmation.
