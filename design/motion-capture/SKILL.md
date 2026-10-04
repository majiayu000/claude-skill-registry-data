---
name: motion-capture
description: Use when a film needs product screenshots or UI crops, a product state the live app doesn't show, sharper crops for a camera zoom, or when lint reports a shot with no provenance.
---

# Motion capture

ENGINE is `../../engine/`. Everything lands in the film folder `<slug>/`.

1. **Plan from the shotlist.** For each shot, list the page (URL), the state it must be in, and the elements that move on their own (buttons, cards, rows, badges). Those become `elements`.
2. **Write `<slug>/capture.json`** (format in the header of `ENGINE/capture.py`):
   - `scale: 2` by default; 3 if the camera will zoom past 2x on that shot.
   - `transparent: true` for any element that morphs, pops or flies on its own; its ancestors' backgrounds are cleared for that shot only.
   - A logged-in app: save a Playwright session once to `~/.config/motiontale/<app>.json` with mode 600 and point `storageState` at it. It is a credential: capture refuses one inside the film folder or readable by others. Never put a password in capture.json. Or use the browser you're already logged in to: start Chrome with `--remote-debugging-port=9222` and set `"cdp": "http://127.0.0.1:9222"`; capture works in a tab of its own, closes only that tab, and scale follows that browser's own pixel ratio. Only a local browser is accepted.
3. **Writes are blocked.** Capture lets only GET/HEAD/OPTIONS requests out, so a patch or a click can't change real data. `"allowWrites": true` in capture.json lifts that; use it only on a demo account.
4. **States the product doesn't show on its own** (a filled form, an open menu, seeded demo data): a `patch` is JavaScript run on the real page before the shot. It edits the real DOM, so the pixels are still the product's; the patch is recorded in provenance.json. Never draw the state instead.
5. **Run** `PY ENGINE/capture.py <slug>`. It writes `shots/`, `crops.js` (element boxes on their page, in CSS px), `provenance.json` and `facts.suggested.md`.
6. **Look** at every PNG. Wrong state, cookie banner, loading skeleton, personal data: fix the capture.json (a patch that clicks the site's own reject button, a `waitFor`, a seeded account) and run again. Never paint over a capture. A part of a page is an element capture by selector; a patch that scrolls before a viewport shot is unreliable.
   A screenshot taken elsewhere (a phone, an emulator): `PY ENGINE/capture.py import <slug> <png> <source url> [x0,y0,x1,y1] [name]` records its source, box and hash.
7. **Facts.** Copy every number you will show from `facts.suggested.md` into `facts.md` and set its kind: `fact` (true of the real product; the captured URL is its source) or `example` (seeded demo data, shown with an "Example" label). `lint.py` blocks numbers it can read in the source without a row; `film.py check facts` catches the rest on screen.

## Rules
- Real pixels only: a capture, a crop of a capture, or a capture of a patched real page. Nothing redrawn.
- Personal data never appears: use a demo account or patch it out, and say which in provenance (the patch is recorded).
- Place crops with `crops.js` boxes so an element lifted off its page lands on its original pixels.
- `lint.py` blocks `shots/` images on screen without provenance.json, any image in `shots/` it doesn't list, and any whose file changed since capture.

## Done when
Every shot in the shotlist has a capture, every PNG has been looked at, `facts.md` covers every number shown, and `python3 ENGINE/lint.py <slug>` shows no `asset` or `invent` line.
