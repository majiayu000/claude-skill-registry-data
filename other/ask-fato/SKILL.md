---
name: ask-fato
description: Ask which fatodono skill fits your situation. A router over every fatodono kit and skill.
disable-model-invocation: true
---

# Ask Fato

You don't remember every fatodono skill, so ask.

Before you say what a skill does or recommend skipping one of its steps, find its `<skill>/SKILL.md` on this machine and read it. The summaries here are only for orientation.

Route by the user's **situation**, not by kit. A **kit** is only the plugin a skill ships in; it matters once the skill turns out not to be installed (see the end).

## The launch flow: working app → store

The route an app takes from "it works" to "it's in the stores".

1. **`legals`** writes the legal documents the app needs (privacy policy, terms of service, subscription terms, refund policy, account deletion page, and region-specific ones such as the Turkish distance sales contract), plus the company's own agreements (founders' / shareholders' agreement, IP assignment, contractor agreement), and works out which of them this app actually needs. It reads the facts from the code and asks only what the code can't show (company name, support address, refund rules), so the later it runs, the fewer questions it asks. Drafts, not legal advice. It's model-invoked: the user can just say "write the legal documents for my app".
2. **`store-shots`** makes the App Store and Google Play screenshots from the app's real screens: framed in device mockups, captioned in every language, checked against each store's rules, plus Play's feature graphic. Every panel's claim must point at the code that makes it true. The user writes, with the agent, an adapter: the app's own capture program, on any platform, held to a contract by `store-shots adapter test`. Needs uv, Chrome (or Chromium, Edge) and whatever the adapter captures on: a simulator, an emulator, a browser. Model-invoked: "set up store screenshots for this app".

## Naming

- **The app, company, product or a feature needs a name**, is still on a placeholder, or the user wants a shortlist judged → **`brand-naming`**. It writes a strategy brief first, generates hundreds of candidates across separate passes, engineers their sound, and screens them for trademark, language and domain problems down to 3-5 finalists shown in context. Screening is a pre-screen, not trademark clearance. It can run before launch or at a rebrand. Not for naming variables, functions or files. Model-invoked: "we need a name for this app".

## After launch

- **The app changed** (a new SDK, a new country, a new paid plan) → **`legals`** again. It finds the documents the app already has, in the repo or on its site, and updates them instead of starting over.
- **A screen, a headline or a language changed** → **`store-shots`** again. It redoes only the images that change touched.

## Skills and kits

| Skill    | Kit                  |
| -------- | -------------------- |
| `legals` | `fatodono-founderkit` |
| `store-shots` | `fatodono-founderkit` |
| `brand-naming` | `fatodono-founderkit` |

## When the right skill is not installed

Each kit is its own plugin, so the user may have installed only some of them. If no `<skill>/SKILL.md` turns up, the skill isn't installed. Read it raw from GitHub instead (for example with `curl -s`), at `https://raw.githubusercontent.com/itsfatodono/skills/main/plugins/<kit>/skills/<skill>/SKILL.md`; if that fails too, say only what its summary here says. Tell the user it isn't installed and give them the install command for its kit:

```bash
claude plugin install <kit>@fatodono
```

In an agent other than Claude Code, they install the single skill instead:

```bash
npx skills@latest add itsfatodono/skills --skill=<skill>
```
