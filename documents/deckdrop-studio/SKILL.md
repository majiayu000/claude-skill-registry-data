---
name: deckdrop-studio
description: Build, run, troubleshoot, or extend a DeckDrop-style macOS slide workflow that turns PDFs, docs, presentations, and image sets into editable PowerPoint drafts with human review before export. Use when Codex needs to work on a workspace containing `DeckDropApp`; inspect the ingestion, extraction, planning, review, and export pipeline; regenerate the Xcode project; or validate the DeckDrop app and tests.
---

# Deckdrop Studio

Use this skill for a DeckDrop or slide-generation workspace. If the current repo contains `DeckDropApp` and `project.yml`, use that workspace by default. Otherwise, pass `--workspace /path/to/workspace` to the runner script.

## Quick Start

1. Read `references/project-map.md` for the current pipeline map and main files.
2. Run `bash scripts/run_deckdrop_studio.sh doctor`.
3. Run `bash scripts/run_deckdrop_studio.sh inspect` to confirm the workspace shape.
4. Use `bash scripts/run_deckdrop_studio.sh test` after pipeline or UI changes.
5. Use `bash scripts/run_deckdrop_studio.sh build` when you need the app product or export pipeline compiled.
6. Use `bash scripts/run_deckdrop_studio.sh open` to jump into Xcode.

## Workflow

### Source Intake

- Keep one primary source of truth unless the user explicitly asks for a multi-primary workflow.
- Support PDFs, documents, presentations, and images as primary sources, with optional support docs and images.
- Keep the visible intake summary high-signal: pages or slides, words, tokens, support counts, and warnings.

### Draft-First Deck Generation

- Favor a review-first flow: build an editable draft deck, let the user edit slide titles, body text, and captions, then export the final `.pptx`.
- Preserve source order and wording unless the user asks for a rewrite-heavy presentation.
- Treat "extract everything" as an additive mode that appends raw or reference slides instead of replacing the polished deck.

### Editing Guidance

- Read `project.yml` before changing targets, entitlements, or bundle resources.
- Keep DeckDrop app-local except for intentional reuse from `VibeWidgetCore`, such as Keychain-backed secrets.
- Pipeline logic belongs in `DeckDropApp/Sources/Services/`; menu bar and draft-editor UX belongs in `DeckDropApp/Sources/Views/`.
- The Python extractors and Node writer are part of the product contract. Update them together with the Swift call sites when payloads or output shapes change.

### Validation

- Run `doctor` before builds if the local setup is unknown.
- Run `test` after parsing, planning, export, or model changes.
- If you change export structure, verify the editable deck, manifest, and optional split or preview artifacts still exist.
- If you change source-type support, make sure the same staged-input and build-request flow still covers PDF, document, presentation, and image paths.

## Resources

- `scripts/run_deckdrop_studio.sh`: workspace detection and local `doctor`, `inspect`, `generate`, `open`, `build`, and `test` commands.
- `references/project-map.md`: target layout, pipeline map, source and artifact contract, and key files.
