---
name: reaLooksmaxxing
description: 'The /rea-looksmaxxing video, beat by beat: the 11-step "moneymaxx like Clavicular" play, what each section shows and says, its music, tempo and sound effects, and the /rea-looksmaxxing page on the site that outlines the same play. Use when the owner asks to recut, remake, extend or post the /rea-looksmaxxing video, write copy for it, or change its page.'
---

# reaLooksmaxxing

A 48 second promo (1080p, 29.97 fps) for log, cut to the slowed "rude" track.
It walks through how Clavicular makes money as an 11-step play, and plays it
for laughs. Each step lands on the beat with a kicker, a headline and a
handwritten sticker line. The joke is that every step is a real log, treg or
SubQ job.

## Where it lives

- Build script: `~/.buzz/REPOS/log-hyperframes/effectcraft/clavJcuts.jsx`
  (EffectCraft). The copy is inlined on its `var SEC = [...]` line, and
  `scene4/sections.json` holds the same copy.
- Type: `scene4/type.html` is rendered by Playwright to one PNG per part
  (`scene4/type/*.png`) plus `scene4/typeParts.json`, and that JSON is pasted
  into the jsx's `TYPE`. After changing the copy, render the type again, or
  the video keeps the old words.
- Project: `effectcraft/reaLooksmaxxingCopyFix.ecproj`. Render it with
  `effectcraft-cli run … renderQueue.render`, started as a detached process,
  never inside a Monitor (a Monitor dies at 30 minutes and takes the render
  with it). A full render takes about an hour and needs disk space for the
  pagefile.
- Output: `~/.buzz/OUTBOX/reaLooksmaxxing.mp4` (92 MB) and
  `reaLooksmaxxingPhone.mp4` (25 MB, for sending).
- Page: `log.listeningkit.com/rea-looksmaxxing`
  (`site/apps/web/src/landing/useCases/ReaLooksmaxxingPage.tsx`, copy in
  `reaLooksmaxxing.ts`). It embeds Clavicular's post
  `x.com/clavicular/status/2118075785613287786` (Claude Code answering his
  Instagram DMs, which is step 9).

## Tempo and sound

- Music: `assets/music/rudeSlowed.mp3` at -6 dB, starting at -0.49 s.
  115.9 BPM, so one beat is 0.518 s (`BEAT = 60 / 115.9`, first beat at
  0.035 s). Every section starts on a beat.
- Sound effects run a further 6 dB under the music (`sfx(name, t, db - 6)`)
  so the mix never clips: whips and whooshes on each cut, a pop as each
  sticker lands, riser, bass drop and boom into the title, shine on each
  platform logo, and a boom on "really".

## The beats

| Section | Beats | Background | Kicker | Headline | Sticker (handwritten) |
|---|---|---|---|---|---|
| s1 | 4 | nightclub clip | step 1. | create "content" | goto nightclubs, bars, the beach. (SubQ cards: treg pulled 40 of his clips, top one 8.44M views) |
| s2 | 4 | TikTok clip | step 2. | be controversial. | the more outlandish the takes the better. (SubQ cards) |
| how | 3 | "moneymaxx" word clip | | now here's how he | moneymaxxs. |
| s3 | 4 | TikTok clip | step 3. | buy your accounts. the aged the better | we're building a bot farm. (sub: tiktok, youtube, instagram) |
| s4 | 4 | TikTok clip | step 4. | download Log by ListeningKit | free, open sourced & goated. (sub: + can automate your entire social media) |
| s5 | 4 | TikTok clip | step 5. | connect up the accounts | let Claude Code warm up the (then: instagram, twitter, reddit, discord, facebook, youtube, tiktok.) |
| platforms | 14 | full screen | | each platform's logo, two beats apiece | |
| really | 4 | full screen | | the "really" hit | |
| s6 | 3 | TikTok clip | step 6. | go | f*cking viral. |
| s7 | 4 | makeup clip | step 7. | create an offer playing on people's insecurities | insecurity sells. (sub: we don't recommend it) |
| s8 | 4 | TikTok clip | step 8. | call to actions everywhere | funnel them to discord, instagram, wherever you want! |
| s9 | 5 | TikTok clip | step 9. | deploy Claude Code to funnel them into your offer | if you're hungry enough you can too! (sub: clav created camp looksmax, he made millions of dollars) |
| s10 | 4 | montage of earlier clips | step 10. | repeat step 1, 2, 3 | plaster yourself on social media. |
| s11 | 3 | limo clip | step 11. | | profit. (big) |
| outro | 5 | blackjack clip | | your brand might be a bit cooked | but atleast you moneymaxxed. |

In steps with SubQ panels, the type moves left (to x 520) at 56% scale so the
panels have room.

## Rules for the copy

- **No line gets cut off.** Headlines, stickers and subs wrap balanced, with a
  1300 px limit on subs and narrow stickers. After changing any copy, render
  the type and check every part's PNG for an EDGE warning before rendering
  the video.
- **The tone is deadpan.** The step says the thing straight, and the sticker
  is the joke. Step 7's "(we don't recommend it)" stays.
- **The numbers are real.** 40 clips, 8.44M views, and "millions of dollars"
  come from treg's TikTok search and the research in
  `~/.buzz/RESEARCH/LOOKSMAXXERS_MANAGERS_2026_11_06.md`. SubQ's scores and
  scripts are illustrative.
- **The page is a summary, never the 11 steps.** It runs like a platform
  page: the hero's use case (how it works, call by call), Clavicular's post
  shown plainly (never boxed in a card), the three-step play and the prompt
  (`reaLooksmaxxing.ts`). The step-by-step lives in the video only.
