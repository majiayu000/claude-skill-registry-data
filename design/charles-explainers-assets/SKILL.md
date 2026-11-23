---
name: charles-explainers-assets
description: Build the visual that teaches what I'm saying in a reel - the real thing doing what I describe, a before/after flip or a side-by-side, a mark that shows what changes (a guide, a hatched band, corner brackets, a before|after sweep), a definition tab above the demo, a coloured agent cursor that makes the change on my word or moves the part itself, the CSS or another short caption under it, red marks on a real screenshot - sized for the slot charles-claude-editing gives, timed to my words, and simple enough to read in the 1-5 s a phone viewer gets. Use whenever a video explains a term, a fix, a technique, a number or a mechanism (my list reels, "10 niche ___ hacks", Day N of Removing AI Slop, reverse-engineering explainers), when charles-claude-editing asks for an explainer asset at a size, or when I say a teaching visual is too busy, too fast, too small, stale, hard to read, not engaging, or that it's hard to see what changed.
---

# Goal

Every line I explain gets one visual that a muted viewer understands in the time it's up: the real thing, doing the thing, changing on my word.

**Rich across time, simple within a frame.** Engagement comes from something new happening about every second: a pointer moving in, a state flipping on my word, the fix proving itself, the next asset. Overwhelm comes from things at once. So each frame has one subject and one change, everything else waits its turn or gets cut, and nothing on screen ever sits frozen.

Why: each visual is up for 1-5 s in a card 270-390 pt wide on a phone, next to my face, the list and the captions. My notes have pushed both ways, and the split is space versus time. "Graphics are too busy" (the animation hacks) and "the texts go by too fast" (a comment on design terms) were too much at once. "The video isn't as engaging as I'd like it to be" (unslop repos), "The other deals are too boring when you show them" (Black Friday) and "Stale assets in the screen for too long … should be avoided" (my note on this skill) were too little happening over time. And practice what I teach: my audience learned Hick's law, ease-out and the AI tells from me, so they notice when a visual breaks them.

# The contract

charles-claude-editing usually calls you after picking the layout. You get:
- **The lines:** what I say, the list term, the change word (the word the fix lands on), and word times once the take is cut. Before it's filmed, estimate 4.7 spoken words a second. Count code and numbers as said aloud (100vh is 4 words, 0.95 is 3, 150 is "one fifty", 2), and add 0.2 s at each full stop or question mark. If no change word was given, take the word that names what changes or its cause, and note it.
- **The slot:** its design size, the band the viewer actually sees, the area text must stay inside, and where captions sit. `references/slots.md` has the ones in use.
- **The format:** list reel, hack reel, Day N levels or talking explainer.

You return:
- **One clip per asset** at the slot's design size, rendered at 2× and 60 fps, with no audio. Every line I explain gets at least one asset, and a long line gets more (One asset per item, below).
  - A flip (a before, then an after) is 9.0 s with the change at exactly 4.50 s, the before looping from the start and the after looping to the end. The editor slides it until the change lands on my word and can show any window of it. When my line's before runs past 4.3 s, the hack-reel editor slows the clip's first second to fill the gap, so keep anything whose timing is the lesson out of that second (the push-in and the scene settling are fine).
  - Anything else is the demo's own run from its opening pose, looping where its form loops, with its main move's time in `explain.json` for the editor to retime.
- **`explain.json`:** per line, the takeaway and the change word and time; per asset, its form and a one-line reason, its in and out times, every word shown with its in and out times, and the cursor's actions; and click cues on the clearest changes. That's about four in 45 s at most and never two lines in a row, inside charles-claude-editing's six a minute.
- **`check/phone.png`:** the phone check (below), from `kit/check.mjs`.

Whoever draws the card owns it. In the hack-reel card, the list kit draws the card, its tab and the change from one asset to the next, reading your `explain.json`. Check what the editor draws in any other slot. The UX-principles `assemble.py` only lays clips end to end, so there each clip carries its own card, its tab and, in its first 0.12 s, the fade-through from the previous item's card. In a slot rendered as one span (a Day N card), you draw them too. Never yours: captions, music, sound, the list, title and timer, and where the slot sits. Never burn my spoken words into a clip.

# Workflow

1. **Beat sheet first.** Before building anything, write into `explain.json` for every line: the takeaway in 8 words or fewer, the change word, the subject (the real thing the line is about), and the form of each asset in order. Why: the visual is decided here. A line without a written takeaway gets decoration instead of an explanation.
2. **Pick the form** with the tree below, and give long lines their extra assets. For every flip, pick its mark too (Mark the change).
3. **Fit the frame budget** below.
4. **Build** with the kit (`references/kit.md`): the form from `references/forms.md`, the cursor from `references/agent-cursor.md` and every word on screen from `references/text.md`. Copy the closest gold example named there, or `kit/example/`, and change it; never start from a blank page.
5. **Time it** to my words (Timing, below).
6. **Run the phone check** (`kit/check.mjs` makes the sheet). Fix the largest fault first, re-render, check again.
7. **Hand over** the clips, `explain.json` and the sheet.

# Pick the form

A Day N levels reel skips the tree: every line is a level of the one live demo (`references/forms.md`, Levels). Otherwise walk the tree from the top and take the first branch that fits.

```
What is the line doing?
├── Giving a fix ("Use X", "X looks sloppy, do Y")
│   ├── My line has no problem half (fix-first) → AFTER ONLY: the fix in action, tagged After
│   ├── The flaw shows in a still frame (radius, contrast, alignment, spacing, copy)
│   │   └── FLIP IN PLACE: one crop, the flaw, then the fix on the change word
│   └── The flaw is motion or timing (duration, easing, stagger, jank, spring)
│       ├── The versions differ only in feel (the same duration on another curve, a spring
│       │   against a tween, durations under 2× apart), on a simple element whose moving
│       │   part stays 40 px or bigger at half width, in a slot that doesn't tag its clips
│       │   Before/After (the hack-reel card does)
│       │   └── SIDE BY SIDE: both start on the same frame, labelled only with their values
│       └── Otherwise (600 ms against 200 ms, a pop out of nothing) → FLIP IN PLACE
├── Naming a principle or a law: a rule that one way works better than another
│   ("Anticipation wind-up", "Hick's law", "Snappy timing", "Frequency of use")
│   ├── The slot tags its clips Before/After and flips the tag (the hack-reel card)
│   │   └── FLIP IN PLACE, the change on the principle's name
│   ├── Its "without" version isn't a mistake anyone makes: it names a way of working,
│   │   not a better result (pose to pose)
│   │   └── DEMO + DEFINITION TAB
│   └── Otherwise → SIDE BY SIDE: the same component without the principle (left, Before)
│       and with it (right, After), running from the same frame, under the definition tab
├── Naming a term the viewer may not know: what a thing is called ("Kerning", "OKLCH", "Tabular numbers")
│   └── DEMO + DEFINITION TAB: one move that shows the term, with no Before/After; the tab
│       says what it means. A word most of my viewers already know gets the move alone
├── Claiming something about real products or AI output ("AI loves eyebrows", "Tinder adds noise")
│   └── THE REAL THING: a screenshot, a recording or the code itself, with the claim marked in red.
│       A reveal shows the effect first and the evidence on the word that names the cause
├── Stating a number or a relationship that no code on screen carries ("respond within 400ms")
│   └── MEASURE: a redline or a timeline on the subject, with the numbers
├── Explaining a mechanism ("the request reaches the server after")
│   └── CAUSE → EFFECT: the agent cursor or the trigger acts, the result lands, nothing else moves
├── Showing off a tool or effect rather than teaching it
│   └── SHOWCASE: its strongest real examples, 3-8 cuts of 0.5-1.5 s each
└── A joke, opinion, transition or call to action
    └── NONE: hand back "no explainer"; the editor decides what, if anything, replaces the card
```

Why the main branches:
- **A fix comes first.** Most of my lines are fixes, and a fix that names a term ("use tabular nums") is still taught by showing the fix.
- **A principle is taught by its contrast.** Shown alone, a wind-up is just a card moving. Next to the same card without one, the wind-up is the only thing that differs, so the eye goes straight to it. A list item's 1-2 s leaves no time for a before, a change and an after, and a flip would ask the viewer to remember a before they barely saw. My note on the UX-principles mock, whose cards were all single demos: "it would've been better to have the before/after side by side for many of them to better understand the principle". A principle that names a way of working (pose to pose) has no wrong version to show, so it gets one demo.
- **A flip for a fix.** A fix lands on my word, so the change itself is the event, and the subject stays full size. In the hack-reel card the frame's own Before/After tag flips with it, and a pair under one tag would be mislabelled.
- **For a fix, side by side only when the difference is in the feel.** A big difference shows in a flip. Two curves at the same duration don't, because nobody can compare them from memory.
- **One move for a term.** The line says what a thing is called, so there's no wrong version to compare with, and a Before/After would add a second state to decode in about a second.
- **The real thing.** My most-watched list reel marked pages that models really built, none drawn for the video. Real beats a recreation. A reveal runs the other way from a fix: the strange effect is the question, so it comes first.
- **A measure only when no code carries the numbers.** When a fix has code, the code already shows the values, and a redline on top is a second label.
- **None is an answer.** A visual on a joke steals the punchline, and an asset added for its own sake is clutter.

# One asset per item, more for long lines

Every item in a list gets its own asset, with its own tab if it's a term: never one asset shared between items, never a skipped item. An asset stays up 3 s at most, or 6 s for a flip, whose change is a new beat halfway and whose code is there to be read: charles-claude-editing's 3 s rule, with its exception for code. When my line runs longer, cut to another asset at the start of a clause, never mid-word, and take the first branch that fits. Don't cut for less than 1.2 s: the asset runs up to 1.2 s past its cap instead, because a new asset takes about a second to find. When the change sits late in my line, the extra asset may come first, as long as the flip's change stays on its word.

```
What does the rest of my line do?
├── Keeps describing one detail of the demo → the same demo, cropped in on that detail
├── Names where it's used ("every iOS sheet does this") → a real product doing it
├── Warns about a near-miss ("not tracking, kerning") → the near-miss, flipping to the right one
├── Says how to build it → the code alone, filling the card, its token changing on the word
└── Otherwise → the same idea on a second subject (a card after a button)
```

An item's tab stays up across its assets. A Day N level stays one asset however long it runs: its next beat is the next tag or cursor action in the same live demo.

Why: I asked for one asset per item, and more for a long one, to keep it engaging. One loop playing for 8 s is a stale asset, and each new asset gives the viewer a new reason to keep watching.

# The frame budget

Hick's law: the more there is to look at, the longer it takes to find the point, and the viewer has 1-5 s. Per frame of a clip:

| Element | At most |
|---|---|
| Subject: the component, screenshot or diagram. It and its code fill the card, with no empty band wider than 10% of the card's width or height. Lay it out for the after: before the fix, the room its added code lines will take doesn't count. A term card is cropped to its content, so it has none. A side by side's two panels are one subject: the same component twice, identical except for what the principle or fix changes. The room a well keeps for its component's own move (a hop, a menu opening) counts as filled | 1 |
| Glance text, read during playback: a definition tab, Before/After, a principle tag, a measurement, or a side-by-side's pair of values. In a principle's side by side the tab is the glance text, and the Before and After over its panels are chrome: the same two words in the same two places on every card, read once and then known by position | 1 |
| Pause text, for people who pause or screenshot: a code block or a property, 4 lines at most. A side by side's property under each panel is one pause text | 1 |
| Pointer: the agent cursor with its label, a plain pointer or a fingertip. More only when my line is about more than one agent (`references/agent-cursor.md`), or in a side by side whose lesson is the pointing or the input (`references/forms.md`), which gets one per panel, moving together. A keycap that presses is a pointer | 1, or one per agent up to 4 |
| Events at a time. On the word, the code changing and the tag flipping are one event, the fix; the component shows it after (Timing, below). A side by side's panels running the same trigger together are one event. The one exception is agents working at once when that's my line's point (`references/agent-cursor.md`) | 1 |
| Kinds of mark: a flip's change mark (Mark the change, below) or the red marks on a real thing, with up to 6 of that kind | 1 |

Everything else is cut: badges, meters, graphs, onion skins and traces (unless they're the lesson: the key poses in pose to pose, the path in moving in arcs, the spacing in slow in and slow out, the tappable area in a hit area), lenses, speed tags, counters, verdict labels, titles, and devtools overlays such as paint flashing. A flip's change mark isn't one of these: it covers only the part that changes, and only around the change. Why: those were in my animation-hack clips when I said "Graphics are too busy -> make them MUCH more simple. Viewers only see the screen for a brief time so make it simple (just the before/after component + the css)".

# Make it worth watching

Simple within a frame doesn't mean plain. A card is worth watching when its subject is real and in colour, its flaw happens for a reason and costs something, and the change is the best-made moment in the clip. It never gets there through moves laid on top: a camera that punches in, a wipe across the card, a cursor running to the code on every line.

Why: two notes on the cards for design hacks part 2, both on 22 Nov 2026. The first build was a small grey component in the middle of a big grey card, with a fix that happened by itself: "The explainer assets are way too boring. Look at how the original video did it and make it much more engaging like that ... Include zoom ins/colours/agent cursors". The second had a real app in colour on every card. It also had a camera that punched in and pulled back on eight of ten, the agent editing the code on all ten, two wipes, and brackets that flipped from red to green: "make the transitions even better. It feels tacky at times I'm ngl ... make the graphics more visually interesting". A frame-by-frame critique of that build named the camera first, then the wipes, the brackets and the cursor resting on the code it changed. The third build kept the colour and the cost and dropped the rest (that video's `explainers/DESIGN-LOG.md` has the critique).

- **Real colour.** The subject is a product with its own colour in it: album art, product photos, a brand panel, a hero image, a dark browser with colourful tabs. The UI keeps its one accent and the content brings the rest. A white or grey component on the grey ground is a wireframe, not a card. When I want cards that look like a studio made them, charles-studio-explainers adds a colour world, photographed objects and an idea per card on this same contract.
- **Fill the band.** The subject spans the band's width (the frame budget's 10% rule), drawn at the size where its copy reads at 20 px or more.
- **The flaw is an event with a cause.** A plain arrow on desktop UI, or a fingertip on touch UI, uses the product, and the flaw follows from that: a double click prints two receipts, a tap lands beside the x, a refresh flashes white. After the fix the same action runs again and goes right. The kit's `route()` takes the pointer's stops, and its `ring()` opens a ring on every click and tap, so a double click or a tap that missed is seen.
- **One thing uses it.** One pointer, one device, one object per card. Why: a card with a laptop window, a mouse and a phone, for a line about hover on phones, was "the busiest card with the smallest change" to both critics, and its buttons were 14 pt. One tall phone with rows twice the size said it better. A touch that has to miss is drawn as its contact patch (about 25 pt), small enough not to overlap the target it misses: a fingertip-sized disc over the target's corner read as a tap on a dead button.
- **Show the cost.** When the flaw costs the user something, make it happen on screen: the click that lands on a photo because the page jumped, a second charge, a toast that drops as the pointer reaches Undo. A cost is what makes a viewer care about the fix.
- **The change is the event.** From 0.3 s before the change word to 0.5 s after it, only the fix moves: no pointer is travelling (unless it's carrying the change), the camera is still and no mark is drawing in.
  - A state blends in place (0.12-0.45 s), or the same element travels to its new place and size.
  - Nothing wipes across the card.
  - Nothing appears or vanishes in one frame, unless the flaw itself is a pop (a flash of the wrong theme, a layout shift).
  - Two layouts never cross-fade over each other: the old words go before the new ones come.
  - Something in the UI changes within 0.4 s of the word, not only the code.
  - The payoff is that change. What a viewer would point at happens on the word, not a second after it: the duplicate receipt goes back in, the box opens, the white page turns dark, the sinking toast stops. A button greying, an outline appearing or a thin bar stopping is a label for the fix, not its payoff. If the payoff needs a state that isn't there yet (a page still loading, a toast still up), stage the before so that state is on screen when the word lands.
  - Nothing goes back on the word: no page loading its first state again, no field cleared and typed again, no parts pulled back to where they started. Reset the scene at least 0.3 s before the word, and let the fix carry on from where the flaw left things.

  Why: on the second build, five things moved in the half second around the change on one card, and on three others nothing but the code and a bracket changed at all. On the third, the first critics' most wrong note was "on the change word the scene rewinds, or only the code moves": receipts slid back, a field cleared and was typed again, and a blind reader took that as the fix deleting what was typed. The second critics found the fix on the word but its payoff 0.9 to 1.35 s later on six cards of ten: "the word is a subtraction or a label".
- **The camera holds.** One slow push runs under the whole clip (Timing, Never stale) and nothing else moves the frame. Zoom only when the lesson is under 4 px in the final frame (Look, Magnify), and then once: the move settles 0.3 s before the change, never reverses, runs on `E.travel`, and frames the subject so that nothing is cut by the card's edge or the code block at either end. Why: the second build's zooms ran on the ease-in-out, which covers 63% of its distance in the middle fifth of its time. The critique called that "the hard zoom cut he already dislikes, with soft shoulders", and each zoom pushed part of the subject under the code block or past the edge.
- **Pointers move like a hand.** A pointer's glide, a carried part and a page scrolling run on `E.travel` (the minimum-jerk curve, 36% of the distance in the middle fifth), 0.25-0.45 s across the card. Never `E.inOut` over that distance: it sits, snaps and sits.
- **The agent comes only where it changes the design itself:** it drags a hit area out, carries a part or retypes a label (Mark the change). When a plain pointer is already using the product, the code changes by itself on the word (`references/agent-cursor.md`, When it appears). Why: with one agent doing both jobs on the second build, it made up to five trips in 3.5 s between the product and the code, and it sat on the code as it changed.
- **Start at rest.** The editor cuts a flip in mid-loop, at the change minus my line's lead-in (`win.b` in `explain.json`). At that time the scene is in a clean pose with nothing in mid-move, and its first action starts 0.2-0.4 s later. The lead-in is an estimate until I've filmed, so hold that pose from 0.3 s before the cut-in time. Why: a hard cut onto a toast half-way down or a page in mid-scroll reads as a glitch, and the viewer needs a moment to find the subject.

Gold: part 1's contact sheet (`videos/design-hacks/design/assets/contact-sheet.jpg`) for colour and fill, and `videos/design-hacks/design-part-2/explainers/` (`scenes/src/`) for the event, the cost and the change, card by card.

# Timing

- **The fix starts on the change word.** The code (or the control) changes within one frame of the word's first sound. The component shows it at once if it's a state, or on its next run, within 1.0 s, if it's a motion. When the agent has to move to run that proof (a hover, a second click), it leaves when its hold ends at T + 0.5 s, and the proof starts as it arrives. Why: my voice tells the viewer when to look. Early reads as a glitch and late as lag, and the cause comes before the effect.
- **Text enters 0.2-0.45 s before the word it explains** and stays for the line. In a list, where the term opens the line, it enters on the line's cut. Why: it needs a head start to be read while I say it.
- **The flaw happens on screen by 0.6 s into the line,** through its natural trigger (a pointer, a finger, time) or one camera push. Never a still before. Why: my voice is naming a problem, and a still picture makes the line feel dead.
- **The after runs at least 1.0 s at reel speed** and includes a proof beat: the same interaction again, now working. If my line leaves less, ask the editor for a hang of up to 0.5 s. Why: I allow "a little hang if waiting for an animation to finish/digest", never a clipped word.
- **Short items** (a line under 2 s, as in a 20-item list, and every other item of a list whose lines are mostly under 2 s, so they all behave alike): the main move starts within 0.15 s of the cut and is done by 0.6 s, then the end pose holds to the next cut under the slow push-in (Never stale, below). A flip in a short item changes on its word instead and is done 0.45 s after it (a sweep 0.55 s). No loop and no proof beat. The agent cursor comes only when its action is the change itself, arriving in the before (`references/agent-cursor.md`, When it appears). Why: there's no time for a proof, and a replay mid-item reads as a glitch, but a pointer carrying the part on the word is the transition itself.
- **A short side by side** starts both panels on the same frame; the after's move is done by 0.6 s, and the before plays its flaw at real speed, even if that runs past the cut (a 2 s spinner). Its end pose still shows the difference: the trace of what differed when that's a path or a spacing (the arc's dotted path, a tick for each frame), or the state that differs (the before's spinner still turning). When the two would end alike (squash and stretch, anticipation, secondary action) and the line runs 1.45 s or more, run the pair again on a new item (the next card, another icon), starting within 0.25 s of the first run's end and done 0.25 s before the next line. A new item is a new event, not a replay. Why: the comparison is the lesson, and two identical panels show none. In the UX-principles rebuild (13 Nov), six motion principles held identical panels for up to 1.4 s, and both fresh reads called it the weakest part.
- **Every main move finishes 0.25 s before the next line starts.**
- **Demos play at real speed and loop about once a second,** holding the start pose 0.25 s and the end pose 0.4 s each cycle, so a 200 ms move is seen four or five times in a line. Never slow a demo whose lesson is timing or feel. Why: slowed down, a 200 ms dropdown looks like the sluggish one it's meant to beat, and press feedback looks laggy. The one exception is a line about the shape of a path (moving in arcs, squash and stretch), which may run at 0.5× with both versions at the same speed.
- **Never stale.** Something in the asset is always moving: the demo, the cursor, a transition or, when nothing else is, a slow push-in on the whole subject (linear, running from the cut so it never visibly starts: 2% a second on an asset that's up for a second or two, 0.6% a second on one that's up for more than 3 s, so the whole push stays under 4% and the subject's edges never reach the card's). Nothing sits frozen for more than 0.6 s. And no more than 1.5 s passes between one new thing ending and the next starting: the flaw, the cursor arriving or acting, the change, the proof beat, a punch-in on a detail, the next asset. A loop's repeat is motion, not something new, and so is the same action giving the same result again (a third click opening the same answer the same way). An action is new when its result differs: the first one after the fix, another item, a punch-in. Why: I don't want stale assets on screen, and a frozen picture under my voice reads as dead air.
- **Between assets in one card,** whether they belong to two lines or to one long line, the same object at a new state morphs into it (shared parts glide and resize). A new subject fades through: the old one goes in a frame, the card reshapes, and the new one comes in from 97.5% scale. Never a cross-dissolve. Why: on the Day N reels I had the dissolves between levels replaced with transitions, and a dissolve's double exposure is unreadable at phone size.

# Mark the change

A flip in place shows the before and then the after in the same spot, so nothing on screen compares them. Every flip whose difference is a still property (a colour, a size, a gap, a word, an alignment) marks the part that changes: red on the flaw in the before, then moving with the fix on my word as it turns green. A flip whose flaw is something the viewer watches happen needs no mark (the tree's first branch). Why: my note of 16 Nov on the 20 practical design tips cards: "There should also be better visual indicators showing the difference between before and after if we're not doing the two column layout (especially in the transitions between the before/after to make it more clear)". Without a mark, anyone looking at the wrong part sees nothing change. The first blind read of those cards missed the gray tint, the toast padding, the text tint and the stat gap.

Walk the tree from the top and take the first branch that fits.

```
What does my line say changes?
├── What happens when someone uses it (a second charge, a toast that leaves, a page that
│   jumps, a key that does nothing)
│   └── NO MARK: the event is the mark. The pointer or the finger that causes it shows where
│       to look, a ring opens on each click or tap, and after the fix the same action goes right
├── How parts line up (left, right, the baseline, digits lining up)
│   └── A GUIDE along each part's edge where it sits now, a zigzag or a step, that
│       straightens into one line as the parts land on it
├── How much space (padding, a gap, space above or below, line height, half the height)
│   ├── Space inside a filled part (a button's or a toast's padding) → a DIMENSION LINE
│   │   beside the part, outside it, shrinking or growing with the value
│   └── Otherwise → a BAND hatched over exactly that space, growing or shrinking with it
├── Where a part that's already there goes (away, apart, to the side, swapping places)
│   └── THE AGENT grabs it and carries it there on the word, its selection round it. In a swap
│       it carries one part, and the other glides into the place it left
├── How big one part is, or its shape (go bigger, a tighter radius, a bigger hit area)
│   └── THE AGENT selects it and drags its corner handle (or its radius handle) on the word.
│       A part you can't see, like a hit area, shows as its selection box
├── What a part says (a button's label, a link's words)
│   ├── In one label (a word or a phrase) → THE AGENT selects it in its colour (a double-click
│   │   for a word, a drag for a phrase); the new words land in the selection, which resizes
│   │   to them and turns green
│   └── The same fix in several labels (every Title Case label on a page) → a box on each
│       wrong letter or word, shrinking onto its replacement
├── A colour across the whole subject (every gray in the app, every brand colour)
│   └── A SWEEP: build the subject twice and wipe the after across the before, left to right,
│       behind a line with a grip (grey while it waits, green once it moves), so for half a second both sit side by side at its edge.
│       The agent carries the grip, unless a card next to it already has the agent
├── A colour, a fill, a stroke or a shadow on some parts (a series in a chart, the text on a
│   banner, icon strokes)
│   └── CORNER BRACKETS 6-8 px outside each part (round the shadow's reach, for a shadow), or
│       a ring round something small and round. A new colour on text or a surface sweeps
│       through it left to right; a shadow or a swatch changes in place. A stroke too thin to
│       see changing gets magnified first (Look)
├── Which parts stand out (everything bold, two primary buttons side by side)
│   └── CORNER BRACKETS round the parts that lose their emphasis, turning green as they do
└── Something new appears (an empty state's next step, a missing label)
    └── CORNER BRACKETS round the old part, or round the empty place where the new one goes,
        growing round the new part ahead of it
```

Why an event gets no mark: on design hacks part 2's second build, brackets round an event drew in while the pointer was still travelling and flipped to green a few frames after the fix. The critique counted them among what read as tacky, and on three cards they were the only thing that changed on the word.

Why the agent moves parts itself: a part moving under a pointer shows the cause with the effect, the way a designer moves a layer in Figma, and I asked for "fake agent cursors that move components around" (16 Nov). A position, a size and a word all have something on screen to take hold of. A space, an edge or a colour doesn't, so a mark shows it instead.

The timeline, with the change at T (`markLife` in the kit):
- **It's on by T − 0.95, in red.** It draws in from T − 1.25, so a before shown for less than 0.95 s opens with it already there. An agent enters in the before on its own timeline (`references/agent-cursor.md`). Why: the editor slides the clip until its change lands on my word and can cut in anywhere in the before, and the mark can't wait for a cut it can't know.
- **It moves on the word, never before it,** on the fix's own curve, and turns green as the fix lands, between 45% and 65% of its progress (`markTurn`): the guide straightens as the lines land, the band shrinks with the padding, the brackets grow ahead of the new part. Why: its motion is the transition the eye follows, so it has to be the fix itself. Green that arrives first marks the unfixed design as right, and a slow blend sits in the muddy grey halfway between red and green.
- **It holds green until T + 1.0 and is gone by T + 1.25,** so the after ends clean. An agent lets go when its part lands and fades 0.2 s later.

Rules for every mark:
- **One per flip:** one kind, up to 6 of it (the frame budget). When the fix changes more than my line names (a swap moves two parts), mark what my line names and let the rest move unmarked. An agent's action is its flip's mark, so it gets no other.
- **It never covers what it marks.** A guide runs beside the edge, a band fills only empty space, brackets sit 6-8 px clear, and nothing tints what it encloses. Why: the viewer has to see the part change, not the mark.
- **It never looks like the UI.** Use corner brackets, not a full or dashed box, which reads as a drop zone, an empty state or a border. Never put a red ring round a field: it reads as a validation error. Never tint a part's own fill: red ends on a toast read as an error toast, and hatching on a black button reads as its colour. Why: in the 16 Nov blind read, every mark that looked like UI was read as UI.
- **It ends on what changed,** never on what stayed the same. Why: a first build of "keep body text regular" ended with green on the title, which didn't change, and nothing on the body, which did.
- **The change has to be visible before it's marked.** Within what's true, push the values to where the change shows at phone size: a gray tint of 3 to 7 levels a channel showed nothing even under a sweep, so use the visible end of the range. Show one subject magnified rather than two small ones. Then measure a pixel of the changing part in the before and after stills. Why: a stacking bug once left the one part that should change pixel-identical, and only a measurement caught it.
- **Red only on the flaw, green only on the fix** (the kit's `MARK`), with lines 2.5-3 px wide in the final frame. On a dark surface use the light pair (`dark: true`), where the dark pair vanishes. A sweep waits in grey and turns green once it moves. An agent's selection keeps the agent's colour; only new words or a new value land green.
- **It lives in the subject's box,** so it rides the zoom and the push-in. The agent and its selection live on the panel.
- **No words, numbers or arrows on it.** The code under the subject already carries the values, and the mark's motion does the pointing.

Gold: `videos/practical-design-tips/explainers/` (`scenes/tips.js`): every branch of the tree across its 20 cards.

# Words on screen

Every word on screen adds something I don't say: what a term means, the value that changed, the principle's name, the code to copy. Never my own words back (a "Layered shadows" tag over "layer the shadows" teaches nothing), and never a sentence.

- **Reading time:** aim for 15 characters per second the text is fully on screen (from fully in to the start of its fade-out), and never go over 20. A 1.2 s list item has about 1.1 s with its text fully in, so it gets 16 characters, 22 at most. Why: subtitles cap adults at about 17-20 characters a second with nothing else to watch, and here the viewer also watches the demo. My design-terms definitions ran at a median 30 a second, 17 of the 20 over 20, and the comment was "the texts go by too fast".
- **Every term keeps its tab.** Cut the definition to the shortest true gloss that fits. If nothing true fits, ask the editor to give that item more time rather than drop the tab. If the cut is fixed, use the shortest true gloss and flag its rate in `explain.json`. Give the editor the full definition for the post caption, where I already list them.
- **Sizes, in the final 1080×1920 frame** after the slot's scale: 26 px for anything the viewer must read, 30 px bold for tabs and tags, 40 px for a number that stands alone. Code is the one exception at 24 px, because its changing token is highlighted and the rest is for people who pause; that's the size I approved in the hack reels. Text that can't reach its size is dropped, not shrunk. A component's own copy is must-read when the lesson is in it (the value that changes, the error, the grouped digits); the rest is part of the picture and can go down to 20 px, the dialog copy in my approved motion-hack clips. Why: the reel is about 390 pt wide on a phone, so 26 px is about 9 pt.
- **Contrast:** 4.5:1 or more against whatever is directly behind the text, on its worst frame. Text dimmed on purpose as the lesson (the plans staging pushes back) is exempt; text the viewer must read never is. Why: "Sorry the text contrast is bad" was the first line of my UX-principles caption.

`references/text.md` has the definition tab, the code block, tags and the other captions.

# Look

- **The real thing:** a real-looking component from a real kind of product (a checkout, a settings page, a chat), with real copy, drawn at its real CSS size and magnified as a whole. Never grey bars or a wireframe. If a real screenshot exists (a page an AI built, the app's own UI), use it. Why: real reads faster than abstract, and "use the real thing over a recreation" is my editing rule.
- **The demo runs on the values it teaches:** the real 150 ms ease-out, the real 0.97, exactly the CSS in its code block. Why: my audience copies them, and some check.
- **Performance flaws are reproduced on the render's clock.** Hold frames at the rate the flaw really causes, as the kit's `left` toast does (a new frame every 33-83 ms, about 17 fps). Why: a frame-stepped render never drops a frame, so a captured "before" of jank comes out smooth.
- **Colour:** one calm neutral ground per reel (the hack reels use #e6e9ee), one accent for the UI, red only for the flaw, green only for the fix, and each agent's own colour on its cursor and on what it selects (`references/agent-cursor.md`). The kit's syntax colours inside a code block don't count, and neither does the content's own colour (album art, photos, a brand panel), which every card needs (Make it worth watching). Why: colour carries meaning on the controls and the marks, so any other accent there is noise; the accent rule was never a reason to keep a card grey.
- **None of my own AI tells:** no cream backgrounds, monospace eyebrows or "01/10" labels, pills, badges, gradient backgrounds, glows, emoji or section numbering. Why: I made a reel listing them, and my audience watched it.
- **Same chrome, different subjects:** the card, tab, Before and After labels, code block and cursor look and sit the same for the whole reel. The subjects alternate (type, interface, motion; desktop, phone, close-up) so neighbours never look alike.
- **Magnify, then mark:** when the difference is under 4 px in the final frame, crop tighter or zoom the whole subject first, then mark it (Mark the change). Never a lens or a callout bubble.
- **Render at 2×** and scale down once. Why: the 1080-wide cards' small text looked soft in Photos.

# Phone check

Before handing over, for every clip:
1. **Sheet:** frames at mid-before, 0.1 s before the change, 0.1 s after it and mid-after (for a clip with no change: its opening, the middle of its main move and its end pose), with the tab or state tag drawn on even when the list kit draws it in the reel. Shrink them to the slot's width on a phone: its width in the final frame × 0.36, about 270 pt for the hack-reel card. The flaw shows in the before frame and the fix in the after, and every word on them reads. In a flip, the before frame has its red mark on the part that changes, and the after has it green on the fix (a flip whose flaw is an event has no mark).
2. **Muted glance:** play the line muted at reel speed once and write what changed in one sentence. An agent can't play video, so it reads the line as a grid of frames 0.06 s apart, left to right (`kit/glance.mjs`). If it doesn't match the takeaway in `explain.json`, fix the visual, not the sentence. In a flip, the mark moves with the change and nothing else moves with it. For a fresh read, give the sheet to a subagent that hasn't seen the script and ask what changed.
3. **The change, frame by frame:** for a flip, lay out every frame from 0.2 s before the change to 0.7 s after it, 1/30 s apart (render them with `render.mjs --stills`). Only the fix moves in them: nothing pops in a single frame or wipes, no pointer is still travelling, two layouts never show at once, and nothing has gone back to where it started. Why: on design hacks part 2 everything that read as tacky lived in these frames, and stills and a grid 0.06 s apart showed none of it. A fresh critic that scored "the change itself" on them found a scene that rewound on the word.
4. **Budget and pace:** count each frame against the table, and scrub for any stretch over 0.6 s with nothing moving, or over 1.5 s between one new thing ending and the next starting.
5. **Words:** reading time, sizes and contrast, as above, measured with `kit/words.mjs`. For everything it lists apart (copy under 26 px, dimmed text, text over the footage), say why it passes, or fix it.
6. **Truth:** the code is complete and is what the demo does, the values are the real ones, and nothing claims what I didn't say.
7. **Safe area:** everything the viewer must see is inside the slot's text area and band.
8. **Gold:** put a frame next to the closest gold example. If yours is smaller, emptier, busier or greyer, that's the first fix.

# Faults that come back

- **Too busy** (the animation hacks, first version): graphs, lenses, onion skins, speed badges. Cut to the component and its code.
- **Too boring** (design hacks part 2, first build, 22 Nov): a small grey component floating in a big grey card, and a fix that happened by itself. "Way too boring." Give it a real subject in colour that fills the band, a flaw that a pointer or a finger causes, and what that flaw costs (Make it worth watching).
- **Tacky** (design hacks part 2, second build, 22 Nov): a camera that punched in and pulled back on every card, a wipe across the card, brackets that flipped colour a few frames after the fix, and the agent and its chip sitting on the code as it changed. "It feels tacky at times." Hold the camera, let the fix be the only thing that moves on the word, blend in place or travel, and keep the agent for changes it makes to the design itself.
- **A still before** (the first design-hacks reel): the voice names the problem while the picture waits. Make the flaw happen.
- **A principle on its own** (the UX-principles mock, 13 Nov): every card a single demo, so a wind-up read as a card moving. Put it next to the same component without it.
- **Twin end poses** (the UX-principles rebuild): a side by side of a motion principle whose panels end alike and hold for a second. Keep the trace of the difference, or run the pair again on a new item.
- **Small grey halves** (the animation-rules reel): grey stand-ins in small panels, with labels too small to read. Fill each panel with the real component in colour, as big as the panel allows, and label it at 30 px.
- **Text too fast** (design terms): a median 30 characters a second. Cut it to the shortest true gloss, and put the full definition in the post caption.
- **Code too small or partial** (the typography hacks): a one-line chip, about 22 px in the reel, with half the recipe. Show the full recipe at 24 px or more in the final frame.
- **Low contrast** (UX principles): white text over a white wall. Give it a backing, or move it and measure again.
- **Repeating me:** a tag that says what I'm saying. Name the principle instead, or show nothing.
- **A spare pointer, or a pointer over the change.** One pointer per agent in my line, aimed off the text it changes.
- **Stale** (my note on this skill): a still, or one loop, held through a long line. Cut to a new asset at least every 3 s, and keep something moving.
- **A dissolve between levels.** Morph the shared parts.
- **An unmarked flip** (20 practical design tips, 16 Nov): a gray tint, a toast's padding, a text tint and a stat's gap flipped in place with nothing on them, and the first blind read missed all four. Mark the change.
- **A mark that looks like UI** (the same cards, first marked build): a red ring round a typed email read as "invalid email", hatching on a black button read as its colour, and dashed boxes read as drop zones. Use corner brackets and dimension lines, outside the part.
