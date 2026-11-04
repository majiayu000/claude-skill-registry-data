---
name: product-knowledge
description: >-
  What this prototype is, what the mobywatel.ai challenge asks for, how the reference prototype works and how
  we beat it, and where product truth lives. Use for "what does the app do", "does it do X", "what should we
  build next", "how do we differentiate", scoping, specs, pitch or demo questions.
---

# Product knowledge

The competition brief is `docs/product/competition-brief.md`. Read it first. This skill tells you how to use
it, where the other sources are, and how to keep them honest.

## Where product truth lives (most to least trustworthy)

| Question                                | Source                                                               |
| --------------------------------------- | -------------------------------------------------------------------- |
| What does the prototype do _right now_? | The code: `apps/pwa/src/features/*`, routes in `apps/pwa/src/app/`   |
| Which matters work end to end           | `packages/core` state machines + `packages/content` scenarios        |
| How each matter is designed             | `docs/services/<matter>.md` (the `service-journeys` skill)           |
| Competition rules, dates, form fields   | `docs/product/competition-brief.md` (dated snapshot of mobywatel.ai) |
| Concept, pitch, submission text         | `docs/product/` (owned by the `product-manager` agent)               |
| What we promise users in copy           | `apps/pwa/messages/pl/*.json`, `packages/brand` copy                 |
| Personas and their data                 | `packages/content` (fictional; the `prototype-guardrails` skill)     |
| Why the stack is what it is             | `docs/decisions/*.md`                                                |
| What's next                             | `NOTEBOOK.md` if it exists, open PRs (`gh pr list`), `docs/product/` |

**Code wins.** If a doc and the code disagree, the doc is wrong. Say so; don't repeat the doc.

## The competition in one screen

- **Organiser:** Klub Parlamentarny Rozwój Plus; honorary patron Marcin Horała (Vice-Marshal of the Sejm). Not
  a government service, not the official mObywatel.
- **Goal:** a clickable prototype of a new mObywatel app that is better than the reference by Janusz
  Cieszyński: **simpler, more convenient, more accessible, or handling more matters**.
- **Deliverable:** an `https://` link to a prototype that can be walked through (screens and whole processes),
  **without login**, up until the results. Static images or a video alone don't count; a video can be an extra
  link.
- **Form:** name or team, e-mail, city, category, concept title, description (**30–4000 characters**),
  prototype link, optional extra link, Polish technologies used (optional), website.
- **Deadline:** 30.11.2026, end of day, Polish time. On 2026-10-24 the site also showed "Nabór zakończony";
  the founder confirms with the organisers.
- **Judging:** no published scoring. The bar is the reference prototype. The form asks "what works better in
  your version and who does it help". Polish technologies (Bielik, PLLuM, Polish companies) are a plus, not a
  requirement.
- **Prize:** the top 10 concepts are presented in the Sejm.
- **Suggested areas:** new home / documents / navigation; one matter end to end with fewer steps (meldunek,
  new ID, vehicle registration, 800+); a confirm-before-send assistant (voice or text); seniors and
  accessibility (large text, plain language, screen readers, help from a relative); reminders (expiring ID,
  OC, inspection); privacy and data control (who checked my data, share only what is needed).

## The reference prototype (what we must beat)

- **Assistant instead of menus:** the user talks (text or voice) and the assistant looks things up in
  fictional registries and handles the matter.
- **Confirmation cards:** every action is shown as a card (what, source registry, rows) and the user taps to
  confirm.
- **Scripted on the web:** mobywatel.ai runs prepared scenarios without a live model; the downloadable version
  has a Python server with tool calling (OpenAI, Anthropic or any OpenAI-compatible model), speech in and out,
  and 15 UI languages.
- **Four personas:** Marta (Warsaw, 35, three kids), Jan (Kraków, 43, own firm), Ewa (Lublin, 57, cares for
  her mother, ID expiring), Kacper (Gdańsk, 20, new driver). Home shows a document wallet, reminder tiles and
  suggestion chips ("Zgubiłam portfel", "Miałam stłuczkę").
- **Knowledge base:** copied gov.pl service cards, searched locally.

## How we differentiate (keep this list current in `docs/product/`)

Each bet names the angle it wins on. Candidates, to be decided by the founder:

1. **More accessible:** senior mode as a first-class mode, not a setting; screen-reader-first chat; help from
   a relative (shared access).
2. **Simpler:** chat is not always the shortest path. Pair the assistant with direct, visible actions so a
   task takes fewer taps than talking. Measure steps (the `service-journeys` skill).
3. **More convenient:** an installable PWA that works offline, with proactive reminders that open straight
   into the matter.
4. **More matters / Polish tech:** an LLM port that runs Bielik or PLLuM.

Never claim a bet is won without a measured comparison against the reference.

## How to answer a product question

1. Frame it with the brief.
2. Check the claim in code and name the screen, state machine or scenario.
3. Say what state it is in: **built** (on `main`), **on a branch** (open PR), **planned** (`NOTEBOOK.md`,
   `docs/product/`), or **not planned**.
4. Say where it was checked: unit test, Playwright flow, built preview on a phone viewport, or a real phone.
   The service worker and offline only count from a build (`pnpm preview`) or the deployed link, never from
   `pnpm dev`.

## Scoping a slice

One user-visible outcome per slice. State the persona, the matter, before/after steps, the copy, empty and
error states, the guardrails impact (the `prototype-guardrails` skill) and how it is verified. Hand it to the
`pwa-architect` agent for the plan (the `add-feature` skill).
