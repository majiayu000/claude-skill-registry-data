---
name: social-stack
version: 1.2.1
repo: https://github.com/yourhandle/skynet-social-stack
description: |
  Build, render, and schedule social-media post packs end-to-end across LinkedIn,
  Instagram, Facebook, X/Twitter, Pinterest, YouTube. Picks the right template
  (carousel / single card / news mix / X pack / Pin / video drip), generates
  HTML w/ html2canvas PNG download, builds GHL CSV in canonical 6-col format,
  applies image rotation + no-fake-claims + humanizer rules, schedules cross-platform
  drips, wires ManyChat keyword funnels.

  Distilled from shipped patterns:
    - LinkedIn editorial dark+gold cards (Fraunces, 1080x1350) — 30+ batches
    - Tenfoldmarc-style cream+rust carousels (Archivo Black + circuit + robot mascot)
    - FB personal-news 9-card mix (4 info + 2 motiv + 3 sell + locked closer)
    - X 12-pack drip (MWF 3wk)
    - Pinterest 1000x1500 batch
    - GHL CSV format (canonical 6-col)
    - ManyChat keyword → WA template flow

  Trigger when user says: "build a carousel", "social pack", "LI cards batch",
  "FB news drip", "X pack", "Pinterest batch", "GHL CSV", "schedule drip",
  "post pack for [topic]", "/social-stack", or pastes a topic + asks for cross-platform content.
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - AskUserQuestion
---

# Social Stack — Master Social-Media Post Engine

Ship a complete platform-ready post pack in one session: **HTML → PNGs → GHL CSV → drip → ManyChat funnel**.

Not generic. Niche-tuned, brand-locked, claim-safe, rotation-respecting.

---

## INPUTS — ask if missing

1. **Topic** (e.g. "Claude Code limits", "AEO pivot", "n8n SaaS killer")
2. **Format** — carousel (6-slide multi) / LI single card / FB news mix / X pack / Pin batch / video drip
3. **Volume** — how many posts (default per format below)
4. **Platforms** — LI / IG / FB / X / Pin / YT (multi OK)
5. **Drip start date** + cadence (default: tomorrow, MWF or daily)
6. **Brand variant** — agency (`@your-agency`) or personal (`@yourhandle`)
7. **CTA** — DM keyword? link? save?

If 1 or 2 missing → use AskUserQuestion. Don't proceed.

---

## DECISION TREE — pick the template

| User signal                                                                                 | Template                                    | Default volume           |
| ------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------ |
| "carousel", "swipe", multi-slide tip pack                                                   | `templates/carousel-cream-rust/`            | 5–6 slides × N carousels |
| "LI card", "image card", quote/value post, dark editorial                                   | `templates/li-card-editorial-dark/`         | 15–30 cards              |
| "personal FB news", news commentary mix                                                     | `templates/fb-news-9card/`                  | 9 cards × 3 days         |
| "X pack", "tweet drip", short text                                                          | `templates/x-pack/`                         | 12–20 tweets             |
| "Pinterest", "Pin", vertical 1000×1500                                                      | `templates/pin-card/`                       | 30 pins                  |
| "feature card", "announcement", "launch post", model/product drop w/ photo + why-it-matters | `templates/cream-feature/`             | 1 hero card              |
| "video drip", existing MP4s                                                                 | no template — go to `recipes/video-drip.md` | —                        |

Full tree: `references/post-type-decision-tree.md`.

---

## EXECUTION FLOW

### PHASE 1 — Plan (3 min)

- Confirm inputs.
- Pick template (decision tree).
- Draft outline: hook → tricks → CTA. **Apply `references/no-fake-claims.md`** — only real builds, real metrics, real case studies.
- If using your photos → `python <your-images>/_pick-next.py --count N` (rule: `references/image-rotation-rule.md`).

### PHASE 2 — Build HTML (10–20 min)

- Fork the chosen template into `outputs/<slug>-<YYYY-MM-DD>/index.html`.
- Render parameterized data (carousels array / cards array / etc).
- Embed `html2canvas` for per-card PNG download + "Download all" button.
- 1080×1350 (LI/IG carousel), 1080×1080 (IG single), 1080×1920 (Story/Reel), 1000×1500 (Pin).
- Avatars: copy picked photos to `outputs/.../<slug>/_avatars/` for same-origin html2canvas.

### PHASE 3 — Captions + humanize (10 min)

- Write platform-tuned captions: LI long-form / IG hook+CTA / FB conversational / X tight.
- Run through **`references/humanizer-checklist.md`** — strip em-dashes, AI tells, "delve", "moreover", inflated symbolism.
- Apply `references/no-fake-claims.md` — flag any unverifiable metric.

### PHASE 4 — GHL CSV (5 min)

- Use `scripts/build_ghl_csv.py` — outputs canonical 6-col headers (see `references/ghl-csv-format.md`).
- One CSV per platform (LI / FB / IG / Pin / X). X does NOT use GHL — separate text file.
- Date-shift to drip window: `scripts/shift_dates.py --start YYYY-MM-DD --cadence mwf|daily|weekday`.

### PHASE 5 — ManyChat + funnel (if CTA = DM keyword)

- Wire keyword across IG/FB/WA per `references/manychat-keyword-flow.md`.
- WA template needs 24–72h Meta soak — submit BEFORE drip Day 1 or dead-funnel risk.

### PHASE 6 — Mark + ship

- Mark each photo used: `python _pick-next.py --use FILE.jpg "<post-tag>"`.
- Save deliverable summary to `outputs/<slug>/_README.md`.
- Add memory entry (see `references/memory-update-template.md`).

---

## OUTPUT CONVENTIONS

```
outputs/<slug>-<YYYY-MM-DD>/
├── index.html                  # interactive preview + PNG download
├── _avatars/                   # photos used (rotation-tracked)
├── captions/
│   ├── linkedin.md
│   ├── facebook.md
│   ├── instagram.md
│   └── x.md
├── csv/
│   ├── ghl-linkedin.csv
│   ├── ghl-facebook.csv
│   ├── ghl-instagram.csv
│   └── ghl-pinterest.csv
└── _README.md                  # what / where / when / how to ship
```

---

## RULES — always apply

1. **No fake claims.** Real builds only. No invented metrics. → `references/no-fake-claims.md`
2. **Image rotation.** Always pick via `_pick-next.py`. Never by eye. Mark used after. → `references/image-rotation-rule.md`
3. **Humanize.** No em-dash storms, no "delve/moreover/it's worth noting", no rule-of-three filler. → `references/humanizer-checklist.md`
4. **Brand split.** Personal posts (motivation + casual Q, no hard sell) vs SkynetLabs (sell + proof). → `references/brand-split.md` (or memory: `feedback-personal-social-style`)
5. **GHL CSV format = 6-col canonical.** Don't invent headers. → `references/ghl-csv-format.md`
6. **NDA scrub.** Strip client names from FB/IG/Pin (LinkedIn = signal but check). E.g. an NDA-bound client's name scrubbed from FB/IG/Pin per prior precedent.
7. **Date-shift safety.** Run shifter BEFORE upload or lose 9/30 pins to past dates (Pinterest precedent).
8. **24–72h Meta soak.** Submit WA templates BEFORE Day 1 or funnel dies.
9. **Responsive output contract.** Every PNG/PDF/MP4 ships fully responsive — fixed-px export node + fluid preview frame, viewport tests 360/480/768/1024/1440, ≥44px touch, role=img + aria-label. → `references/responsive-output-contract.md`

---

## RECIPES — full playbooks

- `recipes/carousel-launch.md` — 5-carousel × 6-slide drop, LI+IG primary
- `recipes/li-card-batch.md` — 15–30 LI editorial dark+gold cards
- `recipes/fb-news-3day.md` — 9-card personal FB news, 3×3 drip
- `recipes/x-pack-mwf-drip.md` — 12-tweet pack, MWF over 3 weeks
- `recipes/pin-batch.md` — 30 pins, +14d shift
- `recipes/cross-platform-pack.md` — same content × 4 CSVs (LI/FB/IG/Pin)
- `recipes/post-mortem.md` — engagement retro after every batch (top 5 / bottom 5 / pattern extraction)
- `recipes/repurpose-chain.md` — 1 topic → 9 derivatives across LI/IG/FB/X/Pin/Newsletter
- `recipes/competitor-sweep.md` — 15-min Sunday peer sweep, pattern-match weekly

---

## TEMPLATES (6 working, v1.3.0)

- `templates/carousel-cream-rust/` — Archivo Black + circuit + robot mascot, 1080×1350
- `templates/li-card-editorial-dark/` — Fraunces serif + dark+gold, 1080×1350 (NEW v1.2)
- `templates/fb-news-9card/` — 9-card mix (4 info + 2 motiv + 3 sell + locked closer), 1080×1350 (NEW v1.2)
- `templates/x-pack/` — image-tweet 1200×675, 12-tweet pack w/ thread followups (NEW v1.2)
- `templates/pin-card/` — vertical 1000×1500, 30-pin batch, 3 palettes, UTM auto-inject (NEW v1.2)
- `templates/cream-feature/` — cream+emerald hero/announcement card, Fraunces + framed photo + why-it-matters strip, 1080×1350, `render.js` headless export (NEW v1.3)

Every template ships with: `index.html` (responsive preview + html2canvas export), `data.json` (sample data), `README.md` (responsive contract + usage), `_avatars/` (rotation-log photo dest).

All templates inherit `references/responsive-output-contract.md`.

---

## SCRIPTS

- `scripts/build_ghl_csv.py` — canonical 6-col CSV builder (postAtSpecificTime, content, link, imageUrls, gifUrl, videoUrls). QUOTE_ALL. Validates input.
- `scripts/shift_dates.py` — date-shift canonical CSV by N days, MWF/daily/weekday cadence. Try/except on malformed dates.
- `scripts/pick_avatar.py` — wraps `_pick-next.py` w/ rotation-log validation + forced --mark or --no-mark (no silent skip)
- `scripts/utm_inject.py` — adds utm params per row to GHL CSV
- `scripts/seed_replies.py` — first-30-min engagement seed comments
- `scripts/caption_variants.py` — A/B hook variants from hook-bank

---

## ANTI-PATTERNS — don't do

- Don't render HTML with random Picsum / Unsplash hot-link images — html2canvas can taint.
- Don't ship without humanizer pass — AI-tell em-dashes kill reach on LI.
- Don't claim case-study metrics you haven't verified — no-fake-claims rule.
- Don't reuse a photo without checking rotation log.
- Don't paste GHL CSVs without date-shift if window has shifted.
- Don't skip Meta WA template soak — DM keyword posts will dead-funnel.

---

Last updated: 2026-04-30 (v1.2.0 — responsive contract + 4 templates shipped)
