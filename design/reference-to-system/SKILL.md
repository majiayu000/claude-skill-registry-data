---
name: reference-to-system
description: Derive a complete, traceable atomic UI system from a product’s intent, roles, functions, user flows, states, constraints and reference material. Use when an AI coding or design agent must plan or audit the foundations, components, variants, templates and validation coverage for an app, website or digital product; reconstruct missing flows before design; turn briefs, folders, flowcharts or reference interfaces into a component inventory; or let a designer focus on aesthetics without overlooking structural UI requirements.
---

# Reference → System

Build the smallest sufficient UI system from product behaviour. Keep structural coverage deterministic and aesthetic decisions human-led.

## Workflow

### 1. Inspect available sources

Read the files or folders the user provides. Classify each source as approved requirement, owner decision, canonical output, system artifact, QA evidence, historical material or decorative reference. Never treat a visual reference as permission to copy its style.

Preserve the decision trace:

```text
source → observation → rule → artifact → validation
```

### 2. Run the intake gate

Read [references/intake-contract.md](references/intake-contract.md). Establish:

- what the product must do and must not do;
- users, roles and permissions;
- core and secondary functions;
- user flows, screen maps or flowcharts;
- data objects and integrations;
- loading, empty, error, success and permission states;
- devices, input modes and accessibility constraints;
- technical, legal and content constraints.

Ask only for missing information that materially changes the structure. If no flow artifact exists, reconstruct a draft flow with the user and label it `proposed`. Do not proceed as though an unknown core flow were verified.

### 3. Register requirements and flows

Assign stable IDs. Separate `verified`, `implemented-not-verified`, `planned`, `proposed`, `historical`, `excluded` and `not-documented`.

Use the starter project in `assets/starter-project/` when creating machine-readable output. Copy it into the user’s chosen destination, or run:

```bash
python3 scripts/bootstrap_project.py /path/to/new-project \
  --name "Product name" \
  --purpose "What the product enables"
```

### 4. Build the coverage matrix

Read [references/coverage-model.md](references/coverage-model.md). Create one coverage row for every meaningful requirement, flow step and state. Derive UI patterns before naming components.

Do not jump from screenshots to components. Use this sequence:

```text
requirement → flow → step → state → UI pattern → component → template → validation
```

### 5. Consolidate the atomic system

Read [references/design-system-contract.md](references/design-system-contract.md). Consolidate repeated patterns into:

- foundations and semantic/context tokens;
- atoms;
- molecules;
- organisms;
- templates.

Each component must reference the requirements it satisfies, its dependencies, supported states and responsive behaviour. Create components because flows require them, not because a generic library usually contains them.

Keep appearance open unless the user supplied an approved visual direction. The designer owns typography, colour, spacing, density, composition, imagery and motion character.

### 6. Define templates and validation

Define templates only after component coverage is known. Cover canonical, narrow and wide widths, short and long content, relevant themes or contexts, keyboard focus, reduced motion where applicable and error recovery.

Run:

```bash
python3 scripts/validate_project.py /path/to/project
python3 scripts/build_inventory.py /path/to/project
```

Fix every error before calling the system structurally complete. Warnings may remain only when clearly documented as future work.

## Non-negotiable gates

- Cover every core function, flow step and state.
- Give interactive components `default`, `hover`, `pressed`, `focus` and `disabled` states unless a state is demonstrably inapplicable.
- Keep references and dependencies valid and non-circular.
- Distinguish a proposal from verified evidence.
- Do not fabricate product decisions, metrics or accessibility results.
- Do not publish client data, private links, source design files, third-party assets or identifiers.
- Do not call a design system complete solely because a component count is high.

## Handoff

Return:

1. confirmed inputs and unresolved decisions;
2. requirements and flow summary;
3. coverage gaps, if any;
4. atomic inventory and dependency notes;
5. template coverage;
6. validation result and explicit limits;
7. the next aesthetic decisions for the designer.
