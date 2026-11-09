---
name: yt-viral
description: >-
  Find what is actually working in the user's niche on YouTube and rank it
  by how far each video beat its own channel, then name the formula. Use for
  "what's working right now", "find viral videos in my niche", "why did this
  blow up", competitor research, or a swipe file.
---

# yt-viral

Use `rank.py` for profile comparisons across YouTube, TikTok and Instagram. It compares
views within each platform/profile by format, similar length and actual observation age,
then progressively falls back to looser cohorts and finally the same profile, any format.
Sparse data produces a clearly labelled provisional result, not silence. A single-video
profile has no meaningful multiple. See [input schema](references/input-schema.md). Supporting shares
and watch fractions are shown separately; do not treat missing data as zero.

The older `swipe.py` remains available for legacy competitor JSON without age/format data;
label its result as a crude channel-relative comparison, not the fairer ranking.

```bash
python3 swipe.py collected.json --min 2.0
```

## Collecting the input

The legacy swipe helper skips channels below four videos. The new rank helper instead
falls back and labels uncertainty. Collect inputs however the user prefers - `yt-dlp --flat-playlist -J`
against a channel URL is the fastest, the public page works, a manual list works.

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Read, do not scrape.** Public listings only, never a logged-in session, never the user's own
account credentials.

## Reading the output

The multiple is the signal. The formula line is a judgement about the TITLE, matched against
[the 21 formulas](../yt-script/hooks.json) - it is not a claim about why the video worked, and you
should say so when you present it.

What to hand back: the top five with their multiples, the formula each used, and the ONE structural
thing they share. Then the harder line - which of those the user could actually make this week, in
their voice, with what they have.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
