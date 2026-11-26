---
name: listingCopy
description: Write a Marketplace listing's title, description and photos by the copy rules, each with a good and a bad version, from research on high-response classified and service ads. Use when the owner asks for listing copy, a new listing, a rewrite, "the copy sucks", or before `log facebook listing create`.
---

# listingCopy

The rules for a listing's words and photos. They come from what high-response
classified and service ads do, found through TinyFish (rule 53) on 2026-10-23;
the sources and findings are in the workspace's
`RESEARCH/LISTING_COPY_RESEARCH.md` (letters A-F below). The listing's fields
and how its photos reach Facebook are in `docs/listingMedia.md`.

The test under every rule (D): **bad copy describes the seller, good copy
describes the reader's situation.**

## Before writing

Write these down first (D's method):

1. What the reader believes right now, in their words: "My garage is full and I
   don't know who'll take it all."
2. The one thing they should believe after reading: "I send a photo and get a
   price, and they take everything."
3. The objection in the way: price, hassle, trust, time. The copy answers it.

Facts the copy may claim only when the owner has said they are true: same-day
pickup, licensed, insured, the towns served, each price. If one isn't known,
leave it out; never guess it (E: be honest).

## Title

| Rule | ✅ Good | ❌ Bad |
| --- | --- | --- |
| The exact service, the city, one real benefit (A, B, C) | `Junk Removal Bethlehem PA – Free Quote From a Photo` | `Junk Removal & Cleanouts: Houses, Garages, Basements` (no city, no benefit, a list of places) |
| Under about 70 characters, so it isn't cut off (A); 100 is Facebook's limit (`validateListing`) | `Garage & Basement Cleanouts Bethlehem – Same-Day Pickup` (55) | a title that runs past 70 and loses its end in search |
| The words people search with (A) | `junk removal`, `haul away`, `cleanout` | `residential debris solutions`, `decluttering services` |
| No caps, no hype words, no symbol strings (E, F, A) | `Junk Removal Bethlehem PA – Free Quote` | `JUNK REMOVAL!!! ⭐ CHEAP ⭐ WOW` |
| One service per listing (B, A, E) | `Hoarder Cleanouts Bethlehem PA – Free Quote` | `We Do Everything – Junk, Moving, Cleaning, Yard` |

## Description

It answers three questions, in this order (A): what you do, why pick you, how
to get a price.

| Rule | ✅ Good | ❌ Bad |
| --- | --- | --- |
| Open with the reader's situation, not the seller (D) | `Garage you can't park in? Basement full of boxes?` | `Junk removal and full cleanouts in Bethlehem and nearby.` |
| Services as a short list to scan (A, C) | `• Furniture, mattresses, appliances` on its own line, one group a line | one sentence listing nine things |
| Prices as numbers (A, C) | `Small load (a few items): $99` | `Great prices!` / `Call for pricing` |
| Never "cheap"; say "free quote" (B) | `Free quote from a photo` | `Cheapest junk removal in town` / `affordable` |
| Say what happens next (A) | `1. Send a photo 2. Get your price 3. We load, haul and sweep up` | nothing about how it works |
| Credentials and area only if true (A, C) | `Bethlehem, Allentown and Easton` (once the owner confirms them) | `Licensed & insured` with no licence |
| The call to action in the reader's words, naming what they get (D, A) | `Send a photo of the pile here and get your price` | `Contact us` / `Inquire within` |
| Plain tone, no exclamation marks (B, D) | `We take it all and leave it swept.` | `Best service ever!!! Don't miss out!!!` |
| Real urgency only, a fact (D) | `Pickup tomorrow if you message today` (only if true) | `Limited time offer!` |
| Paragraphs of two or three lines, no walls of text (A) | short blocks with a blank line between | one 10-line paragraph |
| Spell-checked, one language (E, F) | | typos, mixed languages |

## Photos

| Rule | ✅ Good | ❌ Bad |
| --- | --- | --- |
| 4 to 6 photos of real past jobs (A) | the pile, the truck loaded, the room empty | one photo, or stock images |
| The cover is the strongest before-and-after (A, C) | a split before/after of the same room | a logo or a text card |
| Real over made-up: "homeowners can spot fake photos easily" (A) | photos from real jobs | generated images; the Bethlehem listing's two photos are generated (`images.jsonl`) |

How photos are stored, varied and uploaded: `docs/listingMedia.md`.

## Worked example: the Bethlehem listing

**❌ What went up on 2026-10-22** (listing 1425935622848350):

```
Junk Removal & Cleanouts: Houses, Garages, Basements

Junk removal and full cleanouts in Bethlehem and nearby.
Houses, apartments, garages, basements, sheds, storage units, hoarder cleanouts.
We load it, haul it and sweep up. Furniture, appliances, bags, debris.
From $99 for small loads. Message a photo of the job for a quote.
```

What's wrong with it, rule by rule:
- The title has no city and no benefit; it is a list of places.
- The description opens with the seller, not the reader's problem.
- The services are one long sentence of nouns.
- There's one price, and nothing about how it works.
- The call to action, "message a photo", is the best idea in it, but it's buried at the end.

**✅ Rewritten by the rules.** The parts in `[brackets]` need a fact from the owner
first; leave a line out if it isn't true.

```
Junk Removal Bethlehem PA – Free Quote From a Photo

Garage you can't park in? Basement full of boxes? A whole house to clear after a move?
Send us a photo of the pile and we'll reply with a price. No visit needed.

What we take:
• Furniture, mattresses and appliances
• Boxes, bags and everyday clutter
• Garage, basement, shed and storage unit cleanouts
• Hoarder and estate cleanouts

Prices:
• Small load (a few items): $99
• [Half truck: $___]
• [Full truck: $___]

How it works:
1. Send a photo here
2. Get your price
3. We load it, haul it away and sweep up

[Bethlehem and the towns you cover]. [Same-day pickup when we have a slot, only if true.]
```

## Versions: one ad, several ways to say it

An ad that goes out on more than one listing in a city carries **copy
versions**: whole title-and-description pairs, each with its own angle (a
garage cleanout, "moving out? we take what's left", one big item, a free quote
from a photo). Write them in `listing.json` as `copyVersions`:

```json
"copyVersions": [
  { "id": "photoQuote", "title": "Junk Removal Bethlehem PA – Free Quote From a Photo", "description": "..." },
  { "id": "garageCleanout", "title": "Garage & Basement Cleanouts Bethlehem – Same-Day Pickup", "description": "..." },
  { "id": "movingOut", "title": "Moving Out of Bethlehem? We Take What You Leave Behind", "description": "..." }
]
```

- **How many:** at least as many as the listings the ad will have live in
  that city, never fewer than 3. `log facebook campaign fill` counts the ones
  already live (ready, publishing, unconfirmed, active, under review) and
  refuses with `notEnoughCopyVersions` when it is short.
- **How different:** every two titles differ by at least half their words, not
  counting the city's.
- **Each by the rules above:**
  - every title names the city, at most 70 characters, no emoji, no words in
    capitals, no "!", no banned words;
  - every description has a price with a number, a list, and the photo ask.
- **The first version is the ad's own title and description;** leave `title`
  and `description` out, or make them match it.
- **Check before saving:** `log facebook listing lint --file listing.json`
  lists every broken rule; `listing create` and `campaign fill` refuse the same.
- **Which copy gets which:** each copy of the ad (`campaign fill`, `heal`)
  takes the version least like what's live in its city, by shared words (title
  counted twice as much as the description). A replacement skips the version
  the lost copy used. Code: `src/facebook/marketplace/copy`. The checkable rules,
  one by one: [docs/specs/marketplaceCopy.md](../../docs/specs/marketplaceCopy.md).

## Checklist before `log facebook listing create`

- [ ] Title: service, city and one benefit, under 70 characters, no caps or symbols
- [ ] First line: the reader's situation
- [ ] Services as a list; prices as numbers; never "cheap"
- [ ] How it works, in three steps
- [ ] Only true claims (same-day, licensed, insured, towns)
- [ ] Call to action: send a photo, get a price
- [ ] 4 to 6 photos, the strongest before/after first
- [ ] Spell-checked, plain tone, no exclamation marks
- [ ] Going out on more than one listing in a city: enough copy versions, and `log facebook listing lint` passes

## After it's up (A, C)

- Reply within the hour: the check (`log facebook check`) says when a chat
  arrives, and the host checks every round.
- Watch the clicks: the check saves each listing's clicks in the last 14 days
  to `clicksCount`. Try one change at a time (title or cover photo) and compare.
