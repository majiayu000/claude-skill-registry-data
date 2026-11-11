---
name: linkedin-writer
description: "Writes LinkedIn posts in the user's own voice, learned from 5 to 10 of their best posts, using formats ranked by measured reach and engagement (milestone, short prediction, origin story, lesson-learned, comparison hook, comment-keyword lead magnet) and a hard anti-slop test. Also researches what is winning in a niche from public posts, and returns ranked idea banks. Use when someone asks for a LinkedIn post, LinkedIn ideas, to turn a story or result into a post, or to make a LinkedIn draft sound less like AI. Drafts only; never posts."
---

# LinkedIn Writer

Posts that sound like you, built on formats that measurably travel, and filtered so nothing reads like interchangeable AI thought leadership.

By Johann (@johannships). The format ranking comes from scoring my own posts by impressions, likes, comments and reposts; the anti-slop test came from drafts I rejected.

## Step 0: learn the voice (first run, then reuse)

Ask the user to paste **5 to 10 of their own best LinkedIn posts** with impressions if they have them (each post's analytics shows it). Write `voice.md` next to this file:
- capitalisation and punctuation habits
- line pattern (one sentence per line? short paragraphs?)
- typical hook types they use
- words they use and words they never use
- emoji, hashtag and tagging habits (count, do not guess)
- CTA style
- which of their posts did best and which format it was (map to the table below)

Show it once, apply corrections, reuse it after. No samples: use the defaults below and label the draft "default voice".

## Inputs

- Topic, story or result (required), with any real numbers.
- Mode: **draft** (default), **ideas**, **niche research**, or **edit** (their text).
- Audience: who should read it (e.g. COOs at mid-size companies). Ask if unclear; it changes everything.
- Anything the user supplies (hook, bullets, CTA, a "use this" line) is **locked**. Improve around it. Never swap their hook for one that is merely similar.

## Formats ranked by measured performance

| Format | What it does best | Shape |
|---|---|---|
| Milestone | Highest reach (about 2.5x the next format) | State the win in one line. One proof line. Thank people. Short. A graphic helps. |
| Short prediction | High reach, low engagement | 3 to 5 lines. One bold, specific claim. No hedging. |
| Origin story | Strong reach | Surprising fact, specific context, credibility moment, what went wrong, one lesson. |
| Lesson-learned story | Best engagement rate | Credibility hook, story, a lesson that challenges the usual advice. |
| Comparison hook | Good engagement | "X costs $Y. it took me Z." Then what it actually was. |
| Comment-keyword lead magnet | Most comments | Useful asset, 3 to 5 bullets of what is inside, one proof line, "comment WORD and i'll send it". Link goes in a DM or comment, never in the body. |
| Product announcement | Weakest | Only problem, what you built, what it does. Keep it short. |

Notes from the data:
- Photos of the author or a branded graphic lifted reach on every format.
- Keyword CTAs inflate comments; they do not prove buyer quality.
- One acquisition or funding post can out-travel everything. Do not imitate that structure without an equal event.

## Voice defaults (overridden by voice.md)

- One thought per line, lots of whitespace. Most lines under 12 words. Fragments are fine.
- No setup ("I want to share..."). Start inside the story.
- Real numbers, only ones the user gave you.
- Let the lesson come through the story; do not announce "here's what i learned".
- Soft CTAs only ("feel free to reach out"). Never "LIKE and SHARE".
- Never: em dashes, "I'm thrilled to announce", "delve", "leverage", "utilize", headers or bold in the body, more than 2 hashtags.

Example (milestone, default voice):
```
just sold my second company

idea to exit in 10 months. fully bootstrapped.

big thanks to everyone who helped make this happen
```

## Anti-slop test (run on every draft)

Reject and rewrite if any is true:
- It still works for another industry after swapping three nouns.
- The hook is a broad claim ("AI is changing everything") with no proof or tension in line 2.
- It lists verbs (pull, flag, draft, route, approve) with no recognisable scene.
- It claims "fewer delays" or "more capacity" with no mechanism.
- It invents a client, quote, outcome or permission.
- Every line is a staged one-line reveal or a "not X, but Y" contrast.

Fix pattern: one recognisable problem in the reader's world, the evidence they would want, the human decision that stays, a specific consequence.

## Mode: niche research ("what's winning in my niche")

Needs web access (WebSearch/WebFetch in Claude Code, or web search in Claude.ai). If none, ask the user to paste 5 to 10 posts with their visible reactions and comments.
1. Find 7 to 10 recent public posts from credible operators in the niche. Record author, hook, full text, visible reactions and comments, date, URL.
2. Split one-off events (acquisitions, funding, celebrity reach) from repeatable editorial wins.
3. Name the repeatable openings: an operating scene, a surprising verified number, a defensible contrarian belief, or live product proof.
4. Output a table (author, hook, engagement, repeatable lesson), then 3 hooks built from those patterns using the user's real context. Label counts with the date seen.

## Mode: ideas

Return a ranked bank of 3 to 5 distinct concepts (not paraphrases of one thesis). For each: provisional hook, the real scene, the tension, what the reader gets, a proof visual, CTA or none, and a claim-status note (verified / user-said / needs checking). Before reusing a story, ask whether they already posted it; a new photo or hook does not make an old story new.

## Mode: edit

- "Improve this" or "in my voice": smooth their wording, cut repetition. Do not add a second thesis, a safety lecture or a new CTA.
- "More concise": cut 40 to 60 percent at once. Keep the proof hook, one concrete example, the lesson, optional CTA.
- "Sounds like AI": simplify. Ordinary words, fewer contrasts, less symmetry. Keep the concrete mechanism.

## Output

Draft mode: only the post text, ready to paste. If asked for options, 2 to 3 with different hooks. Never name a client, employer or partner unless the user confirms it is approved for public use; default to category language ("two enterprise teams").

## When something is missing

- No numbers: write without them.
- No web access in research mode: ask for pasted posts, say research ran on pasted data only.
- Third-party article as the source: check the original and its date first. Never say "just published" about something old. Build an original take for the user's audience instead of paraphrasing.

## Feedback log

Append rejections, edits and post results to `feedback.md` (date, format, result or correction, rule going forward). Read it first next time.
