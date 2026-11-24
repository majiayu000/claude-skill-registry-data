---
name: opendesigner-smart-ui
description: Optional. An assistant's answers show a part of the person's own system (a chart, a form, a booking step) instead of text. Reads the repo, writes an A2UI catalog, checks each answer before it renders.
license: MIT
compatibility: Python 3.10+ (standard library, no network) for scope, catalog, prompt, validate and text. The renderer is plain JavaScript in any browser. The audit needs Playwright for Python, which the skill never installs. Needs the opendesigner skill beside it (the library and slots.py).
metadata:
  version: "0.3.1"
  homepage: "https://github.com/ckryptickunal/OpenDesigner"
---

# OpenDesigner: Smart UI

Use this when someone has an assistant or chatbot in their product (or wants one) and asks for answers that show interface instead of only text: "make the bot show a table", "generative UI", "the assistant should let people book from the chat", "intelligent UI", "A2UI", "MCP Apps". It is optional: nothing in the other skills needs it.

The idea in one line: **the model picks a part and fills in words and numbers; it never picks a colour, a size or a URL.** Every part comes from the person's library, every value is checked against their tokens before anything renders, and anything that changes data waits for the person to press a button.

Talk plainly, one decision per message, and recommend one option with its reason (`../opendesigner/references/rules.md`). First mention of a term: its plain meaning, then "Designers: X · Code: Y" from the glossary (Smart UI, catalog, surface, slot, A2UI, MCP Apps).

## Before you start
- A design system: `opendesigner/build/css/tokens.css` in the project. No system yet: offer the `opendesigner` skill first (a 5-question sketch is enough). A project with its own CSS variables can map `--ds-*` to them instead; say which variables are missing (`smartui.py scope` lists them).
- The scripts run from the person's project. `smartui.py` is `scripts/smartui.py` in this skill; the library and `slots.py` live in the `opendesigner` skill next to it.

## The flow
Follow `references/flow.md`. In short:

1. **Scope.** `python3 smartui.py scope --write` reads the repo: the product and its users (PRODUCT.md, DESIGN.md, `opendesigner/state.json`), where the assistant lives, the framework, the tokens, and the actions (API routes, tool definitions). It proposes the intents the assistant must answer and the parts each needs. Show the list. Anything it could not find says "not known": ask, never guess. Nothing is invented about the product.
2. **Use cases.** Ask first: `usecases` and `templates` load their app module and call its read actions once, with sample values, to see the data (a read action that calls a paid API or a live database would be called). Then `smartui.py usecases --app <their app module> --write` ranks the answer types this product needs (a table, a chart, pictures, a place, steps...) from its own data, PRODUCT.md, the project's research and its screens, each with its reason and part, and names any type the library has no part for. No fixed list: a billing tool, a council service and a travel app get different lists. Without research on what assistants in their industry show, offer `research.py` first. The person confirms: `usecases --confirm "..."`, then `smartui.py confirm KeyFacts,Comparison,...` for the parts (record their words in the reply).
3. **Catalog.** `smartui.py catalog --allow-images <their image hosts>` writes `opendesigner/smart-ui/catalog.json` (an A2UI v1.0 catalog) and `od-components.js` (the parts' own markup for the renderer). Visual options are only lists of their token names. Ask once which image hosts and link domains are theirs; with none, images are off.
4. **Prepare the parts.** `smartui.py templates --app <their server module> --write` binds a part to each read action's data for the confirmed answer types (`opendesigner/smart-ui/templates.json`). Show the drafts and let the person fix titles and labels. At run time a matcher finds the prepared part with no model, it fills from the data as it lands, and the model writes only the sentence. Their own agents (data, RAG) plug in beside it: `references/your-agents.md`.
5. **Wire it in.** `references/adapters.md`: in their own chat (any framework) with `<od-surface>`; through A2UI; or inside Claude and ChatGPT through MCP Apps. Each answer: `smartui.py prompt --for "<message>"` (or the same selector in their code) sends the model only the few parts that fit, never all of them.
6. **Validate.** Every answer goes through `validate` (Python, `smartui.py validate`) or `od-validate.js` (the browser) before it renders. A failure comes back as A2UI errors the model can repair; send them back once, then fall back to text.
7. **Audit.** `smartui.py audit --fixtures` renders every confirmed part in every state (`references/states.md`) at 320, 375 and 1440 px, 200% text, dark, right-to-left and reduced motion, and checks the floors and the craft checks. `--ledger` records failures in the audit ledger. Report what was checked and what was not.

## Rules (full text in `references/rules.md`)
- **R1** No interface when text is enough. A short factual answer stays text.
- **R2** One part per answer unless the person asked for more.
- **R3** Anything that books, pays, sends or deletes is a button the person presses, and asks first. The model never presses it.
- **R4** Nothing off-system: no colours, sizes, styles, classes, handlers, HTML or outside URLs. Unknown parts and properties are refused, not dropped.
- **R5** Accessibility floors: WCAG 2.2 AA contrast, 24 px targets (44 px for main actions), visible focus, one polite live region, reduced motion, and every control named differently.
- **R6** Honest data. A number shown must be in the data the model was given (`validate --source`). Missing stays missing.
- **Pictures** come only from the host's data, with alt text and a shape (`R5-alt`, `R5-ratio`); a price shows its currency (`R6-currency`); sold out or nearly gone is never green (`R6-stock`).
- **R7** In Claude or ChatGPT, the host's look applies only if the person opts in. In their own product, their tokens win.

## The parts
`references/components.md`: 34 parts in seven jobs (answer, data, choose, act, confirm, media, pictures), the system's toast for feedback after a change, and parts made for one kind of product (flights). Each is a library component with slot marks; `smartui.py catalog` lists only the ones that are marked. Add a part to the library first (the library's own rules), then to `assets/set.json`.

## Commands
```
python3 smartui.py scope [--project .] [--write] [--json]
python3 smartui.py confirm <Name,Name,...>
python3 smartui.py catalog [--tokens opendesigner/build/css/tokens.css] [--allow-images host ...] [--allow-links host ...] [--all]
python3 smartui.py prompt --for "<message>" [--data data.json] [--k 3] [--json]
python3 smartui.py validate <reply or answer.json | -> [--source data.json] [--partial] [--max-parts 2] [--a2ui] [--json]
python3 smartui.py text <reply or answer.json>          the plain-text version, for a host that shows no interface
python3 smartui.py audit --fixtures [--only slug,slug] [--answer file] [--ledger]
python3 test_smartui.py                                   the shared validator fixtures in Python and JavaScript
```

## What is tested and what is not
Say this plainly when you set it up; `references/adapters.md` has the table by host. The validator, renderer and states run in tests and in the audit. Host tests (A2UI renderers, MCP Apps in Claude and ChatGPT) are recorded there with their dates; a host that is not in the table has not been tried.
