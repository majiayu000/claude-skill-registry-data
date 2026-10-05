---
name: shorts-script-adapter
description: "Adapts a section of a long-form YouTube script into a self-contained Shorts script (up to 3 minutes, default under 60 seconds) — optimized for vertical format and the Shorts feed."
status: stable
category: youtube
subcategory: scripting
version: 1.1
eval_score: 4.5
tags: [youtube, scripting, shorts, vertical-video, short-form, adaptation]
---
# Shorts Script Adapter

## What This Skill Does
Adapts a section of a long-form YouTube script into a self-contained Shorts script — optimized for vertical format and the Shorts feed. YouTube Shorts supports videos up to 3 minutes; this skill defaults to under 60 seconds (where engagement peaks) but handles any target length within the limit.

## When To Use This Skill
- You've published a long-form video and want to drive discovery by clipping one strong moment as a Short
- You want to batch-produce Shorts from an existing video library without filming separate content
- You have a concept that doesn't warrant a full video but has strong standalone value as a Short (45 seconds to 3 minutes)
- You're testing a new topic on Shorts before committing to a full video
- You want a 1–3 minute Short that develops a single idea with more depth than a sub-60-second clip allows

## What You Need To Provide
**Required:** The source script section or the specific moment from a long-form video you want to adapt (paste the exact text — 200–600 words works best); the core point or insight you want the Short to land.
**Optional:** The long-form video title (for cross-promotion framing); whether this Short should drive viewers to the full video; channel tone; maximum target length in seconds (default 55 seconds — Shorts supports up to 3 minutes, but sub-60-second clips consistently outperform longer ones in the feed).

## How the Assistant Approaches This
1. Identifies the single sharpest, most self-contained argument or insight in the source material — Shorts work when they make one clear point with no loose threads. If the source section makes multiple points, selects the one with the strongest standalone hook.
2. Restructures the content for the Shorts format: front-loads the hook in the first 3 seconds (the "don't scroll" moment), delivers the core point efficiently, and ends with a pattern-interrupt or question rather than a traditional outro (Shorts viewers don't watch CTAs).
3. Strips all transitional language designed for long-form ("as I mentioned earlier," "in the next section") and rewrites for immediacy. Calibrates word count to the target length at approximately 2.3 words per second (a 55-second Short runs ~115–130 words; a 2-minute Short runs ~260–280 words). For Shorts over 60 seconds, adds a mid-point re-hook to retain viewers past the scroll threshold.

## Output Format
Script in two parts:
1. **Shorts Script** — complete word-for-word script with on-camera cues in [brackets], labeled with approximate runtime
2. **On-Screen Text Suggestions** — 3–5 text overlays timed to specific moments (Shorts rely heavily on on-screen text to retain viewers on mute)

Total written length: 150–200 words. No preamble — delivers the script immediately.

## Quality Criteria
- [ ] Hook is complete and compelling within the first 3 seconds of spoken content
- [ ] Script is genuinely self-contained — a viewer who hasn't seen the full video understands it completely
- [ ] All transitional long-form language has been removed or rewritten
- [ ] Word count fits comfortably within the specified time limit at normal pace
- [ ] On-screen text suggestions are specific (exact words, not "add text here")
- [ ] The Short makes one clear point — not a summary of multiple points

## Example

### Input
**Source material (from a full video on sleep and productivity):**
"Here's something that most productivity content completely ignores: the quality of your first hour after waking up has a disproportionate effect on your cognitive performance for the rest of the day. There's a concept called sleep inertia — the groggy, low-functioning state your brain is in for 15 to 60 minutes after you wake up. During sleep inertia your prefrontal cortex, the part of your brain responsible for decision-making and focus, is running at significantly reduced capacity. The mistake most people make is trying to do their most important work during this window, or worse, flooding themselves with information — email, news, social media — while their brain is least equipped to process it. A much better approach: do nothing cognitively demanding in the first 30 minutes. Physical movement, a hot drink, light conversation, or even just sitting quietly all allow sleep inertia to clear before you ask your brain to do anything hard."

**Core point to land:** Don't do cognitively demanding work in the first 30 minutes after waking — your brain physically isn't ready.
**Target length:** 55 seconds
**Drive to full video:** Yes

### Output

**Shorts Script**
*Estimated runtime: 52 seconds*

---

[DIRECT TO CAMERA — confident, slightly urgent]

Stop trying to do deep work in the first 30 minutes of your day.

Your brain has something called sleep inertia. For the first 15 to 60 minutes after you wake up, your prefrontal cortex — the part that handles focus and decision-making — is running at reduced capacity.

[beat]

It's not motivation. It's not discipline. It's literally biology.

Most people make it worse by immediately checking email or scrolling. You're flooding a system that isn't ready.

The fix is simple: keep the first 30 minutes light. Movement, coffee, something physical. Save the hard thinking for when your brain has actually woken up.

[look directly at camera]

The full video on morning routines is linked. I cover three more of these — every one of them is backed by research.

---

**On-Screen Text Suggestions**

- **0:00–0:03:** "Stop doing this in the first 30 minutes" [bold, white on dark background]
- **0:07–0:10:** "SLEEP INERTIA" [caps, emphasized — appears as word is spoken]
- **0:14–0:16:** "15–60 MINUTES after waking" [stat callout]
- **0:27–0:30:** "Movement / Coffee / Conversation" [list appears as alternatives are named]
- **0:42–0:45:** "Full video linked ↑" [subtle, bottom of frame]

---

## Known Limitations
- This skill adapts existing material — it cannot manufacture a compelling Short from a source section that doesn't contain a self-contained insight. If the source material is context-dependent (e.g., "as we saw in the previous section"), the adaptation will be limited until that context is rewritten into the Short.
- On-screen text suggestions are starting points. Timing adjustments are needed based on your actual speaking pace and editing rhythm — treat them as placement guidance, not final copy.
- Shorts that are fundamentally promotional ("watch my full video on X") perform significantly worse than Shorts that deliver standalone value. This skill prioritizes standalone value and treats the full-video CTA as secondary — if you want a primarily promotional Short, specify that explicitly.
- YouTube supports Shorts up to 3 minutes (since October 2024), but the algorithm still favors shorter content in the Shorts feed. Shorts over 90 seconds need a stronger hook strategy and mid-point re-engagement to compete with sub-60-second clips.

## Related Skills
- [full-script-writer](../full-script-writer/SKILL.md)
- [hook-generator](../../pre-production/hook-generator/SKILL.md)
- [chapter-timestamps](../../post-production/chapter-timestamps/SKILL.md)
