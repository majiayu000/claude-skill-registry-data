---
name: docs
description: >-
    Review and update plainworks' documentation so it reads naturally and reflects the kit as it is
    today — keep Markdown paragraphs flowing without hard column wrapping, preserve intentional
    structure, sync commands, package/layer structure, gates, and examples with the actual code, fix
    stale links, drop history/plan narration, keep prose humanized and scannable with a task-first
    quickstart, and add mermaid diagrams where they clarify architecture or flow. Use when writing or
    auditing docs, repairing AI-generated hard wraps, after a change that makes docs outdated, or
    before a release.
user-invocable: true
---

# Reviewing and updating plainworks' docs

Documentation fails two ways: it falls out of **standard** (arbitrary source line breaks, history narration, dead links), and it becomes **out of date** (commands, package lists, layer map, gates, and examples that no longer match the code). This skill checks both. plainworks is foundation infrastructure consumers build on, so a stale doc misleads every downstream consumer. Run it over the whole `docs/` tree, a single file, or the docs touched by a change set.

The authoritative doc policy lives in the Documentation section of [`../../copilot-instructions.md`](../../copilot-instructions.md). The baseline wins over any local habit.

## Docs in scope

- `docs/**` — `architecture.md` and other design or policy docs.
- `README.md` and any top-level `*.md`; per-package `README.md` (the generator ships one per package).
- `.github/skills/**/SKILL.md` and their `references/*.md`; `.github/instructions/*.instructions.md`.
- TSDoc (`/** */`) and `//` comment prose in the packages in scope (these are docs too).

Never touch `tmp/` (gitignored scratch) and never add a committed doc that references it.

## Pass 1 — Standards (how it reads)

- **Flowing Markdown prose.** A Markdown paragraph is one continuous source line. Do not hard-wrap prose to a column or add source newlines to control how it looks at one width; renderers wrap for the reader's viewport. Collapse AI-generated hard wraps only within the same logical paragraph.
- **Preserve intentional structure.** Keep blank-line paragraph boundaries, headings, list items, blockquotes, tables, link definitions, mermaid diagrams, and fenced code blocks. Never join separate list items or paragraphs.
- **Code comments wrap (the exception to the rule above).** A `/** */` or `//` comment is read at its source column, not reflowed by a renderer — so wrap its prose to the Biome print width (100 columns), like the code it documents, instead of trailing off-screen on one line. Preserve TSDoc tags, directives, lists, tables, and code examples, and never join separate comment paragraphs. Run `bun run check-comments` to find over-width comments and `bun run format-comments` to reflow them (Biome never touches comment content).
- **No history/plan/process narration.** A doc or comment describes the system as it is now, not how it got here or what a plan intends. Delete "previously…", "we changed…", batch/plan/PR references, and TODO-narration.
- **`tmp/` stays uncommitted.** No committed doc references a `tmp/` plan or handoff note.
- **Frontmatter exemption.** YAML folded scalars (a skill's `description: >-`) already collapse to one logical line — leave their wrapping alone.

## Pass 2 — Up-to-date check (whether it's still true)

Verify each doc against the code it describes; a doc that lies is worse than none:

- **No legacy left behind.** Delete every mention of a removed or superseded API, option, file, or workflow. Never document a "deprecated", "legacy", or "old way" path next to the current one, because plainworks is alpha and keeps one current model (see [Development stage](../../copilot-instructions.md#development-stage-alpha-redesign-over-compatibility)).
- **Commands & gates** match the root `package.json` scripts and `turbo.json` (`bun run verify` and its `--list`, the individual gate scripts, `bun run gen package`, turbo `--filter` forms) — no renamed or invented script or flag lingers in the docs.
- **Package & layer structure** matches reality: the `packages/*` / `apps/*` / `internal/*` split and the L0–L4 layer map come from `internal/boundaries/layers.json`; the README, `docs/architecture.md`, and instructions copies are generated (`bun run sync-layer-map`) and `check-layer-map` fails on drift. Never hand-edit between the `layer-map` markers.
- **Governance table** (task runner, generator, build, lint, boundaries, version sync, tests, releases) names the tools actually in use.
- **The TS6-now/TS7-later rationale** stays accurate to the catalog pin and the boundaries guard.
- **Examples run.** Code/command snippets reflect current behavior and current APIs — never pseudo-code.
- **Atom docs match the lock.** Docs describe `elements` atoms as **vendored** and **locked** (`src/shadcn/`, pinned by `shadcn.lock.json`) with owned primitives in `src/atoms/`. A doc that calls vendored atoms editable, tells a reader to change one in place, or skips the **deviation ladder** (theme → call site → `ui` wrapper) is stale.
- **Screenshots match the UI.** App READMEs embed images that `ui:capture --docs` generates from the checkpoints marked `docs` (the showcase keeps them in `apps/showcase/docs/images/`). When a UI change makes one stale, rerun `bun run ui:capture --docs` in that app and look at the new images. Never edit or add one by hand.
- **Links resolve.** Internal relative links point at files that exist; other-repo references use full URLs, never bare `#123`.

## Pass 3 — Clarity & developer experience

A doc is for a developer skimming under time pressure. **Simple and organized beats complete** — a crowded, jargon-dense, or overlong explanation is a **defect**, not thoroughness, because the reader gives up on it. Optimize for the shortest organized version that still answers the question, using current documentation best practices rather than old habit.

- **Humanized, plain language.** Write for a developer skimming, not a spec lawyer. One idea per sentence; active voice, direct instructions ("Call `createStore`", "Run `bun run test`"). **Describe the benefit, not the mechanism** — what the reader can now do, not the internal shape — and name a representative identifier or two rather than dumping an exhaustive API list. Cut filler and hedging.
- **Scannable, uncrowded structure.** Meaningful headings, short lists, tables; bold the load-bearing terms; keep paragraphs to a few sentences. Never a wall of text.
- **Task-first, quickstart up top.** Lead with the shortest copy-pasteable path to a first working result, before deep reference. Know which Diátaxis mode each page is (tutorial / how-to / reference / explanation) and don't blend them.
- **Real, runnable examples.** Every non-trivial capability shows a real snippet against the current API — the common path first, then options and failure cases.
- **Diagrams where prose is the wrong tool.** For architecture, layer/dependency direction, a connection/reconnect flow, an auth handshake, or a state machine, add a focused `mermaid` diagram right where the concept is introduced — one idea per diagram, with a one-line caption so it degrades where mermaid isn't rendered. Don't diagram the trivial.
- **Every element earns its place.** Delete restated-obvious prose and decoration. Meaning over volume.

## Apply, then validate

Fix every instance of a pattern across the whole scope, not just the first hit. When repairing hard wraps, read and judge the Markdown structure rather than running a blind line-joining script. Then, if TSDoc/examples changed, typecheck/build the affected package:

```bash
turbo run typecheck build --filter=@plainworks/<name>
```

Prose-only changes need no build/test gate. Verify internal links by path before finishing.

## Commit

Use the [`commit`](../commit/SKILL.md) skill — one compact `docs:` Conventional-Commit line (e.g. `docs: sync architecture layer map with the boundaries config`). No `Co-authored-by` trailer, no plan/batch/tool narration.
