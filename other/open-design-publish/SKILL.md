---
name: open-design-publish
description: Share an Open Design artifact as a live link (a temporary no-account link, or your own Netlify, Vercel, Cloudflare Pages or GitHub Pages), or as one self-contained HTML file — use whenever the user wants to share, publish, deploy or host an Open Design artifact, or get a link to send to teammates or stakeholders; also when they want a single HTML file to attach or send
---

<!-- generated:open-design-agent-kit -->

Share an Open Design artifact with people who don't have this project open.

Request: the rest of the user's message (if there is none, ask the user: "Which design should we share, and how?")

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

## 1. Find the artifact

If the request names a design, find its entry file (`get_open_design_artifact`, or the `.open-design/` folder). If several match or none is named, ask the user which one. It must be registered; if it isn't, register it first with `register_open_design_artifact`.

## 2. A file, or a link?

- **A file to attach or send** (email, Slack, a ticket): call `export_open_design_artifact` with `format: "standalone"`. It writes one self-contained `.html` under the artifact's `exports/` folder, with its local CSS, scripts, images and fonts inlined. Give the user the path, and mention anything it still loads from the internet (such as web fonts). Nothing goes online. Stop here.
- **A link**: continue below.

## 3. Prepare the link

Call `publish_open_design_artifact` with the `entryPath`. Pass `provider` only if the user already said where:

- `netlify-temporary` or `cloudflare-temporary`: no account, the link lasts about an hour unless claimed
- `netlify`, `vercel`, `cloudflare-pages` or `github-pages`: the user's own account, a link that lasts

Without a provider, the tool returns the choices: show them to the user and call it again with their pick.

## 4. Follow the returned instructions exactly

They check the host's CLI, then **stop for the user's explicit yes** before anything goes online. That stop is mandatory: say what goes out, who can see it, how long it lasts, and that the small "Made with Open Design" footer badge is included unless they ask for `badge: false`. Deploy only the bundle folder the tool names.

## 5. Finish

Give the user the link. For a temporary link, also give the claim URL and when it expires, for them only. Then record it by calling `publish_open_design_artifact` again with `published`, as the instructions show, so a later publish updates the same site.

For a redesign with a base screen, offer a before/after page for the client (`compare_open_design_before_after`). On a flow, run it before publishing: the published site links to it from the map. Otherwise publish the before/after page itself like any design.
