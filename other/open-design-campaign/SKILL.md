---
name: open-design-campaign
description: Turn one brief into a whole campaign — one master design exported to every channel size (social, link previews, banners, display ads), plus an optional landing page and email, in every language you need, checked and shown on one campaign sheet — use whenever the user wants a campaign, a launch kit, assets for several channels or sizes at once, ad banners in several sizes, or the same creative in several languages, even if they don't mention Open Design
---

<!-- generated:open-design-agent-kit -->

Build a campaign with Open Design: one message, one visual system, every channel.

Brief: the rest of the user's message (if there is none, ask the user: "What is the campaign for, which channels, and which languages?")

**How to talk to the user.** Many people using Open Design don't write code, so:
- Use the user's own words. If they say "artifact", "design tokens" or give a file path, use those terms back; otherwise use the plain words below.
- Keep the machinery out of replies: no tool names, no ids like `od:prototype:poster-hero`, no internal files (`.artifact.json`, `.comments.json`, `config.json`), and not the words "register", "manifest", "sidecar", "entry" or "surface", unless the user used them first.
- Explain a print term the first time it comes up, in one short clause, and not again.
- Say where a file is the way the user would find it ("in your Open Design folder, under seed-swap-flyer"). Give a raw path only where the user can click it (Claude Code, Claude Desktop's Code tab, VS Code) or asks for it.
- End each reply that finishes a step with one line on what they can do next, with at most two options ("Want it in Instagram sizes too, or is it ready to print?").

| Instead of | Say |
|---|---|
| artifact, entry, registered | your design, saved |
| design system, active design system | your style (the first time: "a saved style: colours, fonts and spacing") |
| surface, skill, template, recipe | kind of design, starting layout, or nothing |
| workspace, output directory | your folder, your Open Design folder |
| bleed | print edge ("a few millimetres extra that the printer trims off") |
| trim size | final size |
| preflight findings, errors | "I checked it and fixed…", "one thing to look at:" |
| export | save as PDF, save as an image |
| inline preview, MCP App | the preview above |

## 1. Agree the copy deck

Before designing anything, agree the words with the user. Draft them from the brief and show them as a short table:

- `headline` (≤ 6 words), `subhead` (one line), `cta` (2–4 words), and `legal` (one short line, if the brief needs one);
- one row per language (`locale` column: `en`, `de`, `ja`…) or per audience, if the user wants several. Translate faithfully and keep each row's meaning identical.

When the user is happy, save it as `copy.csv` in the campaign folder (`<output dir>/<campaign-slug>/copy.csv`), with a header row: `locale,headline,subhead,cta,legal`.

## 2. Build one fluid master

Call `prepare_open_design_brief` with `od:prototype:poster-hero` (or a better-fitting poster or social skill from `list_open_design_skills`), the brief, `format: "ig-portrait"` and `fluid: true`, plus `collectionId` (the campaign slug), `collectionName` and `screenRole: "master"`.

Build it as the brief says, and also:

- every piece of copy is an element with `data-od-field="<column>"` from the copy deck, holding the first row's text;
- add `data-od-fit` to the headline and subhead, so long translations shrink (to at most 70%) instead of overflowing;
- design the wide band (`@container (aspect-ratio > 1.2)`) and add a very wide band for banners (`@container (aspect-ratio > 3)`: headline and call to action side by side, everything else hidden with `data-od-priority`).

Register it (`register_open_design_artifact` with the same `format`, `collectionId`, `collectionName` and `screenRole: "master"`).

## 3. Pick channels

Ask which channels the campaign needs, unless the brief says. Offer this menu (format ids in brackets):

| Channel | Formats |
|---|---|
| Instagram / Facebook feed | `ig-portrait`, `ig-square` |
| Stories, Reels, TikTok | `story` |
| X | `x-image`, `x-header` |
| LinkedIn | `linkedin-image`, `linkedin-banner` |
| Link previews (website, Slack) | `og-image` |
| Display ads (150 KB each) | `banner-mrec`, `banner-leaderboard`, `banner-skyscraper`, `banner-mobile` |
| Email header | `email-header` |
| Print | `a4`, `a3`, `letter`… |

## 4. Check every shape

Call `export_open_design_artifact` with `presets` set to the chosen formats, `data: "<campaign folder>/copy.csv"`, `nameField: "locale"` and `checkOnly: true`. Fix every **error** in the findings (per shape and per row). For a shape that looks wrong or has errors, call `adapt_open_design_artifact` with those format ids and tune it in the same file. Tiny ad sizes usually need their own `@container` rule: headline and call to action only. Repeat until there are no errors.

## 5. Other pieces (optional)

If the user wants a landing page or an email, build each with its own skill (`od:prototype:saas-landing` or `od:prototype:web-prototype`, and `od:prototype:email-campaign`) using the same design system and the first row of the copy deck. Register each with the same `collectionId` and `collectionName`, and `screenRole` `landing` or `email`. Check each with `check_open_design_artifact`.

## 6. Export and show the sheet

1. Export the master: `export_open_design_artifact` with the same `presets`, `data` and `nameField: "locale"`, plus `campaignSheet: true`. This writes one image (or print PDF) per shape per row, named `<name>-<locale>-<format>`, and `exports/campaign-sheet.png`, which shows every shape and every other piece, with a red dot on any that still has errors. If the export says the outputs are over the limit, export one batch of locales at a time.
2. If there's an email, export it with `format: "email"` (and `baseUrl` once its images are hosted).
3. Show the user the campaign sheet, list the files per channel, and mention anything still flagged. The export also writes `exports/campaign-sheet.json`, which lists each tile in sheet order with its errors.
