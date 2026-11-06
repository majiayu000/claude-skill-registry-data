---
description: 'Render a visual change and actually look at it, instead of judging appearance by reading code. Boots the Next.js dev server and captures screenshots with headless Chromium, in either theme. `/preview live [<site>]`, or any ask naming the host — "на превью", "выложи на превью", "on preview", or "задеплой" / "deploy" on an unmerged branch — publishes one site from the branch to preview.vovazakharov.com instead, for a phone or a machine the dev server does not reach.'
---

## What this skill is for

Looking at a visual change with your own eyes before claiming it works.

The failure mode this exists to prevent is specific and common: reasoning about
appearance by reading the code that produces it. Spacing, overflow, contrast,
and how something reflows at a narrow width are not reliably derivable from
source — they have to be rendered and observed.

## Procedure

### 1. Boot the dev server

```bash
pnpm dev <site> --port <port> > tmp/preview/dev.log 2>&1 &   # site is vova, lsa, bible or basilisk
for i in $(seq 1 60); do curl -sf -o /dev/null "http://localhost:<port>/" && break; sleep 1; done
```

Poll rather than sleeping a fixed interval — the server answers in a few
seconds, but the _first_ request to any route pays a compile cost of 20-30s.
Nothing needs faking: this project has no credentials, no database and no
external calls, so the dev server is the real thing.

### 2. Find a browser

Chromium ships with the remote session at `/opt/pw-browsers/chromium`. Fall back
to a system `chromium` or `google-chrome` when that path is absent, so this
works on a laptop too:

```bash
CHROME=$(command -v /opt/pw-browsers/chromium chromium google-chrome 2>/dev/null | head -1)
```

There is deliberately no Playwright dependency — Chrome's own `--screenshot` is
enough, which keeps this out of `package.json`.

### 3. Capture

```bash
"$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --virtual-time-budget=6000 --window-size=<W>,<H> \
  --screenshot=tmp/preview/<name>.png "http://localhost:<port><route>"
```

`--screenshot` captures the **viewport, not the full page** — a `1280,900`
window yields a 1280×900 image and everything below the fold is simply absent.
To see a whole page, raise the height (`--window-size=1280,3000`); the image
grows to match.

**Put the theme in `<name>`.** The two themes differ only by a launch flag, so a
filename without it silently overwrites one capture with the other, leaving
whichever ran last as the evidence for both.

### 4. Report what you saw

"Captured 3 screenshots" is not a finding. Read the images back and say what
they show, whether it matches what was intended, and surface the ones that
don't.

## Routes

- **`/`** — home
- **`/cv`** — the CV, English
- **`/cv/cto/ru`** — the CV, Russian: `ru` copy is longer and wraps differently,
  so it is a distinct layout, not a translation spot-check

The locale sits inside the CV's own route (`/cv/<variant>/<locale>`), not in a
prefix: there is no `/en/…` or `/ru/…` on this site, and `/cv` renders the
English `cto` variant directly.

## Dark mode

**A colour change needs both themes.** A value that reads correctly against a
dark surface can be invisible against a light one, so shoot the route twice
whenever the change touches colour at all.

Add **`--force-dark-mode` alone**. Mantine's `ColorSchemeScript` resolves `auto`
against the OS preference, so `<html>` gets `data-mantine-color-scheme="dark"`
with the flag and `"light"` without it.

**Do not add `--enable-features=WebContentsForceDark`.** That is Chrome's
automatic inverter: it fabricates a dark rendering out of the light one, which
the project's own CSS never produces. A preview captured that way is a picture
of a page that does not exist — the trap that makes a dark preview a lie.

**Check the theme actually applied before reporting a themed capture:**

```bash
"$CHROME" --headless=new --no-sandbox --disable-gpu --force-dark-mode \
  --virtual-time-budget=6000 --dump-dom "http://localhost:<port><route>" | grep -o '<html[^>]*>'
```

Confirm the expected attribute is there. A theme that silently failed to apply
otherwise reads as a design finding.

## Widths — capture at 500px or wider, never narrower

`--window-size` has a **500px floor**, and below it the capture lies. Measured
by reading `innerWidth` inside headless Chromium 141:

- `--window-size=360,800` → `innerWidth` **500**
- `--window-size=390,844` → `innerWidth` **500**
- `--window-size=500,844` → `innerWidth` 500
- `--window-size=768,1024` → `innerWidth` 768
- `--window-size=1280,900` → `innerWidth` 1280

Any requested width under 500 is laid out at 500 CSS px and the screenshot is
_then_ cropped to the width asked for. Content that fits at 500 gets sliced
mid-word and reads as horizontal overflow that isn't there — a 390px capture of
`/en/cv` and `/ru/cv` produces exactly that, while the same page in a real
browser at 360px reflows correctly.

So: **never report a sub-500 capture as a layout finding.** Neither flag-level
workaround survives contact — `--force-device-scale-factor=2` leaves
`innerWidth` at the requested window width, and `--headless=old`, which had no
such clamp, is gone as of Chrome 141.

768 (tablet) and 1280 (desktop) are honored exactly and are the useful pair.

**Below 500 needs CDP, not a flag** — see § "Driving the page" below.
`Emulation.setDeviceMetricsOverride` sets a real layout viewport, so 360 and 390
are honest there.

## Driving the page — hover, true phone widths, measurement

`--screenshot` renders one static frame of a page nobody is touching, which
three things need more than:

- **Any `:hover` rule is invisible in a plain capture, and silently so.**
  Headless Chromium reports `(hover: none)`, so `styles/_mantine.scss`'s `hover`
  mixin takes its `:active` branch and the hover rule never applies — the
  capture shows the resting state and looks like a correct render of it. Pass
  `--blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4`
  to make the page report a hover-capable pointer.
- **True phone width**, per the floor above.
- **Overlap, ink extent and computed values**, where the eye is guessing at a
  few pixels — an absolutely-positioned control against a heading is the case
  that motivated this.

All three come from the DevTools Protocol, and Node's built-in `WebSocket`
speaks it with no dependency: launch with `--remote-debugging-port=<port>`, poll
`http://127.0.0.1:<port>/json/list` for the page target, then send
`Page.navigate`, `Emulation.setDeviceMetricsOverride`,
`Input.dispatchMouseEvent` (a `mouseMoved` at an element's centre sets
`:hover`), `Runtime.evaluate` and `Page.captureScreenshot` — the last taking a
`clip` with a `scale`, which is how a 25px chip becomes readable.

**Measure ink, not boxes.** A block-level heading's rect spans the whole column
whether or not its glyphs reach the corner, so a box-intersection test reports
collisions that aren't there.
`Range.selectNodeContents(el).getBoundingClientRect()` gives the text's real
extent.

Write these as throwaway scripts under `tmp/preview/`; nothing here belongs in
`package.json`.

## A printed page is looked at the same way

A change to `print.scss` or `prose.scss`'s print rules is visible only on paper,
and paper paginates — where a screen does not, so the screen capture that passes
says nothing about the page that fails. Rasterize the committed PDF and read it
back:

```bash
python3 -m pip install --target tmp/pdfium pypdfium2 pillow
PYTHONPATH=tmp/pdfium python3 -c "
import pypdfium2 as p
d = p.PdfDocument('<path>.pdf')
for i in range(len(d)):
    d[i].render(scale=1.4).to_pil().save(f'tmp/preview/page{i+1}.png')
"
```

The install is per session, nothing here having a place to put it; the target
directory is gitignored with the rest of `tmp/`.

**Never rasterize by pointing Chromium at a `file://…pdf`.** It renders the
built-in _viewer_ rather than the document, exits 0, and writes a plausible
blank PNG — a capture that reads as a page with nothing on it.

## Published, for someone else to look at

`https://preview.vovazakharov.com` serves one site built from a branch.
**Publish there only when the operator asks**, since they ordinarily pull the
branch and run the dev server themselves. The ask is `/preview live [<site>]`,
or any wording that names the host — «на превью», «выложи на превью», "on
preview" — and, on an unmerged branch, a plain «задеплой» or "deploy"
(`.claude/rules/deployment.md` says when it means production instead); a bare
`/preview` or «посмотри, как выглядит» is the screenshot pass above. With no
site named, publish the one the branch changes, and ask only when it changes
several. Offer it, without publishing, when the change is one that setup cannot
show: a phone layout, a browser or machine they do not develop on, or behaviour
that only a real host has. **Once a session has published a branch, it
republishes after each visible change it pushes, unasked** — the operator
looking at the preview is looking at that branch.

```bash
gh workflow run preview.yml --ref <branch> -f site=<site>   # vova, lsa, bible or basilisk
gh run watch "$(gh run list --workflow=preview.yml --branch=<branch> \
  --limit 1 --json databaseId --jq '.[0].databaseId')"
```

It dispatches from any branch, unmerged ones included. It never touches
production — `.claude/rules/deployment.md` has where it sits beside the other
doors. What the operator should be told with the link:

- **The slot holds one site, the last one published**, from whichever branch
  published it. Another session's publish replaces yours without warning; the
  receiver's single commit, `Built <site> from <sha> (<ref>)`, says what is up
  there now.
- **Links and cards still name production.** Canonical URLs, `og:image` and the
  sitemap come from the site's own URL, so a preview link pasted into a chat
  unfurls as the production page, and a link to another of the sites leaves the
  preview.
- **It is not counted or crawled.** The analytics tag counts the production host
  only, and every publish writes a `robots.txt` disallowing everything.

## Artifacts

`tmp/preview/` — gitignored. Use `docs/remove-before-merging/` instead when the
images must ride the branch for the operator to review; `/finalize` sweeps that
tree before the PR goes ready. Never leave image files to land on the trunk.

## Related

`/qa-checklist` classifies some verification steps as `manual-only` precisely
because they need a human's eye on pixels; `/preview` is what lets you close
some of that gap yourself — with the 500px floor above marking exactly where the
gap remains.
