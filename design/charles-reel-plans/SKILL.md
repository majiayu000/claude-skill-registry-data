---
name: charles-reel-plans
description: "Plan one of Charles' reels before he films it - from a video idea and a reference (his own reel, someone else's reel, or a post to credit), tear the reference down, write the script in his voice, source the real assets with their licences, write the caption with the credit, pick the music and its start point, write the plan file the edit reads, and publish a shareable plan page (an Artifact): the reel playing as a moving mockup over its music and a blurred stand-in for his footage, with full screen and Safe area and Instagram UI toggles, then the script, the caption options, the assets with their sources and the references the video came from. Use whenever Charles gives a video idea and a reference and wants the script, the assets, the caption, a mockup or a plan before filming (\"make a video like this\", \"plan this reel\", \"script and assets for\", \"mock up this video\", \"do an evolution of ___ like this tweet\"), and to update or republish a plan's page."
---

# Goal

Charles gives you an idea, and usually a reference. You give back everything up to the camera: the script he reads, the caption with its credit, the real assets with their sources, the music, `edit/plan.json` for the session that edits his footage later, and a link to the plan page, where the reel plays as a moving mockup over its music, beside the script, the caption options, the assets and the references. He reads the script, films and sends the footage. The one thing you may ask him for is his own angle on the topic, when charles-scripting-voice needs it (step 5).

Why: he judges a reel on his phone before he films it, often away from this Mac. A localhost page fails him there ("The local host is down so I can't even see the video", 16 Nov 2026), and a mockup without its music doesn't feel like the reel. The edit can only follow his taste if the plan already says, line by line, what's on screen and where.

The worked example is `videos/evolution-of-design/`, a list reel. Its `PROCESS.md` records the run this skill came from, with every decision and pitfall.

# What you make

In `videos/<video>/`, copied from `templates/video/`:

| File | What it holds | Who reads it |
| --- | --- | --- |
| `SCRIPT.md` | What he says and nothing else, in his notes' format (step 5) | Charles, to film |
| `edit/plan.json` | Every line in order with its on-screen text, its asset and where that sits, plus the hook, the music and the caption (`references/plan.md`) | The kit, and the session that edits |
| `assets/<dir>/<group>/` | The real images, with `sources.json` beside them | The kit, the edit and the credits |
| `research/` | `REFERENCE.md` (the teardown), the research notes, `ASSET-BRIEF.md` | You, and the next video in the format |
| `README.md` | The brief, the files, the published link, the caption ready to paste, what's checked | Everyone |
| The published page | The player: the reel over its music, a little short of the window's height, a play bar with full screen at its end, the **Safe area** and **Instagram UI** toggles, and the music under them. Then **Script** (SCRIPT.md as written, each line jumping the reel there), **Caption** (each option with Copy), **Assets** (each asset as the reel shows it, with its source and licence) and **References** (every post, reel and video the plan came from, linked, with what it gave this video). Nothing else goes around the player: no music menu, now-playing line or labels | Charles, on his phone |

Why: what he objected to was the clutter around the player ("too much fluff around the video player section"), not the sections: "Still include the other sections... like the assets and the script and the video caption options", and "Keep the toggle to see the unsafe area too (that was actually useful)". Then, the same day: "put music below the video playback", "make the video playback itself a bit smaller and let me full screen", and an option for the Instagram UI as well as the safe area (16 Nov 2026). Two days later: "include a section for references (tweets, ig/tt videos/etc) that helped create the video" (18 Nov 2026). `kit/page/` builds exactly this, so never add panels, labels or menus to it.

# The edit's rules every plan follows

These come from charles-claude-editing, and that skill wins wherever the two disagree. A plan follows them because the
mockup is only worth judging if it shows the reel the edit will make. `kit/build.py` measures every rule marked ✓ each time
it builds and prints what fails.

- **Safe area (1080×1920):** Instagram's header covers the top 250 px, the username and caption sit below y 1500, and the
  buttons run down the right side from y 840, from x 940 across. Text stays 80 px from both sides and left of x 940 below
  y 840. Footage and pictures may run into these areas, but words and key information never do. ✓ for captions, the hook
  and the list. Why: the app's own UI sits there on every phone.
- **Type:** Helvetica Neue only. Captions are Bold 66 px, white with a thin black outline and a soft shadow, in sentence
  case, at y 1380. A hook title is Bold black text on white, each line in its own rounded box, near the top. A list reel's
  title is Medium 56, its subtitle Regular 40 and its list Bold 30 (the 22 Backgrounds reel's 45 and 36 read small: "this
  text hook should probably be a little bigger", 16 Nov 2026). The list reel's stopwatch (digital-7 mono) is the one
  exception. Why: native-looking type reads as made on his phone, and that organic look is half of what the edit is for.
- **Captions:** 2-3 words a line ✓, no animation. On a split they sit on the seam. When an asset sits at y 1380 they move
  above or below it, never over it ✓. They stay off his face whenever it's on screen and sharp ✓: an asset at 1380 can push
  them up to right under his mouth, never onto it, and a line with nothing there keeps them at 1380 ("make sure the
  captions don't block my face when the full blur isn't on", 23 Nov 2026). Censor words TikTok blocks, like s*****e, in
  captions and the hook ✓. A list reel's list is its captions, so only its sign-off gets word captions.
- **Hook title:** only when he asks for one. Two lines at most ✓ (three only when a CAPS word gets its own), up for his
  first sentence, 3-5 s ✓. When the reel opens on a split, it sits on the seam. It raises the stakes and opens a question the
  reel answers. A label for the topic doesn't do that ("Both of these are 50% lightness" was "boring"). When nothing does,
  leave the hook off, or use "<Topic> for dummies" ("if u can't just don't have a text hook", 16 Nov 2026).
- **Assets:** the real thing, never stock or AI-made, unless AI art is the subject. Sticker-sized so he stays on screen,
  except tweets, recordings and code, which have to be big enough to read. Never over his eyes or the captions, always
  whole, sharp at the size it's drawn ✓, with no black bars, rounded corners, pop-ins or emoji tiles. Web pages in dark
  mode, starting at the visual part. Anchor on pop culture the viewer knows.
- **Behind an asset:** an asset over his face takes everything behind it out of focus, his footage and the reel's own
  title, list, stopwatch and hook, so only the asset and the captions stay sharp: `"backdrop": "blur"` on the visual,
  the editing skill's overlay with blur (`spotlight` has it by default). An asset without one stays off his face ✓. Why:
  with the list still crisp over a face that's gone, "it's not obvious that we're trying to do a full blur background"
  (23 Nov 2026). The page draws each backdrop from one table that mirrors the editing skill's layouts
  (references/plan.md, Backdrops), so when those layouts change, change the table, not a beat.
- **Timing:** charles-claude-editing's Pacing. Never more than 4 s without something new on screen ✓, and no still asset up
  longer than 3 s ✓, counted across every line it stays up for, unless it's a tweet or code he's reading or the payoff he's
  talking about (`long_ok`). A layout that covers his face (`spotlight`, `screen`, a box over it) comes off within ~2 s
  unless he's reading it out, and a long list is proof, not reading: 1-2 s with a fast scroll. Most stills move, so give
  the line a short clip with its push-in, pan or cuts made in, since the page draws a still as it is. Back-to-back assets
  are hard cuts.
- **Music:** a track from `assets/music/<mood>/` ✓: chill, emotional storytelling, funny, motivational, suspenseful, upbeat
  or wholesome. Exposés and serious news always get suspenseful. Skip quiet intros, and keep it 8-9 dB under his voice ✓.
- **Sound effects:** a camera shutter when a screenshot appears, a click on a highlight, a soft whoosh on a big transition,
  each written in its line's `sfx`. At most 6 a minute ✓, and at most one meme sound per video ✓, only on a punchline.
- **Export:** 2160×3840 when anything on screen carries small text (UI, code, a tweet, a screenshot), 1080×1920 for captions
  and a hook only. Write which in the README.

# Steps

Walk all eleven in order. Each ends in a file, so a run that stops halfway can pick up from what's on disk.

## 1. Read the house rules, then set up

- Read `AGENTS.md`, `formats/README.md`, and the playbook of any format the reference matches. Copy `templates/video/` to `videos/<video>/` (lowercase words and hyphens).
- Read charles-claude-editing in full. Why: the plan is the edit's first draft. Its layouts, captions, safe area and music rules all come from that skill, and anything in the plan that breaks one is work the editor has to redo.

## 2. Tear the reference down

```
What is the reference?
├── One of his own reels → find its source in the repo (videos/<...>/edit/*.json and its tools/) and copy the layout
│   numbers from the code: title size and position, list rows, colours, timer, collage zone. Then confirm on the posted reel
├── Someone else's reel → open it in his Chrome (Claude in Chrome). Read the caption and counts from the page text, find
│   the <video>, set its currentTime and screenshot the first frame, the last and one per beat. Time every beat
├── A post, thread, carousel or article → it's the idea, not the structure. Collect every card or image in it (on X, the
│   pbs.twimg.com/media images, returned as media ids only, since the extension refuses output with URL query strings),
│   who made it and how they credit others. The structure then comes from a format (step 3)
└── No reference, only an idea or a source of facts → skip the teardown. The format is the one he names, or "talk" (step
    3). Credit a fact source in the caption only when it's one person's work; a Wikipedia article isn't
```

Write `research/REFERENCE.md`: each beat with its time, its words and what's on screen, the layout numbers, and who to credit and how. Why: numbers from code are exact where eyeballed ones drift, and a teardown on disk outlives the session. Copy a reference's structure, pacing and kind of B-roll, and never its caption style (charles-claude-editing).

List every reference in `edit/plan.json`'s `references` as you find it, not only the one he gave: the post or reel the idea came from, the reel whose structure it borrows, where that format started, and any other tweet, reel, TikTok, video, article or repo that changed a line or a visual. Each gets its `url`, `title`, `by` (name and handle) and `why` (what it gave this video, in a sentence), plus `stats` (the counts and the day you read them) when you have them. A still of it (`image`) is optional: a screenshot or contact sheet already in `research/`, never someone else's video. A still of someone else's post stays local (AGENTS.md), so on a computer without it the build leaves it out and says so. Why: the page's **References** section is built from this list, so he can open on his phone everything the video came from, and the caption's credits (step 8) come from the same list.

## 3. Pick the format, then each line's layout

```
What structure does the reference have?
├── Items said one after another against a timer ("20 ___ in under N seconds") → "list" (playbook: formats/list/README.md):
│   a fixed title and subtitle, a two-column list that is the captions, the red stopwatch, 2-4 real images under his chin
│   per item, a sign-off question
├── It matches another row of formats/README.md → that format: its playbook's fixed lines and layout, as plan beats
└── Anything else → "talk": 2-3 word captions and one asset per line in one of the layouts below. Add a TikTok-style hook
    title over the first sentence only when he asked for a hook
```

Give each line of a talk reel a `place`. These are charles-claude-editing's layouts with reelkit's numbers (`tools/reelkit/`; `references/plan.md` has the boxes):

```
What does this line show?
├── Nothing new, and the last asset went up less than 4 s ago → no visual, captions only
├── A photo, logo, product, meme or small screenshot, wider than tall → "below" (between his chin and the captions, 780×270
│   by default) or "above" (over his head, 780×430), sticker-sized. Use "above" when his face sits low in the frame
├── A portrait asset (a phone screen, a tall post) → "spotlight", or a split. "below" would draw a phone 137 px wide
├── Something big that has to be seen whole (a long post, a chart), or a list he reads out → "spotlight"
├── A tall video or a phone recording → "split", seam 936, the asset on top
├── A landscape video or a desktop recording → "split", seam 768 (the 40/60 split)
├── Immersive B-roll that replaces him → "screen"
└── A list reel's item → "under-chin": the item's collage (step 7)
```

Split a sentence into beats at its phrase breaks, so that no still stays up past 3 s and nothing on screen goes 4 s without changing. Each beat's `say` is its phrase, and SCRIPT.md keeps the sentence whole for him to read. Never cut a word to make a beat fit: charles-scripting-voice keeps his small words ("which is", "so") on purpose. Why: the edit never goes 4 s without something new on screen, and no still asset stays up past 3 s (charles-claude-editing, Timing), while his sentences run 15 to 35 words.

## 4. Research the content

- Find a date and a source for every claim and every item. Search the web for anything after your knowledge cutoff, and write down in `research/` what you searched and what you found.
- Leave out anything political. Instagram stops recommending a reel to non-followers once it reads as political, which is why 2008's HOPE poster became "The App Store opens".

## 5. Write the lines and fit them

- Write every spoken line with charles-scripting-voice (AGENTS.md asks for it). Its fixed format lines win. When a line needs his own angle (what he uses, built or thinks) and you don't have it, ask him in your reply and leave `<his angle>` in that line of SCRIPT.md. Never invent one.
- SCRIPT.md is what he reads and nothing else, in the format of his "2026-11-10 SCRIPTS" Apple Note: the title in bold, `Text hook: <the hook on screen>`, then the lines he says, then the sign-off on its own line. A list reel numbers its lines (`1. Squash and stretch.`), each with a full stop, and starts the last with "And" ("And frequency of use."). A hack or explainer reel opens with its intro line, then gives each item its on-screen label in asterisks (`*Alpha borders*`) with the sentence he says under it. A roundup adds `GitHub:` and `Example:` lines under each label. No years, timings, screen notes, pronunciations or production notes: those go in `edit/plan.json` and the README, and this replaces charles-scripting-voice's screen notes in angle brackets. Why: he reads it straight off his phone while filming, and anything that isn't a line he says is in the way ("Just make it the actual verbal script ... Don't add extra jargon/text that isn't useful", 16 Nov 2026).
- Put on-screen text that isn't his spoken words in the plan: a list label in `label`, the hook in `hook`. When a word is said differently from how it's written, `say` holds the spoken form and `label` the written one ("Glossy web two point oh buttons" and "Glossy Web 2.0 buttons").
- A list label is at most 5 words, and the list has to fit: `kit/build.py` measures every label in Helvetica Neue Bold and stops, naming the widest, if the list runs past 68 or 1012 px. Shorten that label, or narrow `number_width` (49 px for item numbers, 77 for years) and `col_gap`.
- A label names the one moment its item is remembered for, when it has one ("iOS 7 kills skeuomorphism", "Google's Material Design"). When it doesn't, the label lists the item's two or three most recognisable things, the ones its asset shows ("Cybertruck, Slack's logo", "Angry Birds, Minecraft"). Never write a style made up by joining a thing to a trend ("Cybertruck brutalism"), a trend stretched from one example ("Logos lose their serifs", from Google's one logo), or one feature standing for a whole year ("Facebook's Like button"). Why: "I don't think Facebook's like button should epitomize an entire year of design", and "instead of stuff like cybertruck brutalism, better encapsulations might be cybertruck, xyz, abc (in case there were multiple things that happened except for a single defining moment)" (16 Nov 2026). At 30 px, the two columns' widest labels share 762 px, so a list of three rarely fits and most lists are two.
- Pick what people remember as design: a redesign, a launch, a tool, a product's look. Never pick a show or a meme whose design isn't what it's known for (Stranger Things, for 2016, became Figma's launch). Why: "idk how I feel about stranger things as an epitome of design" (16 Nov 2026).
- The list on screen stays short. When a name alone doesn't bring back what happened, the line he says adds it in a few words: on screen "Cybertruck, Slack's logo", said "Cybertruck, the Slack logo roast"; on screen "Google's logo, Apple Watch", said "Google drops its serifs, Apple Watch". `label` holds the short form, `say` and SCRIPT.md what he says. Why: "Slack's logo itself doesn't really bring people back to what happened there ... It's a lot of text so maybe put it in the script ... The list on screen can be more abbreviated" (16 Nov 2026).
- Let the kit time the lines (`references/plan.md`, Timing). A subtitle like `(20 years in under {under} seconds)` fills in from where the list ends. Why: "under 30" only beats "under 35" if it's true, and a promise the reel breaks reads as clickbait.

## 6. Source the assets

- Write `research/ASSET-BRIEF.md` from `references/sourcing.md`: his rules for found images, the sizes and kinds, where files go, the tools, and one row per group with the pick and anchors in order of preference.
- Split the groups across at most 4 agents, each writing only into its own group folders, and let only one of them capture from the Wayback Machine at a time. Why: with four at once, the Wayback Machine served one agent a bot-traffic block page, and Wikimedia answered 429 to original-size requests.
- Groups about his own work (the Eradicating AI slop pages, his apps) use his own renders and captures, never found copies.
- Look at every pick with the Read tool before keeping it: the right thing, the right year, sharp, no watermark, shown whole.

## 7. Compose and review

- **Nothing covers a subject.** `kit/collages.py` lets images overlap only at their edges, and throws out any layout where something lies over another image's focus box: its inner 80% by default, nearly all of the pick. Give an image its own `"focus"` when its subject sits off-centre, and lay a page whose words run to its edge on top (`"top": true`). Why: in the first version, stickers covered Nyan Cat's face, the iOS 6 before and the Stranger Things title ("make sure the overlap ... don't cover core subjects", 16 Nov 2026).
- **Nothing dark sinks into his footage.** An image that's mostly black (a title card, a dark frame around a screenshot) reads as a hole over his warm, blurred room. Crop to its light part, find a cleaner version (a logo on transparent), or pick another image. Why: "the black contrast is also really bad" on 2016's Stranger Things title card (16 Nov 2026).
- **Words that matter read on a phone.** Anything meant to be read (a repo name, a tweet's key line, a headline) has letters at least 20 px tall on the 1080 grid once it's in the collage, about 7 pt on the phone. A whole screenshot shrunk under his chin never gets there. Cut a card from the real screenshot instead, with only those words, in lines of about 25 characters, on the screenshot's own background, and give it `"focus"` over all of it. Body text that's only texture (a page of a 2009 site) can stay small. Why: he couldn't read any of the GitHub capture in the first version. The repo name, its description and its stars, cut into a card, read at a glance.
- **List reels:** order each item's images in `edit/collages.json`, the pick first. Use 3 by default, and a 4th only when it's small. Render with `kit/collages.py <video> --sheet` and judge every collage on `build/contact-sheet.jpg`. Give the image that carries the item's words `"top": true` (ChatGPT's launch title, a tweet), shrink one with `"scale"` below 1, and try other layouts with `"seed"`, side by side. A layout depends on its seed and on the side the previous item's pick sits, so after changing one, re-render the set and look at the sheet again. When you cut or reorder items, give each the `"seed"` of its old position first, so the others keep the layouts already reviewed. Logo cards stay at least 90% visible on their own.
- **Talk reels:** crop each asset to what its line is about and keep it whole: no cut-off phone sides, no black bars. Put a transparent diagram or logo on a white card with padding, the way collages.py frames logos, so it reads over his footage. When a line explains a term, a fix or a mechanism, its visual is charles-explainers-assets' job: say so in the beat's `note`, and let a still stand in on the page.
- **Red marks:** one box, strike or arrow per asset, and only where it makes the label readable (2015's serif logo struck through).

## 8. Write the caption and credits

- Put the caption in the README's Delivery section, ready to paste, and in your reply. It never goes in SCRIPT.md.
- His captions are short: a hook line or a question, a credit line, then 4-5 hashtags ("Let me know if you want a part 2! Shoutout @ayoships for the format"). No em dashes, and no full stop at the end of a line.
- Every caption option (`caption`, `caption_alt` and each of `options`) shouts out the original authors by name and handle: whoever had the idea, made the format, or made what the reel teaches from, with the platform when it isn't Instagram ("S/o Damir Sokolovsky (@heydamir on X) for the idea"). Search for an Instagram account first and tag it if there is one. Why: "Make sure in the captions of each of these videos we also s/o original authors" (16 Nov 2026). A shorter alternative that drops the credit gets posted without it.
- Ask a different question from the sign-off, so the comments get two ways in. Add a shorter alternative, and an optional first comment crediting the artists whose work is on screen.
- Never reuse a caption line or a hashtag set he's already posted (`repost/reels.json` has them).

## 9. Pick the music

- Pick the mood folder in `assets/music/` (charles-claude-editing, Music), plus one alternative: the reference's own track when it's in the library.
- Set `at` where the full beat starts, never in a quiet intro. Print the track's loudness every 0.5 s, then every 40 ms around the candidate, and start on the first hit after a break. Check that the next breakdown comes after the reel ends. Why: the page plays exactly this clip under the mockup, and the edit starts the track at the same point.

## 10. Build, check, publish

From the video folder:

```bash
python3 -I <skill>/kit/build.py . --site
```

That writes `build/plan.html` (the page, which opens from disk), `build/music/` (the track cut from its `at`), `build/times.json` (each line's start and length), `build/posters/` (a still of each clip, for its asset card), `<assets_dir>/SOURCES.md` and `build/site/`, the shareable copy. Then:

1. Fix every check the build prints, or write in the README why one stays (a tweet he reads for 5 s is `long_ok`).
2. Look at every collage at full size (`assets/collages/<group>.png`, laid on a mid-grey at 1050 px wide): no subject covered, and every card's words readable. Then export full-size frames of the first line, a middle line, the busiest line and the last, plus one with `&safe=1&ig=1`: `python3 -I <skill>/kit/capture.py "file://$PWD/build/plan.html?solo&t=<s>" build/frame.png --size 1080x1920 --scale 1`. Nothing that matters may sit under Instagram's header, caption or buttons. Why: the browser pane scales its screenshots down, so only full-size frames show small text.
3. Read the page's sections once, as he will. The build prints how many script lines it tied to the plan's lines: every line he says should be tied, so it lights up and jumps the reel, and a line that isn't means SCRIPT.md and a beat's `say` (or a list item's `label`) disagree. Every caption option is there, and every reference, each with its `why` (the build flags one without, and a plan that still has only the old `reference`). Each asset card's title is plain words for what's on screen, because it's the visual's `what` (a list item's card takes its label): "The AI palette, then the same colours at one lightness", never a file, folder or skill name like "Day N card p1-chips (charles-explainers-assets)". Why: he reads these on his phone ("Don't add extra jargon/text that isn't useful", 16 Nov 2026). For the phone layout, use device emulation (playwright-core with a 390×844 viewport) and scroll the page once before a full-page screenshot. `capture.py` can't lay a page out narrower than about 500 px, because of Chrome's minimum window size, and the asset stills only load as they scroll into view.
4. Publish with the Artifact tool: `file_path` build/site/index.html, `root` build/site, `files` the list in build/site/files.json, and `icon` "video" on the first publish. After any change, publish the same file path again so the link stays: the page alone when only the plan changed, with files.json again when media changed, and `null` for any media path that's gone. The page is private until he shares it from its Share menu, so tell him.
5. Open the link with `#check` on the end in his Chrome, in a new tab or with a reload (changing only the hash of an open page doesn't reach the page's frame, so no dot shows), press Play with sound, and check that the dot after the clock turns orange, which means the music is playing, and that the count beside it reads all of the reel's files ("20/20"), which means they all came into memory. Then pause it, and leave the tab on the plain link. Why: nothing outside the page can see into its frame, so its own dot and count are the only proof, and only `#check` shows them. Test playback cold too, as another computer gets it, because this Mac's cache hides a slow load: the pages once played fine here and badly on his other computers, where clips seeked over and over while they arrived and the music came in seconds late ("transitions don't work properly or the a-roll/b-roll doesn't load properly", 18 Nov 2026). With playwright-core, serve `build/site/` through `page.route` over a throttled link (about 12 Mbps, CPU slowed 4x), press Play, and check that every line's clip or still shows within its first 150 ms and stays within 0.1 s of the reel's clock (read the clock from `#scrub`, not the rounded `#t-now`). Then have the route answer a range request with the whole file, as a host without byte ranges does, and pause, play again and jump to a later script line: the reel has to carry on from where it was. It started over on his other computer ("every time I click pause and then play again, it restarted the video from the start", 18 Nov 2026).

## 11. Hand over

- README: the brief, the files, the link, the music pick, and what's checked and what isn't. Timing is always an estimate until there's a cut.
- Make sure the format's playbook (`formats/<format>/README.md`) lists the video as in production. Once it's posted, its row there gets the plays and what it taught (AGENTS.md).
- In your reply, give the link first, then the script exactly as SCRIPT.md has it, ready for his notes, and the caption. Then say what he films (how many lines, about how long), the judgement calls he might overrule, and what isn't checked.
- After filming, the editing session writes `edit/cuts.json` and rebuilds, and the page switches to the cut's real times.
- No AI voice reads the script. The page plays the music alone, and lines take their estimated length until there's a cut. Why: the AI copies of his voice (IndexTTS-2, then his ElevenLabs clone) "sound like shit" (19 Nov 2026).
