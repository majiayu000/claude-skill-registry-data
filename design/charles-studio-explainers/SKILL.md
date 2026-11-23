---
name: charles-studio-explainers
description: "Make the explainer cards in my reels look hand-made by a design studio instead of plain UI mock-ups: each line gets an idea (the moment it fires in an app or game people know, recreated, or a real object that puns on it), one signature move, one colour family lit from a side, and big confident type, on charles-explainers-assets' timing, slots and readability rules, then hill-climbed with fresh critics against a reference. Use when explainer graphics are called boring, plain, flat, generic or not engaging, when I want cards that look like a studio made them, look premium, pop, or match a reference (Tobi Donadon's Construct Design, an Awwwards or Apple Design Award look), when I say hill climb the visuals, or when a list, hack or principle reel needs a card per item people would screenshot. Triggers on: more interesting, MUCH more interesting, boring cards, studio look, visually engaging, make it pop, like this reference, hill climb, explainer graphics, before/after cards."
---

# Goal

Every card still teaches its line in the second a phone viewer gets, and now it also looks like a studio made it: an idea you could say in one sentence, a real-looking object acting it out, one colour family lit from a side, and one move a person would describe to a friend ("the anchor drops on the price", "a coin scratches off +40 XP").

Why: my first cards for 20 Psychology Principles were clean white UI side by sides, and I said: "Make the explainer graphics MUCH more interesting. Reference this reel and hill climb until we can make it like this" (22 Nov 2026, pointing at Tobi Donadon's article "How to Make Claude Design Like a Real Studio" and his Construct Design library). Clean and correct isn't enough to hold a scroll. A clear idea, a rich material and a move that lands are.

Then, after five rounds of object metaphors: "try to use practical examples from mobile apps. Not ones that are too abstract. Think of what the best apps and games use like Monopoly Go, Duolingo, Candy Crush, etc. U can even recreate UI from iconic/well known apps to create a familiarity effect" (23 Nov 2026). A moment people have felt in an app they use reads faster than a clever metaphor.

# Keep from charles-explainers-assets

Load it first. Its contract wins on everything it covers, and this skill only adds the look:

- **The slot, the clip length and the frame:** for a list reel's term card, a transparent 1080x480 clip at reel y 1080 with the card at x 80-950, y 1150-1500, inside the safe area. On a card that flips in place (the hack-reel card), there's no Before tile and the look goes on the one stage: `references/flip-cards.md`.
- **Timing:**
  - The After's move starts by 0.15 s and is done by 0.6 s.
  - Nothing sits frozen. Hold the end pose under a slow push-in, with a living loop such as a bob, a flicker or a spin.
  - The change from the previous item's tab happens in the first 0.14 s.
- **One subject and one change at a time.** Where there's a Before, the Before and the After show the same thing, with and without the principle.
- **In a fast list, drop the Before.** When each item is up for about 1.4 s (a 20-item list reel), show only the After, filling the whole card, with no Before or After labels. Why: "having a before doesn't really add that much value" (23 Nov 2026), and it took a third of the card. Keep a Before for slower formats, where the contrast is the lesson (hack reels, Day N).
- **Words on screen:**
  - The tab says what the principle means in plain words, on one line.
  - Words the viewer must read are 26 px or more in the final frame.
  - The words that carry the principle are 34 px or more.
- **The phone check:** `check.mjs`, `glance.mjs` and `words.mjs` in that skill's kit, and a frame from mid-move and the end pose of every card, looked at over a frame of my footage.

# The studio layer

`references/craft.md` has each rule with its numbers and the reason for it. In short:

1. **The real moment first.** If people have felt the principle in an app or game, recreate that moment, big:
   - Duolingo's streak about to reset, a daily prize wheel, Candy Crush's out-of-moves screen;
   - Monopoly Go's free dice gift, a dating app's blurred likes, Spotify Wrapped, the App Store's ratings card;
   - an iOS reminder and its notification.

   Use the app's own look (its type, its colours, its button style), without logos or mascots. Never put generic names in it (Maya, Noah, Leo, Sarah, Alex): they mark a screen as generated. Write the app's own copy, never a caption to the viewer.

   **An idea before a template.** Only when there's no real moment to show, find the real-world object that is a pun on the principle:
   - an anchor for price anchoring, a wooden decoy duck for the decoy effect, a wax seal for commitment;
   - a scratch card for variable rewards, a candle burning down for a streak about to end, a candle frozen in ice for a streak freeze;
   - an instant photo developing for social currency.

   Say the card in one sentence before building it. If you can't, there's no idea yet.

   Never put a UI widget on the studio side (a checklist, a leaderboard, price rows, a score card, a share pill). Turn it into the object it stands for: a receipt that prints, game pieces on numbered steps, kraft price tags, an enamel pin you'd wear. Why: round 4's critic read those widgets as the default Claude builds.
2. **Photographed materials, never game icons,** except inside a recreated game screen, where the game's own glossy icons (a gift, dice, a treasure chest) are the real thing. Generate each object as a studio product photograph, with real wear, on a transparent background (`references/objects.md`). Why: the first critic's single most wrong note was glossy, toy-like 3D icons. They "read as a mobile-game ad", and the reference's objects (a marble orb, a crystal prism, a card over a tile grid) look photographed.
3. **Lit, not pasted.** Each object gets:
   - its world's light on its lit side and its deep colour on the far side;
   - a cast shadow on the backdrop, and a contact shadow where it stands;
   - grain over the whole card, type and photos included (`L.obj`, `L.stage`).

   Flames light their card and even the type beside them. Why: round 3's critic, of photos set on a gradient without these: "nothing sits in light", a template with stock PNGs.
4. **One colour family per card,** lit on its object, with the deep colour behind the type. Two or three cards in 20 stand on cream instead, with dark ink and one loud colour, and never black. Every word you must read passes 4.5:1. Why:
   - The critic flagged the stock violet, magenta and orange gradient as the AI tell.
   - The reference puts one loud hero on cream, and round 3 had no neutral ground at all.
   - A near-black world turns the card into a hole on my black T-shirt.
   - A light behind the type put most white headlines at 2-4:1.

   **No two cards in a row share a colour.** Two light cards count as the same colour, whether white, grey, cream or a pale tint. Recreated app screens are often white, so when a white screen's neighbour is light too, put its panel on a coloured stage: a paywall on a savings green, the Calendar icon on its red. Run `kit/neighbours.py` on the clips in list order. Why: each card replaces the last in the same slot, so a repeat reads as one card that changed its words. Charles, 23 Nov 2026: "don't have back to back same colours". Round 6 had put a lime Wrapped card before the lime runner, and four pairs of white or pale cards in a row.

   Brand colours: keep the hue, and use its deeper shade for words. Duolingo's orange on white is 2.2:1, and #b85c00 is 4.5:1. White text on a bright game button gets a dark outline, the way games draw it.
5. **A light you can name, standing still.** Light each world softly from its object's side, and give every glow a source. Why: in round 2 a pool of light that slid onto the After bleached the very numbers it pointed at. The critic called it "the single most wrong note", AI glow rather than studio light. The Before only dims to about 78% as the After plays.
6. **Before is the default, After is the studio, and few words.**
   - Before is a flat tile in the card's own colour, with one element Claude builds by default in plain type at 26 px or more. Never a black block, which reads as a dead third of the card.
   - After is the object on its world. It says its point in three words or fewer, as the biggest type on the card, and some of its words are up by 0.3 s.
   - The labels are 24 px chrome. Why: round 3 put 20-30 words on a card that a phone viewer sees for 1.4 s.
   - Numbers get a second voice:
     - thin numerals for prices and gaps;
     - dot-matrix for scores and counters;
     - mono for small print on receipts, tickets and tags.

     The Before stays in plain regular weight. Why: one bold sans everywhere was round 4's second biggest note.
   - Words keep 40 px inside the card's edges. The payoff (the seal, the prize) is always whole, and props drawn in code look as real as the photos: paper gets warm stock, grain and a curl shade.
7. **Four layouts across the set:**
   - the object beside its words;
   - type locked with the object (YOU with a crystal ball as its O, a shoe standing on the word "runner");
   - the object cropped big by the card's bottom or right edge;
   - the object carrying the words (a ticket, a stamp card, a calendar).

   Why: one composition 20 times reads as a template, and the reference's signature move is type and subject locked together (SPOTTED set behind a head).

   **Space a type lockup by eye, from the letters.**
   - The small line sits one cap height above the big word. Measure from the word's x-height when it's lowercase, because a lowercase word has no ascenders.
   - No two letters touch.
   - The object rests wholly on the letters.

   Why: Charles called round 6's "You're a runner" weird spacing. "You're a" floated 88 px above the word, -0.045em left its letters all but touching, and half the shoe hung past the last r.
8. **One signature move, built from Disney's principles:**
   - a wind-up before the pop;
   - a squash on landing;
   - follow-through after it: a swing that settles, coins that arc, a page that tears away.

   Rigid things (iron, brass, a coin, wood) never squash: they fall, stop and rock. The move lands by 0.6 s and then holds still, except where real life flickers (a flame).
9. **The tells to refuse:**
   - Tobi's four default looks: the paper edition, the black launch page with a purple glow, the KPI dashboard and the dark dev tool;
   - game icons and stock gradients;
   - glows with no source, and objects with no shadow;
   - giant faint words that repeat the label;
   - anything clipped by the card's edge, crossing the "After" label, or resting against the top edge, which the tab covers on a long line. Bring things in from the right or the bottom where you can; only a fast drop (an anchor) comes through the top, and it's gone from the edge in a few frames.

# Steps

1. **Read the reference,** if I gave one. Write down what it does in plain terms: the ideas, the materials, the light, the colour, the type and the moves. Save its images in the video's `research/reference/`, which stays local.
2. **Write the beat sheet,** as charles-explainers-assets does, and add to each line its idea: the object, the move and the colour family.
3. **Explore three directions,** rendered side by side on two or three lines, before building all of them (`references/hill-climb.md`). One of them can be your own synthesis.
4. **Generate the objects** with `kit/fal_gen.py` and look at each one on a mid colour. Make every changed state of an object (a happy plush and a sad one, a candle and the candle in ice) with the edit endpoint from the first image, so the two match. Measure each object's visible bounds with `kit/bbox.py` before you place it.
5. **Build** with `kit/studio.js` on charles-explainers-assets' renderer, one file of builders per few cards, joined by `kit/bundle.sh`.
6. **Hill-climb.** Render stills at 0.3 s and at the end pose, sheet them over my footage (`kit/sheet.sh`), and have a fresh critic score them against the reference. Fix the biggest problem first, re-render, look again, and log every round in the video's `DESIGN-LOG.md`.
   - Stop at the bar I named, or when three rounds in a row don't raise the score.
   - Fix by eye too. Collisions, clipped text and blow-outs show up on the sheets before any critic sees them.
7. **Run charles-unslop, emil-animations and charles-polish over every card,** and fix what they find: generic names and copy, entrances from scale 0, springs past bounce 0.3, numbers that roll more digits than changed, dead frames mid-move, collisions. I asked for this pass on 23 Nov 2026.
8. **Run charles-explainers-assets' phone and words checks, and `kit/neighbours.py`** over the clips in list order, then deliver.

# Deliver

The same as charles-explainers-assets:

- every clip (HEVC with alpha at 2x for the edit, VP9 with alpha at 1x for the plan page);
- `explain.json` with each line's tab, takeaway and source;
- the phone sheet;
- the generated objects in `gen/`, with `gen/jobs.jsonl` saying the model, the prompt and the date;
- `DESIGN-LOG.md` with each critic round's scores and what it changed.
