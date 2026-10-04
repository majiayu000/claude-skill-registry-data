---
name: product-design
description: Experimental end-to-end product-design orchestrator that frames project context, retrieves research, models experience flows, defines visual direction, creates artifacts, and validates rendered outcomes. Use only when explicitly asked for "end-to-end product design", "design this feature end-to-end", "redesign this flow", "build an experience from this brief", or "create a product experience". Use the stable specialist skills for isolated audits, dashboards, AI features, design systems, handoff, or case studies.
metadata:
  version: "1.1.1-main"
  argument-hint: "[product brief, evidence, source files, or URL]"
---

# Product Design

> Experimental foundation. Retrieval quality, context persistence, and end-to-end behavioral benchmarks are still being expanded. Do not present this skill as production-ready or use it implicitly.

Produce a coherent product experience, not a collection of fashionable screens. Ground decisions in the user's evidence and constraints, preserve choices already made, and expose uncertainty that could materially change the design.

## Route before working

Use this skill for end-to-end creation or redesign. For a narrow request, use the specialist skill directly:

- existing artifact diagnosis: `ux-ui-audit`;
- analytical workspace or KPI surface: `dashboard-redesign`;
- AI capability or agent experience: `ai-product-design`;
- component library or token review: `design-system-review`;
- approved-design specification: `handoff-to-dev`;
- portfolio narrative: `case-study-writer`.

Combine specialist skills only when their distinct output is required. Load only the repository resources needed for the task.

## 1. Establish project context

Build the smallest context model needed for the decision. Read [references/project-context.md](references/project-context.md) and use `data/project-context.schema.json` when context must persist or be validated.

Distinguish:

- supplied facts and constraints;
- observed evidence;
- reasonable inferences;
- unresolved assumptions;
- decisions already made by the user.

Preserve the user's chosen direction unless evidence or constraints invalidate it. Ask only when a missing answer would materially change the result; otherwise state the assumption and continue.

Validate persisted context:

```bash
SKILL_DIR="/absolute/path/to/product-design"
python3 "$SKILL_DIR/scripts/validate_context.py" "/absolute/path/to/project-context.json"
```

## 2. Research for a decision

Read [references/research-workflow.md](references/research-workflow.md) when current evidence, benchmarking, user research, market context, or precedent is needed.

Start with the decision the research must change. Separate product evidence, standards, empirical research, expert guidance, competitor behavior, and visual inspiration. Current or consequential claims require current primary sources. Competitor frequency is precedent, not user need.

Research output must end in design implications, rejected assumptions, and remaining uncertainty—not a link inventory.

## 3. Retrieve applicable knowledge

Use the bundled search for focused guidance when Python is available:

```bash
SKILL_DIR="/absolute/path/to/product-design"
python3 "$SKILL_DIR/scripts/search.py" --query "<dominant design problem>" --context design-context/project-context.json --limit 5 --diagnostics
```

Resolve `SKILL_DIR` from this skill's loaded `SKILL.md`; never assume the user's project is the skill directory. Omit `--context` when no persisted context exists. Use one dominant intent per query. Verify why each result applies. Accept abstention; use labeled general reasoning or gather missing context instead of forcing a weak match.

The seed data is intentionally small. Read [references/knowledge-governance.md](references/knowledge-governance.md) before adding or importing records.

Validate the knowledge file after changes:

```bash
python3 "$SKILL_DIR/scripts/validate_data.py"
```

## 4. Model the experience

Read [references/design-reasoning.md](references/design-reasoning.md). Define:

- user intent and success;
- entry, orientation, decision, action, feedback, recovery, and completion;
- information architecture and object relationships;
- required states, permissions, and failure paths;
- content and data needed at each decision;
- platform, input, responsive, and accessibility behavior.

Resolve the product model before visual styling. Marketing pages, transactional flows, expert tools, dashboards, public-service sites, and safety-critical systems must not inherit one another's default structures.

## 5. Establish visual direction

Read [references/visual-direction.md](references/visual-direction.md) for UI creation or substantial redesign.

When direction is unsettled, propose two or three genuinely different approaches and compare their task fit, brand fit, implementation cost, accessibility risk, and failure mode. Once the user has selected a direction, develop it rather than reopening the choice.

Commit to:

- one visual thesis;
- hierarchy and composition logic;
- density and spacing character;
- typography roles and rationale;
- semantic color behavior;
- imagery and icon language;
- motion purpose and restraint;
- one recognisable signature element;
- clichés and conflicting treatments to avoid.

**Constraint:** Industry alone does not determine aesthetics; cards, gradients, glass, dark mode, large headings, illustrations, and animation require a product or brand reason.

## 6. Create and inspect

Build at the fidelity requested. Preserve real content, interactions, data relationships, and existing brand constraints.

For implemented or interactive work, inspect the rendered result at relevant content breakpoints and critical states. Exercise the primary path with the intended input modes. Correct visible, interaction, accessibility, overflow, state, and console failures, then inspect again.

Completion requires rendered inspection; source code or a static ideal state is insufficient.

## 7. Evaluate the outcome

Read [references/evaluation.md](references/evaluation.md). Evaluate against the original decision and task, not preference alone. Separate:

- confirmed defects;
- risks requiring verification;
- deliberate tradeoffs;
- opportunities;
- strengths that must be preserved.

Use the relevant specialist audit after creation when the scope warrants it. A self-review is not evidence of user comprehension.

## Expected deliverable

Scale the output to the request. A complete engagement can include:

1. context and decision frame;
2. evidence-backed research synthesis;
3. experience model, journey, IA, and state requirements;
4. selected visual direction and design-system decisions;
5. screens, prototype, or implementation;
6. rendered validation findings and corrections;
7. unresolved questions and next validation step.

Generate only the artifacts needed to complete the user's task.

## Quality gate

Before delivery, confirm:

- **Context and evidence (§1–3):** sources are traceable; facts, observations, inferences, preferences, and unknowns remain distinct; nothing is invented.
- **Experience model (§4):** structure fits the task, with critical states, permissions, and recovery paths.
- **Visual direction (§5):** choices follow the selected thesis and supplied product or brand rationale.
- **Rendered result (§6):** critical paths, states, accessibility, overflow, interactions, and console behavior were inspected and corrected.
- **Outcome (§7):** conclusions preserve valid user decisions, match performed checks, and identify remaining verification.

If a check fails, return to its phase, correct the gap, and run the gate again.
