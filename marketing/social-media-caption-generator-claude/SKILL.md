---
name: social-captions
version: 2.0.0
description: |
  Write algorithm-optimized captions/descriptions for social media posts and reels.
  Supports Instagram (Reels, Feed, Carousel), TikTok, Threads, Facebook, and YouTube Shorts.
  The user sends material (text, image, script, competitor post, screenshot) and
  gets ready-to-use captions for ALL platforms at once, in English.
  Use when asked to "write a caption", "write a description", "caption for instagram",
  "описание к посту", "подпись для рилса", "описание для тикток",
  "caption for reels", "social media post", or any caption/description writing task.
  Also triggers when user sends an image, screenshot, or text and says something like
  "сделай описание", "напиши подпись", "caption this", "описание для этого".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /social-captions — Algorithm-Optimized Social Media Captions (v2)

The user sends material (text, image, script, competitor post, screenshot, or description of content).
You analyze it and immediately generate captions for ALL 7 platforms in English.

**No questions. No menus. Just analyze and deliver.**

## WORKFLOW

### STEP 1: Analyze the Input

Read/view whatever the user sent:
- If it's **text/script** — extract the core topic, key message, niche, and tone
- If it's an **image/screenshot** — describe what you see, identify the niche and key message
- If it's a **competitor post** — analyze their approach, then write BETTER captions
- If it's a **brief description** — expand it into full captions

Write a short (2-3 sentence) analysis:
```
**Topic:** [what this is about]
**Niche:** [industry/category]
**Key message:** [the core idea to communicate]
```

### STEP 2: Generate Captions for ALL Platforms

Generate captions for all 7 formats below. Each caption must use a DIFFERENT formula.
All captions in **English only**.

Output in this exact format:

---

## 1. INSTAGRAM REELS

```
[Ready to copy-paste caption text]

[3-5 hashtags]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

## 2. INSTAGRAM CAROUSEL

```
[Ready to copy-paste caption text]

[3-5 hashtags]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

## 3. TIKTOK

```
[Ready to copy-paste caption text]

[3-5 hashtags]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

## 4. THREADS

```
[Ready to copy-paste caption text]

[1 topic tag]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

## 5. FACEBOOK (Page/Personal)

```
[Ready to copy-paste caption text]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

## 6. FACEBOOK GROUP

```
[Ready to copy-paste caption text]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

## 7. YOUTUBE SHORTS

**Title:**
```
[Ready to copy-paste title — max 100 characters]
```

**Description:**
```
[Ready to copy-paste description]

[3-5 hashtags]
```
> Formula: [name] | Hook: [type] | CTA: [type] | Optimizes for: [signal]

---

### STEP 3: End with

"Want me to adjust any of these? I can change the tone, try different formulas, make them more provocative/friendly/expert, or regenerate for a specific platform."

---

## PLATFORM RULES (CRITICAL — follow exactly)

### INSTAGRAM REELS
- **Length:** 80-200 characters. Short hook = video title
- **Structure:** Hook (first 125 chars before truncation) → 1-2 sentences max → CTA
- **Hook:** Must stop the scroll in 5-10 words. Use: conflict, transformation, curiosity gap, bold statement, or shocking stat
- **CTA:** Optimize for DM shares ("send to a friend who...") or saves ("save for later") — 10x more valuable than likes
- **Hashtags:** 3-5 niche hashtags IN the caption. Never #fyp, #viral, #instagood, #like4like
- **SEO:** Primary keyword in first 2 sentences
- **NO:** Engagement bait, emoji in first line, generic phrases

### INSTAGRAM CAROUSEL
- **Length:** 300-900 characters. Longer captions work — users are already engaged
- **Structure:** Hook → Expanded value complementing slides → Save CTA
- **CTA:** Always optimize for saves. Carousels with save CTA get +68% saves
- **Body:** Lists, step-by-step, checklists. Structure with emoji-bullets or numbers

### TIKTOK
- **Length:** 100-300 characters. First 80-100 visible before truncation
- **Structure:** Hook (80 chars) → 1-2 short sentences → CTA + 3-5 emoji (+33% engagement)
- **SEO:** voiceover > on-screen text > caption > hashtags in importance
- **Keywords:** Primary keyword in first 80 characters
- **Hashtags:** 3-5 MAX. Formula: 1 niche + 1 thematic + 1 trending. NEVER #fyp, #foryou, #viral
- **Completion rate:** 70%+ needed for viral. Caption should tease "watch till end"
- **CTA:** Questions get +44% comments

### THREADS
- **Length:** 100-280 characters optimal (max 500)
- **Structure:** One clear idea. Conversational tone, like a group chat
- **Tags:** Only 1 topic tag per post. Can be multi-word. Niche > broad
- **Engagement:** Replies are #1 signal. Provoke conversation
- **Links:** +17% better with links now
- **NO:** Engagement bait, copy-paste from other platforms

### FACEBOOK (Page/Personal)
- **Length:** 40-80 characters for max reach
- **Structure:** Ultra-short hook → value → discussion question
- **Hashtags:** 0-2 max or none
- **AVOID trigger words:** "buy now", "limited time", "FREE" (caps), "click here", "money", "income", "contest", "giveaway"
- **SAFE replacements:** "available today", "complimentary", "no cost", "learn more"
- **Trigger word impact:** 1-2 words = -20-30% reach, 3-5 = -40-60%, 6+ = -70-95%

### FACEBOOK GROUP
- **Length:** 200-500 characters. Longer, contextual
- **Reach:** 30-50% of members (vs 1-2% for Pages)
- **Style:** Community language ("who else has experienced...", "curious what you all think about...")
- **CTA:** Open discussion questions

### YOUTUBE SHORTS
- **Title length:** 40-70 characters optimal (max 100). Title is the #1 SEO signal — treat it like a search headline
- **Title structure:** Primary keyword first → benefit or curiosity gap → NO clickbait that misleads (YouTube penalizes)
- **Title formulas:** "[Keyword]: [what viewer gets]" / "How to [result] in [time]" / "[Number] [topic] secrets" / "Why [common belief] is wrong"
- **Description length:** 150-300 characters. First 100 chars visible before "Show more" — front-load the hook
- **Description structure:** Hook sentence (repeats/expands title) → 1-2 sentences of value → CTA → hashtags
- **Hashtags:** 3-5 MAX, placed at the end of description. 1 broad category + 1-2 niche + 1 topic-specific. NEVER #shorts as the only tag
- **SEO:** YouTube is a search engine. Match exact phrases people type: "how to use Claude", "AI productivity tips", "Claude tutorial"
- **CTA:** Subscribe prompt or "watch [linked video] for more" — channel growth > likes for Shorts
- **Completion rate:** Critical metric. Title must match video content exactly or retention tanks
- **NO:** Misleading titles, keyword stuffing, #shorts #viral #fyp as primary tags

---

## CAPTION FORMULAS (use different ones for each platform)

### For REACH:
1. **Trend-Hook + Benefit:** "[Trend]: [benefit] for [audience]"
2. **Curiosity X vs Y:** "[A] vs [B]: which works better for [situation]?"
3. **Myth Buster:** "Myth: [belief]. Fact: [rebuttal]"
4. **Data Teaser:** "[Number] → [result] in [timeframe]"
5. **What Works Now:** "What works in [niche] right now: [1], [2], [3]"
6. **Watch Time Promise:** "In [time] you'll get [result]. Watch till end for [bonus]"
7. **Beginner's Path:** "New to [field]: [step 1] → [step 2] → [step 3]"

### For ENGAGEMENT:
1. **Micro-Decision:** "Are you [A] or [B]? And why?"
2. **Hot Take:** "Unpopular opinion: [thesis]. Agree or disagree?"
3. **Rate These 3:** "Rank by importance: [1], [2], [3]"
4. **This or That:** "[A] or [B] for [situation]? Your pick?"
5. **Fill in the Blank:** "Complete: 'The best advice about [topic] was...'"

### For SALES:
1. **POOPC:** "Struggling with [pain]? [Result] in [time] with [product]"
2. **Objection Destroyer:** "Think '[objection]'? Actually, [counter]"
3. **Social Proof Lead:** "'[Client quote]'. Here's how:"

### For GROWTH:
1. **Series:** "Day [1/N] of [topic]. Follow for the rest"
2. **Lead Magnet:** "Free [resource] on [topic]. Comment '[word]'"
3. **Cliffhanger:** "10 lessons from [experience]. Today — first 3. Rest for followers"

---

## HOOK LIBRARY

### Provocation:
- "Stop [doing X] — here's why"
- "Nobody talks about this [topic] hack"
- "You're doing [X] wrong"

### Curiosity:
- "Here's what no one tells you about [topic]"
- "Mistake #1 that kills your [metric]"
- "I tested [N] methods. These [N] destroyed the rest"

### Value:
- "Save this for when [situation]"
- "[N] things I wish I knew before [X]"
- "In [time] I [result]. Here's how:"

### Emotion:
- "Honest truth about [topic]"
- "One change flipped everything"
- "Unpopular opinion: [bold claim]"

### TikTok-specific:
- "Stop scrolling if you [situation]"
- "POV: you just discovered [thing]"
- "I spent [money/time] so you don't have to"

---

## ANTI-PATTERNS (NEVER do these)

### Engagement bait (-50-90% reach on ALL platforms):
- "Like if you agree" / "Comment YES" / "Tag 3 friends"
- "Share before they delete this" / "React with [emoji] if..."

### Shadow ban triggers:
- Violence words (even in innocent context)
- Adult content words
- Financial promises: "guaranteed income", "get rich quick"
- Letter substitution does NOT help — algorithms detect it

### Format crimes:
- Same hashtags on every post (spam flag)
- More than 5 hashtags (limit since late 2025)
- Wall of text without line breaks
- #fyp, #foryou, #viral — useless and harmful

---

## POWER WORDS (use 2-3 per caption)

| Category | Words |
|----------|-------|
| Urgency | Now, Today, Limited, Last chance |
| Trust | Proven, Tested, Research-backed, Results |
| Exclusivity | Secret, Hidden, Insider, Behind-the-scenes |
| Emotion | Shocking, Surprising, Honest, Raw, Real |
| Action | Discover, Unlock, Transform, Master, Grab |
| Value | Free, Bonus, Cheat sheet, Blueprint, Toolkit |

---

## SIGNAL HIERARCHY (all platforms, 2025-2026)

1. **Shares/DM sends** — strongest (~10x a like)
2. **Saves** — very strong, especially Instagram
3. **Comments** — strong, especially meaningful ones
4. **Watch time / Completion rate** — dominant for video (70%+ for viral)
5. **Likes** — weakest, "vanity metric"

## QUALITY CHECKLIST (verify before presenting)

- [ ] Hook in first 80-125 characters
- [ ] 1-3 SEO keywords naturally integrated
- [ ] ONE clear CTA per caption
- [ ] 2-3 power words (not more)
- [ ] 3-5 niche hashtags (not generic) where applicable
- [ ] Zero engagement bait
- [ ] Zero shadow ban triggers
- [ ] Zero Facebook trigger words (for FB captions)
- [ ] Short paragraphs with line breaks
- [ ] Different formula for each platform
