---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: pinterest
repo: remorses/pinterest-cli
description: |
  `pinterest` CLI and TypeScript SDK to search Pinterest by text or by image (visual search from an
  existing pin URL or id, with optional crop) and download original pin images and videos, using the
  user's logged-in Chrome session via playwriter (cookies copied once, then the site's resource API
  from Node, no clicks). Returns original i.pinimg.com URLs, mp4 or HLS videos, carousel slides,
  title, description, alt text, outbound link, pinner, board and save counts. Also related pins,
  board search and board listing. ALWAYS load this skill when the user mentions Pinterest, shares a
  pinterest.com pin or board URL, or wants to find, find similar, or download reference images,
  textures, moodboard or design assets from Pinterest.
---

# pinterest

Every time you use this skill, read both in full. Never pipe them to `head`, `tail` or `sed`:

```bash
pinterest --help
curl -s https://raw.githubusercontent.com/remorses/pinterest-cli/main/README.md
```

The README ends with an **Agent notes** section (asset workflow and gotchas). Follow it.

If `pinterest` is not on PATH, install it from the README Setup section (https://github.com/remorses/pinterest-cli).

## Folders

Always download into a folder named after the search query, in kebab-case, never into a shared `./assets` folder:

```bash
pinterest search "paper texture" --limit 100 --download ./assets/paper-texture
pinterest search "ocean waves" --scope videos --download ./assets/ocean-waves --kind video --concurrency 8
pinterest similar https://www.pinterest.com/pin/1104085664920412828/ --limit 100 --download ./assets/crumpled-paper
pinterest board kaboompics_/paper-textures-copy-space-backgrounds --limit 500 --download ./assets/kaboompics-paper-textures
```

For `similar`, `related` and `board`, name the folder after what the images show or the board name.

## Rules

- Show the user the pin URLs (`https://www.pinterest.com/pin/<id>/`) and, for images, upload a few downloaded files with `kimaki upload-to-discord` so they can pick.
- When the user likes one pin, run `pinterest similar <pin>` to find more like it. Add `--crop` to focus on one object.
- Downloads go under a folder the user named, or `./assets` in the project folder, always in a `<query-slug>` subfolder. Never `~/Downloads` unless asked.
- Every `pinterest search` shows up in the user's Pinterest recent searches. Do not run many probing queries; pick good ones.
- Never save, follow or react on the user's account, and never open `pinterest.com/r/pin/...` links.
- Mention `link` and `pinner` when the user plans to publish an asset: pins are saved from other websites and users.
- If a command fails with a playwriter error, ask the user to click the playwriter extension icon in Chrome.
