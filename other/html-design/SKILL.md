---
name: html-design
description: Create, redesign, repair, validate, preview, and package lightweight standalone HTML deliverables. Use for marketing experiences, product prototypes, infographics, motion narratives, documents, browser tools, dashboards, guided workflows, knowledge interfaces, mini-games, presentations, reusable style and brand systems, and local-model text, vision, image, or code tools that must run without a build chain or hosted service.
---

# HTML Design

Build the usable application, not a page that describes it. Default to one self-contained `index.html` with inline CSS and JavaScript. Keep the result inspectable, portable, and runnable from local storage.

## Route The Request

Choose a deliverable type, interaction kind, and model capability independently.

Deliverable types:

- `application`: an operational browser app; inferred for ordinary tool, dashboard, guided, and knowledge work.
- `marketing`: launch, campaign, conversion, or brand storytelling.
- `prototype`: a testable product concept, service flow, or interaction hypothesis.
- `infographic`: visual explanation, comparison, process, map, timeline, or data story.
- `motion`: a time-based composition, kinetic explainer, or interactive sequence.
- `document`: a reading-first report, guide, case study, manual, or long-form narrative.
- `game` and `presentation`: inferred from their matching interaction kinds.

Application kinds:

- `tool`: calculators, converters, generators, forms, inspectors, and focused utilities.
- `dashboard`: metrics, comparisons, trends, filters, and decision views.
- `guided`: multi-step configuration, diagnosis, review, and structured workflows.
- `knowledge`: guides, notes, FAQs, summaries, and organized reference material.
- `game`: lightweight touch-friendly games with a complete play loop.
- `presentation`: full-screen HTML narratives with keyboard navigation and print output.
- `motion`: animated HTML compositions with a timeline, playback controls, and reduced-motion fallback.

Model capabilities:

- `none`: browser logic only. Use this by default.
- `text`: text generation or transformation.
- `vision`: image understanding, OCR, chart reading, or screenshot analysis.
- `image`: image generation through a configured local endpoint.
- `code`: code-oriented generation or explanation through the chat endpoint.

Read [references/design-workflow.md](references/design-workflow.md) before creating or substantially redesigning an interface. Read [references/deliverables.md](references/deliverables.md) for the selected artifact contract. Read [references/kind-contracts.md](references/kind-contracts.md) for `tool`, `dashboard`, `guided`, `knowledge`, `game`, or `presentation` starter work. Read [references/request-routing.md](references/request-routing.md) when choosing or composing scenarios from a natural-language brief. Read [references/scenario-blueprints.md](references/scenario-blueprints.md) when a benchmark fixture or reusable domain scenario applies. Read [references/style-registry.md](references/style-registry.md) and [references/visual-directions.md](references/visual-directions.md) to select and adapt a subject-specific visual system.

For games, also read [references/games.md](references/games.md). For presentations, also read [references/presentations.md](references/presentations.md). For motion, use the dedicated `motion` kind and validate its timeline, playback controls, and reduced-motion fallback. For model-enabled apps, also read [references/local-models.md](references/local-models.md). Before delivery, read [references/quality-checklist.md](references/quality-checklist.md).

## Workflow

1. Inspect the audience, environment, core task, inputs, outputs, data sensitivity, and required states.
2. Choose the deliverable type and interaction kind, then write a compact contract. Use `recommend --brief` when a registered single scenario or multi-scenario composition may fit.
3. Choose one visual direction independently of the scenario. Filter the style registry when a reusable family is appropriate; otherwise define a custom direction.
4. Preserve working domain logic when modifying an existing app.
5. Preserve all decision-relevant user content; do not invent data, metrics, or conclusions.
6. For presentations, select an existing brand pack first. When no brand applies and visual ambiguity is consequential, generate three real-content style previews rather than asking for abstract adjectives.
7. Scaffold only when no useful implementation exists.
8. Replace starter content and behavior with the actual task; a registry style is a seed, not a finished theme.
9. Implement empty, ready, working, success, partial, error, and reset states where relevant.
10. Validate with `scripts/webapp.py validate --strict`.
11. Run the primary workflow in a real browser at desktop, narrow mobile, and 320 px widths. For fixed-stage presentations, inspect the scaled composition rather than reflowing it.
12. Build a zip only when the user needs a distributable package.

## Scaffold

List supported kinds:

```bash
python3 scripts/webapp.py kinds
python3 scripts/webapp.py deliverables
python3 scripts/webapp.py styles
python3 scripts/webapp.py scenarios
python3 scripts/webapp.py contracts
python3 scripts/webapp.py recommend --brief "<user request>"
```

Create a browser-only app:

```bash
python3 scripts/webapp.py scaffold \
  --kind tool \
  --out <folder> \
  --title "<title>" \
  --summary "<purpose>"
```

Create a styled prototype:

```bash
python3 scripts/webapp.py scaffold \
  --deliverable prototype \
  --kind guided \
  --style crafted-research \
  --out <folder> \
  --title "<title>" \
  --summary "<testable hypothesis>"
```

Create a scenario-specific artifact with a fixed domain contract, a default style, and structural checks:

```bash
python3 scripts/webapp.py scaffold \
  --scenario prototype-route-planner \
  --out <folder> \
  --title "<title>" \
  --summary "<testable hypothesis>"
```

Override the scenario's default visual family without changing its task contract:

```bash
python3 scripts/webapp.py scaffold \
  --scenario prototype-route-planner \
  --style neo-swiss-editorial \
  --out <folder> \
  --title "<title>" \
  --summary "<testable hypothesis>"
```

Create a branded presentation:

```bash
python3 scripts/webapp.py scaffold \
  --kind presentation \
  --brand <built-in-id-or-brand-pack-path> \
  --out <folder> \
  --title "<title>" \
  --summary "<narrative purpose>"
```

Create a model-enabled app:

```bash
python3 scripts/webapp.py scaffold \
  --kind tool \
  --ai text,vision \
  --out <folder> \
  --title "<title>" \
  --summary "<purpose>"
```

Supported kinds are `tool`, `dashboard`, `guided`, `knowledge`, `game`, `presentation`, and `motion`. Supported model capabilities are `none`, `text`, `vision`, `image`, and `code`. Use `styles --json`, `scenarios --json`, `contracts --json`, and `recommend --json` to consume versioned registries and routing output. Base starters for the six established kinds carry executable kind contracts and design dials; a scenario may replace that base contract with a stronger domain-specific blueprint. Scenario and style are independent axes: a scenario provides workflow and semantic checks, while `--style` provides a visual system and overrides `defaultStyle`. Brand packs and registry styles are mutually exclusive during scaffolding because explicit brand identity takes precedence.

Do not scaffold over a non-empty directory. Treat starters as interaction engines, not finished themes or domain implementations.

For presentation visual discovery, generate a temporary board with the actual title and purpose:

```bash
python3 scripts/webapp.py styleboard --out <folder> --title "<title>" --summary "<purpose>"
```

List reusable brand seeds with `python3 scripts/webapp.py brands`. Create a custom pack with:

```bash
python3 scripts/webapp.py brand-init --from neutral-corporate --out <brand-folder> --name "<brand name>"
```

Read [references/presentations.md](references/presentations.md) before editing a pack. Keep brand identity in `brand.json`, local logo assets, and optional `brand.css`; keep slide-specific overrides in the deck.

## Architecture Threshold

- Use one `index.html` for browser APIs, modest state, local data, ordinary model tools, and lightweight games.
- Keep small SVG, CSS, and JavaScript inline when that improves portability.
- Use separate local files only for large media, complex game logic, workers, WASM, or an HTML file that has become difficult to maintain.
- Keep the project purely static even when files are split.
- Do not introduce React, Tailwind, npm, or a build chain solely for visual polish.
- Do not add a manifest unless the user's own workflow requires metadata.

## Local Models

Keep model credentials outside the app. Never embed keys, tokens, or authorization headers in HTML.

Copy `.webapp.local.example.json` to `.webapp.local.json`, configure an OpenAI-compatible local endpoint and model, then run:

```bash
python3 scripts/webapp.py serve <folder> --open
```

The local server exposes same-origin `/runtime/ai/chat`, `/runtime/ai/image`, and `/runtime/health` routes. It reads credentials only from the environment variable named by `apiKeyEnv`.

For model-free apps, direct file opening can work when browser security rules allow it. Prefer the local server for reliable module loading, file access, clipboard behavior, and browser testing.

## Validate And Build

Run:

```bash
python3 scripts/webapp.py validate <html-file-or-folder>
python3 scripts/webapp.py validate <html-file-or-folder> --strict
python3 scripts/webapp.py validate <presentation> --strict --rendered
python3 scripts/webapp.py build <folder> --out <app.zip>
python3 scripts/webapp.py build <folder> --out <app.zip> --force
```

Treat strict static validation as the quality floor, not visual proof. Use rendered presentation validation when Playwright is available. Test real inputs, invalid inputs, reset, copy/download, persistence, asynchronous failure, and keyboard navigation as applicable.

The build command refuses to overwrite an existing archive unless `--force` is explicit. It excludes `.webapp.local.json`, Git data, caches, existing zip files, and development output.

Run the repository self-check after changing this skill, its scripts, or its starters:

```bash
python3 scripts/check_skill.py
```

## Optional Cover Assets

Generate a local fallback cover and icon only when the user needs them:

```bash
python3 scripts/generate_cover.py <folder> \
  --title "<title>" \
  --summary "<purpose>" \
  --kind <kind>
```

Treat generated artwork as a safe fallback. For presentation-sensitive work, create content-specific artwork based on the actual concept.
