---
name: rfc
zh_name: "技术方案 RFC"
en_name: "RFC"
emoji: "📐"
description: "A request for comments: the problem, goals and non-goals, the proposal with the alternatives considered, risks, rollout and open questions, with a status banner, grounded in the code and docs it changes."
en_description: "A request for comments: the problem, goals and non-goals, the proposal with the alternatives considered, risks, rollout and open questions, with a status banner, grounded in the code and docs it changes."
category: doc
scenario: engineering
tags: ["rfc", "design doc", "proposal", "engineering", "architecture", "技术方案"]
triggers:
  - "rfc"
  - "design doc"
  - "technical proposal"
  - "request for comments"
  - "engineering proposal"
  - "技术方案"
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
  example_prompt: "Write an RFC for moving our image exports to a job queue: problem, goals and non-goals, the proposal with alternatives, risks, rollout plan and open questions. Read the current export code first."
---

# RFC

**Intent.** A proposal people can review and decide on. Readers skim the summary and the decision; reviewers read the alternatives and the risks.

## Ground it

Write only what the sources say. Gather them yourself before writing a word:

- the code and docs the proposal changes (read them; cite file paths);
- related issues, earlier RFCs or ADRs the user points to;
- if it comes from a spec or openspec change, its proposal and design files.

Keep the list of files, commits and refs you read: they go in a **Sources** section at the bottom of the page and in `sources` when you register (`register_open_design_artifact` with kind `html`). If something the document needs isn't in the sources, ask the user, or mark it plainly as an open question. Never invent numbers, dates, names or quotes.

## Structure

1. **Header:** title, `RFC-<number>` if the repo numbers them, author(s), date, and a status banner: `<p class="status" data-od-status="draft|proposed|accepted|rejected|superseded">…</p>`. Superseded RFCs link to their replacement.
2. **Summary:** three to five sentences: what changes and why, in plain words.
3. **Problem:** what's wrong today, with evidence from the sources (code paths, numbers, user reports).
4. **Goals** and **Non-goals:** short bullet lists. Non-goals matter: they stop scope creep.
5. **Proposal:** the design, at the level a reviewer needs. Diagrams as simple HTML boxes, or a `diagram` artifact exported as an image; code in `<pre>`.
6. **Alternatives considered:** each with why it lost. At least one.
7. **Risks and mitigations:** a two-column table.
8. **Rollout:** steps, flags, migration and rollback.
9. **Open questions:** numbered, each with an owner if known.
10. **Sources.**

## Design

- One readable column (`max-width` 720–780px), body 16–17px with line-height 1.55–1.65, generous space between sections. It must read well on a phone: tables sit in an `overflow-x: auto` wrapper, nothing has a fixed width wider than the screen.
- Style from the active design system (`--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`); status colours are the only extra colours (green for accepted/done, amber for proposed/in progress, red for rejected/high severity, grey for superseded).
- Headings are short labels; the content does the talking. Code, paths and commands in a monospace face, with `overflow-wrap: anywhere` so long paths wrap on phones.
- Finish with `check_open_design_artifact` and fix every error at desktop and mobile width.
