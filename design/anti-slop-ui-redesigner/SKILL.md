---
name: anti-slop-ui-redesigner
description: Use when a frontend project, webpage URL, or UI screenshot feels generic, template-like, visually weak, unresponsive, or visibly AI-generated and needs a product-specific redesign with preserved behavior and verified implementation.
---

# Anti-Slop UI Redesigner

Turn one authorized page into an evidence-backed audit and a verified redesign. Deliver real code changes or a runnable standalone implementation. Never stop at a critique, mockup, or list of suggestions.

## Select the input mode

Read [input-modes.md](references/input-modes.md), select exactly one mode, and state it.

| Mode | Source | Required delivery |
| --- | --- | --- |
| `project` | Local code project | Modify the project and preserve its contracts |
| `url` | Authorized webpage URL | Capture it in a real browser; build original runnable code |
| `screenshot` | UI screenshot | Preserve visible truth; build a runnable page and label assumptions |

Process one page. Infer product purpose, primary user, route, and must-preserve behavior from available evidence. Ask one focused question only when a missing fact would materially change the implementation.

Do not copy third-party source, brand assets, copy, icons, imagery, or distinctive identity. Do not invent features, customers, testimonials, metrics, or hidden interactions.

Resolve the absolute directory containing this `SKILL.md` and assign it to `REDESIGN_SKILL`. Invoke bundled tools with `node "$REDESIGN_SKILL/scripts/redesign.mjs"`; never assume the user's working directory contains this Skill.

## Create the brief

Run:

```bash
node "$REDESIGN_SKILL/scripts/redesign.mjs" brief \
  --mode project \
  --source /absolute/source/path \
  --page /target-route \
  --purpose "Concrete product purpose" \
  --user "Primary user" \
  --preserve "navigation, forms, real content" \
  --output ui-redesign
```

Change `--mode` and `--source` for `url` or `screenshot`. Review `brief.json` and record visible assumptions.

## Establish evidence before editing

For `project`, inspect repository instructions and scripts, start the page, and test its primary behavior. For `url`, confirm authorization and inspect public visual and DOM evidence without taking source code.

For `screenshot`, preserve the original and create a non-fabricated baseline:

```bash
node "$REDESIGN_SKILL/scripts/redesign.mjs" ingest-screenshot \
  --source /absolute/path/interface.png \
  --output ui-redesign/before
```

Treat responsive and interaction behavior as unproven. The Review Board will label the repeated original image as `Source`, not as three captured breakpoints.

For every runnable source, capture mobile, tablet, and desktop simulators at 375, 768, and 1440 widths:

```bash
node "$REDESIGN_SKILL/scripts/redesign.mjs" capture \
  --url http://127.0.0.1:3000/target \
  --output ui-redesign/before \
  --channel chrome
```

Omit `--channel chrome` when Playwright Chromium is installed. Inspect the screenshots, console findings, accessibility results, and `interaction-baseline.json`. Exercise important controls; DOM presence alone does not prove behavior.

## Audit and choose a direction

Run:

```bash
node "$REDESIGN_SKILL/scripts/redesign.mjs" audit \
  --manifest ui-redesign/before/capture-manifest.json \
  --output ui-redesign
```

Apply [audit-rubric.md](references/audit-rubric.md) to extend `audit.md`. Every issue needs evidence, impact, a concrete change, and an acceptance criterion.

Use [design-direction.md](references/design-direction.md) to derive one product-specific direction. Write `selected-direction.md` and `design-tokens.json`. Do not apply a fixed “premium” house style.

## Implement, then verify

Follow [implementation-playbook.md](references/implementation-playbook.md).

- In `project` mode, preserve routes, data flow, component contracts, content truth, and recorded behaviors. Change the smallest coherent file set.
- In `url` or `screenshot` mode, copy `$REDESIGN_SKILL/assets/standalone-template/` to `ui-redesign/implementation/`, then replace its placeholders with an original, dependency-free page.

Implement in stages: tokens; structure; typography and color; components; responsive states; restrained motion. Test primary controls after each stage.

Capture the redesigned page to `ui-redesign/after`, then run:

```bash
node "$REDESIGN_SKILL/scripts/redesign.mjs" qa \
  --brief ui-redesign/brief.json \
  --before ui-redesign/before/capture-manifest.json \
  --after ui-redesign/after/capture-manifest.json \
  --interactions ui-redesign/before/interaction-baseline.json \
  --output ui-redesign

node "$REDESIGN_SKILL/scripts/redesign.mjs" review-board \
  --before ui-redesign/before/capture-manifest.json \
  --after ui-redesign/after/capture-manifest.json \
  --candidate-url http://127.0.0.1:4173 \
  --output ui-redesign/review-board
```

Open the Review Board and visually compare all three widths. Automated checks cannot judge hierarchy, product specificity, or whether the result still looks generated.

## Completion gate

Read [output-contract.md](references/output-contract.md). Do not claim completion unless:

- real code changes or a runnable standalone implementation exist;
- before/after evidence exists at 375, 768, and 1440 widths for runnable sources; screenshot mode preserves the original source and captures the implementation at all three widths;
- baseline controls and primary behaviors remain present and tested;
- there is no horizontal overflow or new console error;
- controls have accessible names, visible focus, and adequate touch targets;
- contrast and reduced-motion checks pass;
- `audit.md`, `selected-direction.md`, `design-tokens.json`, `interaction-baseline.json`, the Review Board, and `qa-report.md` exist.

Return `fail` for a critical behavior regression or unusable page. Return `conditional pass` for a runnable implementation with explicit non-critical assumptions or warnings. Make limitations visible.

## Common mistakes

- Treating gradients, cards, pills, or centered heroes as defects without product evidence.
- Restyling before recording behavior and responsive evidence.
- Copying a reference site instead of deriving an original direction.
- Claiming success from a single desktop screenshot.
- Hiding uncertain screenshot behavior instead of reporting assumptions.
