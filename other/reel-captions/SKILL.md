---
name: reel-captions
description: "Write CAPTIONS-PLATFORMS.md for one finished short video: a per-platform post caption for Instagram, TikTok, YouTube Shorts (title + description), Facebook, Threads, Bluesky and X, each within that platform's limits, with your comment-keyword CTA on the platforms where it belongs and never on X. Keyword, CTA, platforms, hashtags and limits come from a config file; a checker script fails the file on any miss. Use after an edit is finished, when asked to 'write the captions', 'caption this reel for every platform', or before scheduling."
author: Johann (@johannships)
version: 2.1.0
---

# Reel captions

One finished reel in, one `CAPTIONS-PLATFORMS.md` out, validated by
`scripts/check_captions.py`. This skill writes text only: it never posts or
schedules. Pipeline position: after `edit-style` (or `longform-edit` for
long-form), before your scheduler.

## Setup (once)

```bash
cp config.example.json config.json
```

Edit `config.json`:

| key | meaning | example |
|---|---|---|
| `keyword` | default comment keyword your DM automation answers | `GUIDE` |
| `cta` | the EXACT CTA line, used verbatim | `comment "GUIDE" & i'll send you the link` |
| `cta_platforms` | where the CTA line must appear | instagram, tiktok, facebook, threads, bluesky, youtube_description |
| `no_cta_platforms` | where the CTA, the keyword and the word "comment" are banned | twitter |
| `skip_platforms` | never write these | linkedin |
| `limits` | max characters per platform | bluesky 300, threads 500, X 280 |
| `hashtags` | `[min, max]` per platform, `default` for the rest | instagram `[4, 7]` |
| `core_hashtags` | your always-on tags | `#yourniche` |
| `ban` | characters or phrases never allowed | em dash, en dash |

Only promise a keyword your DM automation actually answers. If unsure, ask
the user before writing it into the captions.

## Inputs

- The reel folder: `final.mp4`, `captions.srt` (transcript of the FINAL render),
  and optionally the editor's `CAPTION.md` (draft caption and title). Never edit `CAPTION.md`.
- A per-reel keyword if the video says a different one out loud. The keyword
  in the caption must be the one SPOKEN in the video.

## Steps

1. Read `captions.srt`. The hook = the first spoken line, nearly verbatim.
2. Read `CAPTION.md` if present; reuse its title and phrasing.
3. Fill the format below. Write the CTA line first, then fit the body around
   it. When over a limit, shorten the body, never the CTA.
4. Check every number against the video or the editor's QA claims list. If
   they differ, keep the measured number and add a `# OPEN:` comment line.
5. Run `python3 scripts/check_captions.py <reel>/CAPTIONS-PLATFORMS.md`. Fix every FAIL and re-run until PASS.

## Format

```
# <reel> per-platform captions. Source: CAPTION.md + captions.srt
keyword: <KEYWORD or none>
cta: <exact CTA line or none>
## instagram
<CTA line>

<hook>

<2 to 5 short paragraphs>

<CTA line again>

<core + 1 to 2 topic hashtags, one line>
## short
<CTA line>

<hook>

<1 to 2 sentences that carry the point>
## twitter
<hook + one line, one paragraph, no CTA, no hashtags, aim for 130 to 200 chars>
## bluesky
<CTA line>

<hook + one line; whole text within the limit INCLUDING the CTA>
## youtube_title
<one line, 40 to 60 chars ideal, max 100, no emoji>
```

`short` feeds TikTok, Facebook, Threads and the YouTube description. Add
`## tiktok`, `## facebook`, `## threads` or `## youtube_description` only to override it.

## Dual endings (recommended for keyword reels)

Comment-keyword DM tools usually only work on Instagram. If your edit exports two endings (`final.mp4` with
"comment KEYWORD" for Instagram, `final-bio.mp4` with "link in my bio" for the rest, see `edit-style`), start from
`config.dual.example.json`: `cta_platforms` is Instagram only, `bio_cta` is the exact bio line, and
`bio_platforms` must carry it and must never say "comment" or the keyword. A `bio:` header line overrides it per
reel. Worked example: `examples/CAPTIONS-PLATFORMS.dual.md` (passes the checker with the dual config).

## Rules

- **CTA everywhere except X** (single-ending reels; with dual endings the non-Instagram platforms get the bio line instead). X is a short description, not a funnel: a
  comment-gate line there reads as spam. The checker refuses an X text with
  the CTA, the keyword, or the word "comment".
- **No keyword on this reel?** Write `keyword: none` and either an engagement
  question as `cta:` ("which one would you use?") or `cta: none`.
- **Instagram:** CTA, hook, short paragraphs, CTA again, one line of
  lowercase hashtags. No @mentions, no links (they do not click on IG).
  Turn emoji bullets into plain "- " lines.
- **Short platforms:** CTA, hook, 1 to 2 sentences, no hashtags.
- **YouTube title:** a claim or an outcome ("This free tool replaces a $50/month app"), not a label ("Tool review").
- **Voice:** contractions, plain declaratives, "&" is fine. No em or en dashes,
  no "Not X. Y." lines, no "game-changer", no rhetorical-question openers.
- **Never:** first comments, collaborator tags, LinkedIn text, music notes,
  private data (revenue, client names, account ids).

## Worked example

Config keyword `GUIDE`, video says "comment GUIDE". Full passing file:
`examples/CAPTIONS-PLATFORMS.md`. Its X section:

```
## twitter
this free tool replaces a $50/month app. it runs on your own laptop, no account, no upload & the code is public.
```

Checker output:

```
  bluesky                126 chars
  instagram              333 chars
  twitter                112 chars
  youtube_title           39 chars
PASS
```

## Failure handling

| problem | do |
|---|---|
| no `captions.srt` | transcribe `final.mp4` with the `use-local-whisper` skill first |
| no `config.json` | the checker exits and says so: copy the example and fill it |
| the spoken keyword differs from the config | use the spoken one in the header (`keyword:` / `cta:` lines override the config) and flag it with `# OPEN:` |
| a platform limit cannot fit the CTA plus a hook | cut the body to the hook alone; if still over, report it, do not drop the CTA |
| Claude.ai without a shell | write the file, then check limits by hand with the table above and say the checker was not run |

## Hand-off

Report: the file path, the keyword and CTA used, the checker result, and every `# OPEN:` line.
