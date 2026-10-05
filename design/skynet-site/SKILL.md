---
name: skynet-site
version: 1.0.0
description: |
  Build a premium client website end-to-end — competitor research, niche-tuned design
  system, conversion funnel, SEO/AEO base, Vercel deploy, GitHub repo, speculative
  pitch with 5-8 scope-unlocking questions. Distilled from 9 shipped client wins
  (wedding, wellness, medical, luxury rental, clinic pitch, indie event,
  coach funnel, 20-niche demos, agency theme rebuild).
  Trigger when user says: "build a site for", "design website", "spec build for client",
  "/skynet-site", pastes a client brief / Upwork JD asking for a website, or wants
  a landing page / agency demo / niche site.
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
  - WebSearch
  - Agent
  - AskUserQuestion
---

# Skynet Site — Master Website-Design System

Goal: ship a client-ready demo + pitch in one session. Not template fill. Not generic. Niche-tuned, conversion-optimized, deploy-ready, SEO-safe.

Source patterns: 9 shipped builds. See `case-studies.md` for full table.

---

## INPUTS — ask if missing

1. **Brief** (Upwork JD / Fiverr buyer note / email / verbal)
2. **Niche** (wedding / wellness / medical / luxury rental / law / HVAC / etc.)
3. **Client name** OR placeholder OK
4. **Budget signal** (anchors pricing tier)
5. **Timeline**

If brief missing → use AskUserQuestion. Don't proceed without niche + brief.

---

## EXECUTION FLOW (one session)

### PHASE 1 — Research (parallel, 5-10 min)

Launch 3 Agent calls in ONE message:

- **Agent A — Competitor teardown.** 8-12 competitors in niche. Extract: palette, fonts, hero pattern, CTA style, pricing visibility, sameness gaps.
- **Agent B — Niche taste signals.** Wedding ≠ corporate. Healthcare ≠ SaaS. Find what BUYERS in this niche perceive as "premium". Ref Awwwards, Behance, Dribbble for niche.
- **Agent C — Keyword + EEAT.** Primary city + service + intent keywords. Schema markup needed (LocalBusiness / FAQPage / Organization / Service). Trust signals niche expects (license #, certifications, years, photos).

Output → `docs/RESEARCH.md`. Use it. Don't ignore it.

### PHASE 2 — Design Token Lock

Pick palette + font pair from niche match table (see `design-tokens.md`). DO NOT default to navy+gold for everything — that's corporate, not luxury. Wedding = warm beige + claret + Instrument Serif. Medical = forest + mint + Cormorant Garamond. Premium health = bone + sage OR cobalt + acid yellow.

Output 1 design.md w/ tokens, never 5 random variants UNLESS budget ≥$1K AND brief unclear (then ship 5 variants like the health-brand play).

### PHASE 3 — Stack Pick

| Budget / scope   | Stack                                                                            |
| ---------------- | -------------------------------------------------------------------------------- |
| <$300, fast      | Static HTML+Tailwind CDN+vanilla JS, Vercel                                      |
| $300-1K, premium | Pure HTML/CSS/JS, Vercel, no build step (no-build premium pattern)               |
| $1K+, hero anim  | Next.js 15 + React 19 + Tailwind 3.4 + R3F v9 + Drei v10 + Framer Motion + Lenis |
| WordPress brief  | Build Vercel demo first. Port to Divi/Kadence Phase 2 (coach-funnel pattern)     |

**Never** ship raw template clone — always niche-tune palette + fonts + copy + photos.

### PHASE 3.5 — 3-Variant Lock (MANDATORY)

**ALWAYS ship 3 different landing-page variants per client.** No exceptions. Client picks 1 → polish + ship. Pattern validated across a home brand (5 variants → V4 picked), a health brand (5 variants), a CPG brand (5 variants w/ floating switcher), a wedding brand (3 iterations).

**Why:** Client cannot articulate taste in advance. Showing 3 cuts the back-and-forth from 5+ revisions to 1 pick + 1 polish round. Doubles close rate vs single-variant pitches.

**3 variants must differ on AXIS not detail:**

| Variant                 | Axis                                                    | Example                        |
| ----------------------- | ------------------------------------------------------- | ------------------------------ |
| **V1 — Editorial**      | Magazine grid · serif display · whitespace-heavy        | wedding-brand modern v3        |
| **V2 — Cinematic**      | R3F 3D hero OR MP4 loop · dark · animation-forward      | health-brand 3D helix          |
| **V3 — Bold / Minimal** | Glassmorphic OR brutalist · single accent · type-driven | health-brand magazine OR Aesop |

Pick 3 axes that span the niche's taste range. NEVER 3 variants that look ~80% the same — defeats the point.

### PHASE 3.6 — Sticky Variant Switcher (MANDATORY)

**Every multi-variant build = sticky variant switcher visible to client.** Default placement: **top-right header** OR **floating top-right pill** (per `recipes/variant-switcher.md`).

**Spec:**

- Position: `position: fixed; top: 20px; right: 20px; z-index: 99`
- Three labeled pills (V1 / V2 / V3) OR grid icon → dropdown
- Active state: filled w/ accent color
- Persist via URL hash `#v1` `#v2` `#v3` so client can share specific variant link
- Mobile: collapse to bottom-right floating button → modal sheet
- Kill on production after client picks (just delete the component, single variant remains)

Live examples:

- Home brand — `example.vercel.app` grid icon top-right
- Health brand — `example.vercel.app` `<VariantNav>` top
- CPG brand — floating design-switcher toolbar

Code recipe: `recipes/variant-switcher.md`.

### PHASE 4 — Build (locked 8-section funnel)

Order non-negotiable. Buyers expect this rhythm.

1. **Hero** — cinematic (R3F mesh OR MP4 loop OR Ken Burns image). H1 = niche + city + outcome. Sub-H = trust shorthand. 2 CTAs (primary form + secondary tel:). Sticky mobile call bar bottom.
2. **Trust strip** — logos / press / certifications / years / jobs done / 5-star. ALWAYS show.
3. **Services grid** — 6 cards × icon + 2 lines + mini CTA. Real services from brief, not generic.
4. **About** — first-person voice if solo founder, "we" only if team. Italic dropcap. Asymmetric photo stack.
5. **Process timeline** — 3-4 steps "How it works". Reduce decision friction.
6. **Testimonials carousel** — 6 cards w/ photo + city + service. NEVER reuse same testimonial across niches (caught in an early 20-niche batch).
7. **Photo gallery** — real work, before/after where applicable. Unsplash CDN labeled per niche, NOT Picsum.
8. **FAQ accordion** — 6-8 niche-real Qs. JSON-LD `FAQPage` schema.
9. **Lead-magnet block** — gated PDF / waitlist / quote → email capture. Web3Forms or Formspree.
10. **Footer CTA** — form + tel: + map. Repeat primary CTA.

Plus: exit-intent modal (desktop, 1× session), sticky header CTA after hero scrolls past.

### PHASE 5 — Premium Signatures (pick 4-6, niche-fit)

Wedding/luxury signatures — reusable:

- 196px italic display headline w/ accent highlighter strip behind one word (skewed -3deg)
- Giant background numerals 01/02/03 at 5% opacity per section
- Ken Burns 22s slow zoom on hero + final CTA images
- Film grain SVG turbulence overlay (35% opacity, mix-blend overlay)
- Marquee scrolling brand band (38s linear, ✦ separators)
- Mouse-follow cursor orb (raf, 0.14 easing)
- Italic dropcap on About paragraph (4.6em, accent color)
- Asymmetric image stack (img2 overlaps img1, -120px offset, 8px paper border)
- Inline CTA: arrow + label + italic split (`→ Inquire — begin your vows`)
- Editorial pricing table w/ hairline dividers (NOT gold ribbon cards)
- Logo monogram italic Instrument Serif

Skip if niche = HVAC/plumbing (overdesigned hurts conversion). Apply heavily if niche = wedding/luxury/wellness/photography.

### PHASE 6 — Conversion Guardrails

- Lighthouse mobile Perf ≥90, LCP ≤2.5s
- Hero loads <1s on fast connection (priority hint + preload)
- Tap targets ≥48px
- Form ≤6 fields
- Primary CTA visible every viewport scroll
- Phone link `tel:+1...` w/ click tracking
- DemoBadge sticky bottom-right: "Built by SkynetLabs ↗"

### PHASE 7 — SEO + Compliance

- `robots.txt` + `sitemap.xml` + `vercel.json` (cache headers + security)
- Spec demo: `noindex,nofollow` 90 days minimum (Feb 2026 SpamBrain)
- LocalBusiness + FAQPage + Organization JSON-LD
- og:image 1200×630 (render via existing LI card pipeline if available)
- Canonical URL, meta description, twitter card
- Footer disclosure: "Demo by SkynetLabs · example.com" (legal+SEO shield)

### PHASE 8 — Ship + Pitch

```bash
# 1. Repo
gh repo create <niche>-demo --public --license mit --description "..."
git init && git add . && git commit -m "feat: initial demo"
git push

# 2. Vercel
vercel --prod
# Confirm clean alias: <niche>-demo.vercel.app
```

Send pitch using `pitch-template.md`. Always:

- Demo URL in first 3 lines
- Bullet list of what's built using THEIR vocabulary from brief
- 5-8 scope-unlocking questions (see `scope-questions.md` per niche)
- 1 bonus pricing-lever Q
- Soft close: "live on your domain inside the week"
- NO fee quoted upfront

---

## OUTPUTS

```
GITHUB/<niche>-demo/
├── index.html (or app/ if Next.js)
├── docs/
│   ├── RESEARCH.md         # Phase 1 output
│   ├── DESIGN-TOKENS.md    # Phase 2 output
│   ├── CLIENT-PITCH.md     # full pitch log + scope Qs
│   ├── CLIENT-MESSAGE.md   # verbatim message sent
│   └── DIVI-PORT-MAP.md    # if WP brief
├── public/
│   ├── og.png
│   ├── favicon.svg
│   └── photos/             # niche-real, NOT Picsum
├── README.md               # MIT, "fork to use"
├── vercel.json
├── robots.txt
├── sitemap.xml
└── package.json (if Next.js)
```

---

## RULES (hard learned)

1. **Build first, pitch second.** See `feedback-speculative-build-pitch`. ~10× higher close rate vs cold proposal.
2. **3-variant lock + sticky switcher.** Always ship 3 differing-on-axis variants w/ top-right sticky switcher. Client picks → polish.
3. **Niche-tune everything.** Wedding luxury ≠ corporate luxury. Navy + bright gold reads SaaS. Match buyer's mental palette.
4. **Real photos, not Picsum.** Unsplash CDN per niche minimum. Real client photos when available.
5. **Unique testimonials per niche.** Same testimonial across 20 sites = caught + flagged.
6. **Footer credit always.** "Built by SkynetLabs ↗" + example.com link. Free portfolio surface.
7. **noindex spec demos 90 days.** Then flip per-demo when traffic proven. SpamBrain Feb 2026.
8. **No batch SEO publish.** Drip 3-5/week × months for case studies. Scaled-content classifier.
9. **Phase 2 upsell ALWAYS in pitch.** Full site / SEO pages / retainer / membership. Phase 1 is audition.
10. **5-8 scope Qs not 16.** One early pitch sent 16, slowed reply. 5-8 is sweet spot. 1 of them = pricing-lever.
11. **First-person if solo, "we" if team.** Don't fake size. Imply depth via process + photos + trust grid.
12. **No invented metrics.** See `feedback-no-fake-claims`. Real builds, real wins, real photos only.
13. **Image rotation log.** If using your own photo set, run `python _pick-next.py` from your images folder. Never by eye.

---

## REFERENCE FILES

- `case-studies.md` — 9 shipped client builds, full table w/ stack + outcome
- `design-tokens.md` — niche → palette + font pair lookup
- `scope-questions.md` — 5-8 Qs per niche template
- `pitch-template.md` — verbatim message structure
- `competitor-research-template.md` — parallel agent prompts

---

## When NOT to use

- Existing retainer client (use direct build, skip pitch flow)
- Pure WordPress edit job (no demo needed, just quote)
- Hourly/UI-fix bug (this is overkill)
- E-commerce w/ 100+ SKUs (different system — Shopify/Woo, not landing)

For those: skip skill, build direct.
