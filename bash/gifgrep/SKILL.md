---
name: gifgrep
description: "Search GIF providers, download results, extract stills."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GIF, Search, Media, Tenor, Giphy]
    category: media
    related_skills: [gif-search]
prerequisites:
  commands: [gifgrep]
---

# gifgrep Skill

Search GIF providers (Tenor and Giphy) with the `gifgrep` CLI or its TUI, download results, and extract stills or contact sheets. Requires the `gifgrep` binary. API keys are optional for Tenor and required for Giphy.

## When to Use

- User asks for a GIF for a reaction, a chat reply, docs, or a PR
- Searching Tenor or Giphy by query, previewing results, and downloading one
- Extracting a still frame or a contact sheet from a GIF file

## Prerequisites

- Install `gifgrep`: `brew install steipete/tap/gifgrep`, or `go install github.com/steipete/gifgrep/cmd/gifgrep@latest`
- `GIPHY_API_KEY` is required for `--source giphy`; `TENOR_API_KEY` is optional (a Tenor demo key is used if unset). Keys live in the Hermes `.env` (secrets only); never print them.
- Run commands with the `terminal` tool. Still previews with `--thumbs` work in Kitty and Ghostty only.

## How to Run

1. Search with the `terminal` tool, preview the results, then download the chosen one.
2. Use `--format url` or `--json` for pipe-friendly output; use the TUI for browsing.
3. Extract stills or sheets from a downloaded file with `gifgrep still` / `gifgrep sheet`.

## Quick Reference

```bash
gifgrep cats --max 5
gifgrep cats --format url
gifgrep search --json cats
gifgrep tui "office handshake"
gifgrep cats --download --max 1 --format url
```

Stills and sheets:

```bash
gifgrep still ./clip.gif --at 1.5s -o still.png
gifgrep sheet ./clip.gif --frames 9 --cols 3 -o sheet.png
```

Providers:

```bash
gifgrep cats --source auto
gifgrep cats --source tenor
gifgrep cats --source giphy
```

`--download` saves to `~/Downloads`; `--reveal` shows the last download in Finder. `--json` prints an array of results (`id`, `title`, `url`, `preview_url`, `tags`, `width`, `height`). Sheets are a single PNG grid of sampled frames; tune with `--frames` (count), `--cols` (grid width), and `--padding` (spacing).

## Procedure

1. Search: `gifgrep <query> --max 5`, or `gifgrep search --json <query>` for structured results. Pick the source with `--source auto|tenor|giphy` when the user names one.
2. Preview: use the TUI (`gifgrep tui "query"`) for browsing, or `--thumbs` for CLI still previews in Kitty/Ghostty.
3. Download: `gifgrep <query> --download --max 1 --format url` for the top result, or download a specific result from the JSON output.
4. Verify the asset before recommending or using it (see GIF asset hygiene below).
5. Extract: `gifgrep still <file> --at <time> -o <png>` for one frame, `gifgrep sheet <file> --frames <n> --cols <n> -o <png>` for a grid.
6. Report the local file path and the source URL with attribution.

### GIF asset hygiene

- Before recommending or using an animated GIF URL, verify it resolves successfully, has `Content-Type: image/gif`, and is actually animated (multiple frames or loop metadata; inspect with `file`, `identify`, or a small script).
- Record attribution, license, and source URL alongside the asset.
- Do not hotlink when a local asset is needed: download or copy it into the project and reference the local file.

## Pitfalls

- Giphy search fails without `GIPHY_API_KEY`. Tenor works without a key on the demo key; if Tenor results look wrong, check whether a key is set.
- `--download` saves to `~/Downloads`, not the working directory. Say where the file landed.
- A URL that no longer resolves, or that serves a still image instead of an animated GIF, is not usable as a GIF. Verify before sending it on.
- TUI mode is interactive and cannot run headless. In a non-interactive run, use the CLI flags and `--json` instead.

## Verification

- After a download, confirm the file exists in `~/Downloads` (or the `--out` path) and `file` reports it as a GIF.
- After a still or sheet extraction, confirm the PNG exists and view it with `vision_analyze` when the user asks what it shows.
- Before sharing a GIF URL, confirm it resolves and serves `Content-Type: image/gif`.
