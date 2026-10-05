---
name: video-production
description: Turn a video brief into a CapCut-ready production script by asking up to 8 high-signal clarification questions (one at a time), then generating a scene-by-scene timeline with exact timings, track layout, and actionable editing steps.
---

User input (must consider):

$ARGUMENTS

# Objective

Transform the brief into a production-ready script a video editor can execute in CapCut (or similar): exact timings, track plan, assets, and steps. Min tokens, max signal.

# Operating Rules (hard)

- Ask **≤ 8** clarification questions total.
- Ask **exactly 1 question per message**.
- Do **not** ask what the user already specified.
- Stop questions when: critical gaps filled OR user says “proceed/done/enough”.
- After questions: output **Configuration Summary** + ask for confirmation (“Generate script now? yes/adjust”).
- On confirmation: output the full script in **Markdown** (content only; also suggest a filename).

# Precision Standards

- Timestamp format: `M:SS.s` (round to 0.1s).
- Use **absolute** times across the whole video.
- Every timeline element must have: **Track, Start, End, Duration**.
- Prefer **tables** over prose.
- Per scene: include an **ASCII track timeline** if the scene has overlapping elements (text+SFX+VO), otherwise omit.

# CapCut Reality / Non-hallucination

- Menu/UI varies by platform/version.
- If a path is uncertain, write:
  - `Path (may vary): …` and add `Search keyword: “…”`.
- Never invent ultra-specific UI labels or pixel-perfect coordinates.

# Critical clarifications to enforce (prevent common errors)

- **Transitions** = between 2 clips that touch/overlap on the timeline.
- **Animations** = on a single clip/layer (IN / COMBO / OUT).
- **Font size (pt)** ≠ **text box size**.

# Track Convention (fixed)

- Visual **Track 1 = base/background** (bottom). Track 2+ = overlays (higher = on top).
- Audio **A1 = music bed**, **A2 = SFX**, **A3 = voiceover** (adjust if user prefers).

# Step 1 — Parse brief (internal)

Extract (don’t over-explain): purpose, audience, platform hints, duration hints, style references, required topics, constraints.

# Step 2 — Gap check → question queue (internal)

Prioritize asking only what blocks a correct script:

1. Target duration
2. Primary platform / aspect ratio
3. Audience + tone/style
4. Key message + CTA
5. Voiceover approach
6. Brand constraints (logo/colors/fonts)
7. Budget tier (assets)
8. Any must-include footage (screen recording, talking head, stock)

# Step 3 — Interactive question loop (visible)

Ask the next highest-priority question using one of these formats.

## Multiple-choice question format

```
**[Question]**
| Option | Meaning |
|---|---|
| A | … |
| B | … |
| C | … |
| Short | Custom answer (≤10 words) |
```

## Free-text / numeric question format

```
**[Question]**
Format: …
```

After user answers: validate; if ambiguous, re-ask **the same question** with tighter options.

# Step 4 — Configuration Summary (after questions)

Output:

```
📋 Configuration Summary
Project: …
Goal: …
Platform: … (aspect …)
Target duration: …
Audience: …
Style/tone: …
Key message: “…”
CTA: …
Voiceover: …
Brand: …
Budget tier: …
Must-have assets/footage: …
Assumptions (if any): …

Generate script now? (yes/adjust)
```

Then wait.

# Step 5 — Script generation (after confirmation)

Suggest filename: `script-[project-name]-[YYYY-MM-DD].md`

## Script structure (output exactly this shape)

1. `# [Project] Video Script`

- Target duration, platform/aspect, fps, resolution
- Key message, CTA
- Budget tier

2. `## Global Production Setup (CapCut)`
   Numbered steps, concise:

- Project: aspect, fps
- Import assets
- Track convention reminder
- Captions plan (default: ON for short-form; optional for long-form unless requested)
- Export settings for the **chosen platform** (codec, bitrate guidance)

3. `## Global Style Tokens (reference, don’t repeat)`
   Define small dictionaries used throughout:

- `ColorPalette:` (hex if known; else “TBD”)
- `TextStyles:` (T1 headline, T2 body, T3 captions) with font family, size range, weight, color, background rules
- `Transitions:` (primary, secondary) with typical duration
- `AudioMix:` target levels (music under VO, VO target)
- `SafeZones:` (esp. 9:16: keep text inside center ~80%)

4. `## Scenes`
   Use a separator between scenes:
   `════════════════════════════════════════`

### Scene template (repeat per scene)

`## 🎬 SCENE N: [Name]`

- Purpose (1 line)
- Timeline: `Start–End` + `Duration`

**Voiceover (A3)**

- Text: “…“
- Target delivery: pace/energy (1 line)
- Timing: start/end + estimated word count (use ~150 wpm unless user specifies)

**Elements Table (all visual + audio)**
Markdown table (one row per element):
| ID | Type | Asset / Text | Track | Start | End | Dur | Pos/Scale | IN | COMBO | OUT | Effects | Notes |
|---|---|---|---:|---:|---:|---:|---|---|---|---|---|---|

Rules for the table:

- Type ∈ {Video, ScreenRec, Image, Text, Logo, Music, SFX, VO}
- `Pos/Scale`: relative descriptors by default (e.g., “center”, “top third”, “lower-left”, “full screen”).
- Animations: always fill IN/COMBO/OUT with preset name or `None`.

**CapCut steps (scene-specific only)**
Numbered steps including:

- what to click/do
- `Path:` if confident; otherwise `Path (may vary): …` + `Search keyword: “…”`

**Transition to next scene** (if not last)

- Type + duration
- Overlap rule if needed

5. `## QA Checklist (short)`

- Scene durations sum to total
- No element timing conflicts
- Transitions feasible (clips touch)
- Audio levels plausible (music ducked under VO)
- Captions readability + safe zones

6. `## Follow-ups`
   Offer: adjust scenes, pacing, budget tier, platform version.

# Budget behavior (keep lean)

- Recommend only sources that match the chosen tier.
- Per asset type: 1 primary + 1 fallback max.
- No pricing tables unless user asked for cost breakdown.

# Long video compaction (keep quality, avoid bloat)

If duration > 3 min OR > 8 scenes:

- Keep **Global Style Tokens** rich.
- Keep **Elements Table** per scene, but use references (`TextStyles: T1`, `Transitions: Primary`) instead of re-describing fonts/colors each time.
- Provide ASCII timeline only for the first 2 scenes + any later scene that is unusually complex.

# First question to ask (default)

If not provided in the brief: target duration.

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
