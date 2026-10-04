---
name: generating-app-verify
description: >-
  Generate a project-local verification skill that drives the real app the
  way a user does — web, CLI, API, or desktop. Apply when the user invokes
  /generating-app-verify, asks for a control or verify skill, or the
  project has no scripted way to prove behavior. Use refreshing-app-verify
  to keep the feature map honest. Use testing.mdc for when to write tests.
user-invocable: true
disable-model-invocation: true
version: "1.2.0"
author: "Ali Farahat"
tags: ["verification", "e2e", "feature-map"]
when_to_use: |
  USE WHEN:
  - The user asks to create a verify / control skill for this app.
  - The project has no scripted way to prove UI, CLI, or service behavior.
  DO NOT USE WHEN:
  - A verify skill already exists and has drifted (use refreshing-app-verify).
  - The user only wants a unit test (testing.mdc).
---

# Generate an app verify skill

> **Leading words:** interview the repo, drive like a user, feature map,
> prove one feature, skills/verify-app.

Every serious project needs a way to launch the app, exercise a feature as a
user would, and keep evidence. This skill writes that as
`skills/verify-<app>/` (Agent Skills path — not `.cursor/` only).

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Interview the repo (surface, run, drive, observe, isolate). Ask the user only what you cannot observe.
2. Write `skills/verify-<app>/SKILL.md` with Launch, Doctor, Drive, Evidence, Cleanup, Helpers. Helpers live under `helpers/` (not `scripts/`). A Launch helper is required even when the app is a one-shot CLI (ready signal = usage line + exit).
3. Seed a feature map (`features/README.md` + 3–5 user-POV feature files).
4. Run launch → doctor → drive **one** mapped feature → evidence still exists after cleanup.
5. Point at `/refreshing-app-verify`.

If the checkout does not start, fix that first (or report it). A skill
written against a broken base teaches the wrong steps.

## Interview

- **Surface:** web UI, CLI/TUI, desktop, API, mobile? Pick the primary.
- **Run:** the repo's own documented dev command. Ports, env, seed, auth.
- **Drive:** existing harness first (Playwright, expect, curl). Then browser/CDP, PTY, or HTTP.
- **Observe:** screenshots, transcripts, bodies, logs, exit codes, DB.
- **Isolate:** can two instances run? If not, say so — refuse to double-drive a shared session.

## Generated skill

Frontmatter: `name: verify-<app>` and a description that names the app and
surface. Sections with **no placeholders**:

- **Launch** — exact command, ready signal, teardown.
- **Doctor** — read-only "is this instance worth driving?"
- **Drive** — real selectors/commands from this repo. ARIA, data attributes, prompt strings, routes — not coordinates.
- **Evidence** — what to capture and where. Real user path, not internal setters. Side effects counted. Mocks only at a production boundary.
- **Cleanup** — kill what you started. Evidence survives.
- **Helpers** — executable; invocation shown in the body.

Feature files use four H2s: Sub-features / How to get to it (user POV) /
Driving it with the harness / Gotchas. Shape:
[references/feature-map.md](references/feature-map.md).

## Reply contract

Paths written, which feature you proved, where the evidence lives, and that
cleanup left the evidence in place.
