---
name: nicheCreativeResearch
description: Take a new niche, industry or offer from nothing to tested listing creatives - find what operators say gets messages, collect real winning listings, turn every winner image into JSONL, have SubQ define what a winner is in that niche, build the scene/action/before/after rubric from it, spin the owner's concept out against it, generate, show, and score. Use when the owner says to explore a new niche, industry or offer, or "do what we did for junk removal" for something else.
---

# nicheCreativeResearch

The routine behind the junk removal creatives, written so it runs the same way
for any niche, industry or offer. Junk removal (2026-10-23) is the worked
example all the way through. The picture side of each step is `listingCreative`;
the words are `listingCopy`.

## Hard boundaries

- **Only what the owner said.** The niche, the offer, the platforms and the options
  are the owner's words (rules 39-41). Nothing the owner didn't name goes into a search, a
  matrix, a rubric or a write-up.
- **Every lookup is TinyFish through treg, every claim from a page fetched**
  (rule 53). Give the owner links straight away when they ask for something to open.
- **Never judge the owner's creatives.** What winners show is data. The owner's concept is
  what gets spun out, never replaced.
- **Money only as asked** (rule 41): generation and SubQ calls are named with
  their cost before they run, each frame is generated once.
- **No text or logos inside generated images, no phone words in prompts.**

## The pipeline

```
1 sources ──► 2 winner listings ──► 3 creatives.jsonl ──► 4 SubQ: what wins here
                                                               │
8 measure ◄── 7 phone media ◄── 6 generate once ◄── 5 rubric + spin-outs
```

Everything for a niche lives in one workspace folder,
`RESEARCH/<NICHE>_CREATIVES/`, and its finished media in this repo,
`media/listings/<creative>/`.

### 1. Sources: what operators say gets messages

Search where the people who sell that service talk (for junk removal:
r/sweatystartup, r/smallbusiness, r/sidehustle, the Junk Removal Winners and
Junk Removal Networking Facebook groups, YouTube, TikTok). For each source write
down the URL, who is speaking (operator, or marketer/course seller), short exact
quotes, any numbers (messages, jobs, $), and the evidence grade: **A** first-hand
with numbers, **B** first-hand anecdote, **C** vendor claim.

- Reddit loads through `www.reddit.com/...` (not `.json`, not old.reddit).
- Facebook group posts load with the post and the top 3 comments.
- Marketplace listings open only through `m.facebook.com/marketplace/item/<id>/`.
- YouTube gives descriptions and chapters, no transcript.

Junk removal: 39 searches, about 75 pages, 19 sources, in
`RESEARCH/JUNK_REMOVAL_MARKETPLACE_SOURCES.md`. Best numbers: Craigslist every
morning to "$1,000 per week" (A), a note in two local groups to "2 jobs in as
many days" (A), "30% of my business" from free-item messages (A).

### 2. Winner listings: the real ones, with any sign they get answers

Collect live listings in the niche and fetch their images (`image_links` on the
fetch). Signs a listing works: the poster keeps paying to repost it (the same
title many times on a Craigslist hub), "Highly rated on Marketplace", seller
reviews, an operator saying so. Never competitors from the owner's own cities.

Junk removal: 8 Craigslist posts (Akron, Greenville, Irvine, 5 in the Bay Area)
and 4 Marketplace listings, 63 images.

### 3. creatives.jsonl: every winner image as one line

One line per image: `listing`, `platform`, `city`, `signal`, `order`, `role`
(cover, before, after, beforeAfterStack, action, trust, serviceArea...),
`scene`, `shows`, `action`, `people`, `overlay`, `pairWith`, `camera`, and the
`file`. Written from looking at each image, nothing guessed.

Junk removal: 58 lines, `RESEARCH/JUNK_REMOVAL_CREATIVES/creatives.jsonl`.

### 4. SubQ: what a winner is in this niche

SubQ's Decisions API (`src/subq/decisions`) gets the whole `creatives.jsonl` as
state and the images, **at most 4 per call**, so pack them into labelled contact
sheets. Ask what the winners are, not what to do: `choice` for the main scene,
the before/after layout and the cover; `noul` for each element (same angle,
crew working, phone snapshot, overlays, people in frame);
`score` for how much mess, what the after looks like, how authentic. The
answers are the niche's definition of a winner (`subqReading.json`).

Junk removal: a flyer cover (89%), then real phone photos of a room- or
yard-sized pile, the crew working (99%), an after from the exact same spot
(99%), bare (88%), Before/After or the number on top (99%), almost never a
homeowner in frame. The owner's own rules sit above what the winners show: no
vehicles in any frame, whatever the winners do (`listingCreative`).

### 5. Rubric and spin-outs

The rubric is the winner definition laid out as slots. For a service that
clears something it is **scene, action, before, after**; another niche keeps
the same idea (where it happens, the work being done, the problem, the result)
with its own words. Then the owner's concept is spun out into new creatives in that
composition (`spinOuts.jsonl`, the shape of the owner's `images.jsonl`: prompt, avoid,
aspect, keepSameAs), and SubQ scores each plan against the winners: in the
winners' composition, raw phone snapshot, shows the job happening, what it is
most missing.

Junk removal: garage 94%, side yard 95%, basement 82%, the owner's Bethlehem set 42%
(missing crew at work).

### 6. Generate once

`reapi.image-gen.gemini-3-pro-image` through treg, 2K, 9:16, about $0.03 a
frame. The before first, then the action and after as edits of the before (its
output URL is the reference), so the place and people match. Each frame once,
then show the owner every one.

Junk removal: 9 frames for $0.20 on the second run. The first run's prompt said
"iPhone" and the model drew a Photos app screen into the pictures, and every
shot with a car, truck or trailer in it came out wrong. Both are now prompt
rules: no phone words, no vehicles.

### 7. Phone media

Render each frame into the iPhone Photos viewer with the town in the title and
faces scribbled out in red (`listingCreative`, `python/creative`), into
`media/listings/<creative>/raw|ios|iosScribbled/`.

### 8. Measure

Run SubQ over the made frames the same way as step 4, publish (rule 8, `--live`
only when the owner says), and count messages per listing. What gets messages goes
back into the niche's winner definition. Junk removal: not done yet.

## Starting a new niche

1. The owner names the niche, the offer and the cities.
2. `RESEARCH/<NICHE>_CREATIVES/` and `RESEARCH/<NICHE>_MARKETPLACE_SOURCES.md`.
3. Steps 1-8 in order, each step's file before the next starts, each paid step
   named with its cost first.
