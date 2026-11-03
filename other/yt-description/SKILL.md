---
name: yt-description
description: "Writes the full YouTube description for a finished long-form video, in the creator's exact channel format. Pulls the latest published description off the channel with yt-dlp and uses it as the live skeleton, reads the word-for-word script from the video-editor job (or the Notion beat sheet if the job isn't there), builds real chapter timestamps by indexing the final exported file, decides which links belong based on what the creator actually said, and hands back copy-paste-ready copy. Triggers: write a youtube description, youtube description, yt description, description for this video, write the description, description copy, youtube desc, video description, write my description, description for the new video."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/yt-description/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# YouTube Description Writer

A finished long-form video needs a description that matches every other one on the
channel: offer link up top, tool links, timestamps, follow block, summary, what-I-cover
bullets, closing CTA. The format is not invented here — it is **pulled live from the
last video the creator published**, so the skill tracks the channel instead of drifting from it.

Long-form only. Shorts don't use this format.

---

## The Flow

```
latest published description (yt-dlp)  →  skeleton
word-for-word script (video-editor job / Notion)  →  what the video says
final exported file (whisper index)  →  real chapter timestamps
links.md + what they named on camera  →  link blocks
                    ↓
        filled description → chat + descriptions/
```

---

## Step 0 — Identify the video

The creator names it (a `<job-slug>`, a title fragment, "the video I just finished").
Resolve it to two things before doing anything else:

- **a video-editor job folder** — `ls ~/Projects/video-editor/projects/` and match.
  `ls -t` there orders by most recently touched, which is usually the one they mean.
- **its Notion page** — resolve it exactly per the standing rule in `CLAUDE.md`
  ("Resolve every video reference"; the lookup mechanism lives there, this skill
  does not pick one). The Data source ID comes from `notion-pipeline.md`. Search on
  one distinctive title keyword, not the whole phrase.

Two hits, ask which. Zero hits: create the page at the stage the video is actually
in (a finished export waiting on its description is `Review` or `Ready`) via MCP
`notion-create-pages`, per the CLAUDE.md rule, then carry on with the job.

---

## Step 1 — Pull the skeleton

```bash
.claude/skills/yt-description/scripts/fetch_skeleton.sh --count 2 \
  --channel https://www.youtube.com/@<YouTube handle from CLAUDE.md Creator Profile>/videos \
  --out <scratchpad>/skeleton
```

Reads the newest 2 long-form uploads off the channel. Always pass `--channel` with
the `/videos` URL of the channel in `CLAUDE.md` (Creator Profile); env
`YT_DESC_CHANNEL` also works. A different channel never means editing the script.
**`skeleton-1.txt` is the format** — the new description copies its block order, its
emoji, its spacing, its register. `skeleton-2.txt` is only there to separate a fixed
block from a one-off (a referral block that showed up in one video is a one-off; the
follow block is fixed).

Read both. **The pulled skeleton always wins.** The list below is only the example
shape, so you know what kind of blocks to expect:

1. `🚀` one line naming what this video's viewer gets from the offer, `⤵️`, then the
   offer URL (offer per `backbone/offer.md`, URL from the skeleton / `references/links.md`)
1b. optional `🎁` free-resource block (URL from the skeleton, never from memory)
2. `🔗` one block per tool/repo used in the video: emoji, name, short parenthetical, `⤵️`, URL
3. optional `💳` grouped referral block (only for a video that walks through those products)
4. the channel's fixed like/subscribe line, verbatim from the skeleton
5. `⏰ TIMESTAMPS`, blank line, then chapters
6. `Follow me on other platforms` + one line per platform (handles per `CLAUDE.md`)
7. `Summary ⤵️` — 4 to 6 paragraphs
8. `What I cover ⤵️` — 8-ish `-` bullets
9. optional `⚠️` disclaimer line (only when the topic needs one)
10. closing offer paragraph ending `First link down below. 👇`

If `skeleton-1.txt` differs from this, **the file wins, not this list.** That's the
whole point of pulling it live.

**Empty channel** (no long-form uploads yet, so `fetch_skeleton.sh` writes no
`skeleton-*.txt`): use the example shape above as the format, take every URL from
`references/links.md`, and say in the handoff that the shape is the example, not a
pulled skeleton.

---

## Step 2 — Get the word-for-word script

The description has to describe what they actually said, not what the plan was.

**Video-editor lane (preferred):**

```bash
python3 .claude/skills/yt-description/scripts/collect_script.py <job>
```

(`python` on Windows.) Prints the spliced transcript(s) — the exact kept words from
the cut — plus a coverage number: how much of the final export the transcripts
account for. Under 90% means the video was assembled outside the splice (Premiere,
extra sections, a re-order), so the text is still good but its **timings are not**
and part order isn't guaranteed. Over 105% means the parts run longer than the
export: they include superseded or overlapping takes, so timings are equally
untrustworthy and some of the text may not be in the video. Either way, read the
parts, work out the real running order from the content, and take every timestamp
from Step 3.

**Notion lane** (no job folder, or the job has no transcript): read the page body
with the `notion-fetch` MCP tool on the page ID from Step 0. That's a **beat sheet,
not a transcript** — it's what they planned to say. Write the summary from it, but
keep claims general enough to survive the difference, and tell the creator in the handoff
that the copy came from the beat sheet.

---

## Step 3 — Build the chapters

Timestamps always come from **the final exported file**, never from the editing
transcript. A section-assembled cut re-orders and pads the timeline; splice times
are wrong by minutes there.

```bash
.claude/skills/yt-description/scripts/chapter_index.sh <final.mp4> <scratchpad>/idx.tsv
```

The file is `projects/<job>/outputs/<job>.final.mp4` (or `<job>.mp4`), and
`finalize.sh` also drops a copy in `~/Downloads/`. One faster-whisper pass
(`base.en` by default, `YT_DESC_WHISPER_MODEL` overrides) with native word
timestamps, so the index is real words, one per row. It runs on the shared
`~/.cache/content-os/whisper-venv`; the first ever run on a machine builds that
venv with `uv` (or `./setup.sh` pre-builds it), after that it's a minute or so
for a 20-minute video.

Then pick the chapter boundaries yourself from the script — you know where the
video turns — and write **the words they say as each chapter opens** (5 to 10 of
them, not the chapter title) one per line:

```bash
python3 .claude/skills/yt-description/scripts/find_times.py --index <scratchpad>/idx.tsv --phrases <scratchpad>/phrases.txt
```

Back comes one line per chapter: time, match score, what matched. **Score below
0.6 is not a usable timestamp** — that line isn't in the final cut, so pick a
different opening phrase from the same beat and re-run.

Start the phrase on the beat's **actual first words**, throat-clearing included
(`All right guys, so I'm going to...`, not `So I'm going to...`). Cutting the
preamble moves the chapter 3 to 5 seconds late, because the match lands exactly
where you pointed it. Then **round each time down 2 to 3 seconds** — the match
marks where the phrase starts, and a chapter that opens a beat early reads better
than one that clips their first word. Validated against a published video: full
opening lines minus a 2s nudge land within a second or two of the chapters that
actually shipped.

Chapter rules YouTube actually enforces (break one and the whole chapter list
silently doesn't render):

- the first chapter is `0:00`
- at least 3 chapters
- every chapter at least 10 seconds long
- ascending order
- `M:SS`, or `H:MM:SS` past an hour

Titles read like the channel's: short, title-case, concrete. `Intro`,
`The Software Stack`, `Live Demo: <what gets demoed>`, `Build It Yourself (Tutorial)`,
`Final Thoughts`. Last chapter is a `Final Thoughts` variant. If there's a stretch
where they pitch the offer, it gets its own chapter (e.g. `Get it from my community`),
people skip to it.

---

## Step 4 — Decide the links

Read `references/links.md`. Then go through the script and list every tool, repo,
product, or app they **named on camera**. Each one either:

- is in the registry → use that exact URL,
- is a referral product they actually walked through → referral row, grouped under `💳`,
- is new → resolve it to its official source, put it in the draft, and flag it in
  chat as new-and-unverified. Never invent a URL.
- was mentioned in passing and isn't part of the build → no link. Three or four
  link blocks is the shape; ten is clutter.

Slot 1 is always the offer line, rewritten for this specific video's payoff. The
community (name/price per `backbone/offer.md`) is the only CTA: nothing from the
"What is NOT sold" list in `backbone/offer.md`, no apply links, no call bookings.

---

## Step 5 — Write it

Fill the skeleton. Where the writing actually happens:

**Offer line (slot 1).** Name the artifact from *this* video that a viewer would
want: `🚀 Get <the artifact from this video> ⤵️`. Concrete object, not a benefit
claim. Match the offer's positioning in `backbone/offer.md`.

**Summary.** 4 to 6 paragraphs, in their register (`voice-dna.md`): first person,
plain words, real numbers, no hype adjectives. Open with the outcome or the claim
the video proves. Then how the machine works, in the order the video shows it. Name
the free open-source pieces and say they're free. Say plainly how the offer relates
to this video (what the viewer gets inside vs. what the video shows for free),
matching the positioning and deliverables in `backbone/offer.md`. Close on the
point actually made on camera.

**What I cover.** 8-ish bullets, one per real beat of the video, specific enough
to be searchable. These are the SEO surface — use the words someone would type.

**Closing paragraph.** Same shape every time: what the community is and what's
inside it (the deliverables listed in `backbone/offer.md`), including this video's
artifact, then `First link down below. 👇`.

Hard constraints: no em dashes (the newest description doesn't use them — colons
and commas instead), under 5000 characters total, and the first ~150 characters
matter most since that's all that shows before "show more".

---

## Step 6 — Deliver

Save to `descriptions/<job>_<YYYY-MM-DD>.md` (`mkdir -p descriptions` first), then
print the **raw description block** in chat inside one fenced code block so they can
copy it in one grab. Nothing above it but a one-line note, nothing below it but
flags that need their eyes:

- any link marked new-and-unverified
- any chapter that scored low
- whether the copy came from a transcript or a beat sheet
- whether the format came from a pulled skeleton or the example shape

No preamble, no summary of what you did.

---

## Rules

- **The skeleton is pulled, never remembered.** Every run starts with
  `fetch_skeleton.sh`. If the creator changed their format last video, the new description
  changes with it.
- **Timestamps come from the exported file.** Editing transcripts are for text.
- **No invented URLs.** Registry, or resolved-and-flagged. Never from memory.
- **One CTA: the community** (name/price per `backbone/offer.md`). Nothing from the
  "What is NOT sold" list in `backbone/offer.md`, ever.
- **Describe what they said.** If the script and the plan disagree, the script wins.
- **No em dashes** in anything written here.

---

## Files

| File | What |
|------|------|
| `scripts/fetch_skeleton.sh` | Pulls the newest long-form descriptions off the channel (yt-dlp, 2 steps: IDs then bodies). `--channel <url>` (the channel from `CLAUDE.md`) or `YT_DESC_CHANNEL` picks the channel. |
| `scripts/collect_script.py` | Reads a video-editor job's spliced transcript(s), reports coverage vs the final export, prints the script. |
| `scripts/chapter_index.sh` | Word-level faster-whisper index of the final exported file (`base.en`, `YT_DESC_WHISPER_MODEL` overrides) on the shared `~/.cache/content-os/whisper-venv`. |
| `scripts/find_times.py` | Fuzzy-matches chapter opening phrases against the index, returns timestamps + confidence. |
| `references/links.md` | The link registry: fixed links, tools already used, referral links, and how to resolve a new one. |

## Notes

- The chapter index runs faster-whisper from the shared persistent venv at
  `~/.cache/content-os/whisper-venv` (built once by `uv` on first use or by
  `./setup.sh`; `CONTENT_OS_WHISPER_VENV` overrides the path). Model default is
  `base.en`, `YT_DESC_WHISPER_MODEL` overrides. Nothing else to install: no compiler toolchain, no separate speech binary.
- The index is real words (`word_timestamps=True`), not sub-word tokens, so tool
  names like `DaVinci Resolve` match cleanly. `find_times.py` still drops
  apostrophes on both sides before matching so a contraction tokenizes the same
  way in the phrase and in the index (`you're` -> `you` + `re`).
- A job's `outputs/` may hold `<job>.mp4` (base cut), `<job>-4k.mp4`, and
  `<job>.final.mp4`. `collect_script.py` prefers `.final.mp4`. If the running order
  of a section-assembled job is ambiguous, the index from Step 3 settles it: match
  the first line of each section and sort by time.
