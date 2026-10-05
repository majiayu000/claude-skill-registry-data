---
name: readme-writing
description: How to write a README that gets a project understood and running fast — lead with what/why, a 60-second quickstart, then usage, config, contributing, and license. Covers required sections, show-don't-tell examples, scannability, badges, and failure modes. Use when writing or auditing a project README.
type: skill
version: 2.0.0
updated: 2026-06-29
---
# README Writing

The README is the **front door** of a project. Most readers arrive with one of three jobs: *decide if
this is worth their time*, *get it running*, or *find one specific answer*. A good README serves all
three in the order they appear — orientation first, action second, depth on demand. This skill is the
deep reference for writing one: the required sections, the writing moves that make it scannable, the
runnable-example discipline, and the failure modes that quietly drive readers away. Heavy detail lives
in `references/`; copy-paste material in `examples/`; a runnable linter in `scripts/`.

## Mental model

A README is read in **three passes**, and you write top-to-bottom to match them:

| Pass | Reader's question | What answers it |
|---|---|---|
| Skim (10s) | "What is this and is it for me?" | Title + one-line description + badges |
| Try (60s) | "Can I get it running?" | Install + minimal quickstart |
| Use (later) | "How do I do X specifically?" | Usage, configuration, links to deeper docs |

Optimize ruthlessly for the first 60 seconds. A reader who can't tell what the project does, or who
hits a broken install command, leaves and does not come back. Everything else is recoverable; the first
screen is not.

## The required sections (in order)

A complete README has these, roughly in this sequence. Not every project needs every one, but you must
make a deliberate choice to omit, never an accidental one.

1. **Title + one-line description** — what it is and who it's for, no preamble, no "Welcome to".
2. **Badges** — build status, version, license, coverage. Signal of health, scanned in a glance.
3. **Why / value** — the problem it solves, optionally a screenshot, GIF, or short result example.
4. **Install** — the minimal commands to get the dependency in place, copy-pasteable and verified.
5. **Quickstart / Usage** — the smallest end-to-end example that produces a visible result.
6. **Configuration** — options, env vars, defaults — as a table, not prose.
7. **Contributing** — how to set up a dev environment and the contribution flow (link to `CONTRIBUTING.md`).
8. **License** — the SPDX name and a link to the `LICENSE` file.

The full anatomy, with what to include and skip per project type (library vs CLI vs service vs
framework), is in `references/anatomy.md`.

## Lead with what and why

The opening is the most-read and most-botched part. State the **what** in one line, then the **why**.
Do not bury it under a logo, a table of contents, or a wall of badges.

```markdown
# Forge

Forge builds and maintains AI agents and skills through a self-improving maker/checker loop —
so your automation gets better on every run instead of rotting.

[![build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![npm](https://img.shields.io/npm/v/forge)]()
[![license](https://img.shields.io/badge/license-MIT-blue)]()
```

Within two sentences the reader knows the category (agent tooling), the mechanism (maker/checker loop),
and the payoff (self-improving, no rot). Compare the anti-pattern: *"Welcome to Forge! Forge is a
powerful, flexible, modern, enterprise-grade platform for..."* — three adjectives and zero information.
See `references/writing-style.md` for the full list of filler phrases to cut.

## The 60-second quickstart

The quickstart is a promise: *paste these commands and see it work.* It must be **copy-pasteable**,
**self-contained**, and **actually run** — test it in a clean checkout before shipping.

```markdown
## Quick start

\`\`\`bash
git clone https://github.com/acme/forge && cd forge
npm install
npx forge audit ./my-project    # prints a scorecard
\`\`\`

You should see a table of findings within a few seconds. Next, try `forge fix` to apply them.
```

Rules that make or break it:

- **Show the expected output**, or at least describe it ("you should see a table"). A command with no
  visible result leaves the reader unsure it worked.
- **One happy path only.** Do not branch into "if you use yarn / pnpm / bun" in the quickstart — pick
  one, link the rest. Optionality kills momentum.
- **No undeclared prerequisites.** If it needs Node 20+, a running Postgres, or an API key, say so
  *before* the commands, not in a stack trace the reader hits later.

## Show, don't tell

Prose describing behavior ages badly and is hard to trust. A **runnable example** is self-verifying —
either it works or the reader sees it break. Prefer concrete examples over adjectives at every turn.

```markdown
## Usage

\`\`\`js
import { Forge } from 'forge';

const forge = new Forge({ target: './my-project' });
const report = await forge.audit();

console.log(report.score);        // 87
console.log(report.findings[0]);  // { rule: 'no-secrets', severity: 'high', file: '.env' }
\`\`\`
```

The inline comments showing return values turn a snippet into documentation. This is why `examples/`
ships a `good-readme-example.md` and a `README.template.md` you can adapt — see *Files in this package*.

## Make it scannable

Readers skim, they do not read. Structure for the eye:

- **Headings every few paragraphs** so the table of contents (and the reader's scroll) has anchors.
- **Tables for anything with structure** — config options, CLI flags, comparison matrices. A 5-row
  table beats two paragraphs of "the `--depth` flag controls...".
- **Code blocks for anything runnable**, always fenced with a language for syntax highlighting.
- **Short paragraphs.** One idea each. Walls of text are scrolled past, not read.
- **Link out for depth.** The README is a launchpad, not the manual. Link to `docs/`, the wiki, or a
  hosted site rather than inlining a 200-line configuration reference.

Audience calibration matters too: a library README assumes a developer who will read code; a CLI
README assumes someone who wants commands; an end-user app README assumes neither. Details in
`references/anatomy.md`.

## Common pitfalls (failure modes)

- **The broken quickstart.** Commands that don't run in a clean checkout — stale flags, missing
  `install` step, undeclared env var. The single most damaging README bug. Test it cold.
- **Burying the lede.** A logo, badge wall, or 30-line table of contents before the one-line
  description. The reader scrolls looking for "what is this" and gives up.
- **Adjective soup.** "Powerful, flexible, blazing-fast, enterprise-grade" — these are unfalsifiable
  and information-free. Replace with a concrete capability or benchmark.
- **Telling instead of showing.** Paragraphs describing the API instead of a code block using it.
- **The novel.** Inlining the entire configuration reference, changelog, and architecture doc. The
  README becomes unmaintainable and unscannable. Link out.
- **Drift.** Examples that no longer match the current API because nobody re-ran them. Treat README
  snippets as testable artifacts (see `scripts/lint-readme.mjs` and `references/maintenance.md`).
- **No license.** A repo with no `LICENSE` is, legally, all-rights-reserved — nobody can safely use it.
  Always state the license.

## When NOT to write a heavy README / trade-offs

A README is not the right home for everything, and more is not better:

- **Deep, multi-page docs** belong in a `docs/` site (Docusaurus, mdBook, ReadTheDocs), not the README.
  A README that scrolls for ten screens has failed at being a front door. Link instead.
- **API reference** that's mechanically derivable (TypeDoc, rustdoc, Sphinx) should be generated, not
  hand-written into the README where it will drift.
- **Internal-only / throwaway repos** may need only a title and a one-line run command — don't gold-plate
  a README nobody outside the team will read.
- **Monorepos** often want a thin root README that routes to per-package READMEs, rather than one giant
  document trying to cover every package.

The trade-off is always **completeness vs. scannability**. When they conflict, scannability wins in the
README and completeness moves to linked docs.

## Files in this package

- `references/anatomy.md` — full section-by-section anatomy + what to include per project type
- `references/writing-style.md` — voice, filler phrases to cut, scannability techniques, badges
- `references/maintenance.md` — keeping a README honest: testing snippets, drift, automation in CI
- `examples/README.template.md` — a fill-in-the-blanks starter README with every required section
- `examples/good-readme-example.md` — a complete, worked example README for a sample CLI tool
- `scripts/lint-readme.mjs` — runnable Node check that a README has the required sections + a quickstart code block

Pairs with the `documentation-structure` skill (for organizing the wider `docs/` tree the README links
into) and the `technical-writer` agent (for tightening prose and voice). Also see the `changelog-writing`
skill for the companion `CHANGELOG.md`.
