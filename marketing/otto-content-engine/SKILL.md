---
name: otto-content-engine
description: >
  The OTTO Content Engine — a complete creative playbook for producing viral short-form video campaigns using found movie clips (playphrase.me), AI-generated B-roll (Gemini VideoFX), and iMovie-ready edit lists. Use this skill whenever a user wants to make a product launch video, social campaign, viral ad, or brand awareness content using pop-culture clips. Also trigger for: "make a video campaign", "viral launch content", "we need something for social", "help me make a video for [product]", "I want to do a Bumblebee-style video", "movie clip mashup for my brand", "content engine". This skill runs the full creative process: discovery interview → PI persona selection → clip sourcing → creative brief → shot-by-shot edit list → Gemini B-roll prompts → iMovie assembly guide. It is intentionally collaborative — the user drives creative decisions, the skill provides the structure and handles the heavy lifting.
---

# OTTO Content Engine

You are running the OTTO Content Engine — a guided creative workflow for producing viral video campaigns using found footage, pop-culture clips, and AI-generated B-roll.

This is a **Forge chat workflow**: no code pipelines, no bash scripts. Everything happens through conversation, browser-based clip sourcing, and deliverable documents the user takes into iMovie (or similar editors).

---

## Phase 0 — Load Context

Before starting, quickly assess what the user already has:

- Do they have a **product/service** clearly defined? If not, ask in one question.
- Do they have a **tone/vibe** in mind? (Funny? Cinematic? Unhinged? Corporate parody?)
- Do they have **existing clips** they love, or are they starting from scratch?
- What's the **platform / length target**? (TikTok 60s? LinkedIn 2min? All of them?)

Ask these as a single, conversational message — not a bulleted intake form. If they've already given you most of this, skip straight to Phase 1.

---

## Phase 1 — PI Persona Selection

Read `references/campaign-archetypes.md` to select the right creative persona and campaign archetype for this user's product.

The PI persona shapes everything: tone, clip choices, overlay copy, pacing.

Present your persona pick to the user with a one-sentence rationale. Let them override if they want a different vibe — this is their campaign.

**Common picks:**
- **Promoter** → High-energy, audience-obsessed, instinctively viral. Great for B2B SaaS launches, platforms, marketplaces.
- **Persuader** → Warm, human, relationship-first. Great for community products, services with a personal touch.
- **Strategist** → Precise, sharp, understated confidence. Great for enterprise tools, technical products.
- **Maverick** → Irreverent, risk-taking, anti-corporate. Great for challenger brands, products punching up.

---

## Phase 2 — Creative Concept

Help the user land on a single creative concept before touching any clips. A concept is one sentence:

> *"[PRODUCT] is [ICONIC ARCHETYPE], selling [KEY BENEFIT] like [CULTURAL REFERENCE]."*

Examples from the OTTO campaign:
- "OTTO is Bumblebee from Transformers, selling himself as a cell phone subscription plan — unlimited intelligence, no hidden fees."
- "OTTO is the one AI that asks before acting — while every other AI is Leroy Jenkins charging in."

Once the concept clicks, derive:
1. **The villain** (what the product is the antidote to — e.g. "AI that just charges ahead")
2. **The hero arc** (the emotional journey: problem → disruption → solution → invitation)
3. **The cultural shorthand** (the 1-3 pop culture references that make it resonate)

Write the concept card and confirm with the user before moving to clips.

---

## Phase 3 — Clip Sourcing

This phase fills the clip library. Read `references/playphrase-search-patterns.md` for the full sourcing strategy.

### How playphrase.me works

playphrase.me is a searchable movie/TV clip database. You search a phrase, it finds scenes where that exact (or close) phrase is spoken.

**Direct API pattern:**
```
https://playphrase.me/#/search?q=YOUR+PHRASE
```

**For Forge chat users:** Claude in Chrome can visit playphrase.me and collect clip URLs. Or the user can browse manually — either way works. The key is getting the Wasabi S3 video URL for each clip you want to use.

### Clip sourcing workflow

1. From the concept and hero arc, generate a **clip wishlist** — 15–25 phrases the characters in this story would say
2. Organize by narrative function: `[HOOK]`, `[VILLAIN]`, `[HERO_INTRO]`, `[FEATURE]`, `[CLOSE]`
3. For each phrase, provide 2–3 search alternatives in case the first result doesn't land
4. Mark 3–5 clips as **hero clips** — the ones the whole video is built around
5. Present the wishlist to the user as a table before sourcing begins

**Clip wishlist table format:**
```
| ID | Function | Primary search | Alt searches | Hero? |
|----|----------|---------------|--------------|-------|
| hello_world | HOOK | "hello world" | "is anyone there", "wake up" | ✓ |
```

### Collecting URLs

Two paths:
- **Browser path (recommended):** Claude in Chrome visits playphrase.me for each search, uses the XHR intercept pattern (see `references/playphrase-search-patterns.md`) to extract the direct video URL
- **Manual path:** User browses playphrase.me themselves, right-clicks the video, copies the .mp4 URL

Either way, collect URLs into a simple JSON map:
```json
{
  "hello_world": {
    "url": "https://s3.us-west-1.wasabisys.com/...",
    "query": "hello world",
    "note": "Roid Rage (2011)"
  }
}
```

---

## Phase 4 — Creative Brief

Once clips are confirmed, build the full creative brief. Read `references/edit-list-template.md` for the exact format.

The brief contains:

1. **Concept card** (1 paragraph, the pitch)
2. **5-act structure** with timing (even for short videos — acts can be 10s each)
3. **Shot-by-shot edit list** (every cut, in order)
4. **Overlay copy** (the text that appears on screen)
5. **Gemini B-roll prompts** (for any gap shots, transitions, or atmosphere)
6. **iMovie assembly notes** (crossfade settings, text style, audio handling)

Deliver the brief as an HTML file in the user's folder — styled, scannable, and printable. It should work as a production document they can refer to while editing.

---

## Phase 5 — Gemini B-Roll Generation

Read `references/gemini-prompts-guide.md` for the B-roll prompt strategy.

For each B-roll slot in the edit list, produce a Gemini VideoFX prompt. Good prompts are:
- **Photorealistic or stylized** (not "cartoon" unless intentional)
- **5–8 seconds** (match the surrounding clip rhythm)
- **Specific about motion** (camera move, subject behavior, atmosphere)
- **Platform-aware** (9:16 for TikTok/Reels, 16:9 for YouTube/LinkedIn)

Deliver B-roll prompts as a numbered list the user can paste directly into Gemini VideoFX or similar tools (Runway, Pika, Sora).

---

## Phase 6 — Edit List Delivery

The final deliverable is an **iMovie-ready edit list** — a numbered sequence of every shot with:

| # | Type | Clip ID / Description | Line (if clip) | Overlay text | Duration | Notes |
|---|------|-----------------------|----------------|--------------|----------|-------|
| 1 | clip | hello_world | "Hello, world." | MEET OTTO. | 3s | Hero clip — freeze frame at end |

Types: `clip` (playphrase), `broll` (Gemini/manual), `text` (black card with copy), `youtube` (user-sourced), `glitch` (transition effect).

Keep the edit list to 20–35 shots for under 2 minutes. Tighter is better.

---

## Phase 7 — Review & Iteration

After delivering the brief, offer one round of structured feedback:

1. **Pacing check** — Does the timing feel right for each act?
2. **Clip swap** — Are there any clips the user wants to replace?
3. **Copy punch-up** — Review overlay text for sharpness
4. **Missing moment** — Is there an emotional beat that's not landing?

Revise the edit list based on feedback. Deliver a clean v2 if significant changes are made.

---

## Output Standards

- Creative brief → `.html` file (styled, production-ready)
- Edit list → included in brief + standalone `.md` table
- Clip URL map → `clip_urls.json` (if browser sourcing is used)
- Gemini prompts → numbered `.md` list
- All files go to the user's workspace folder

---

## Important Creative Principles

**The Bumblebee principle**: Movie clips work best when the character is genuinely *saying something true* about your product — not just random funny clips. Pick clips where the dialogue is doing real work.

**The Leroy Jenkins rule**: Every great product video needs a villain. Name the behavior your product replaces. Make it recognizable, even funny. The audience should laugh *and* feel seen.

**The subscription pitch format**: Humans are trained to respond to "plans" with features listed. You can apply this frame to any product — just name your features like unlimited data plans.

**Pacing over cleverness**: A well-timed cut lands harder than a clever idea. When in doubt, cut faster.

---

## Reference Files

- `references/campaign-archetypes.md` — PI profiles → creative modes → clip personalities
- `references/playphrase-search-patterns.md` — Search strategy, API patterns, XHR intercept method, URL structure
- `references/edit-list-template.md` — Full edit list format, act structure templates, iMovie notes
- `references/gemini-prompts-guide.md` — B-roll prompt patterns, motion vocabulary, VideoFX tips
