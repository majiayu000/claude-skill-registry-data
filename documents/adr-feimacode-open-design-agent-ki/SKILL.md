---
name: adr
zh_name: "架构决策记录 ADR"
en_name: "ADR"
emoji: "🧭"
description: "An architecture decision record: context, the decision, its consequences and status, with links to the records it supersedes or is superseded by."
en_description: "An architecture decision record: context, the decision, its consequences and status, with links to the records it supersedes or is superseded by."
category: doc
scenario: engineering
tags: ["adr", "architecture decision", "decision record", "engineering", "架构决策"]
triggers:
  - "adr"
  - "architecture decision record"
  - "decision record"
  - "record this decision"
  - "架构决策"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - typography-hierarchy
      - color
      - accessibility-baseline
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Write an ADR for the decision to lay diagrams out in the browser with CSS grid instead of a graph-layout library: context, decision, options considered, consequences and status."
---

# ADR

**Intent.** A short, permanent record of one decision, read months later by someone asking why the system is the way it is. One decision per record.

## Ground it

Write only what the sources say. Gather them yourself before writing a word:

- the code that embodies the decision, and the discussion behind it (issues, PRs, design docs the user names);
- existing ADRs in the repo (`docs/adr/`, `docs/decisions/`, `adr/`): match their numbering and find the ones this supersedes.

Keep the list of files, commits and refs you read: they go in a **Sources** section at the bottom of the page and in `sources` when you register (`register_open_design_artifact` with kind `html`). If something the document needs isn't in the sources, ask the user, or mark it plainly as an open question. Never invent numbers, dates, names or quotes.

## Structure

1. **Header:** `ADR-<NNNN>: <the decision as a short statement>`, date, deciders if known, and a status banner `<p class="status" data-od-status="proposed|accepted|deprecated|superseded">…</p>`. If it supersedes or is superseded by another ADR, link both ways (`Supersedes ADR-0003`, `Superseded by ADR-0012`).
2. **Context:** the forces at play: constraints, requirements, what was tried. Neutral and factual.
3. **Decision:** one paragraph in the active voice: "We will …".
4. **Options considered:** a compact table: option, pros, cons, and why it lost or won.
5. **Consequences:** positive, negative and neutral, as three short lists. Be honest about the costs.
6. **Sources.**

Keep it to one or two screens. An ADR isn't a design doc.

## Design

- One readable column (`max-width` 720–780px), body 16–17px with line-height 1.55–1.65, generous space between sections. It must read well on a phone: tables sit in an `overflow-x: auto` wrapper, nothing has a fixed width wider than the screen.
- Style from the active design system (`--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`); status colours are the only extra colours (green for accepted/done, amber for proposed/in progress, red for rejected/high severity, grey for superseded).
- Headings are short labels; the content does the talking. Code, paths and commands in a monospace face, with `overflow-wrap: anywhere` so long paths wrap on phones.
- Finish with `check_open_design_artifact` and fix every error at desktop and mobile width.
