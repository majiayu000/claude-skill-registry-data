---
name: yt-viral
description: >-
  Find what is working in a niche on YouTube by ranking each video against its
  own channel's normal views, then name the formula behind the title. Use for
  "what's working right now", "find outliers in my niche", "why did this blow
  up", competitor research, or building a swipe file.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/swipe.py *)
---

# yt-viral

Raw view counts measure channel size, not ideas. A video worth studying is one that beat **its own
channel's median** by a wide margin. That is what this ranks.

```bash
python3 ${CLAUDE_SKILL_DIR}/swipe.py collected.json --min 2.0
yt-dlp --flat-playlist -J "https://www.youtube.com/@channel/videos" > a.json
python3 ${CLAUDE_SKILL_DIR}/swipe.py a.json b.json c.json        # yt-dlp output works as is
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.
It reads the formulas from `../yt-script/`, so install the two together.

## Collecting

At least **four videos per channel**, or a median means nothing; the tool skips thinner channels and
says so. Ten to thirty per channel is better. `yt-dlp --flat-playlist -J` on a channel's `/videos`
page is quickest and its output goes straight in; a hand-made list works too:

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

Shorts and long videos are compared separately when durations are known, and a video with no view
count is left out rather than counted as zero. If the tool left some out, mention it.

**Public listings only.** Never a logged-in session, never anyone's credentials.

## Reading the result

The multiple is the signal. The formula label is a judgement about the title's words, matched
against [the 21 formulas](../yt-script/hooks.json) - not a claim about why it worked. Say so.

What to hand back: the top five with their multiples and formulas, and the one thing they share.
Then the harder part: which of them the creator could make this week, in their voice, with what
they have.

A swipe file is for the shape, never the video. Remaking someone's outlier with the names swapped
is the "mass-produced, repetitive" content YouTube's inauthentic-content policy demonetises. If
asked for that, say so and offer the structure to fill with the creator's own material.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
