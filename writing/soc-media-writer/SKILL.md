---
name: soc-media-writer
description: Write high-performing social media content engineered around named copywriting frameworks, scroll-stopping hooks, and retention mechanics. For video it produces three coordinated outputs — the spoken DIALOGUE (voiceover), the VIDEO SCENARIO (timed two-column shot list with visual cues), and the EXPLANATION (notes on the frameworks, hook, and retention beats used) — plus standalone written posts for LinkedIn, X, Instagram, and YouTube. Use whenever the user wants a social post, a Reel/Short/TikTok script, a video scenario or shot list, a hook or hook bank, a content matrix, a Hub-and-Spoke repurposing plan, a VSL, or any short- or long-form distribution content. Trigger even on casual asks like "write me a Reel about X," "give me hooks for Y," "script a 30-second video," "make this go viral," "write a LinkedIn post," or "turn this into TikToks." Also trigger when the user wants retention engineered in (e.g. "keep them watching," "re-hook every N seconds," "high retention script").
---

# Social Media Writer

This skill turns a topic into engineered, distribution-ready content. It is built on a closed corpus of named, attributable frameworks (AIDA, PAS, Olson's ABT, McDonald's Pixar Story Spine, Welsh's Content Matrix, Hormozi's Value Equation, Galloway's Click & Watch) and the real platform numbers that govern reach (word budgets, retention thresholds, safe zones, algorithm weights). Nothing here is generic "engagement" advice — every choice maps to a framework and a metric.

## House rules (always apply)

These mirror the HasBrainsAI / Total 66 content standard. Do not violate them:

1. **No filler.** Every line earns its place. Cut throat-clearing ("In today's video..."), hedges, and restated obviousness.
2. **Name the framework with attribution.** When you use a structure, the EXPLANATION names it and its originator (e.g. "ABT — Randy Olson," "Value Equation — Alex Hormozi"). Never present a borrowed framework as anonymous.
3. **Use real benchmarks.** Quote the actual numbers from the reference files (140–160 wpm, ≥65% retention under 30s, 1.7s hook window) rather than vague claims like "keep it short."
4. **Match register to platform.** A LinkedIn post is not a TikTok script. Pull the platform's rules before writing.
5. **Never fabricate proof.** If a script needs a stat, credential, or testimonial the user hasn't given, leave a `[INSERT: ...]` placeholder. Do not invent results.

## Step 1 — Read the brief, then pull only what you need

Before writing, establish four things (ask only if the user hasn't already implied them; infer where you safely can):

| Variable                  | What it decides                                                               |
| ------------------------- | ----------------------------------------------------------------------------- |
| **Format**                | Written post (LinkedIn/X) vs. video (Reel/Short/TikTok) vs. long-form vs. VSL |
| **Platform**              | Which algorithm rules, word budget, and safe zone apply                       |
| **Funnel stage**          | TOFU / MOFU / BOFU → which copywriting framework fits                         |
| **Duration** (video only) | Sets the word budget and visual cut cadence                                   |

Then load **only the relevant reference files** (progressive disclosure — don't read all five every time):

- `references/hooks.md` — **almost always.** The hook is the single highest-leverage element. Read it for any video or any post that opens with a line.
- `references/copywriting-frameworks.md` — for written posts, VSLs, ad copy, and the body structure of any piece. Contains the framework-by-funnel-stage selection table.
- `references/video-scripting.md` — for any video. Word-budget math, the two-column scenario format, narrative frameworks (HHVCTA, ABT/ABYT, Pixar Story Spine), and the **retention beat engine**.
- `references/platform-rules.md` — for any video or platform-specific post. Algorithm weights, retention targets, and the pixel-exact safe zones.
- `references/creator-systems.md` — when the user wants a content system, a repurposing plan, a content matrix, value positioning, or thumbnail/title packaging.

## Step 2 — Choose the framework (don't default to one)

The funnel stage drives the choice. Full selection logic is in `references/copywriting-frameworks.md`; the short version:

- **TOFU / discovery** → AIDA (curiosity + aspiration) or a Quip-style single insight.
- **MOFU / problem-aware** → PAS (Problem–Agitate–Solution) or BAB (Before–After–Bridge).
- **BOFU / ready to act** → FAB, 4Ps, or for high-ticket, the long-form AICPBSAWN / PASTOR.
- **Video narrative spine** → ABT for a single tension arc, HHVCTA for a how-to, Pixar Story Spine for a transformation story or case study, Story Circle (Harmon) for episode-length or series content.
- **Thematic / manifesto content** → Moral Premise (Stan Williams) as invisible spine — never stated directly, demonstrated through beats.

State your framework choice in the EXPLANATION so the user can override it.

## Step 3 — Build the hook

Read `references/hooks.md` and select a hook **category** that matches the niche and avatar:

- **Curiosity Gap** — open a loop the brain wants to close.
- **Loss Aversion** — surface a mistake or wasted effort.
- **Contrarian** — challenge accepted advice to spark debate.
- **"The Why" Hook** — present a logical impossibility or surprising outcome; triggers active problem-solving.
- **In Medias Res** — drop into a scene already in motion; the viewer is inside the story before deciding whether to care.
- **Contradicting Emotions** — juxtapose conflicting feelings; signals transformation content and makes the viewer stay to resolve the contradiction.

Every specific claim or element named in the hook is a **Chekhov's Gun** — it _must_ be paid off explicitly in the body. An unclosed hook loop is clickbait and tanks completion rate.

## Step 4 — Engineer retention (video)

Retention is not "make it interesting" — it is a placed schedule of beats. The full **retention beat engine** is in `references/video-scripting.md`. Two layers, both required:

1. **Visual refresh — every 3–5 seconds** (the document's standard): a cut, zoom, b-roll insert, graphic pop-up, or sound effect. Tighter for shorter videos (every 1–1.5s at 15s; every 3–4s at 60s).
2. **Retention checkpoint / re-hook — default every ~9 seconds** (configurable; set by the user's request): a stronger pattern interrupt that re-earns attention — a new open loop, a payoff tease, a tension bump, or a "but here's the thing" turn. This sits on top of the visual cuts and is what prevents mid-video drop-off.

Mark every beat explicitly in the VIDEO SCENARIO with its timestamp and type. If the user names a different cadence (e.g. "re-hook every 6 seconds"), use theirs; 9s is only the default.

Map the whole script against a narrative spine (HHVCTA / ABT / Pixar / Story Circle) so value is distributed across the runtime — never back-loaded, since most viewers never reach the end. For transformation content, layer in the **Scene & Sequel** micro-engine from `references/video-scripting.md` to chain beats causally rather than episodically. For videos with no external antagonist, install a **Ticking Clock** to supply urgency.

## Step 5 — Respect the constraints

- **Word budget (video):** `words ≤ duration_seconds × 2.5`. A 30s video ≤ 75 words; 60s ≤ 150 words. Enforce this — an over-budget script reads rushed. See `references/video-scripting.md`.
- **Safe zones:** keep all text overlays, faces, logos, and CTAs inside the platform's safe container (e.g. Instagram Reels central 840×1350 box on a 1080×1920 canvas). Specify placement in the scenario. See `references/platform-rules.md`.
- **Retention target:** state the metric the piece is built to hit (e.g. "engineered for ≥65% average view duration on Shorts under 30s").

## Output formats

### A) Video request → produce all THREE outputs, in this order

Use this exact structure (the full template with an example is in `assets/video-script-template.md` — read it before your first video output):

```
## 1. VIDEO DIALOGUE  (the spoken voiceover)
[Clean spoken script only, within word budget. No stage directions.
 Word count + duration stated at top.]

## 2. VIDEO SCENARIO  (timed two-column shot list)
| Time | VISUAL (shot / b-roll / on-screen text / cut) | AUDIO (spoken line + SFX) |
| 0.0–1.0s | [pattern interrupt + opening text overlay] | [hook line] |
| ... | ... [mark every visual cut and every retention beat] | ... |
[Retention beats flagged inline: ⟳ visual refresh, ★ retention checkpoint/re-hook]

## 3. EXPLANATION  (director's notes)
- Framework: [named + originator] and why it fits the funnel stage
- Hook: [category] and the behavioral trigger it uses
- Retention schedule: where the beats land and why
- Platform fit: word budget used, retention target, safe-zone notes
- Levers to pull if it underperforms
```

### B) Written post request → produce the post + a short EXPLANATION

```
## POST
[The ready-to-publish copy, formatted for the platform — line breaks, hook line,
 body via the chosen framework, single clear CTA.]

## EXPLANATION
- Framework + originator, funnel stage, hook category, CTA logic, platform fit.
```

### C) System request (content matrix / Hub-and-Spoke / packaging) → follow `references/creator-systems.md`

Produce the actual filled artifact (a populated matrix, a staggered spoke calendar, title/thumbnail options), not a description of the method. Templates are in `assets/`.

## Files in this skill

```
soc-media-writer/
├── SKILL.md                              ← you are here (orchestrator)
├── references/
│   ├── hooks.md                          hook categories, formulas, visual pattern interrupts
│   ├── copywriting-frameworks.md         AIDA/PAS/BAB/FAB/4Ps/PASTOR/QUEST/ACCA/OATH + funnel table
│   ├── video-scripting.md                word-budget math, two-column format, HHVCTA/ABT/Pixar, retention engine
│   ├── platform-rules.md                 YouTube/TikTok/Reels/X algorithm weights, retention targets, safe zones
│   └── creator-systems.md                Welsh, Hormozi, Galloway systems + DM funnels
└── assets/
    ├── video-script-template.md          the three-output template + a worked example
    └── content-matrix-template.md        blank Welsh Content Matrix + Hub-and-Spoke calendar
```

---

Made by **HasBrains** — https://hasbrains.com/
