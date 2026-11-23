---
name: charles-create-posters
description: "Make posters and social graphics with the art direction of Quartr's viral posters on X (Jensen Huang's jacket alone on a coat rack, cockroaches for Rollins, a tree of price tags for Dollar Tree): one witty picture idea that could only be this subject, from its own world (name, logo, founder, product, motto, material, heritage, news), made as a photograph, print, pixel field, type texture or collage in the brand's real colours, with a print finish and almost no type. By default the poster is the picture and the subject's logo; event details (an earnings call's date, time and quarter, a publisher line) go on only when the user asks for an event poster. It writes 20+ ideas and kills the weak ones, makes the picture with fal.ai models or code, renders it in Chrome and checks it beside the real posters at feed size. Use when someone wants a poster, key visual or social graphic in this style for a company, brand, product, launch or event (earnings calls included), or wants one critiqued."
---

# Create posters

Quartr's posters on X get 100k+ views because each picture is one idea that could only be that company, made with a
fashion photographer's eye and surrounded by almost nothing. This skill takes that taste (how they find the idea, how
they make the picture, how much they leave out) for any company, brand, product or project. It never takes their
branding: no Quartr name, wordmark or tagline, and no earnings-call text unless the user asks for an earnings poster.

Read all four references before your first idea: [swipe.md](references/swipe.md) (the 22 real posters and how the
NVIDIA one was found), [ideas.md](references/ideas.md) (finding the idea), [pictures.md](references/pictures.md)
(making the picture), [system.md](references/system.md) (canvas, type, logo, layouts, finish).

## What goes on the poster

Walk this first. It picks the template and decides which facts you need.

```
What did the user ask for?
├── An event poster: an earnings call, an investor day, a listing, a launch on a date
│   → new <folder> --event: a lockup (their brand | the subject) and two short sentences, every fact
│     checked against the source (step 1; system.md, "Event posters")
├── A poster with words they gave you: a title, a line, a date
│   → new <folder>, then exactly those words in the one type size (system.md, "Words"). Add none.
└── A poster for a company, brand, product or project, and nothing more
    → new <folder>: the picture and the subject's logo, small on the margin. No other text.
```

Why: the picture is what people share, and every word you add competes with it. Event text nobody asked for also
dates the poster to a moment the user didn't choose, and it borrows Quartr's format, which is theirs, not the style.

## The bar

Every poster passes all eight. Each exists because breaking it is what separates these posters from the copies.

1. **One idea, read in three seconds, that could only be this subject.** Cover the logo and swap in a competitor's:
   if the poster still works, the idea is generic. Why: the picture does all the work in a scrolling feed, and a
   generic picture (a rocket, a chip, a chart) is what every copycat posts.
2. **The idea comes from the subject's own world**, and its story right now beats evergreen lore when there is one.
   Never from finance clip art (bulls, rockets, coins, charts, handshakes), and no finance at all unless the user
   asked for an earnings poster. Why: the swipe file's ideas all come from the company's name, logo, founder,
   product, motto, material or heritage; that's what makes fans share them.
3. **One subject or one pattern, and nothing the idea survives without.** Choose the composition from the idea, not
   from habit: a small object low in a big quiet field (NVIDIA), a big subject that fills the frame (Ferrari, Apple),
   a full-bleed pattern (Rollins, Nu, Verisign), type as the picture (Palantir, Meta). The one thing the idea depends
   on must read at phone size. Why: the NVIDIA team's winner removed Jensen and kept the jacket, and the run never
   repeats one layout; a series of small objects in empty fields reads as a template.
4. **Made like a real photograph, print or painting, never like "AI art".** A named light, a named camera or print
   process, real proportions, no text or logos inside the picture, none of the tells in pictures.md. Why: one waxy
   surface or melted detail and the poster reads as generated, and the whole effect is gone.
5. **The brand's real colours, and at most three.** Hex values from the brand's own files, plus black, white or
   paper. Why: Nu purple, Ferrari red and Cat yellow make the company recognisable before the logo is read.
6. **Almost no type, and what there is sits on the system.** The logo alone by default; the user's words or the
   event lines only when the tree above says so, in one size of Inter Display on the margins (system.md). Why: the
   quiet type is what lets the picture be loud, and what makes a set of posters look like one studio's.
7. **Every fact on it is right.** On an event poster: day, date, time, zone and label match the source, the weekday
   matches the date, and the publisher line claims only what the publisher does. Why: one wrong date and nobody who
   follows the company will share it.
8. **It holds its own beside the real ones.** At feed size and at full size, next to the swipe file, it isn't the
   weakest poster in the row. Why: that's the bar the user asked for.

## Never

- **Never put Quartr's name, wordmark or tagline on a poster** ("Streamed & transcribed in real time on Quartr" and
  its look-alikes), and never give a swipe poster to an image model as a reference: models copy the wordmark and
  the layout along with the style.
- **Never add event text the user didn't ask for:** no dates, times, quarters, "earnings call" or "live on…".
- **Never generate a real person's face or body.** Use their object, an anonymous figure, or a licensed real photo
  turned into a print (pictures.md).
- **Never let an image model draw a logo or any words.** Logos come from real files, type from the poster.
- **Never mock a tragedy** (layoffs, deaths, accidents, lawsuits). The wink is one the subject's fans would share.
- **Never copy a swipe poster's idea** for the same company. Study them for how they think.

## Setup

The kit is in `kit/` next to this file; `<kit>` below means its path.

- `cd <kit> && bun install` once (or `npm install`; Node 18+ works too). Needs Google Chrome (or set `CHROME_PATH`)
  and ffmpeg for `refs`.
- Pictures, edits, upscales and cutouts call fal.ai: `FAL_KEY` in the environment, or in a `.env` in or above the
  working folder, or in `~/.env`. A poster takes 8–16 images, $1–3; tell the user before spending more than $5.

## Steps

Work in one folder per poster: `bun <kit>/poster.mjs new <folder>` (add `--event` for an event poster) makes
`poster.html`, `brief.md`, `pic/`, `logo/` and `out/`. Write everything you decide into `brief.md` as you go.

### 1. The brief

- **What goes on it:** your answer to the tree above, and the user's exact words if they gave any.
- **The subject's world:** the nine things in ideas.md, from real sources, including the last four weeks of news.
- **Event posters only:**
  - **Who's posting** (the publisher), their wordmark file if any, and what their product really offers. With no
    publisher, the lockup is the subject's logo alone and the second sentence is "Live at 05:00 PM ET."
  - **The facts:** find the subject's own announcement (an investor-relations page or press release): the date, the
    time and zone, and the label exactly as written (Q3 FY2027, Capital Markets Day 2026). If the date isn't
    announced, ask whether to use the expected date from the subject's own pattern; when the user has said not to
    ask, use it and say so plainly in your delivery. A date announced without a time is the same: use the usual time
    and say so. Never present a guess as announced. Investor sites often refuse automated fetches (a 403): open them
    in a browser if you have one, or read the date from SEC filings or wire-service releases.

### 2. Study the real ones

`bun <kit>/poster.mjs refs` downloads the 22 posters and writes `~/.cache/charles-create-posters/refs/sheet.jpg`.
Open the sheet, then the three or four posters nearest to where you're heading at full size. Study the pictures and
how little is in each one; their type and wordmark are Quartr's and stay out of yours.

### 3. The idea

Follow ideas.md: at least 20 one-line ideas across at least six moves, score each on the six questions, keep the
three with the highest lowest score, pick one, then subtract. All of it goes in `brief.md`, scores included.

### 4. The picture

Follow pictures.md for the medium. For photographs: write the prompt to the formula, run four candidates, look at
them side by side (`sheet`), pick, fix with `edit`, `upscale` the keeper. For code-made pictures: draw them with
`art.js` inside the poster.

```bash
bun <kit>/poster.mjs gen "<prompt>" --out pic/a.png --n 4             # pic/a-1.png ... a-4.png, prompt beside each
bun <kit>/poster.mjs sheet pic/a-*.png --out pic/a-sheet.jpg
bun <kit>/poster.mjs edit pic/a-3.png "<one change>" --out pic/b.png  # nano by default; --box x,y,w,h keeps the rest
bun <kit>/poster.mjs composite pic/a-3.png pic/b.raw.png --box ... --out pic/b.png   # re-blend a boxed edit, free
bun <kit>/poster.mjs extend pic/b.png --out pic/c.png --scale 0.7 --anchor bottom   # zoom out (models ignore "60% of the frame")
bun <kit>/poster.mjs upscale pic/b.png --out pic/final.png
bun <kit>/poster.mjs cutout pic/thing.png --out pic/thing-cut.png
bun <kit>/poster.mjs recolor pic/b.png --to "#hex" --ground pic/b-cut.png --out pic/c.png   # a backdrop off the brand's colour
```

To zoom out, walk this:

```
Is every edge you'd grow evenly lit plain ground (flat paper or colour, a wall in even light)?
├── Yes → extend --flat: grown in code, free, no seam
└── No (a lit sweep, a vignette, a pool of light, an object near the edge)
    → extend without --flat: the model paints the surroundings and the kit heals its seam
Either way, open the seam view it writes (pic/c.seams.png) and look along the corner marks.
```

### 5. The poster

Edit `poster.html`: the layout that leaves the subject alone (system.md), `--field` and `--ink`, the logo, the words
the tree allows, the finish. Get the logo with `bun <kit>/poster.mjs logo "<Company>" --out logo/brand.svg` and
compare it at 100% with the logo in the subject's own site header: Commons often keeps one from before a rebrand, and
then you take the subject's file with `--url`. Load extra faces with `font`.

### 6. Render, check, critique: at least two rounds

```bash
bun <kit>/poster.mjs render <folder>    # out/poster.png (2520 x 3360), out/poster.jpg, out/poster-feed.png
bun <kit>/poster.mjs check <folder>     # out/check-feed.jpg: yours beside six real ones; out/check-large.jpg
```

Fix every `check:` and `PROBLEM` line `render` prints (it says what it did to the logo and the grain; on an event
poster it also checks the date's weekday and works out `--colA` when a line needs more room). Then open
`check-feed.jpg` and `check-large.jpg` and score your poster 1–10 on each line below, as a creative director who has
the real ones on the wall:

| | Ask |
| --- | --- |
| Idea | Read in three seconds? Only this subject? A wink or a question? |
| Picture | Would a photographer or printmaker sign it? Any tell from pictures.md at 100%? |
| Composition | One subject, enough calm field, the logo on a quiet margin, nothing crowding the edges? |
| Type | Only what the tree allows? On the system: breaks by sense, no orphans, logo optically even? |
| Colour | The brand's own, three at most, one accent? |
| Finish | Grain or paper right for the medium, not overdone? |
| Facts | Event posters: day, date, time, zone, label, publisher claim? |

Look at `check-feed.jpg` as a stranger would: the thumbnail is all most people see, so the one detail the idea
depends on has to read there, and your poster mustn't be the weakest in the row.

If you can start a subagent, get fresh eyes: point a new agent at the blind folder `check` prints (the row and each
poster under a letter, cropped and sized alike so no logo or file gives yours away, in a path with no names in it)
and ask it to say what each poster says about its subject, to rank the whole row best to worst, and to name anything
that looks generated. A ranking keeps it calibrated, since it's as hard on the real posters as on yours. Don't tell
it which is yours, and tell it to keep any files it makes (crops, notes) in that folder and write nothing anywhere
else. If `check` notes that your logo or words sit in
the middle or along the edge (the crop can't hide them there), tell the critic the posters come from different
studios. If it can't say your idea back in a sentence, the idea isn't landing. Fix the poster, not the critic's
reading.

Anything under 8 gets fixed and re-rendered; write what you changed and why in `brief.md`. If the idea scores under 8
after two rounds, go back to step 3 and take the next idea rather than polishing a weak one: re-rendering never fixes
an idea.

Every image call adds an estimate to `spend.jsonl` and prints the running total. Three picture rounds at most; the
cap wins over "anything under 8 gets fixed". At $5 or three rounds without an 8 everywhere, stop making images,
deliver the best version, say plainly what's missing, and recommend the fix or the next idea in a line.

### 7. Deliver

Give the user `out/poster.png` (and `out/poster.jpg` to post), the idea in one sentence, the two runner-up ideas in a
line each, the sources for any real photo or fact that isn't common knowledge, and what the image calls cost.
