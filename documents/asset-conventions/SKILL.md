---
name: "Asset: Conventions"
description: "Where generated visual assets live, how project type and theme are resolved and the quality gate every asset-* skill runs before reporting"
when_to_use: "Loaded by every asset-* skill before it captures, renders or frames anything; also when a README needs a screenshot, GIF or social card and the user hasn't named a skill."
user-invocable: false
metadata:
  family: asset
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Asset conventions

Shared ground for `asset-shot`, `asset-demo`, `asset-still`, `asset-card` and `asset-pdf`. Tool flags and verified APIs: `~/.claude/library/references/asset-tools.md`. Theme resolution and file format: `~/.claude/library/references/theme-conventions.md`.

## Output layout

```
docs/assets/
	shots.yml                 shot-scraper batch config (committed, re-runnable)
	shots/                    raw captures: <route-slug>[-<viewport>].png
	shots/framed/             framed versions, same names
	demo/
		<name>.tape             VHS source
		<name>.storyboard.yml   shot-scraper video source
		<name>.flow.ts          Playwright flow (record.ts)
		<name>.gif|.mp4|.webm   renders
	stills/                   freeze output: <file-slug>[-<lines>].png
	cards/
		card.json               title/tagline/meta/hero spec
		og.png                  1200×630
		github.png              1280×640
	pdf/
		<doc-slug>/page-NN.png  rasterised pages
		<doc-slug>/framed/      framed previews
```

Sources (`shots.yml`, tapes, storyboards, flows, `card.json`) are committed; renders are committed too unless the project's `.gitignore` says otherwise. Filenames are lowercase slugs, hyphenated.

## Project type detection

Check in this order and say which matched:

| Signal | Type | Capture base |
|---|---|---|
| `svelte.config.js` | SvelteKit | dev server (`bun run dev`, read the port from the output) or deployed URL from `package.json` `homepage` / README |
| `next.config.*` | Next | same |
| a directory of `.html` files with no build step | static site | `shot-scraper` on the file paths directly |
| single `.html` / `.jsx` artefact | React/HTML artefact | file path; for JSX, `import-scaffold_artefact` first |
| `bin` in `package.json`, `cmd/` or `main.go`, `pyproject` `[project.scripts]` | CLI | VHS / freeze; no browser |
| `*.pdf` under `docs/`, `dist/`, `export/`, `print/` | PDF project | pdftoppm |

Routes for SvelteKit come from `src/routes/**/+page.svelte` (skip `[param]` routes unless a sample value is obvious from a load function or README); for Next from `app/**/page.tsx` or `pages/**`. Explicit URLs or paths in the invocation override detection entirely.

## Theme resolution

Every render reads a theme target file: `frame` for shots and PDF pages, `vhs` for tapes, `freeze` for stills, `card` for cards. Resolution follows `theme-conventions.md` (`bun ~/.claude/library/scripts/asset/theme.ts <target> --project .` prints the file or the `/theme-factory` command to run). When it exits 3, offer to run `theme-factory` before continuing; do not fall back to inline colours.

## Approval gates

Sources are shown before rendering (a `shots.yml`, a `.tape`, a storyboard, a `card.json`). Rendering is cheap and local, so a render may run without a gate; anything that leaves the machine (GitHub upload) always gates, and the gate is explicit user consent in the conversation.

## Quality gate

Before reporting any image or video as done:

1. Open every output PNG with Read (for video, a frame via `ffmpeg -ss 1 -frames:v 1`). Look for: blank or white frames, a dev-server error page, a cookie banner or hydration flash, clipped text, a viewport that cut the hero in half, wrong theme variant.
2. Fix the cause (wait longer, different selector, taller viewport, hide an element with `javascript:`) and re-render once.
3. If it still fails, report it as failed with the image attached; never describe a broken asset as done.

## Report format

Paths written, dimensions, theme family used, then a ready-to-paste README snippet:

```markdown
![Dashboard](docs/assets/shots/framed/dashboard.png)
```

and, for demos, the GIF line plus a link to the MP4. Offer the next asset in the sequence (shot → card, demo → README) as a single question at the end.
