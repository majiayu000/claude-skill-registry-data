---
name: deck
description: Turns a document, a dataset, or a spoken brief into a Figma Slides deck. Reads the source, agrees an outline before writing anything, then builds slides from the team template's archetypes and audits overlap and wording before handing back. Research reports, plans, retrospectives, proposals — it does not care which. Template values come from the local assets /fig:deck-setup produced. Triggers - "/fig:deck", "make this into a deck", "turn this doc into slides", "슬라이드로 만들어줘", "발표 자료 만들어줘", "덱 만들어줘".
allowed-tools: Read, Write, Bash, AskUserQuestion, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__create_new_file, mcp__plugin_figma_figma__upload_assets, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__whoami
---

# deck — building a presentation deck (Figma Slides)

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

Moves one source into a presentation flow and builds a deck in **a Figma Slides file**. The slide count follows the source's volume and the presentation conditions (it is not fixed).

The design comes from the local assets in `deck.assets_dir` — `template-spec.md` (values and the archetype catalog) and `template.js` (palette, constants, builders). It does not re-read a remote template on every run; it Reads these two.

**Without the assets, run `/fig:deck-setup` first.** Run it again to re-extract when the source template is revised. Never build by inventing values — an invented slide leaves the type scale without exception.

## Triggers

- Natural language: "turn this into slides", "presentation material", "make a deck", "this doc as slides"
- Explicit: `/fig:deck <source>` (a document link, a file path, a topic)

## Procedure

The shape — **align** (intent and source / 1–2) → **design** (agree the outline / 3) → **build** (assets and build / 4–5) → **audit** (structure and wording / 6–7) → **output** (8)

### 1. Confirm the intent

Do not ask everything at once; start with what actually branches. These three are usually enough.

- **The source** — which document or dataset is being moved. Take a link or a path
- **The occasion** — in front of whom, for how long. The presentation length decides the slide count (10 minutes is around 12 slides; 30 minutes carries 25 or more comfortably)
- **The form** — a standalone deck, or a section of an existing one

**Match the density to the source first.** Compress a long report into a short deck and "this feels thin" comes back. Where the source has several tables, lists, and findings, work out first whether each is worth a slide of its own; if a condensed version is what is wanted, confirm with the user what gets dropped.

### 2. Read the source

- Read the source in full. Never build an outline from a summary or a table of contents — what carries a presentation is the numbers, the quotations, and the photographs in the body
- A large document's fetch result lands in a file. Image URLs swamp the body, so substitute them out before reading
- Where the body has drawings or photographs worth using, pull them into a list. Presigned S3 URLs for document images download with `curl` without authentication (they expire quickly, so fetch them immediately)
- Never invent a fact in the deck that the source does not have. Where evidence is needed, go back through the source

### 3. Agree the outline (the gate before writing)

**Agree the composition as a table before building any slides.** Changing the structure after everything is built costs a rearrangement and a re-extraction.

What the table holds: slide number / title / what it carries / which archetype. Whether to follow the source's structure or rearrange it into a presentation flow is settled here too.

- Work the slide count back from the presentation length
- Where four or more slides of the same character run consecutively, put a section transition or a differently shaped slide between them
- For an item with no image, decide here whether it becomes a diagram, a table, or a figure rather than leaving an empty card
- **How closely to follow the template is settled here too.** An archetype is a per-slide rule and the template is a menu rather than a deck, so the more of it you draw on, the more the title positions and content tops scatter. Offer two routes to choose from — ⓐ use the archetypes' own coordinates but hold the title family to one ⓑ go back to the archetypes entirely. Either way the principle is **never to invent a coordinate** (pitfalls 24 and 25)

The file gets created after the "go".

### 4. Prepare the assets

Images go up to Figma to get an imageHash, which is handed to the builder.

1. Collect them into a working folder with ASCII filenames (`pickup-worktop.png` style)
2. Strip the macOS quarantine: `xattr -d com.apple.quarantine <file>`
3. **Measure the original aspect ratio** — `sips -g pixelWidth -g pixelHeight`. Matching the image box to that ratio is what keeps `FIT` from leaving margins (pitfall 6)
4. A scratch folder can be emptied between sessions. Re-collect from the source when it is needed again
5. **Do not trust filenames — open all of them.** A file called `fig10_bakery-display` turned out to be a photograph of a closed-for-business notice. A name is the intent at the moment of shooting, not the content of the photograph. **Confirm a candidate by eye before it goes on a slide** — opening 27 images one at a time costs nothing but tokens, so build a single contact sheet with headless Chrome and look at them at once.
6. **Sweep the source exhaustively for drawings it already has.** A chart drawn for the report and never carried into the deck is a common find. List the whole folder and pick what to use; when comparing several, make a single contact sheet and look at them at once — opening photographs one by one only costs tokens
7. **A report's drawings cannot be used as they are.** Caption paragraphs, footnotes that only work in a document, and the source's section numbers are baked into the image. Crop those out before it goes on a slide. Cropping changes the ratio, so recompute the box size

### 5. Build

The order is **create the file → apply the team template (the user does this) → lay out with archetypes**.

1. **Load the skills** — pass `figma-use` and `figma-use-slides` together in `skillNames`
2. **Read the local assets** — `template-spec.md` and `template.js` from `deck.assets_dir`. They attach to the top of the build script in this order:
   `${CLAUDE_PLUGIN_ROOT}/_common/scripts/deck-base.js` **→** `template.js`.
   Generic helpers first, team constants and builders second (helpers are declarations and hoist; constants are read at call time).
   **Pick from the spec's archetype catalog first.** Where nothing fits the shape of the content, do not improvise a layout — cut the content to the nearest archetype, or split the slide. An invented layout always leaves the type scale
3. **A new file** — check the planKey and the seat with `whoami`. A plan listed with `seat: View` cannot take the `use_figma` writes the build is made of, so a file created there could not be built; stop and say so rather than trying. Then `create_new_file` (editorType `slides`)
4. **MCP cannot apply the team template.** Once the file exists, ask the user to apply the team's shared template from the Templates panel, and wait. Applying it is what brings in the team fonts, colours, and named text styles. Without it, everything breaks into substitute fonts and 'Pick a style'
5. **Confirm what applying it did** — it can pull in the sample slides wholesale. Take one of them as the theme reference (`REF_SLIDE`) and `clone` it to make new slides, then **delete the samples once the build is done**
6. **Upload the images** — get hashes with `upload_assets`. Uploading leaves frames on the page, so clear them along with everything else after the build
7. **Three to five slides per call.** A slide is an isolated subtree, so batched building is safe
8. **Reordering** — a new slide attaches at the end of the row. Repeating `row.appendChild(slide)` in final order sorts them (safer than computing insertChild indices)
9. **Bind the text styles** — after the build, bind each TEXT to the file's named styles by `family|style|size`. Sizes outside the scale and SemiBold staying raw is normal

### 6. Structural verification

Check each batch with a read-only script. Passing saves screenshots.

- **How many distinct values** — count opacity values, accent colours, and font sizes exhaustively and look at how many kinds there are. Secondary-text opacity is one value; accent colours only where meaning is attached (pitfalls 41 and 42)
- **Orphan lines** — count lines holding a single word, and lines under 25% of the width. Exclude short complete sentences (pitfall 39)
- **Order** — put the source's contents and the deck's slide numbers side by side and look for reversals and omissions. Skipping a parent section and coming back to it is the most common mistake
- **Item counts** — compare the number of items the source covers against the number of slots on the slide. Check them against a figure written on an earlier slide ("7 stores") too. A layout truncating content is caught by this check alone
- **The skeleton** — sweep the whole deck at once and count ⓐ how many title positions there are ⓑ how many content-top y values ⓒ whether any slide breaks the margins. Look at the **provenance** of the values, not their **count** — is every value that turned up a number that exists in `template-spec.md`? One value not in the template means it was invented on the spot. Where the families were held to one, check that promise too
- **Out of bounds** — nodes outside 0–1920 and 0–1080 in slide coordinates. Check the margin bounds (left 128 / right 1792) alongside
- **Automatic wrapping** — per block, check whether `height / (fontSize × lineHeight)` exceeds `characters.split('\n').length`. Larger means the typesetter is breaking in mid-word (pitfalls 31, 33, 34)
- **Empty cards** — slides where the gap between the card's bottom and the content's bottom is over 100px. Shrink the card to the content and level the heights within a row
- **Alignment** — text whose `textAlignHorizontal` is not LEFT. Any CENTER left outside diagram labels and pull quotes is a node carried over from another family
- **Body contrast** — a template's dimmed colour is usually **for secondary text**. Actually compute the effective contrast against the background and see whether it merely scrapes the WCAG AA floor (4.5:1). If it only scrapes it, use it for subtitles, captions, and sources alone and **keep reading body copy opaque**. Check too that the body colour does not split into two across the deck
- **Line height** — body copy is **1.5×** the font size (WCAG 1.4.12). A template line height tighter than that means it was set for one- or two-line captions and is not enough for a paragraph. Blocks of three lines or more get around 8px of paragraph spacing too
- **The type scale** — slides carrying a `fontSize` outside the spec's scale. Even one means that slide has too much content
- **Surface colour** — more than one card surface colour in a deck is a failure. Use the spec's single card colour
- **Density** — over 40 nodes per slide. A transplanted table trips this immediately
- **Screenshot checkpoints** — the first batch (the visual system) and the last (overall quality). Walk these one at a time
  - [ ] Does the image read large inside its box, without excessive margin above and below
  - [ ] Does the card look empty at the bottom (a fixed height larger than the content makes an empty box)
  - [ ] Does a title already inside the image duplicate the slide title
  - [ ] Do the table's columns encroach on each other
  - [ ] Did the intended font actually apply

### 7. Wording audit (the last gate, particular to decks)

Correct structure with wrong sentences still means rebuilding. Slides carry many short sentences, so the following pile up especially fast. **Dump the whole deck's text and sweep it in one pass.**

- **Do not join sentences with a middle dot.** `did A · did B` becomes two sentences. Keep the tight dot inside compounds and short lists of equals
- **Cut parenthetical dashes.** `there are rules — 20 seconds, 120 seconds` → break it into sentences or change the word order. A dash separating a table's labels can stay
- **Do not use words that point at a position in the deck.** "as covered on the previous slide", "see the next slide" become false the moment a slide moves once. After a rearrangement, sweep with a regex for previous/next/earlier slide and check nothing is left. Where a pointer is genuinely needed, point by name rather than by position ("the robots were covered separately")
- **Do not carry over identifiers that only work inside the source document.** Section numbers, stage codes, and ticket numbers become names and figures. The audience is not listening with the source open
- **Remove parenthetical insertions.** Definitions, conditions, and dates get written out as sentences rather than wedged into parentheses
- **Unify proper nouns.** Where one thing appears under two names (a short form and a full form), settle on one
- **Fix translationese and passive voice.** The "with respect to", "by way of", "was observed to be", "is being permitted" family
- **Recount the figures.** Compare the count in a title against the actual row count, and the same figure on an earlier slide against a later one
- **Cut overstatement.** Replace it with the evidence figure, or delete it
- **Break lines at the boundaries of meaning.** Never mid-word; between subject and predicate, or at a clause boundary, is fine. `the bakery display and the chilled showcase ⏎ form the browsing path` is correct; `from entering the store and receiving a drink ⏎ to leaving` splits one unit.
  **Do not settle on "one sentence per line."** Fix that and you start cutting sentences to fit the column width, and the source's writing disappears wholesale.
  **Roughly level the line counts against the neighbouring column** — one column full of fragments makes that column look misaligned.
  The automatic check: per text, `rendered line count > manual newline count` means automatic wrapping happened. Only touch it then.
- **Insert manual line breaks wherever CJK text breaks mid-syllable-cluster.** In a narrow column the typesetter cuts mid-word, because CJK has no spaces to break at. The automatic check catches all of it — per text, `rendered line count > manual newline count` means automatic wrapping happened.
  When the lines will not level, do not just add breaks — shorten the sentence. A line on a slide is supposed to be short

Finer points of style follow whatever writing standard applies where it is being written. Without one, the items above already filter most of it.

### 8. Output

- The deliverable is the Figma deck URL. Hand it over with a summary of the slide composition
- Speaker notes get filled in only on request
- A re-run edits the existing slides. It does not delete and rebuild (only when the user says "from scratch")

## Archetypes

The builders live in `template.js` in `deck.assets_dir`. Do not improvise a new layout; use what is there and pass variations as parameters. Below are the standard names `/fig:deck-setup` produces — where the template has no such form, that builder does not exist either.

| Builder | Use |
|---|---|
| `titleSlide` | Cover — the official background image full-bleed, plus title and subtitle |
| `sectionSlide` | Part transition — one large sentence |
| `cardGridSlide` | N cards of a label plus a key statement |
| `autoCardSlide` | A tall card with a status badge, a title, and evidence lines (auto-layout) |
| `imageDescSlide` | N cards of real screens or photographs |
| `metricsSlide` | Numeric results — a large figure, the metric name, a description |
| `timelineSlide` | Milestones and roadmaps |
| `closingSlide` | Closing — the background rotated 180° plus a footer |
| `statusBadge` | A status chip — done, planned, undecided, by colour |
| `phoneMock` | An app-screen phone mock-up — bezel plus screen |
| `nameSection` | Naming a slide row (section) |
| `applyTextStyles` | Binding named text styles after the build |

**The cover and closing backgrounds use the official assets as they are.** Upload the background images from `template-assets/` and pass them as `bgImageHash`. Where a wordmark, a phrase, or a motif is baked into the image, do not reproduce it with shapes — a reproduction always ends up wrong. Templates commonly have the closing slide reuse the same background flipped.

**Image fit defaults to `FIT`.** On a UI screenshot, a cropped header, tab, or button takes the message with it. `FILL` is for photographs and backgrounds, where cropping is fine. A tall app screen goes in `phoneMock`; a wide one goes in a box.

**Where the source is a narrative report, the list above is not enough.** Two frequent derivatives get assembled by hand.

- **A findings slide** — a photograph or chart on the left, a subheading and an evidence list on the right. Size the photograph's box to the original ratio, and make the right side a vertical auto-layout frame
- **A table slide** — hold the column x coordinates in an array and put a 1px rule under each row. Distinguish status and character values by colour. Up to about 12 rows fits on one slide

An item with no screen becomes a diagram rather than an empty card. A chain (A→B→C), a contrast (two boxes, system and customer), and a 2×2 of cards cover most of it.

## Pitfalls

1. **Applying the template drags the sample slides in wholesale** — clear them after the build. Keep one theme-reference slide back before clearing
2. **`upload_assets` leaves frames on the page** — delete them after the build too. The hashes are already stored in the file, so the images survive the frames going
3. **`getSlideGrid()` results can be stale** — if a slide you just made is missing, confirm again with a separate read call
4. **Writing x/y before `appendChild` shifts the node by 240px** — the preamble helpers force the order
5. **Writing characters without loading the font throws** — one `loadFonts()` at the top of the script
6. **An image box whose ratio differs from the original leaves a large margin under `FIT`** — size the box to the original ratio. A flat image like 4:1 goes vertically centred with the leftover space filled by text
7. **A card's fixed height larger than its content reads as an empty box** — add lines or reduce the height. Level the bottom edge across slides of the same character
8. **A figure column and a name column overlap by a few px** — make the text box narrower than the column gap. The overlap check catches it
9. **A title already inside the image duplicates the slide title** — make the slide title a conclusion instead, or remake the image
10. **Text inside a diagram box sits high** — subtract the text height from the box height and centre it vertically
11. **`layoutSizing` on a node directly under a slide errors** — put one auto-layout frame in and use it inside that
12. **There is no `layoutSizingVertical='AUTO'`** — it is `'HUG'`. The frame's own `counterAxisSizingMode` is `'FIXED'|'AUTO'`
13. **Image hashes do not move between files** — rebuild in another file and the images come out blank. Where the theme has to be reapplied, move things by clone within the same file
14. **A crop you made cuts straight through an element** — even at exactly the right ratio, a cut through the middle of a table row or a card halves the letters. The ratio check does not catch it. Cut at row rules and block boundaries, and pad the width shortfall with the edge colour
15. **A title and a description placed at absolute coordinates overlap later** — raise the font size and the text below does not follow. Build the title-and-description pair as a vertical auto-layout from the start
16. **Several slides end up with the same name** — neighbouring titles like `what already works` and `what is already going well` confuse an audience. Sweep every title in the deck at once and remove the duplication

17. **A shape absent from the catalog leads to an invented layout** — and an invented slide shrinks the text and leaves the scale, without exception. Common shapes — tables, diagrams, contrasts, pull quotes — get looked up in the catalog first. An empty catalog means running `/fig:deck-setup` first
18. **Putting the content band right under the title punches through the bottom** — a template holds a separate content-top y per column count. The gap between title and content is intentional, so use the spec's value as it is
19. **Do not transplant a table onto a slide as it is** — a 12-row table on one slide is a document, not a slide. With many rows, unfold it into a column grid. But **spreading the rows into 12 slots is its own kind of busy** — twelve items laid out at equal weight give the eye nowhere to land, and the colour tag on each repeats twelve times into noise. **Use the original table's classification column (grouping, status, character) as a hierarchy**: make 3–5 groups from that column, and give the colour to the group headings rather than to the items. Cut each item's sentence to fit one line — two-line items twelve deep is half of what makes it busy. Columns dropped (evidence, numbering) become a subtitle line, or go back to the report
20. **Fixing the body y in a two-column layout leaves one side gaping** — because the title line count differs per column. Either unify the body y across all columns (alignment first) or measure the title height and add it (spacing first). Apply one of the two consistently across the deck

21. **Where there is no photograph to use, leave it without one** — with a photograph for one item out of four, that photograph stops being evidence and becomes a misreading. Forcing one in makes the cell structure differ per column and the baseline collapses. When assets are short there are only three things to do: cut the items, get more assets, or switch to an archetype that matches the asset count. **A hybrid cell is not a fourth option.**
22. **A run of text-only slides makes a deck unreadable** — keep to the archetypes and still, with nothing but letters, "this needs pictures" comes back. Ask of each slide "what is this shown as", and where there is no answer, make one of three: ⓐ a chart or photograph from the source ⓑ a native diagram of the flow or the contrast (boxes and arrows are enough) ⓒ a figure pulled out large. Conversely, leave a slide whose body is a quotation, and the opening and closing slides, as letters alone — filling everything is its own kind of noisy
23. **Do not drop a white-background chart bare onto a dark slide** — it reads as a white mass floating. Wrapping it in a padded white card (r16) makes it read as intentional. Every chart in the deck needs the same treatment for it to be uniform. Redrawing on a dark background is the proper answer, but first confirm that the source data or the drawing script really is unavailable

24. **Archetype fidelity and deck uniformity trade against each other — this is the user's call, not a rule** — a template's set of slides is a **menu**, not a deck. It is not an order meant to be strung together but a list of alternatives meant to be chosen from, so the more you draw on it, the more it shifts as you page through. Title position alone holds top, left-title-vertically-centred, caption, and no-title, and all four are legitimate. So "it lacks consistency" and "do not deviate from the template" cannot both be satisfied. **Present the two routes with numbers and let the user choose.** ⓐ archetype coordinates, families held to one ⓑ archetypes in full. Choosing ⓑ makes the content top scatter across several values — that is the outcome, not a failure; instead check only that **every value came from the template**. Once chosen, match slides of the same character right down to the internals (six findings slides means the lead, header, body, and description y are identical on all six)

25. **Where the source runs longer than the archetype's slot, borrow another archetype's value rather than making a new one** — a template's body slot is usually two lines of 24R (h64). Moving a report's sentences in makes it four or five lines and it invades the next row. Do not grab an arbitrary y; **raise it to a taller row value from within the same template** — borrowing the y of another archetype that uses the same column composition. If it still does not fit, then cut the sentence. Note in the report which one was borrowed from

26. **Changing the title position changes the picture size with it** — a title at 128 with a subtitle at 200 and the body pushed below gives away 330px of height, shrinking a full-bleed chart by around 30%. Reverting to the caption family (no title, caption at the bottom) nearly doubles the same width. **Compute and report the reduction or enlargement before changing family, and render afterwards to confirm the text is still readable.** White-background charts go in white cards with the image left at `FIT` — a white letterbox is invisible on a white card, so the card size and the image ratio do not have to be matched separately

27. **Pairing nodes by coordinate while moving them in the same loop scrambles the pairs** — code that matches labels to boxes by `y` picks up, on the next iteration, the node the previous one just moved. Even the subtitle gets dragged into the diagram. **State the pairs by ID, or settle them all before any transformation and freeze them into an array, then move.** After moving, print the leading text of each pair and compare

28. **Reusing a caption node as a title brings its alignment along** — a bottom caption is `textAlignHorizontal='CENTER'`. Change only its position and size and you have a centred title. When changing family, cloning an existing node of the target family is safer. At the end, sweep the alignment of every text in the deck and confirm CENTER survives only on diagram labels and quotations

29. **An archetype may have no subtitle slot** — before adding a line under the title out of habit, sweep the template exhaustively and count whether even one slide has text in that position. If none does, the subtitle is a pure addition, and when "let us follow the template" comes up later, it has to come off 26 slides at once. When removing them, **first separate what to discard from what to relocate** — delete what duplicates the title or already exists in the body, and relocate only what carries a fact, such as a figure or a range, into the bottom description slot or the left-title block's description line

30. **A square image box presupposes a square source** — a 4:1 drawing put into a template's square box with `FIT` leaves a thin band floating in the middle of the box. Using a report's drawings, whose ratios all differ, this is why the top edge of the picture sits differently on every slide. Sizing the box to the source's ratio and topping it fixes it, but that is a deviation from the template. **Render the result either way and choose**

31. **CJK automatic wrapping cuts mid-word** — the typesetter breaks by character, producing splits inside a single word. It happens even at widths around 600px. **Pick out only the blocks where `rendered line count > manual newline count`** and rebreak at word boundaries (line count is `height / (fontSize × lineHeight)`). Setting a temporary TEXT node to `WIDTH_AND_HEIGHT`, measuring word widths, and filling greedily does it. When finished, **set `paragraphSpacing` to 0** — `\n` is a paragraph separator, so spacing attaches to every line, inflating the block past the bottom edge

32. **A text-heavy slide gets fixed by hierarchy, not by volume** — do not start deleting sentences in response to "text heavy", least of all where the source's writing was to be preserved. The template gives four instruments. ⓐ **card surfaces** — for a three-item list ⓑ **a hairline rule** — as an underline under a subheading where a 2×2's cell boundaries are invisible, and between rows in a multi-row list ⓒ **status chips** — colour where status is currently distinguished only by dimmed text ⓓ **size hierarchy** — every text on a slide at one size is heavy on its own. Split primary (30R opaque) from secondary (24R dimmed). First **count the slides with zero visual elements** to pick the targets, and leave slides that already have a photograph or a diagram alone however many lines they carry

33. **Measuring text width by summing word widths overruns slightly** — measuring words separately and adding comes out narrower than real typesetting, so a greedily filled line ends up auto-wrapping and dropping its last character onto the next line. **Write it, verify, and retry** — after setting `characters`, if `height / lineHeight` exceeds the intended line count, reduce the limit width by 14px and refill. Five or six passes converge

34. **The auto-wrap check runs on the actual `\n` count only** — using an intermediate value such as a sentence split or a period split makes the segment count exceed the rendered lines, so the genuinely wrapped block passes as "fine". The criterion is always `rendered line count > characters.split('\n').length`

35. **Do not find CJK sentence ends with a regex** — there is no reliable way to tell a sentence-final ending from a particle or an ordinary word ending with the same character, so the pattern catches mid-sentence words too. Where there are only a handful of sentences, **list them explicitly instead.** Losing the sentence-boundary newlines runs the sentences together on one line and hides where they break — do not throw the existing newlines away wholesale when changing the width

36. **Do not let an archetype's slot count truncate the item count** — pick a 4-column layout and the fifth item onward disappears quietly. When the source covers 7 and the slide shows 4, it also contradicts the "7 sites" figure stated on an earlier slide. **Splitting the slide comes first** (4+3, in the source's order); cutting items is the user's decision. Where something must come out, say what came out and why. The check: compare the item count from the source against the slot count on the slide — and against figures written in the title and on earlier slides

37. **Work out first whether it is the assets or the layout** — before assuming "there were only four photographs", count the asset folder. On one occasion `store1~7` were all present and three were dropped purely because a 4-column layout had been chosen. It goes asset count → archetype, not archetype → item count (the reverse direction of pitfall 21)

38. **Where the source is a document, compare one-to-one against its contents** — slide by slide everything can look right while the order is tangled. Skipping a parent section and coming back to it (3-6 after 3-7 and 3-8; back to chapter 3 after chapter 4's discussion) loses the reader. **Pull the source's table of contents, write the deck's slide numbers beside it as a table, and look for reversals and omissions.** For a section in the source and not in the deck, distinguish "left out" from "missed" — where another slide already covers it, say so

39. **Greedy wrapping leaves the last word orphaned** — filling each line to the brim drops a single word onto the last line. The fix is **a binary search for the narrowest width that preserves the line count.** Refilling at that width divides the line lengths evenly. Detect it two ways — a line holding one word, and a line under 25% of the width. But **a short complete sentence is not an orphan**, so before merging, check whether the previous line ends in a full stop and decide which side to merge with

40. **Shoot the whole deck as one image and crop locally** — screenshotting 30 slides individually is 30 calls. Shooting the `SLIDE_GRID` node once at `maxDimension` 13000–20000 and cropping by coordinate finishes it in one call. **The grid wraps every 20 slides** — slide i sits at `x = 240 + (i%20)*2160`, `y = 240 + floor(i/20)*1320`. Do not guess; measure with `absoluteBoundingBox` and confirm the formula

41. **Opacity values and accent colours multiply quietly across sessions** — each round of edits mixes 0.5, 0.6, and 0.7, and Green, Teal, Blue, and Yellow accumulate. The eye does not catch it, so **count them exhaustively and look at how many kinds there are.** Secondary text keeps one value (0.7); accent colours keep only those with meaning attached

42. **One colour must not carry two meanings in a deck** — where Yellow means "review requested" on a status chip and "fault" on a diagram label elsewhere, the reader tries to connect them. **Do not use colour for classification** — rows and columns already separate those. Colour belongs to axes with settled values, like status, and never leaves the mapping written in the spec

43. **A card shrunk to its content goes in the vertical centre of the band** — an archetype's card height presupposes filling from the label's top to the key statement's bottom. Put a paragraph in and shrink the card and it stays pinned to the top with a large gap below. Centring it in the band splits the margin above and below. Keep cards in a row at equal height, matched to the tallest, but put that difference exceeding 100px into the checks

44. **After deleting slides, `getSlideGrid()` keeps returning dead nodes** — calling it again inside the same script leaves the deleted nodes in the array, and it throws on a single `s.name`. The next call comes back stale too. **Take a copy of the slide array before deleting and handle the aftermath from that copy.** Later reads walk up from one surviving node through its parents to the `SLIDE_ROW` and read `children` rather than using the grid. Where slides are named by number, do not forget to renumber the ones behind a deletion

45. **Do not mechanically give one slide to one section of the source** — one-to-one by section is convenient for keeping the order but erases the differences in volume. A section with four sub-items and a section with four sentences getting the same single slide inverts the density. Choose the archetype by item count on top of that (four figures, so a 2×2 metrics slide) and the thinnest section ends up with the largest type in the deck. **Count the slides using the deck's largest type and ask whether that is what belongs there.** And before cutting a slide, count how many more times the same material appears in the deck — appearing twice already means cutting leaves no hole. Whether to cut it from the source too is a separate question: a section there may be tied to a research question, a summary table, or a follow-up item, so find every tie exhaustively before deciding

46. **Settle the register of the body copy first** — where the source is academic or report prose, the sentences get carried over as they are, and on a presentation screen that reads as long-winded. Body copy defaults to the compressed register the language offers (in Korean, nominal endings). **But apply it in layers** — titles and leads stay as present-tense assertions (turning "the bar disagrees with reality" into "disagreement" costs the title its force). Direct quotations stay verbatim, and lists, labels, and table cells already in that register are left alone. When changing register, **swap the endings only and leave hand-placed newlines alone** — the compressed form is the same length or shorter, so the line count and height do not change and no rebreaking or re-verification is needed. Check afterwards that the line count and height are unchanged

47. **A slide child's x/y is relative to its parent, not to the slide** — adding the slide's absolute coordinate to a value read from `absoluteBoundingBox` pushes the node over by the slide's width. Read as `b.x - slide.absoluteBoundingBox.x`, and write that relative value into `node.x` **as it is**. And **do not trust `clone()` to land in the same parent as the original** — a node cloned inside a slide has been known to attach to the slide next door. After cloning, pin membership with `slide.appendChild(clone)`, and only then set the coordinates (the same order as pitfall 4). After placement, check `parent.id` and the slide's child count together

## Related

- No template assets, or stale ones → `/fig:deck-setup`
- Design values and the archetype catalog are in `template-spec.md` in `deck.assets_dir`, the builders in `template.js`, the generic helpers in `${CLAUDE_PLUGIN_ROOT}/_common/scripts/deck-base.js`
- Where a recurring deck needs its own data collection, finish that collection upstream and hand it to this skill as the source
