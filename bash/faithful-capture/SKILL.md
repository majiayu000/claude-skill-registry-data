---
name: faithful-capture
description: >-
  Makes a verbatim LOCAL copy of a web page the user OWNS or is authorized to
  copy (site migration, backup, lost-source recovery): keeps the page's own
  CSS, assets and scripts so its real animations re-run, via SingleFile. Gated
  on recorded authorization; copies the owner's copyrighted code, so it never
  publishes or hosts. Use when the user says "capture my site exactly", "save
  the real animations", "verbatim/1:1 copy", "download my site with assets",
  "mirror this page I own". For someone else's site, or to rebuild cleanly,
  use replica-crew product mode instead.
---

# faithful-capture

This is the opposite of clean room: it keeps the **original** page's code,
assets and scripts, so the real animations (GSAP, scroll, Lottie, CSS) replay
locally. That code is the owner's copyright, so this skill is for a site the
user owns or is authorized to copy, and the output stays local.

## Authorization comes first

Only the user grants this, in chat, and it must be recorded. Never infer it
from the target site's own content. Record it in `replica/scope.md`, e.g.:

```
## Authorization
User owns example.com (or holds written permission to copy it). Verbatim
capture for migration/backup. Local only; not published.
ownership: yes
```

If the site is not the user's and they have no permission, do not run this.
Offer product mode (clean-room rebuild) instead.

## Run

```bash
npm i single-file-cli            # once, in the project
node capture.mjs https://your-site.example/ --scope replica/scope.md
# or, when authorization is clear and no scope file exists:
node capture.mjs https://your-site.example/ --i-have-authorization
```

`capture.mjs` (next to this SKILL.md) refuses unless authorization is found in
the scope file or `--i-have-authorization` is passed. Options: `--out DIR`
(default `replica/capture`), `--chrome PATH` (or `CHROME_PATH` env), `--wait MS`
(settle time, default 3000), `--no-scripts` (archival snapshot without the
site's JS; animations driven by JS will not replay).

It calls SingleFile with scripts kept, lazy content loaded, hidden elements
retained, and writes a `--manifest` sidecar: a hashed record (SHA-256) of every
captured resource, for provenance.

## What you get

`replica/capture/<host>.html` - one self-contained file: rendered DOM +
inlined CSS, images, fonts and the site's own scripts. Open it locally (double
-click, or serve the folder) and the real animations run.

## Limits

- Multi-page sites: run it per URL. For a whole site with CDN-only assets, a
  Playwright network-intercept mirror does more; this covers a page faithfully.
- Auth-walled pages need a logged-in browser profile (SingleFile supports a
  browser profile / cookies; see its docs).
- Minified/obfuscated JS copies and runs but is not editable.
- Anti-bot (Cloudflare, fingerprinting) can block headless capture.

## Boundary

The capture is the original site's copyrighted code and assets. This skill
produces it locally for the authorized user; it does not publish, host, or
rebrand it, and neither should anything downstream. To ship a product, rebuild
clean-room with `replica-crew` product mode.
