---
name: postmortem
zh_name: "事故复盘"
en_name: "Postmortem"
emoji: "🩺"
description: "A blameless incident postmortem: summary with impact numbers, a timeline, root cause and contributing factors, what went well and badly, and action items with owners."
en_description: "A blameless incident postmortem: summary with impact numbers, a timeline, root cause and contributing factors, what went well and badly, and action items with owners."
category: doc
scenario: engineering
tags: ["postmortem", "incident", "retrospective", "sre", "outage", "事故复盘"]
triggers:
  - "postmortem"
  - "post-mortem"
  - "incident review"
  - "incident report"
  - "outage report"
  - "事故复盘"
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
  example_prompt: "Write a postmortem for this incident from the notes and timeline I paste: impact, timeline, root cause, contributing factors, what went well and badly, and action items with owners."
---

# Postmortem

**Intent.** A blameless account of an incident that helps the team learn and prevents a repeat. It describes systems and decisions, never blames people.

## Ground it

Write only what the sources say. Gather them yourself before writing a word:

- the incident notes, chat or pager timeline, and dashboards the user provides. Ask for them if they're missing: **never invent an incident, a timestamp or an impact number**;
- the commits that caused and fixed it (`git log --since … --until …`, `git show <sha>`), and the code paths involved.

Keep the list of files, commits and refs you read: they go in a **Sources** section at the bottom of the page and in `sources` when you register (`register_open_design_artifact` with kind `html`). If something the document needs isn't in the sources, ask the user, or mark it plainly as an open question. Never invent numbers, dates, names or quotes.

## Structure

1. **Header:** title, incident id if any, date, a severity pill (`SEV1`–`SEV4`), status (`data-od-status="draft|reviewed|closed"`), authors.
2. **Summary:** what happened, who was affected and for how long, in three sentences.
3. **Impact:** a row of 2–4 big numbers (duration, users or requests affected, error budget used), each with its source.
4. **Timeline:** a table of timestamps (with the timezone) and events: detection, escalation, mitigation, resolution.
5. **Root cause:** the technical chain, step by step. Link the commits.
6. **Contributing factors:** what made it worse or slower to fix.
7. **What went well** and **What went badly:** two short lists.
8. **Action items:** a table of action, owner, priority and due date, each tied to a cause above.
9. **Sources.**

Use blameless language: "the deploy pipeline allowed…", not "X forgot…".

## Design

- One readable column (`max-width` 720–780px), body 16–17px with line-height 1.55–1.65, generous space between sections. It must read well on a phone: tables sit in an `overflow-x: auto` wrapper, nothing has a fixed width wider than the screen.
- Style from the active design system (`--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`); status colours are the only extra colours (green for accepted/done, amber for proposed/in progress, red for rejected/high severity, grey for superseded).
- Headings are short labels; the content does the talking. Code, paths and commands in a monospace face, with `overflow-wrap: anywhere` so long paths wrap on phones.
- Finish with `check_open_design_artifact` and fix every error at desktop and mobile width.
