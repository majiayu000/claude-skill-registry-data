---
name: create-post-graphic
description: >
  Design branded diagram images for social posts — layer diagrams, flows, loops,
  quote + stat cards, sequence diagrams, numbered steps — as hand-authored HTML
  rendered to PNG, styled from the business's own brand settings pulled from the
  Marky API. Use this when a post announces, teaches, or compares something and a
  designed diagram would beat a stock photo: "make a diagram for this post",
  "turn these steps into an image", "make an infographic". A companion to
  plan-social-content and schedule-posts: it produces the image; those skills
  attach and schedule it.
---

# Post Diagrams

A designed diagram in the brand's own colors makes a post stop the scroll and
carry its point without the caption. This skill turns a post's idea into a
1080x1350 PNG: you author real HTML/CSS (no AI image generation, no stock), style
it from the business's brand settings, render it headlessly, look at it, and
attach it to the post.

**Read the marky-api skill first** for the base URL and your key.

## Why hand-authored HTML

Generated imagery reads as filler and cannot hold exact text. A diagram is
mostly *text in the right places*, and HTML is the strongest layout tool an
agent has. You control every word, the brand colors are exact, and edits are one
CSS line, not a re-roll.

## Stage 1 — Pull the brand

In a plugin install the SessionStart hook already injected a `brand-cache.md` snapshot
with these fields — start from that. If it's missing or possibly stale (see "Write like
the business" in the marky-api skill), fetch fresh:

```bash
curl "https://api.mymarky.ai/api/businesses/BIZ_ID" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Read these fields:

- `palettes[0].colors` — the brand palette. Derive your tokens from it:
  - **accent** = the most saturated mid-tone color (skip near-white / near-black)
  - **ink** = the darkest color (body text)
  - **surface** = the lightest color (page background)
  - **tints** = mix accent with white at ~92% / 82% / 65% for ring/step fills
    (CSS `color-mix(in srgb, ACCENT 8%, white)` etc.)
- `header_font` / `body_font` — use if set; otherwise the system stack
  (`-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`).
- `logo_url` — the footer mark. Render the actual logo (`<img>` capped at ~48px
  tall, `object-fit: contain`); if `logo_background_color` is set and isn't
  transparent, put it behind the image with a little padding and a small
  radius so the logo sits on the background it was designed for. Only when
  `logo_url` is empty, fall back to a text wordmark (`name` in the accent
  color).

## Stage 2 — Pick the archetype

Match the post's *point* to a shape. If none fits, a bold typographic card
(headline + one stat) beats a forced diagram.

| The post... | Archetype | Shape |
|---|---|---|
| announces things built on each other | **Layers** | nested rounded rectangles, core = accent fill, outer rings = tints. Nested rects beat concentric circles: labels stay horizontal and readable |
| shows how something moves through a system | **Flow** | vertical column of cards joined by accent arrows, endpoints as pill chips |
| describes a repeating routine | **Loop** | 4 cards on a circle with arc arrows and a hub label ("every week") |
| quotes a customer or leads with a number | **Quote + stat** | oversized quote mark in a light tint, big quote text in ink, one stat strip below |
| explains two+ parties interacting over time (dev audience) | **Sequence** | lifelines + labeled arrows, dark surface, mono font for message labels |
| gives setup or how-to instructions | **Steps** | numbered cards with accent number badges, joined by short connectors |

**Making a multi-slide carousel instead of one card?** That's the
create-post-carousel skill — it owns the narrative frameworks and slide-copy
workflow, and comes back here for the brand pull and render mechanics.

## Stage 3 — Author the HTML

Start from `assets/_base.css` (copy it next to your HTML files and substitute
the brand tokens at the top). Canvas rules:

- `body` is exactly **1080x1350** (4:5 portrait — the strongest feed crop),
  `overflow: hidden`, generous padding (72px).
- Structure: **kicker** (small caps, accent) → **headline** (60-64px, weight
  800) → the diagram in a centered flex `stage` → **footer** (logo — or wordmark
  fallback — with a top border).
- Type floor: nothing under 25px — phones shrink this image to ~400px wide.

Design rules (non-negotiable):

- **Text wears ink, never the accent on a low-contrast fill.** Labels sit in
  ink on light tints; white text only on the solid accent.
- **One accent hue.** Tints of the accent for hierarchy, gray for secondary
  text. Never a rainbow.
- **Direct labels, not legends.** Every element says what it is, in place.
- **Copy at a 5th-grade level**, short words, and only claims that are true for
  this business — a diagram is still brand copy.
- Numbers must be real. Never invent a stat to fill a slot.

## Stage 4 — Render and LOOK at it

Render with headless Chrome/Chromium. Use an **absolute** `--screenshot` path and
add `--virtual-time-budget=6000` so web fonts (Oswald, Montserrat, …) finish
loading before the shot fires — without it Chrome can silently fall back to a
system font and quietly break the brand typography.

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=6000 \
  --window-size=1080,1350 --screenshot="$PWD/diagram.png" "file://$PWD/diagram.html"

# Linux: google-chrome / chromium / chromium-browser with the same flags.
# On locked-down Linux/CI, add --no-sandbox if Chrome exits immediately.

# Windows (Git Bash): Chrome resolves a RELATIVE --screenshot path against a
# directory it can't write ("Failed to write file ...: Access is denied. (0x5)"),
# so pass ABSOLUTE, Windows-native paths (forward slashes are safest in bash) for
# BOTH the output and the file:/// input. Derive them from your Git-Bash dir with
# cygpath — do NOT hand-type them:
WINDIR=$(cygpath -w "$PWD" | sed 's#\\#/#g')   # /c/Users/you/x -> C:/Users/you/x
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=6000 \
  --window-size=1080,1350 --screenshot="$WINDIR/diagram.png" \
  "file:///$WINDIR/diagram.html"
```

**No local renderer?** Some agent sandboxes (e.g. Cowork) have no Chrome/Chromium
binary, no way to install one, and restricted network egress — so both local
rendering and a Puppeteer/Chromium download fail. Don't get stuck: skip the
hand-authored-HTML render and use Marky's server-side media instead —
`search_media_library` for existing on-brand images, or `upload_media_from_url` (Marky
fetches the URL server-side, past the sandbox's egress limits) for a web image.
Fall back to local rendering only when a browser binary is actually present.

Then **open or read the PNG and inspect it before showing the user.** The two
failure modes to catch: labels wrapping onto arrows or borders, and content
overflowing the canvas. Fix the CSS and re-render; never ship a render you have
not looked at.

## Stage 5 — Attach it

Upload the PNG and use the returned URL on the post (see the schedule-posts
skill for post creation):

```bash
curl -X POST "https://api.mymarky.ai/api/businesses/BIZ_ID/media" \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -F "file=@diagram.png"
```

Keep the `.html` sources next to the PNGs in your content folder — future edits
are a one-line change plus a re-render, and a series stays visually consistent
by reusing the same base CSS.

Before presenting drafts, run every caption through the **humanize** skill's pattern check (score 90+; fix silently, don't show the math). The user's own caption_writing_rules still outrank it.

## Approval gate

Diagrams are brand-facing. If you rendered multiple candidates, let the user pick on
the review board (`${CLAUDE_PLUGIN_ROOT}/scripts/review-board.py items.json --mode pick`
— run in background, parse `BOARD_URL:`, AskUserQuestion with the URL, then read
`feedback.json` for `preferred`/`ratings`/`comments`). Append the result to
`~/.marky/feedback-log.jsonl` with `context: "diagram-styles"`, and check that log
BEFORE choosing an archetype — if the user keeps picking the same style, start there
(see "The feedback log" in the marky-api skill). Otherwise show the rendered PNG
to the user and get their edits
or approval **before** the post schedules, same as captions in
plan-social-content.

**Marky wants your feedback.** If anything here breaks or is confusing, send it
with the submit_feedback MCP tool — see the "Marky wants your feedback" section
in the marky-api skill.

## Tag the post

Set `metadata` on the post when you create it — `{"media_type": "graphic", "created_by": "create-post-graphic", "hook": ..., "topic": ...}` (use `"diagram"` instead when the output is a true flow/chart/steps diagram rather than a designed brand card) — per "Tag every post" in the
marky-api skill. This is what lets future performance reviews compare this post's
engagement against other media types.

