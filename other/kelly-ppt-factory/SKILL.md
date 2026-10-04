---
name: kelly-ppt-factory
description: Busabase-backed project-based PPT production App-in-Skill. Use when the user invokes $kelly-ppt-factory or /kelly-ppt-factory, mentions PPT factory, 规模化 PPT, bulk PPTX, batch decks, reusable PowerPoint style systems, presentation production workflows, pitch decks, sales decks, training decks, report decks, slide-card/storyboard planning, style-consistent deck generation, PPTX QA, or wants to manage many PPTX files through project to deck to slide card to review to generate to render QA.
metadata:
  category: production
  tags:
    - risk:local-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-ppt-factory
    resources:
      - projects
      - decks
      - slide-cards
      - style-systems
      - qa-checks
      - exports
      - settings
    risk: local-write

---

# Kelly PPT Factory

## Overview

Kelly PPT Factory is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. It manages a project-based workflow where each deck is
planned as slide cards first, reviewed like storyboard shots, then generated
into PPTX and rendered for QA. The default user is an operator producing
many style-consistent decks across use cases such as pitch decks, sales
materials, training decks, reports, proposals, and courseware.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, give the user the clickable AirApp URL. Start localhost only
when local preview/debugging is explicitly requested; it uses the same
Busabase resources and never offers another data provider. Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-ppt-factory-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's artifact and product
contracts, stop before the unavailable Busabase operation, and report the
exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly PPT Factory overview"></td>
    <td width="50%"><img src="assets/screenshots/review.webp" alt="Kelly PPT Factory review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>PPT factory dashboard with project, deck, slide-card, QA, and style-score counters.</td>
    <td><strong>Review queue</strong><br>Slide-card and deck approvals before the agent generates or revises PPTX output.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/slides.webp" alt="Kelly PPT Factory slide cards"></td>
    <td width="50%"><img src="assets/screenshots/exports.webp" alt="Kelly PPT Factory exports"></td>
  </tr>
  <tr>
    <td><strong>Slide cards</strong><br>Storyboard-style page specs: objective, layout, copy, visual brief, interaction, style checks, and QA flags.</td>
    <td><strong>Exports</strong><br>PPTX outputs, render paths, generation status, and QA evidence for each deck.</td>
  </tr>
</table>

## Boundary

- The AirApp reads projects/decks/slide-cards/style-systems/QA/exports from
  Busabase and lets a reviewer approve, request changes on, block, or revise
  a slide card or deck — it never generates a PPTX file itself (the browser
  cannot write a binary file to disk).
- Generating the actual `.pptx` file is a trusted skill-root process
  (`scripts/generate_pptx.mjs`), and only ever for a deck whose
  `decision_action` is a genuine `approve` recorded by the review queue —
  never bare status, which a spoofed import could otherwise set directly.
- `scripts/execute_decisions.mjs` never generates a file or flips workflow
  status itself; it only records a planned follow-up operation
  (`execution_status`/`operation`/`target`/`detail`) on each decided row.
- External delivery, client email, file uploads, paid image generation, or
  production publishing are approval-required and should be executed by
  another explicit skill after the user approves.
- Treat client source materials, style references, and generated decks as
  private. Never commit a local credential file, Busabase secrets, or the
  gitignored `exports/` output directory.

## Busabase Resources

Seven Bases under one application Folder (`kelly-ppt-factory`), declared in
`content/kelly-ppt-factory-app/app/js/config.js` and the generated template sidecars under `content/` — see
`references/ppt-factory-schema.md` for exact field shapes:

- `projects`: a client / use-case / theme batch.
- `decks`: one PPTX deliverable under a project — status, slide counts,
  style score, output paths, and the review-queue decision
  (`decision-action`/`decision-note`/`decided-at`) on the same row.
- `slide-cards`: the storyboard unit for one PPTX page — objective, layout,
  structured content, asset brief, style/QA checks, and the review-queue
  decision on the same row.
- `style-systems`: reusable presentation style kits — palette, fonts,
  visual/layout rules, component library.
- `qa-checks`: deterministic or human QA evidence for a deck, slide, or
  export.
- `exports`: generated PPTX output records — path, render path, generation
  status, QA summary.
- `settings`: default client profile and export preferences, one row.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space.

## Review Queue

A slide card or deck is "in the review queue" when it carries a non-empty
`review-summary` (the agent's note on what needs a human look). The reviewer
chooses `approve` / `request_changes` / `block` / `revise`; the decision and
its resulting workflow `status` are written directly onto the slide card's
or deck's own Busabase row (`content/kelly-ppt-factory-app/app/js/providers/busabase-provider.js`'s
`decideItem()`) — there is no separate decisions bucket, since Busabase
reads are always live. From a standalone local preview the write merges
immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge, per the AirApp
boundary in `$busabase-app-creator`.

## PPT Factory Workflow

1. Collect inputs: client style samples, old PPT screenshots/PPTX, briefs,
   outlines, source docs, target audience, deck count, page count, use case,
   and export deadline.
2. Create or update the style kit first (`style-systems`). Extract palette,
   fonts, slide families, image rules, component library, and density
   limits.
3. Create projects and decks. One project is a client/use-case/theme batch;
   one deck is one PPTX deliverable.
4. Draft slide cards before generating PPTX. Each card must include
   objective, layout, title/copy, support layers, presenter notes or
   interaction, asset brief, style checks, and QA flags.
5. Send slide cards or whole decks to `#/review`. Only a deck with a genuine
   `approve` decision is generatable.
6. Generate PPTX with `node scripts/generate_pptx.mjs --deck=<deck_id>` (the
   real generation engine, using `pptxgenjs`) or a richer `pptx` skill pass.
7. Render and visually QA the PPTX. Record QA evidence in `qa-checks`.
8. Export completed PPTX paths and report exactly which files were written.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-ppt-factory-app dev` only when local preview/debugging is explicitly
requested.

## Views

- `#/overview`: PPT factory dashboard — project/deck/slide totals, human
  attention summary, style-kit preview, recent review queue.
- `#/projects`: project list — client/use case, stage, deck count, slide
  count, status.
- `#/decks`: deck list — theme, level, slide counts, style score, PPTX/render
  paths.
- `#/slides`: slide-card workbench — page objective, layout, copy, support
  layers, presenter notes, asset brief, style checks, QA flags.
- `#/review`: review queue — workflow states (`needs_review` /
  `changes_requested` / `approved` / `generated` / `done` / `blocked`),
  decision buttons, review note.
- `#/style`: reusable style kit — palette, fonts, visual rules, layout
  rules, component library.
- `#/exports`: generated output records — PPTX path, render path, QA
  summary.
- `#/settings`: sanitized config — default client profile, style default,
  export prefs, onboarding state. Never expose secret values.

## Demo Mode

- `?demo=overview`, `?demo=projects`, `?demo=decks`, `?demo=slides`,
  `?demo=review`, `?demo=style`, `?demo=exports`, `?demo=settings` open
  deterministic mock scenes for documentation and screenshots. It never
  reads or writes Busabase and never claims a real connection.
- `lang=en` or `lang=zh` forces UI chrome language; with `lang=zh` the demo
  content is meaningfully localized.

## Trusted Scripts

```bash
node skills/kelly-ppt-factory/scripts/generate_pptx.mjs --deck=<deck_id>
node skills/kelly-ppt-factory/scripts/execute_decisions.mjs --apply
```

Both connect with their own credentials (`BUSABASE_BASE_URL`,
`BUSABASE_API_KEY`, `BUSABASE_SPACE_ID`), never the AirApp's ambient
session. `generate_pptx.mjs` is the only script that writes an actual
`.pptx` file (to `exports/`, gitignored) and is gated on a genuine
`approve` decision. `execute_decisions.mjs` never generates a file or
changes workflow status; it only records a planned follow-up.

## Completion Criteria

Finish only when:

- the skill contains the complete canonical `content/kelly-ppt-factory-app/` project and
  `pnpm --dir content/kelly-ppt-factory-app dev` remains supported;
- all persistent config, state, and domain data use `busabase-sdk` and the
  declared resource map — no local JSON, browser storage, or provider
  choice;
- Vault values and API credentials never reach browser-visible surfaces;
- local setup offers Cloud/custom URL OAuth plus the explicit Demo path,
  while a deployed AirApp uses its ambient session;
- Overview, Projects, Decks, Slide cards, Review, Style, Exports, and
  Settings render on desktop and phone widths;
- `pnpm --dir content/kelly-ppt-factory-app run check` and `node --test` pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is
ambiguous, the current user lacks permission, or a same-slug resource is not
application-owned. Never generate or deliver bulk PPTX directly from raw
content without a slide-card review pass. Do not shrink text to fit — split
the page or revise content. Treat render QA as required for client-facing
decks. If style samples conflict, stop and ask which sample is canonical
before scaling the system.
