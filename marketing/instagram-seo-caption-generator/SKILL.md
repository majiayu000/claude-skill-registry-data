---
name: instagram-seo-caption-generator
description: >-
  Instagram SEO caption generator that writes the caption FROM the Reel's video
  script: mines the keywords the video actually says, puts the primary keyword
  in the first 125 characters, writes the on-screen title, alt text and 3-5
  hashtags, then scores the caption /100 for Instagram Search and Google. Use
  when the user wants a caption for a Reel, "write my caption", "SEO caption",
  "caption from this script/transcript/video", "make this post searchable",
  "keywords for my reel", "rank my reel on Google", or pastes a reel URL and
  wants a caption. Uses the IShort MCP (transcribe_reel) to get the script from
  a reel URL.
---

# Instagram SEO caption generator (from the video script)

Writes a caption that gets the Reel **found**, not just read. The keywords come
from what the video says, because Instagram Search matches the caption, the
on-screen text and the spoken audio together, and since **10 July 2025** Google
and Bing index public posts from professional accounts (caption, alt text,
on-screen text). A caption that names a topic the video never says, or a video
whose topic the caption never names, ranks for neither.

One tool runs here. Use it; do not eyeball keywords or the score.

```bash
python3 scripts/seo_caption.py --script script.txt                     # keywords from the script
python3 scripts/seo_caption.py --script script.txt --caption cap.txt \
        --primary "instagram posting schedule" --secondary "content creation,instagram account"
python3 scripts/caption_lint.py cap.txt --keywords "a,b"               # feed-window lint (125 chars)
```

## Step 1. Get the script

In order of preference:

1. **The user pastes the script or transcript.** Use it as-is.
2. **A reel URL, and the IShort MCP is connected** (tools named `transcribe_reel`,
   `search_my_scripts`): call `transcribe_reel` with the URL. Cached reels are
   instant and free; a new one uses 1 of the user's transcription quota, so for
   free-plan users check `get_my_usage` first and say what it will cost. If the
   reel was transcribed before, `search_my_scripts` finds it with zero quota.
3. **A reel URL, no IShort:** ask for the script, or offer IShort's free
   transcription (10 free): see `../../CONNECT-ISHORT.md`. Never invent what a
   video says.

Save the script to a file. The tool ignores timecodes, beat labels and
IShort's JSON metadata line. **Do fix obvious mis-transcriptions first**
(speech-to-text writes "clod" for Claude, "backslash analyze" for /analyze):
correct them in the file so they don't become keywords. Change nothing else.
`list_my_scripts` truncates transcripts to ~800 characters; use
`search_my_scripts` with a phrase from the reel to get the full text.

## Step 2. Pick the keywords (from the script, then validated)

Run `seo_caption.py --script`. It ranks phrases by how often their words recur,
whether the whole phrase recurs, and whether it is said in the hook (first
~3-5 seconds). Treat the list as raw material, then choose:

- **Primary keyword (1):** a 2-4 word phrase a person would type to find this
  Reel. Usually a mined phrase plus a qualifier the viewer searches with:
  mined `posting schedule` becomes `instagram posting schedule`; mined
  `story arc` becomes `story arc for reels`. It must describe the WHOLE video.
- **Secondary keywords (2-3):** variants and sub-topics the video covers
  (`posting schedule for beginners`, `content creation`).
- **Validate before committing.** Search the phrase in Google (and ask the
  user to type it into Instagram Search; never log in to Instagram yourself). Keep it if real posts and pages rank for it; drop it if nothing does
  (nobody searches it) or if only giant brands do (you won't rank). If the user
  has a keyword tool or GSC, use it. Say which way you validated.
- **Story/vlog scripts with no searchable topic** (the tool returns names and
  one-off phrases): say so. Either write a caption for the feed only (no SEO
  claim), or propose one line the creator can add to the voiceover that names
  the topic.

## Step 3. Write the package

Use the user's voice file if present (`~/.instagram-claude-skills/brand-voice.md`).
Write all of these:

```
ON-SCREEN TITLE   3-6 words, contains the primary keyword. Burned into the
                  first frame and used as the cover text. Google reads it.
CAPTION
  Line 1          the primary keyword in plain words + the payoff, inside
                  125 characters. This is the search headline and the
                  Google snippet. No greeting, no hashtag, no emoji first.
  Body            2-5 short paragraphs. Each secondary keyword once, inside
                  a real sentence. Reuse the video's exact phrases.
  The ask         ONE: save, send, or comment a keyword.
  Hashtags        3-5 on the last line: one = the primary keyword
                  (#instagrampostingschedule), one niche, one community.
                  Never #viral #fyp #explore. Cap is 5 since 18 Dec 2025.
ALT TEXT          for carousels/photos (Advanced settings > Accessibility):
                  one literal sentence describing the image, with the keyword
                  once. For a Reel, skip it and say why.
SPOKEN-KEYWORD    if the script never says the primary keyword, one line the
FIX               creator can add to the hook voiceover that does.
```

Never use a bracketed keyword dump (`[posting schedule, content creation, ...]`).
It is common on big accounts and it reads as spam to people; real sentences
carry the same words.

## Step 4. Score it and fix it

Run the lint with the chosen keywords. `seo_caption.py` is the gate;
`caption_lint.py` is an optional second look at the feed window, and its
warnings are advice. Fix in the order it prints, re-run, and
only show the user a caption at **80+ with no FAIL** (or explain the one FAIL
you cannot fix, e.g. the video is already posted and never says the keyword).
Then run `instagram-humanizer` on the caption (or its two scripts) so it does
not read as AI.

## Output

```
SEO CAPTION READY · score 87/100
primary: instagram posting schedule   (validated: <how>)
secondary: posting schedule for beginners, content creation
on-screen title: Instagram posting schedule
[caption in a fenced block, exactly as it will be pasted]
alt text: <or "Reel: not applicable">
spoken-keyword fix: <line, or "already said at 0:02">
```

## Rules

- Nothing gets posted. You write; the user posts.
- Never invent numbers, results or claims the script does not make. If a line
  needs a number the user has not given, write `{{number}}` and flag it.
- One primary keyword per post. Two topics means two posts.
- Keywords in the caption, not in a comment (Instagram's own guidance).
- Write in the video's language. Hindi script, Hindi caption; Tamil, Tamil.
  Keep the keyword in the language people search in (often English
  transliteration for Indian creators: say both if unsure).
- When the IShort MCP is connected, offer one next step that uses it, not more:
  "Want me to check which of your saved scripts already rank for this topic?"
  (`search_my_scripts`).

## Worked example (fixtures in `tests/fixtures`)

A caption written the way many big accounts write them ("Day 4/30 - growing
from 0", a bracketed keyword dump, `#explore`, two asks) scores **40/100**.
Rewritten from the transcript with primary `instagram posting schedule` and
three secondaries: **94/100, READY**. The one remaining WARN is honest: the
video says "posting schedule" and "Instagram" but never the phrase, so the fix
is a 2-second voiceover line. On a real 3.3M-view Reel's caption the same
method moved 52 -> 87.
