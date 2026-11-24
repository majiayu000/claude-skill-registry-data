---
name: form-design
description: "Forms that ask only what is necessary, once."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, forms]
    category: web
    related_skills: [web-design, form-validation, component-states]
    web_designer_stages: [wireframe, components]
---

# Form Design Skill

This skill designs forms that ask only for what is necessary, in a single column, with visible top-aligned labels, correct input types and autocomplete, field sizes matched to expected input, and requirements shown before errors. It covers the layout and structure of data-entry flows. It does not cover validation timing, error wording, or error recovery — the form-validation skill owns those. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For signup, checkout, contact, search-filter and any data-entry flow.
- When a form has more than a few fields, or when fields are being added, removed, or reordered.
- When a long form needs splitting into steps (progressive profiling).

It is NOT for:

- Validation rules, error messages, or what happens after a failed submit — that is form-validation.
- The visual styling of inputs (tokens, colours, radii) — that is the tokens and components stages' work.
- Choosing which fields the business needs; it challenges unnecessary fields, it does not invent the data model.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The wireframe records the form's purpose and the fields it needs, so unnecessary fields can be challenged before they are built.
- The components stage's inventory exists or is being built, so the form's fields are recorded as components.

## How to Run

1. List every field the form asks for and challenge each one: is it necessary for this step, or can it be asked later?
2. Lay the form out in a single column, one field per row, in the order the user thinks about the answers.
3. Give every field a visible top-aligned label. Never use a placeholder as a label.
4. Set the correct input type and autocomplete attribute for each field, and size each field to match the expected input.
5. Show requirements (format, required, optional) on the field before the user can get them wrong.
6. Split a long form into steps (progressive profiling) instead of one long page.
7. Record the form in the components inventory and hand the work to the judger; do not grade it here.

## Quick Reference

- Layout: single column, one field per row.
- Labels: visible, top-aligned, always present — never placeholder-as-label.
- Input types and autocomplete: correct type per field, autocomplete attributes set.
- Field sizing: matched to the expected input length.
- Requirements: shown before errors, on the field itself.
- Long forms: split into steps (progressive profiling).

## Procedure

### 1. What it is

Forms that ask only for what is necessary, in a single column, with visible top-aligned labels (never placeholder-as-label), correct input types and autocomplete, field sizes matched to expected input, and requirements shown before errors.

### 2. How Hermes applies it

Hermes uses one column, top labels, proper type/autocomplete attributes, progressive profiling (split long forms into steps), and its judger checks no placeholder-only label and no unnecessary field survives.

### 3. What it returns to the stage

- `wireframe` stage — `pages`: each wireframe page records the form's fields in order, the single-column layout, and which fields were challenged or deferred to a later step.
- `components` stage — `inventory`: the form's fields and controls are listed as components with their input types, autocomplete attributes, labels, and sizes.

### 4. Good looks like

A form a user can complete without re-reading labels; top labels are always visible; the keyboard shown on mobile matches the field.

## Pitfalls

- Placeholder-as-label: a placeholder that disappears the moment the user types, leaving the field unlabelled.
- Asking for fields that are not needed for this step; every unnecessary field costs completions.
- Multi-column forms that break the reading order and make tab order hard to follow.
- Wrong input type or missing autocomplete, so mobile shows the wrong keyboard and the browser cannot help fill the field.
- Requirements revealed only after an error, instead of shown on the field up front.
- Field sizes that mislead: a tiny field for a long answer, or a wide field for a two-digit code.

## Verification

- Every field has a visible top-aligned label; no placeholder-only label survives.
- No unnecessary field survives the challenge in the How to Run steps.
- Input types and autocomplete attributes match each field; field sizes match the expected input.
- Requirements are shown on the field before any error can occur.
- The visual judger checks the form layout, labels, and component states; the skill does the work and the judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: wireframe, components. Returns: `wireframe` — `pages`; `components` — `inventory`. Judger boundary: visual judger checks form layout, labels, and states.
