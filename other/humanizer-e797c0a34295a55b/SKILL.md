---
name: humanizer
description: Humanizer Skill
---
# Humanizer Skill

Transform AI-generated video scripts, voiceovers, and social media copy into natural, engaging content that sounds human-written — not machine-produced.

## When to Use

- Before rendering any AI-generated video script through Remotion
- When adapting voiceover text for Fish Speech / ElevenLabs TTS output
- Before publishing AI-written social media captions or descriptions
- When tone-shifting content between platforms (YouTube, TikTok, Instagram, etc.)
- After script generation by the Nexus Engine or Agent Zero brainstorming pipeline

## Core Rules

### 1. Kill the AI Voice

AI content has telltale patterns. Strip them out.

| Instead of | Use |
|---|---|
| "In today's video, we'll explore..." | "So here's the thing..." |
| "It's important to note that..." | Cut it — just say the thing |
| "Let's dive in!" | Remove or replace with natural transition |
| "Furthermore, additionally, moreover" | "And", "also", "plus" — or just join the sentences |
| "This is a game-changer" | Be specific: what actually changed? |
| "Without further ado" | Delete entirely |
| "Ladies and gentlemen" | "Hey" or nothing |
| "In conclusion" | Just wrap up — viewers can see it's the end |

### 2. Write for the Ear, Not the Page

Video scripts and voiceovers are spoken content. Read everything aloud before finalizing.

**Short sentences win.** Average 8-12 words per sentence for voiceover. Fragments are fine.

**Contractions always.** "We're" not "we are". "Don't" not "do not". "It's" not "it is".

**Rhythm matters.** Vary sentence length. Short. Then a slightly longer one that carries the viewer forward. Then short again.

**Pause markers.** Use `...` or `[beat]` for natural breathing points in voiceover scripts.

### 3. Match the Platform Tone

| Platform | Tone | Length | Style |
|---|---|---|---|
| YouTube | Conversational, authoritative | 3-10 min scripts | Hook → story → payoff |
| TikTok | Energetic, punchy, fast | 15-60 sec | Pattern interrupt → value → CTA |
| Instagram Reels | Visual-first, minimal VO | 15-30 sec | Let visuals carry, text is support |
| Instagram Caption | Casual, relatable | 1-3 sentences + hashtags | Emoji OK, conversational |
| Twitter/X | Sharp, opinionated | Under 280 chars | Hot take or insight, no fluff |
| LinkedIn | Professional but human | 1-3 short paragraphs | Story-driven, lesson at the end |

### 4. Use Concrete Language

AI defaults to abstract. Push toward specific.

| Instead of | Use |
|---|---|
| "Many people struggle with..." | "Most creators burn out in the first 3 months" |
| "This technique is very effective" | "This cut my editing time from 4 hours to 40 minutes" |
| "There are several ways to..." | "There are three ways. The first one..." |
| "Significant improvement" | "2x faster", "dropped from 60% to 12%" |
| "Various factors" | Name the 2-3 that actually matter |

### 5. Hook in the First 3 Seconds

Every video script needs a pattern interrupt. Options:

- **Contrarian**: "Everything you know about X is wrong."
- **Specific number**: "I made $4,200 in one week with this."
- **Question**: "Why do 90% of creators fail at shorts?"
- **Statement of fact**: "This tool exists and nobody's talking about it."
- **Visual hook**: Describe an unexpected opening shot.

Never start with "Hey guys, welcome back to..." — the scroll-away rate is brutal.

### 6. Write CTAs That Don't Feel Like CTAs

| Instead of | Use |
|---|---|
| "Like and subscribe!" | "If this helped, hit like — algorithm loves it and so do I" |
| "Comment down below" | "Drop your take in the comments — I actually read them" |
| "Follow for more" | "I post stuff like this every Tuesday" |
| "Link in bio" | "Link's in my bio if you want to try it" |

## Prompt Templates

### Video Script Humanization

```
Rewrite this AI-generated video script to sound like a real person talking to camera. Rules:
- Contractions everywhere
- Sentences under 15 words average
- Kill filler phrases (important to note, let's dive in, without further ado)
- Add [beat] markers where natural pauses belong
- Keep the core information intact
- Hook must land in first 5 words

Platform: {platform}
Target length: {duration}
Script: {raw_ai_script}
```

### Voiceover Text Cleanup

```
Clean this voiceover text for TTS synthesis. Rules:
- Remove anything that sounds robotic when spoken
- Replace complex words with simpler alternatives (utilize → use, commence → start)
- Break long sentences into 2-3 shorter ones
- Add natural rhythm: vary sentence length
- Remove parenthetical asides (TTS reads them awkwardly)
- Keep under {word_count} words

Text: {raw_voiceover_text}
```

### Social Media Caption

```
Rewrite this AI caption to sound human. Rules:
- Platform: {platform}
- First line must hook (no "Excited to share...")
- Use contractions and casual tone
- {emoji_policy} (none / sparingly / OK)
- End with a question or soft CTA, not "link in bio"
- Keep hashtags to {hashtag_count} relevant ones, not 30 generic

Caption: {raw_ai_caption}
```

### Multi-Platform Adaptation

```
Adapt this content for {target_platform}. Original was written for {source_platform}.

Adjust:
- Length (shorter for TikTok/Reels, longer for YouTube/LinkedIn)
- Tone (more casual for TikTok, more professional for LinkedIn)
- Structure (visual-first for Reels, narrative for YouTube)
- CTA style (platform-native)

Content: {original_content}
```

## Anti-Patterns Checklist

Before finalizing any content, verify none of these slipped through:

- [ ] No "In today's video/article/post..."
- [ ] No "Let's dive in / jump in / get started"
- [ ] No "It's important to note that..."
- [ ] No "Without further ado"
- [ ] No "Game-changer / game-changing" without specifics
- [ ] No "Various / numerous / several" — name the count
- [ ] No "As we all know..." — if we all know, don't say it
- [ ] No "At the end of the day..."
- [ ] No "It goes without saying..." (then why are you saying it)
- [ ] No passive voice where active works ("The video was created by..." → "I made...")
- [ ] No hedging ("You might want to consider perhaps..." → "Do this")
- [ ] No listicles that promise "7 ways" but pad with filler

## TTS-Specific Guidelines

When humanizing for Fish Speech or ElevenLabs synthesis:

- **Avoid tongue-twisters**: "She sells seashells" patterns trip up TTS
- **Spell out numbers under 10**: "three" not "3" (TTS reads "three" more naturally)
- **Use phonetic spelling for unusual words**: "synonym" → "SIN-uh-nim" if pronunciation matters
- **Break on punctuation**: Periods and commas create natural pauses. Don't put 3 sentences without any punctuation.
- **Avoid slash-separated words**: "and/or" sounds robotic. Pick one.
- **No URLs in voiceover**: TTS reads URLs character by character. Say "link in description" instead.

## Style-Specific Notes

For the 25 Nexus Engine video styles, adjust tone accordingly:

| Style Category | Tone Adjustment |
|---|---|
| Educational (explainer, tutorial) | Clear, patient, "here's how" energy |
| Entertainment (meme, reaction, compilation) | Fast, punchy, humor-forward |
| Motivational (quote, success story) | Measured, powerful pauses, emotional beats |
| News/Commentary | Journalistic but opinionated, "here's what happened" |
| List/Compilation | Energetic transitions, keep momentum between items |
| Storytelling | Conversational, suspenseful pacing, natural reveals |
