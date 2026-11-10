---
name: shot-list
description: Turn an approved script (or a reference video) into a shot list the creator can film without making a single decision on set. Every setting chosen, every line of text written out, every beat given a "must be visibly true" check, recording order separated from video order. Use when planning a shoot, a product demo, a sponsored reel or a screen recording, or when asked for a shot list, takes, or filming plan. Usage - /shot-list <path-to-script.md or video.mp4> [product url]
argument-hint: <path-to-script.md | path-to-video.mp4> [product-url]
---

# Shot List Builder

You are turning an approved script into something **filmable without thinking**. The creator is holding a
camera or driving a browser, and every unmade decision in the document becomes a stall or a reshoot.

**Input**: $ARGUMENTS

---

## Requirements

- Nothing to install for a script input. For a video input (reference or rough cut): **ffmpeg** to pull
  frames, and **Python 3** with `openai-whisper` to transcribe (`pip install openai-whisper`).
- A browser tool (for example Playwright or a browser MCP) if you want to dry-run a live product.

---

## The one rule

**Never write a choice into a shot list. Write the decision.**

| ❌ Never | ✅ Always |
|---|---|
| "Type the topic" | The exact text, in a copy-paste block |
| "Pick a style" | "Click **Creative**", plus one line on why |
| "Choose the model" | "**Nano Banana Pro**. If absent, GPT Image 2.0" |
| "Show the AI editing something" | The exact edit request to type, chosen because it is visible |
| "Set the slide count" | "**8**" |

If you find yourself writing "or", "either", or "your choice", you have not finished the job.
Make the call, state the reason in one clause, and give the creator an override line at the end.

---

## Build it in this order

### 1. Read the approved script first
Every screen beat traces to a VO line. Pull the script's own "on screen" column if it has one.
**Watch for script-vs-screen contradictions**, they cause most revisions:
- VO says «γράφεις **συνοπτικά**» ("you write it **briefly**") → the typed prompt must be SHORT, not a paragraph
- VO says "spin it" → the model must actually ROTATE on screen, not sit static
- VO says "it changes it instantly" → the before AND after must both be on camera

### 2. Dry-run the product before committing
If the script demos a live product, load it first. Sites with bot protection (Cloudflare) block
scripted browsers. **Find this out before writing a capture plan around it**, not during the shoot.
If it blocks, switch to "the creator drives, Claude records" and say so at the top of the document.

If you could not see the UI, **say so explicitly** and mark button names as coming from reference
videos rather than the live product. Never invent interface details.

### 3. Mine the brand's reference videos, if any
Whatever recurs across most reference videos is the real brief. Transcribe them and read the frames.
A feature shown in 4 of 5 references belongs in the shot list even if the written brief never
mentions it.

### 4. Separate recording order from video order
They are almost never the same. A "wow first" hook needs the finished artifact to already exist, so
it is filmed LAST. Put a table at the top mapping take → video position, so nobody is confused
mid-shoot.

### 5. Split into takes, hard cap 90 seconds each
Recording one long exploratory session and hoping the moments are in there is how one product demo
ended up with three separate mistakes. One take per phase. Never record dead time (a two minute
generation wait gets stopped and resumed, not filmed).

---

## The hook is a physical shot, not a screen grab

This is the beat most often got wrong. The strongest product-demo reels open the same way: **the
creator at the desk, the screen showing the finished result, shot from behind or side profile.** A
flat screen recording makes a weak hook because there is no human in it.

Default hook setup, adapt per job:
- Phone or camera on a tripod, **behind and slightly to one side**, shoulder and hair on one edge,
  screen filling most of the frame
- **Rear camera, never front.** The front camera mirrors and flips any text on screen
- Screen bright, room lit so the screen is not blown out
- Laptop angled slightly toward the lens
- **Two variants of the artifact**, cut between them ~1.5s each. A game demo cuts between two games.
  Two different decks, two different builds, two different outputs. This is what sells range in 3 seconds

So: generate or prepare a **second** artifact whenever the hook needs a cut.

---

## Format of the document

Write it as markdown next to the script (or in the project folder). Structure:

1. **Why it is shot this way**: one short paragraph, including any blocker found in the dry run
2. **⚠️ caveat block** if the UI was never seen
3. **Takes table**: take → what → how shot → video order
4. **Setup checklist**: window state, zoom, what must stay out of frame, Do Not Disturb on
5. **"All decisions, made"**: a table of every setting with the chosen value and a one-clause why
6. **"Exact text to type"**: every string in its own fenced block, ready to copy
7. **One table per take**, columns: `#` | `Do exactly this` | `Must be visibly true`
8. **Pacing rules**
9. **Override note**: the one or two places the creator may reasonably disagree, stated plainly

### Every beat row needs
- A number the creator can call out ("redo A4")
- An imperative instruction with the actual value in it
- An explicit **hold**, in seconds, counted out loud
- A "must be visibly true" that a person could check by pausing the footage

### Always include these standing rules
- Move the mouse **slower than feels natural**, fast cursor movement is uncuttable
- **Two full seconds** parked on every end state
- Fumbles: do not stop, pause 3 seconds, redo the step, we cut the bad one
- Close any profile/account menu, brand demo credentials must never be in frame
- One tab, bookmarks bar hidden, zoom 150%

---

## Flag the fragile beat

Every shot list has one beat most likely to fail. Name it, say why, and say what to do if it looks
weak. Usually it is the one where the VO promises a visible change: if the change does not read on
camera, the line is a lie and the client will send a note. Tell the creator to redo it with a bigger ask.

---

## Before handing it over
- Every setting has a value, no "or"
- Every typed string is in a copy-paste block
- Every beat has a hold and a visible-truth check
- Recording order stated separately from video order
- The hook has a physical setup, not just "show the result"
- Any UI you could not verify is marked as unverified

Then hand off to `/demo-reel-capture` for the recording, or `/sponsored-reel` once footage exists.
