---
name: overlay-browser-navigator
description: Navigate and control websites by combining a live browser session with the a11y-overlay semantic layer. Use when Codex must click, type, scroll, route, or recover in a website and should use overlay signals such as landmarks, headings, accessible names, hit boxes, focus order, and visual evidence to choose and verify actions.
---

# Overlay Browser Navigator

Use this skill as an agent navigation policy layered over existing browser
primitives. It does not replace Browser, Playwright, Playwright Interactive, or
Overlay Playwright Runtime.

## Core Loop

1. **Intent**: restate the user goal as a concrete browser outcome.
2. **Observe**: collect the cheapest useful state first: URL, visible text,
   DOM/accessibility snapshot, screenshot, and overlay semantic map when the
   target is ambiguous or visual affordances matter.
3. **Rank targets**: choose likely controls using semantic labels first, then
   overlay signals for visibility, hit box size, focus order, landmarks, and
   nearby text.
4. **Act**: execute with the selected browser primitive.
5. **Verify**: confirm a user-visible state change, URL change, selected state,
   route content, toast, table update, or other explicit success condition.
6. **Recover**: if the action fails or verification does not match, re-observe,
   avoid the failed locator, and choose a different ranked candidate.

## Backend Selection

- Current Codex in-app browser tab or local target:
  - read and use `$browser-use:browser`
- Persistent headed browser, authenticated session, or iterative debugging:
  - read and use `$playwright-interactive`
- Terminal-first one-off browser automation:
  - read and use `$playwright`
- Overlay semantic map, annotations, evidence capture, or authenticated audit
  flow:
  - read and use `$overlay-playwright-runtime`

Prefer the current live browser/session when one exists. Do not relaunch a
browser unless the session is stale or the selected backend requires a fresh
context.

After selecting a backend, follow that backend skill's concrete tool workflow.
Use this skill only as the intent, ranking, verification, and recovery policy.

## Action Guardrails

Stop before delete, publish, pay, invite, sign out, submit, send, upload,
permission-change, or irreversible mutation actions unless the user explicitly
requested that action and the expected verification signal is clear.

## When To Use Overlay Signals

Use the overlay layer when any of these are true:

- multiple visible controls have similar labels
- the intended target is icon-only, visually dense, or near similar controls
- hit box size, occlusion, or focus order may affect the action
- the app is authenticated and route changes can invalidate simple locators
- a previous click/type/route action failed or changed the wrong state
- the user asks for visual evidence or wants to watch browser control

For simple unambiguous links or form fields, a DOM/accessibility snapshot may be
enough. Do not run a full accessibility audit unless the user asks for one.

## Operating Modes

- **inspect**: produce a semantic map of the current screen and candidate
  controls without acting.
- **navigate**: resolve an intent to a ranked target, act, and verify.
- **fill-submit**: locate fields and submit controls, type values, submit, and
  verify the result.
- **recover**: after a failed action, re-observe and choose a different target or
  route.
- **evidence**: capture screenshot or overlay evidence for the chosen target or
  final state.

## Read References As Needed

- For target scoring and action selection, read
  [references/candidate-ranking.md](references/candidate-ranking.md).
- For failure handling and self-healing behavior, read
  [references/recovery.md](references/recovery.md).
- For tasks that primarily ask to read or answer from developer documentation,
  read [references/developer-docs-reading.md](references/developer-docs-reading.md).
- For the full workflow diagram and component boundary, read
  [references/workflow.md](references/workflow.md).

## Output Discipline

When reporting progress or results, include:

- the user intent being executed
- the selected target and why it won over alternatives
- the verification signal used
- any artifact path only if an artifact was intentionally produced

Do not include internal candidate lists unless useful for debugging. If a target
remains ambiguous after one recovery pass, ask the user for a decision instead of
guessing through destructive or high-risk actions.
