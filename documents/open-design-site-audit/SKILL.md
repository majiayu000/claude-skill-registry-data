---
name: open-design-site-audit
description: Audit a live website with Open Design's own checks — contrast, tap targets, phone layout, larger text, broken images, page weight and template looks — and get a short, plain-language report of the biggest problems with marked screenshots — use whenever the user wants a website audited, checked or reviewed for design, accessibility or mobile problems ("audit this site", "what's wrong with our website", "find problems on example.com", "why does our site look bad on phones"), or wants talking points before pitching a redesign, even if they don't mention Open Design
---

<!-- generated:open-design-agent-kit -->

Audit a live website with Open Design's checks and report what a visitor runs into.

Request: the rest of the user's message (if there is none, ask the user: "Which website should be audited?")

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

## 1. Ask only what's missing

You need the address. Up to 3 more pages on the same site are optional (a menu, services or contact page). If the request names them, use them; otherwise audit the home page alone and ask nothing.

## 2. Run the audit

Call `audit_open_design_site` with `url` and `extraUrls` if there are any.

- **`ok` or `partial`**: you get the top problems (`top`), the rest (`otherGroups`), page weight and the report path. `partial` means some pages were blocked; say which and why.
- **`blocked`**: nothing could be audited (a bot check, a members-only page or an empty page). Show the screenshot, say why, and ask for another public page. Don't retry with other settings.
- An error about the browser means none is installed: say so, and suggest installing a browser such as Chrome ([troubleshooting](https://github.com/feimacode/open-design-agent-kit/blob/main/docs/troubleshooting.md) has the details).

## 3. Report it

Tell the user the top problems in plain words, in the audit's order: the title, where (page, phone or desktop), what it costs a visitor and the fix. Point to the report (`report`) and offer to open it in the preview.

- Quote only what the audit found. Don't add a score, a speed rating, SEO advice or problems you guess at from the screenshots.
- Don't call the site a template, generic or AI-made unless `top` or `otherGroups` has "Looks like a stock template". A single pattern (an indigo glow, a row of identical cards) is named for what it is. Patterns listed only in `notes` are common on hand-made sites too: leave them out of the problems, or mention them as such if asked.
- If the report found nothing, say so plainly and list what was checked.
- The audit looks at a site the user may not own. Keep the tone factual: this is evidence for a conversation, not a verdict.

## 4. Next steps

Offer one next step that fits the request:

- **Redesign it**: make a concept that keeps the site's real content and brand and fixes these problems. The `open-design-redesign` skill starts from this audit.
- **Match the brand**: make a design system from the site with `open-design-design-system-from-url`.
- **Share it**: the report is a folder (`index.html` plus images) the user can zip or publish with `open-design-publish`.
