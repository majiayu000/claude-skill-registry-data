---
name: app-publishing
description: Publish a tested Robium application as a coherent project page, article, and media set.
---

# App publishing

Let the application and its real runs own the facts; publishing gives those
facts one clear public identity.

## Start from recorded reality

- Publish only after the application's normal smoke passes. If the story
  presents a hosted path, its hosted smoke must pass too.
- Read the app manifest, README, architecture record, case study, and run
  artifacts before changing copy or visuals.
- Keep runtime and capability facts in `robium-app.yaml`, article framing and
  media in `docs/case-study.md`, and current availability in the website.
- Read [publication-contract.md](references/publication-contract.md) when
  adding metadata, joining app and article records, or deciding which
  repository owns a field.

## Tell one human story

- Lead with the result, tension, or decision that makes this app worth
  reading. State run conditions next to the claims they qualify.
- Explain the decisions a reader cannot infer from the README. Keep one tested
  path and leave exhaustive commands and troubleshooting in the app.
- Cover the outcome, decision, important system boundaries, tested path,
  result, Robium's contribution, and limits without forcing identical public
  headings.
- Read [editorial-system.md](references/editorial-system.md) for drafting or
  revising prose, and [article-starter.md](references/article-starter.md) when
  creating a portable case study.

## Use media honestly

- Real-run media shows what happened. A diagram explains how the pieces
  connect. Generated art may illustrate a concept but must not resemble or
  replace application output.
- Preserve the conditions and source record behind captures. Use literal alt
  text and captions that say whether a frame is simulated, recorded, or live.
- Read [asset-workflow.md](references/asset-workflow.md) when preparing the
  hero, system diagram, social card, motion, or optional conceptual art.

## Keep the surfaces coherent

- Overview, Live, Guide, cards, metadata, and source links share one app ID,
  project identity, navigation, status vocabulary, and visual language.
- Reuse the project shell and lifecycle components. Keep a special robot
  viewer or result panel in a small adapter until a second consumer proves it
  belongs in shared code.
- Read [visual-system.md](references/visual-system.md) when styling project
  surfaces. Do not leak parent styles into embedded Gradio, Foxglove,
  Lichtblick, or other tools.
- Route gateway, orchestrator, and cloud runtime mechanics to `live-demo`.

## Done

- Every public claim traces to repository-owned facts or a scoped real run.
- The application, article, metadata, and media join on one stable identity.
- Overview, Guide, and Live states work on desktop and mobile, including a
  readable unavailable state.
- Deployment, paid capacity, production enablement, and external publication
  remain separately authorized actions.
