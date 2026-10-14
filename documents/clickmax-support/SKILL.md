---
name: clickmax-support
description: Use when the user asks a how-to, troubleshooting, or "why isn't this working" support question about using Clickmax, and the answer should come from the help center.
---

## When this applies

Use this skill when the user asks a **support/help question about how Clickmax works** — how to do something, why something is not working, or where to find a feature — and the answer should come from the Clickmax help center (product documentation).

Not this skill:

- The user wants Max to _do_ an operation on their account (create a lead, build a funnel, send messages, analyze sales) -> the matching operational skill (`clickmax-leads`, `clickmax-funnels`, etc.). This skill is ANSWER-ONLY; it never performs account actions.
- The user asks about their own workspace data (their leads, their orders, their revenue) -> the operational analysis skills. The help center documents the product, not the user's data.
- The user asks "what changed / what's new" about a release -> use `mcp__plugin_clickmax_clickmax__helpdesk_releases_list` / `mcp__plugin_clickmax_clickmax__helpdesk_release_latest` instead of docs search.
- The user only wants to know WHERE a screen is ("onde fica a carteira", "onde adiciono o template da Meta") and a screen-lookup tool is available (Max: `find_screen`) -> use it; it links straight to the screen in one call. Search the help center only when they also need the steps or a fix.

## Key assumptions

- Source = public Clickmax docs (docs.clickmax.io) = the same pages the in-app Central de Ajuda shows. **Single source of truth** for support answers: answer only from page text retrieved this turn — never from general knowledge or from the product rules in operational skills.
- `mcp__plugin_clickmax_clickmax__docs_search` ranks by terms, not by exact phrase → a page matches by covering the question's words. Results carry `snippet` + `coverage` (0–1 share of query terms found) = for **picking**; the page markdown = for **answering**.
- Retrieval = 2 steps: `mcp__plugin_clickmax_clickmax__docs_search` → `mcp__plugin_clickmax_clickmax__docs_page_get` (by the result's `path`) — like `leads_search` → `leads_get`.
- Pasted docs link → take its path (`https://docs.clickmax.io/faq/x` → `/faq/x`) → `mcp__plugin_clickmax_clickmax__docs_page_get` directly.
- `lang` = `pt-BR` default | `en` when the user writes in English.

## Thought process

1. Support/help question? Operational request or question about the user's own data → hand off to the right skill, do not answer here.
2. Entry point: concrete question → `mcp__plugin_clickmax_clickmax__docs_search`; pasted docs link → `mcp__plugin_clickmax_clickmax__docs_page_get`.
3. Judge relevance honestly: usable only if title/snippet genuinely answers the question. Tangential match = no match.
4. Ground: read the chosen page's markdown, answer strictly from it.
5. Nothing relevant → deflect honestly; never stretch an unrelated page.

## Execute guide

- `mcp__plugin_clickmax_clickmax__docs_search` with `query` = the question's key words (drop filler: "como faço pra", "onde fica"); the user's own wording works too. Budget = 1 search + 1 retry with other terms only if top results are off-topic (e.g. product name instead of the user's slang: "modelo de mensagem" for "template"). Never loop searches.
- Pick the single best result by title + snippet; prefer higher `coverage` and the more specific page (FAQ/how-to over section landing pages).
- `mcp__plugin_clickmax_clickmax__docs_page_get` with that `path` → answer **only** from its markdown: relevant steps, faithfully, in the user's language, adding no step/fact the page does not state.
- End with the source: page title + `url` (markdown link).
- `truncated: true` → the answer may be past the cut; if the needed part is missing, say so and link the page.
- Nothing relevant: say honestly it isn't in the help center → point to the official support channel to reach a human. No invented answer, no general knowledge.
- Answer-only: never call a write/action tool from this skill.

## Report

- Answer in the user's language (PT by default; match the user if they write in another language).
- Be concise and practical: the concrete steps or explanation the page gives, in order.
- Always cite the source page (title + `url`) so the answer is traceable.
- The question is how to create something you can build with your own tools (WhatsApp template via `mcp__plugin_clickmax_clickmax__gupshup_templates_create` → `mcp__plugin_clickmax_clickmax__gupshup_templates_submit`, funnel, page, automation, quiz, product…) and the user did not say they will do it themselves → after the cited steps, ask "Quer que eu crie pra você?" and make building it the obvious next action. The offer is a question, not an action: build only after they accept.
  - Max: close with `<cx-cta action="confirm" label="Criar <thing> com o Max" prompt="<the request as an order, e.g. Crie um template de WhatsApp para disparo em massa>">one line on what you will ask</cx-cta>` as the reply's single `cx-cta` — NOT the `find_screen` link card; the manual path stays in the steps.
- On deflection: one honest sentence that you did not find it in the help center, then the official support channel to reach a human. Keep it short and non-defensive.

## Warnings

- Strict grounding is mandatory: not read in a page retrieved this turn → not a support answer.
- Docs ≠ workspace data. "Por que meu pagamento está pendente?" about a specific order = data/operational question, not a docs lookup.
- `helpdesk_search` / `helpdesk_article_*` / `helpdesk_tree` = legacy article base, not what the Help center shows → do not use for support answers.

## Anti-patterns

- Answering a support question from general/model knowledge or from the operational product skills instead of a retrieved page.
- Stretching a weakly-matching page to avoid deflecting.
- Answering from a search snippet without reading the page.
- Pasting the user's whole sentence into repeated searches instead of 1 search + 1 reworded retry.
- Silently performing an account action to "fix" the user's problem — this skill never acts.
- Omitting the source citation on a grounded answer.

---

Clickmax skill revision: `b8294822a4d6`
