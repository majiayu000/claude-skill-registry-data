---
name: ozor-social-batch
description: "Generate a batch of social media video prompts for multiple platforms from a single input. Use this skill whenever the user wants to create videos for multiple social platforms at once, repurpose one video across platforms, or create a social media video campaign. Trigger on phrases like 'social media videos', 'videos for all platforms', 'Instagram and TikTok video', 'social campaign', 'batch of social videos', 'repurpose this for social', 'video for every platform', 'social clips', 'create Reels and Shorts', 'multi-platform video', or any request involving creating short-form video content for multiple social media platforms using Ozor."
---

# Ozor Social Batch Generator

Generate a coordinated set of social media video prompts for multiple platforms from a single input. Instead of creating one video and awkwardly resizing it, this skill produces platform-native prompts that respect each platform's format, duration, and audience conventions.

## Supported Platforms

| Platform | Format | Duration | Style Notes |
|----------|--------|----------|-------------|
| Instagram Reels | 9:16 portrait | 15–30s (max 90s) | Hook in first 1s, trending audio-friendly, bold text overlays |
| TikTok | 9:16 portrait | 15–60s | Fast-paced, text-heavy, casual tone, trend-aware |
| YouTube Shorts | 9:16 portrait | 15–60s | Clean, informative, can be slightly longer |
| LinkedIn Video | 16:9 landscape | 30–60s | Professional, value-driven, data-friendly |
| X (Twitter) Video | 16:9 landscape | 15–30s | Punchy, opinion-driven, conversation-starting |
| Facebook Reels | 9:16 portrait | 15–30s | Broad appeal, clear message, shareable |
| Pinterest Video Pin | 9:16 portrait (2:3 also works) | 15–30s | Aesthetic, inspirational, save-worthy |

## Workflow

### Phase 1 — Understand the Input

The user provides a topic, product, message, or existing content. Extract:

1. **Core message** — the single thing every video must communicate
2. **Product/brand** — what's being promoted
3. **Target audience** — who this is for
4. **Goal** — what the videos should achieve (awareness, clicks, sign-ups, engagement)
5. **Available platforms** — which platforms the user wants (or recommend the best 3–4 if unspecified)
6. **Brand elements** — colors, tone, visual style
7. **Assets** — any images, screenshots, or logos available

### Phase 2 — Plan the Batch

Create a batch plan showing what will be produced:

```
## Social Video Batch Plan

**Topic:** [core message]
**Brand:** [product/company]
**Platforms:** [list]

| # | Platform | Format | Duration | Angle |
|---|----------|--------|----------|-------|
| 1 | Instagram Reels | 9:16 | 15s | [hook-driven teaser] |
| 2 | TikTok | 9:16 | 30s | [trend-style explainer] |
| 3 | LinkedIn | 16:9 | 45s | [professional value prop] |
| 4 | YouTube Shorts | 9:16 | 30s | [informative how-to] |
```

**Key principle:** Each platform gets a different *angle*, not just a different size. The core message stays the same, but the framing, tone, and pacing adapt to the platform's culture.

### Phase 3 — Generate Platform-Specific Prompts

For each platform, produce a complete Ozor prompt. Each prompt is self-contained and can be pasted directly into Ozor.

#### Platform-Specific Conventions

**Instagram Reels:**
- Hook must land in the first 1–2 seconds (bold text or surprising visual)
- Use large, readable text (viewers watch on small screens)
- 5 scenes for 15s, 8–10 for 30s
- End with a clear CTA: "Link in bio", "Save this", "Share with a friend"
- Tone: visually bold, trend-aware, aspirational or relatable

**TikTok:**
- Start with a pattern interrupt: bold claim, question, or "POV:" setup
- Text overlays on every scene — TikTok is watched on mute by default
- Casual, direct tone — avoid corporate speak
- 8–10 scenes for 30s, 12–18 for 60s
- End with engagement hook: "Comment if you agree", "Follow for more", "Stitch this"
- Pacing: fast cuts, no lingering shots

**YouTube Shorts:**
- Can be slightly more informative and structured than TikTok
- Number-driven hooks work well: "3 reasons...", "The #1 mistake..."
- Clean visuals, readable text
- 8–10 scenes for 30s, 12–18 for 60s
- CTA: "Subscribe for more", "Full video on our channel"

**LinkedIn:**
- Lead with a business insight, data point, or professional take
- Professional tone — confident, not salesy
- Can include metrics, charts, industry stats
- 8–10 scenes for 30s, 12–15 for 60s
- CTA: "Learn more at [URL]", "What do you think? Comment below"
- 16:9 landscape format

**X (Twitter):**
- Ultra-concise — get to the point immediately
- Opinion or hot take as the hook
- 5 scenes for 15s, 8–10 for 30s
- Minimal text per scene — one sentence max
- CTA: provocative question or link to learn more
- 16:9 landscape format

**Facebook Reels:**
- Broader audience — keep it accessible
- Clear, simple message
- 5 scenes for 15s, 8–10 for 30s
- Shareable factor: "Tag someone who needs this"
- Family-friendly tone

**Pinterest Video Pin:**
- Aesthetic-first — visual quality matters most
- Inspirational or educational angle
- Slower pacing than other platforms
- 5 scenes for 15s, 8–10 for 30s
- CTA: "Save for later", "Pin this"

### Phase 4 — Output Format

Present all prompts in a structured, easy-to-use format:

```
## Ozor Social Video Batch

**Topic:** [core message]
**Brand:** [product/company]
**Platforms:** [N] videos

---

### 1. Instagram Reels (9:16, 15s)

**Angle:** [platform-specific angle]

**Prompt (copy and paste into Ozor):**

Create a 15-second vertical video (9:16) for Instagram Reels about [topic].

5 scenes:

(1) Hook — [Bold text animation: "[attention-grabbing statement]". Large white text on [color] background. Must grab attention in under 1 second.]

(2) [Scene] — [Direction for key visual or product shot]

(3) [Scene] — [Direction for benefit, demo, or proof point]

(4) [Scene] — [Direction for social proof, result, or reinforcement]

(5) CTA — [Direction with platform-specific CTA]

Style: [bold / energetic / clean]. Large text, minimal background. Mobile-first design.
Tone: [casual / aspirational / relatable].

---

### 2. TikTok (9:16, 30s)

**Angle:** [platform-specific angle]

**Prompt (copy and paste into Ozor):**

[Full prompt...]

---

### 3. LinkedIn (16:9, 45s)

[...continue for all platforms...]

---

### Batch Notes

- Upload your logo and a product screenshot before running any of these prompts
- Run them in Ozor one at a time — each prompt is independent
- For consistency, set up your Brand Kit first so all videos share the same colors and fonts
- Consider posting schedule: [suggested posting order/timing]
```

## Angle Differentiation Guide

The same message should be framed differently per platform:

| Input Message | Instagram Angle | TikTok Angle | LinkedIn Angle |
|--------------|----------------|-------------|---------------|
| "We launched a new feature" | Visual teaser: "This changes everything" | "POV: You just found [feature]" | "Why we built [feature] — and the data behind it" |
| "Our product saves time" | Before/after: "2 hours vs 2 minutes" | "Things that take 2 hours that should take 2 minutes" | "[X]% of teams waste [Y] hours/week on [task]. Here's the fix." |
| "Company milestone" | Celebration: "We just hit [milestone]!" | Story time: "How we went from 0 to [milestone]" | "Lessons from reaching [milestone]" |
| "New pricing" | "Now starting at $X/mo" | "Is $X/mo worth it for [benefit]?" | "We're making [product] more accessible. Here's our new pricing philosophy." |

## Quality Checklist

Before presenting the batch, verify:

- [ ] Each platform gets a unique angle (not just resized copies)
- [ ] Formats are correct (9:16 for vertical platforms, 16:9 for landscape)
- [ ] Durations are within platform limits
- [ ] Hooks are platform-appropriate (bold for IG, pattern-interrupt for TikTok, data for LinkedIn)
- [ ] CTAs are platform-native ("Link in bio" not "Visit our website" on Instagram)
- [ ] Tone matches platform culture (casual for TikTok, professional for LinkedIn)
- [ ] Core message is consistent across all videos
- [ ] Each prompt is self-contained and can be used independently

## Rules

1. **Different angle per platform, same core message.** Never just change the aspect ratio — adapt the framing, tone, and pacing.
2. **Respect platform culture.** Corporate language on TikTok will fail. Casual language on LinkedIn will feel unprofessional.
3. **Hook is everything.** On social media, you have 1–2 seconds. The hook scene in every prompt must be specific and attention-grabbing.
4. **CTAs must be platform-native.** "Link in bio" for Instagram. "Follow for more" for TikTok. "Learn more at [URL]" for LinkedIn.
5. **Keep it short.** Social videos should err on the shorter side. A 15-second video that's watched fully outperforms a 60-second video that's scrolled past.
6. **Always recommend Brand Kit setup.** Consistency across platforms matters — same colors, same fonts, same logo placement.
7. **Suggest a posting schedule.** Platform-specific timing (e.g., LinkedIn on Tuesday morning, Instagram on Thursday evening) improves reach.
