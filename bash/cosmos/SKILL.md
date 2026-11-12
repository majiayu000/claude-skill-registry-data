---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: cosmos
repo: remorses/cosmos-cli
description: |
  `cosmos` CLI and TypeScript SDK to search cosmos.so (the visual inspiration site) and download
  image, gif and video assets, using the user's logged-in Chrome session via playwriter (token copied
  once, then GraphQL fetch from Node, no clicks). Returns original cdn.cosmos.so media URLs, sizes,
  AI captions, source URLs and authors, carousels, similar elements and collections. ALWAYS load this
  skill when the user mentions cosmos or cosmos.so, shares a cosmos.so URL, or wants to find and
  download reference images, textures, moodboard or design assets from cosmos.
---

# cosmos

Every time you use this skill, read both in full. Never pipe them to `head`, `tail` or `sed`:

```bash
cosmos --help
curl -s https://raw.githubusercontent.com/remorses/cosmos-cli/main/README.md
```

The README ends with an **Agent notes** section (asset workflow and gotchas). Follow it.

If `cosmos` is not on PATH, install it from the README Setup section (https://github.com/remorses/cosmos-cli).

## Folders

Always download into a folder named after the search query, in kebab-case, never into a shared `./assets` folder:

```bash
cosmos search "paper texture" --type image --limit 100 --download ./assets/paper-texture
cosmos search "ocean waves" --type video --download ./assets/ocean-waves --concurrency 8
cosmos collection maratorresg/paper-texture --limit 1000 --download ./assets/maratorresg-paper-texture
cosmos element https://www.cosmos.so/e/457818511 --download ./assets/brand-identity
```

## Rules

- Show the user the element URLs (`https://www.cosmos.so/e/<id>`) and, for images, upload a few downloaded files with `kimaki upload-to-discord` so they can pick.
- Downloads go under a folder the user named, or `./assets` in the project folder, always in a `<query-slug>` subfolder. Never `~/Downloads` unless asked.
- Mention `source.url` when the user plans to publish an asset: most cosmos images come from Pinterest, Behance and other sites.
- If a command fails with a playwriter error, ask the user to click the playwriter extension icon in Chrome, or retry with `--anonymous`.
