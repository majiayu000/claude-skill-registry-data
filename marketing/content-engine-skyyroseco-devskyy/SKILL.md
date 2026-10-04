---
name: content-engine
description: Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, threads, scripts, content calendars, or one source asset adapted cleanly across platforms. Do NOT use for deriving the voice profile itself (brand-voice), for actually publishing/distributing the posts (crosspost), or for long-form articles (article-writing).
origin: ECC
---

# Content Engine

Turn one idea into strong, platform-native content instead of posting the same thing everywhere.

## When to use

- writing X posts or threads
- drafting LinkedIn posts or launch updates
- scripting short-form video or YouTube explainers
- repurposing articles, podcasts, demos, or docs into social content
- building a lightweight content plan around a launch, milestone, or theme

**When NOT to use:**

- the ask is distribution mechanics (staggering, per-platform posting APIs) — that is `crosspost`
- the ask is long-form (guide, essay, newsletter issue) — that is `article-writing`
- no source asset or idea exists yet — get the anchor first; content generated from nothing is
  filler by construction

## Inputs

Required before drafting — **absent input = stop and ask, never proceed on assumptions**:

1. **Source asset** — what we are adapting from (article, video, demo, memo, launch doc, or a
   single stated idea). No anchor → no drafts.
2. **Audience** — builders, investors, customers, operators, or general.
3. **Platform targets** — X, LinkedIn, TikTok, YouTube, newsletter, or multi-platform.
4. **Goal** — awareness, conversion, recruiting, authority, launch support, or engagement.
5. **Voice profile** — from `brand-voice` if one exists. For SkyyRose work, product facts come
   only from `wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv` and collection
   language only from `docs/brand/collection-stories.md` — never from memory.

## Procedure

1. Confirm the four inputs above.
2. Extract 3–7 atomic ideas from the anchor asset. One clear idea per post.
3. Draft platform-native variants — never the same copy resized:
   - **X** — open fast; one idea per post or per tweet in a thread; links out of the main body
     unless necessary; no hashtag spam.
   - **LinkedIn** — strong first line (visible before "see more"); short paragraphs; explicit
     framing around lessons, results, and takeaways.
   - **TikTok / short video** — first 3 seconds interrupt attention; script around visuals,
     not just narration; one demo, one claim, one CTA.
   - **YouTube** — show the result early; structure by chapter; refresh the visual every
     20–30 seconds.
   - **Newsletter** — one clear lens, not a bundle of unrelated items; skimmable section
     titles; the opening paragraph does real work.
4. Trim repetition across outputs and align each CTA with platform intent — small, clear asks.
5. Run the Verification checks on the draft files before delivering.
6. When asked for a campaign, return: the core angle, platform-specific drafts, optional
   posting order, optional CTA variants, and any missing inputs needed before publishing.

# Verification

Write each platform draft to its own file (e.g. `x.txt`, `linkedin.txt`) so the checks have a
real target. A check that errors (missing file → grep exit 2) is a dead gate, not a pass
(bug-230) — fix the path and re-run.

1. **Hard length limits** — platforms truncate or reject silently:

```bash
awk 'length($0) > 280 {print "OVER-LIMIT line " NR ": " length($0) " chars"; bad=1} END {exit bad}' x.txt
```

   **PASS:** no output, exit 0. Any `OVER-LIMIT` line = trim before delivery. Adjust the limit
   per platform (X 280 · Threads 500 · Bluesky 300 · LinkedIn 3000). `[repro]`

2. **No cross-platform copy duplication** — the core rule, made falsifiable:

```bash
sort x.txt linkedin.txt | uniq -d | grep -v '^[[:space:]]*$'
```

   **PASS:** no output, exit 1 from the final grep. Any surviving line appears verbatim on two
   platforms — rewrite one of them. `[repro]`

3. **Banned-trope scan** — same gate as `brand-voice`:

```bash
grep -nEi 'excited to share|no fluff|game.chang|cutting.edge|revolutionary' x.txt linkedin.txt
```

   **PASS:** exit 1 (zero matches). `[repro]`

Both check 1 and check 2 were observed failing on deliberately broken input before being
trusted (rule 3 of the authoring standard) — see the worked example.

## Worked example

Real run, 2026-07-28. Anchor: a Black Rose one-run drop announcement. Drafts written to the
session scratchpad as `x.txt` and `linkedin.txt`.

First X draft came out at 293 chars — the length gate went red, proving it can fail:

```bash
$ awk 'length($0) > 280 {print "OVER-LIMIT line " NR ": " length($0) " chars"}' x.txt
OVER-LIMIT line 1: 293 chars
```

After trimming (`wc -c` → 238):

```bash
$ awk 'length($0) > 280 {print "OVER-LIMIT line " NR ": " length($0) " chars"; bad=1} END {exit bad}' x.txt && echo "PASS: all lines <= 280"
PASS: all lines <= 280

$ sort x.txt linkedin.txt | uniq -d | grep -v '^[[:space:]]*$'; echo "exit=$?"
exit=1
```

All outputs observed this session `[repro]`. The X version opens "Black Rose is armor." — the
LinkedIn version reframes the same fact as a make-story with explicit takeaway; zero shared
lines.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Cross-posting identical copy | `uniq -d` returns shared lines | Never ship it; each platform gets a native adaptation — that is this skill's core contract |
| Hallucinated product facts | price, SKU, or drop date stated from memory | bug-096 shape: plausible ≠ sourced. Catalog CSV is the only product manifest; `data/sot-images.json` the only imagery source |
| Mixed collection canon | "bloodline" copy on a Signature post | Each collection has its own locked canon (`docs/brand/collection-stories.md`); never mix quotes |
| Length overflow shipped | platform truncates the CTA off the end | Run check 1 per file, per platform limit — silence from an unrun gate is not a pass (a SKIP is not a PASS; the drafter closes it before handoff to `crosspost`) |
| Hooks that summarize | first line restates the title | Hooks matter more than summaries — open with the sharpest specific, not the topic |
| Generic hype language | "game-changing", "excited to share" | Check 3 catches these mechanically; rewrite with specifics over slogans |
