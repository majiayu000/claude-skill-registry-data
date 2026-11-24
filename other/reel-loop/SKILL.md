---
name: reel-loop
category: video
description: |
  Run one short-form account as a loop: find the reels in a niche that broke out
  against their own creator's normal, take the best one apart (hook, structure,
  shots), write a new script in the account's own voice, produce it (narration,
  scenes, word-by-word captions), stop for a person's approval, publish to Instagram
  through the Graph API, measure at 48 h and 7 d, and push variants of winners as
  Trial Reels to non-followers. A composition skill: research, voice, render and
  layout come from sibling skills; the arithmetic (outlier and winner scores) and
  the publish gate live in a tested script, so no step past the approval is
  reachable without an approval bound to the exact rendered bytes. Poll comment
  keywords into one private reply per comment with a separately byte-approved
  template and durable attempt ledger.
  USE WHEN: "reel loop", "content machine", "find viral reels in my niche and remake
  them", "outliers in my niche", "x times their normal", "nightly content run",
  "remix the winners", "trial reels", "make reels while I sleep", "content-os",
  "comment keyword funnel", "WORKSPACE private reply", "/reel-loop". NOT FOR: editing raw footage into a cut with no loop around it
  (video-cut), one cinematic generation or brand compile (content-engine), a
  multi-account portfolio with canon and spend ledgers (that is the
  agentic-media-studio initiative, which runs one reel-loop per account lane), or
  reposting someone else's video (never).
  Triggers on: reel loop, viral outliers, niche outliers, reel remix, trial reels,
  nightly content, content machine, reel-loop.
license: MIT
primitive: null
required: false
introduced_in: "0.51.3"
---

# reel-loop

One account, one loop, one human button.

```
SENSE → OUTLIERS → DECONSTRUCT → SCRIPT → PRODUCE → QC → [APPROVE] → PUBLISH → MEASURE → TRIAL → LEARN
  1        2           3            4         5       6       7          8         9        10      11
```

Stages 1–6 may run unattended (for example nightly). Stage 7 is a person. Stage 8
refuses to run without stage 7's approval for the exact bytes being published. That
refusal is code (`scripts/reel_loop.py publish`), not a sentence in this file.

The pattern comes from a creator's reel (`@davidmadrazo.ia`, 2026-11-12) showing
Claude doing stages 1–10 every night at 03:55 while he only presses "Aprobar". Its
open counterparts are his free `crecer` plugin (stages 1–4, read-only) and
AttentionOS (stages 1–4 and 8–10, human-filmed video). Neither has a cloned-voice
render or an approval bound to bytes. Survey and per-stage alternatives:
[references/stage-map.md](references/stage-map.md).

## Platform modes

One loop shares research, script, render, QC and byte-bound approval across
platforms. A post card without `platform` is Instagram; `"platform": "youtube"`
selects the YouTube Shorts adapter. Each approval binds the target platform and
destination as well as the rendered bytes. TikTok has no automatic adapter: post
there by a human click or the Higgsfield widget. See
[references/platform-contract.md](references/platform-contract.md) and
[references/post-card.md](references/post-card.md).

## The account folder

Everything for one account lives in one folder. Inside the agentic-media-studio
repo, use `accounts/<handle>/`. Anywhere else, use any folder:

```
<account>/
├── voice.md            how the account talks: 3+ real samples, words it never uses
├── niche.tsv           seed accounts to watch (handle, why), 6–20 rows
├── rules/hooks.md      the hook rulebook, grown from what won (starter: references/script-card.md)
├── consent/voice.md    dated consent of the person whose voice is cloned (required to clone)
├── runs/<date>/        one folder per run: reels.tsv, outliers.json, cards, scripts, renders
└── posts.tsv           our published posts: id, published_at, views, is_trial, source_url
```

Missing `voice.md`, `niche.tsv` or `consent/voice.md`: create it with the person once
(3 questions, not a form), then never ask again.

## Stages

### 1 · Sense: collect view counts for the niche

Pick the first route that works. Never use the publishing account's session for
collecting anything.

1. **Official (preferred):** Business Discovery returns `view_count` for another
   professional account's reels (Facebook Login path; details in
   [references/platform-contract.md](references/platform-contract.md)). It only
   works for handles you already know, so `niche.tsv` is the input.
2. **A person's browser at a human pace:** a read-only pass over `/<handle>/reels/`
   for each seed account, at most 10 accounts per pass, seconds apart. Stop at any
   login wall or warning. This is the `crecer` method.
3. **Pasted numbers:** the person reads the counts off the grid.

Write `runs/<date>/reels.tsv` with the header `account url views date hook`.
Counts can be copied as displayed ("12,3 mil", "1,2 M", "12.3K"); the script parses them.

### 2 · Outliers: compare against the creator's normal, not raw views

```bash
python3 scripts/reel_loop.py outliers runs/<date>/reels.tsv --json > runs/<date>/outliers.json
#   --bar 4 (x the account's normal)  --min-views 20000  --max-age-days 45  --min-sample 5
```

The baseline is the **leave-one-out median** of the account's *other* reels, so a
breakout cannot lift its own baseline. Accounts with fewer than `--min-sample`
other reels never pass. A million views on an account that always gets two
million is not an outlier, and the example file shows it
(`references/example-niche.tsv`). If too many reels pass, raise `--bar`. If none
pass, lower it to 3 and say so in the run note.

### 3 · Deconstruct the top 1–3

For each outlier, fill a **deconstruction card**
([references/script-card.md](references/script-card.md)):

- the hook in three layers: what is seen, what is said, what the on-screen text says;
- why viewers are still watching at 3 s;
- the turn;
- the call to action;
- a shot list with times.

Read the video only if downloads are allowed. If Business Discovery omits
`media_url`, or the owner turned downloads off, work from the caption and the page
text instead. When the download is allowed, run the workspace's
`scripts/video_ingest.py "$URL" --query "$Q" --keep-video`, passing both values
through exported variables. Then read its contact sheet and transcript.

Its speech recognition runs as English today (BRO-3796). Two paths set
`language="en"`. The third, whisper.cpp, passes no language and defaults to the
English-only `ggml-base.en` model. On a non-English reel it returns a placeholder
like "(speaking in foreign language)" and reports low speech. In that case, extract the audio with `ffmpeg -i video.mp4 -ar 16000 -ac 1 a.wav` and
run `whisper-cli -m <ggml-small.bin> -l <lang> -f a.wav`. **Copy the structure, never the wording, footage or
audio.**

### 4 · Script, in the account's voice

Write `runs/<date>/script-<n>.md` from the card:

- **HOOK:** 3 candidates, scored against `rules/hooks.md`, with the best one marked.
- **STRUCTURE:** the beats lifted from the reference.
- **BODY:** our topic, written in the voice of `voice.md`.
- **CTA:** the call to action.

Time every line: 20–35 s total, about 2.5 words per second. Run the draft through
`humanizer` or `unslop` if they are installed. A script that could only have come
from the reference's topic is a copy: rewrite it.

### 5 · Produce

| Layer | Default | Alternatives |
|---|---|---|
| Narration | `omnivoice` local clone (`generate_speech` with the cloned `profile_id`), only with `consent/voice.md` present | ElevenLabs IVC, or the person records it |
| Scenes | `content-engine` generate (Higgsfield / Veo), from the script's shot list | `video-cut` on real footage; Remotion scenes |
| Word-by-word captions | `brainrot-for-good` `/subtitle-generation` (Remotion `createTikTokStyleCaptions`) | `video-cut` burned subtitles |

Captions sit in the 9:16 caption band, not where Reels draws the username and
caption UI.

### 6 · QC

```bash
python3 ../content-engine/scripts/check_vertical_layout.py video runs/<date>/final-<n>.mp4 --expect-captions --expect-title
```

Fix and re-render until the check passes. Then write the post card,
`runs/<date>/card-<n>.json`, using the schema in
[references/post-card.md](references/post-card.md). It records:

- the source reel and its ratio;
- the script path;
- which media are synthetic;
- the voice-consent reference;
- the caption;
- `trial: null` for a normal post.

### 7 · Approve (a person)

Put one approval in front of the person. A Maestro ask, an `AskUserQuestion` or a
chat message are all fine. It must show:

- the render;
- the source reel next to it, with its ratio;
- the script;
- the caption;
- what is synthetic;
- the cost.

For a YouTube card, also show the channel, the visibility (`privacy_status`) and the
audience (`made_for_kids`): the approval names all three.

On "yes", record the decision in the card. Instagram (`platform` and `ig_user_id`
are optional):

```json
"approval": {"by": "<person>", "at": "<ISO time>", "video_sha256": "<sha256 of final-n.mp4>"}
```

YouTube (every field required; changing visibility or audience needs a new yes):

```json
"approval": {"by": "<person>", "at": "<ISO time>", "video_sha256": "<sha256 of final-n.mp4>",
             "platform": "youtube", "channel_id": "<UC… channel id>",
             "privacy_status": "private", "made_for_kids": false}
```

The agent writes this block only after a yes, and only with the hash of the file the
person saw. **Never write an approval the person did not give.** An agent that
approves its own post has removed the only gate the loop has.

The gate checks that the approval is well formed and bound to these bytes. It
cannot prove a person gave it; that rests on the agent following this rule. Where
the approval comes from a Maestro ask or an `AskUserQuestion` answer, put that ask's
id in `approval.by` so it can be audited.

### 8 · Publish

Dry run first; it prints the container parameters, sha256 and size:

```bash
python3 scripts/reel_loop.py payload runs/<date>/card-<n>.json --video runs/<date>/final-<n>.mp4
```

Then publish. This is the only path by which bytes reach Instagram:

```bash
# Instagram (the card's default platform)
IG_ACCESS_TOKEN=… python3 scripts/reel_loop.py publish runs/<date>/card-<n>.json \
    --video runs/<date>/final-<n>.mp4 --ig-user-id <IG_USER_ID>   # add --no-go-live to stop before media_publish

# YouTube Shorts (the approval binds this exact channel)
YT_ACCESS_TOKEN=… python3 scripts/reel_loop.py publish runs/<date>/card-<n>.json \
    --video runs/<date>/final-<n>.mp4 --channel-id <CHANNEL_ID>   # --no-go-live validates metadata, sends no bytes
```

This is the only automatic path by which approved bytes reach either adapter.
Both commands exit 2 and list every reason when:

- the card is malformed (wrong types, unreadable JSON);
- the video is missing, empty, not a regular file or over 300 MB;
- there is no approval, or the approval names other bytes (a re-render needs a new
  approval);
- the card declares a cloned voice and the consent record is missing, undated,
  future-dated or points to a file that does not exist;
- an Instagram caption is over 2,200 characters, 30 hashtags or 20 @ tags;
- with `ffprobe`, the selected platform's video checks fail (Instagram codec/fps/
  duration; YouTube Short orientation and 1–180 s duration); without it they are
  reported as UNCHECKED;
- the trial strategy is invalid;
- for `publish` only, the selected platform's token is unavailable.

`is_ai_generated` is true whenever the card declares synthetic media or sets it
true. The gate cannot see synthetic media the card does not declare.

`publish` reads the video **once**, gates those bytes, and sends **those same
bytes**. Swapping or editing the file after the gate cannot change what is
published. For Instagram, in order, it:

1. creates a resumable REELS container (`POST /<IG_ID>/media`, `upload_type=resumable`);
2. sends the bytes to `https://rupload.facebook.com/ig-api-upload/<version>/<container id>`
   with `offset: 0` and `file_size`;
3. polls the container once a minute until `FINISHED`. Polling has a 5-minute
   deadline, which counts both the requests and the waits between them. No poll
   starts at or after it, and each poll's own timeout is capped at the time left
   (at least 1 s). A poll already in flight can therefore return `FINISHED` up
   to that cap after the deadline, and it is accepted;
4. calls `POST /<IG_ID>/media_publish`.

For YouTube, it confirms `--channel-id` through `channels.list`, creates the
resumable `videos.insert` session using the gated metadata, validates the returned
Google upload host, then does one PUT of the gated bytes. It never retries that
PUT. `--no-go-live` stops after the session is accepted, before any byte PUT.

A Graph API failure after the gate exits 3 and names the step. Failures include:

- an error status;
- a reply that is not a JSON object, or that carries an `error` object;
- an id that is not numeric (`--ig-user-id` is checked before any call);
- an upload `success` that is not `true`;
- a container not `FINISHED` by the deadline.

The token travels only in `Authorization` headers: `Bearer` for Graph calls,
following Meta's content-publishing guide, and `OAuth` for rupload, following the
media reference. It never goes in a URL or a request body.

Error messages carry no text from Meta or the network stack. They hold only the
step, the HTTP status, Meta's numeric error code and subcode, a byte count or an
exception type. That leaves no path for a token echoed by a server or proxy to
reach a message. No raw exception is chained to the error, and the CLI prints
only the type of an unexpected exception.

**Not yet verified live.** `publish` is tested only against a fake Graph API: the
request sequence, the bytes sent, the token handling and the failure handling. It has
never published to a real account, because that needs the owner's Instagram token
and a professional account. The first real run should use `--no-go-live`, then be
checked in the app before `media_publish` is called.

Never upload a render by any other route, whether by hand, through a hosted
`video_url` or through a third-party scheduler. Those send whatever the file or
URL holds at that moment, not the bytes that were approved. Append the receipt
(`media_id`, `sha256`) to `posts.tsv`. Plan for 50 posts per 24 h.

### 9 · Measure

At 48 h and again at 7 d, pull the media insights: `views`, `reach`, `shares`,
`saved`, `reels_skip_rate` and `ig_reels_avg_watch_time`. Never use `plays` or
`impressions`, which were removed in 2025. Insights can lag up to 48 h, so a younger
post is reported as pending, not judged.

### 10 · Trial: push variants of winners to non-followers

```bash
python3 scripts/reel_loop.py winners posts.tsv > runs/<date>/winners.json
#   --bar 2 (x our trailing-30-day median)  --min-age-hours 48  --graduation SS_PERFORMANCE
```

For each winner, the script plans three variants:

- **hook:** a new first line and first frame;
- **color:** a new grade;
- **framing:** a new crop or layout.

Each variant goes back through stages 5–8 with `"trial": {"graduation_strategy":
"SS_PERFORMANCE"}`, so Instagram graduates it to followers only if it performs.
Meta documents graduating a `MANUAL` trial in the Instagram app and documents no
API endpoint for it. Trial posts are left out of the
baseline.

Changing the variant is contested. One school reposts the proven winner unchanged
with a new caption (ericosiu's `trial-reel-distribution`). Treat that as a
registered experiment, not a default. Pick the arm before posting, write the
prediction down, and judge it at 7 d.

### 11 · Learn

Once a week, not after every post, compare outcomes with predictions:

- promote a hook pattern into `rules/hooks.md` only after it has won at least 2 of 3
  times;
- retire seed accounts that stop producing outliers.

Inside agentic-media-studio, this is the L2 playbook review: the account's
playbook changes by PR, and the evaluator is never edited in the same PR.

## Running it on a schedule

Schedule it only when the person asks: through the host's scheduler (T3
`schedule_task`, `/schedule`, or `/loop` for a session). A scheduled run does stages
1–6 and stops at stage 7 with one approval request, plus any due measurements
(stage 9). Nothing scheduled ever publishes.

## Hard rules

- Copy structure, never wording, footage, audio or a person's likeness. Credit the
  reference in the run note, not in the post.
- Clone a voice only with that person's dated consent on file. Declare synthetic
  media with `is_ai_generated`.
- Collect only from public professional accounts, at a human pace, without the
  publishing account's session. No likes, follows, comments or DMs from collection.
- No engagement pods, bought views or accounts posing as independent people.
- Comment-keyword DMs are out of scope here. If added, Meta allows one private reply
  per comment within 7 days.
- Every number in a run note comes from `reel_loop.py` output or a platform
  response, never from the agent's own arithmetic.

## Self-test

```bash
cd skills/video/reel-loop && python3 -m pytest tests/ -q
python3 scripts/reel_loop.py outliers references/example-niche.tsv --now 2026-11-16
# expect exactly one outlier: @alpha /p/A6/, about 114x; @beta's 2.6M reel is not one
```


## Lead funnel

For `@broomva.tech`, end the Reel with: “Comment WORKSPACE and I'll send you the
Act One playbook”. Register the published media ID, keyword, and separate owner
approval in the [post card](references/post-card.md#lead-funnel). Read the
[Meta rules](references/platform-contract.md#lead-funnel-polling-comments--one-private-reply)
before use. The private reply template must contain the owner-approved playbook
link; this skill supplies no assumed URL.

From `skills/video/reel-loop`. The owner's approval binds the post, keyword,
account and exact template bytes together (see the post card):

```sh
# 1. Owner: print the four values and their hashes, check them, record both hashes in card.json.
python3 scripts/reel_loop.py funnel card.json --template /path/to/act-one.txt --ig-user-id NUMERIC_IG_ID --print-binding
# Owner supplies IG_ACCESS_TOKEN through the environment; never put it in argv.
# 2. Dry run (the default): reads comments, sends nothing.
python3 scripts/reel_loop.py funnel card.json --template /path/to/act-one.txt --ig-user-id NUMERIC_IG_ID
# 3. Send. --go-live requires an explicit --ledger; always pass the SAME one.
python3 scripts/reel_loop.py funnel card.json --template /path/to/act-one.txt --ig-user-id NUMERIC_IG_ID --go-live --ledger /path/outside/git/funnel.jsonl
```

`--max-pages` (default 10, at most 100) bounds pagination.

Dry run still requires the approved template and token. It emits only comment IDs,
ages, keyword-hit flags and operational state, never comment text, usernames,
template text, or tokens. It may create an empty ledger but adds no attempts.
Only the owner runs the first live check, on their own test comment from another
account; implementation and CI use fakes only, with network connections disabled.
No credential files are read.

Dry runs default the ledger to `$XDG_STATE_HOME/reel-loop/funnel.jsonl` or
`~/.local/state/reel-loop/funnel.jsonl`. Live sends need `--ledger`, because the
default depends on the environment and two ledgers would each send. The result
prints the resolved ledger path. The ledger is mode 0600. Paths inside **any Git
repository are refused**, so no in-repo PII exception is needed. The ledger
minimizes data to comment and media IDs, a keyed hash of the commenter, template
hash, time and status; usernames, commenter IDs and comment text are not retained.
The hash key lives beside the ledger (`<ledger>.salt`, mode 0600); a used ledger
without it blocks sending. Keep it private and preserve it across runs, posts, and token
changes. Changing/deleting the ledger removes duplicate protection. Use a local
filesystem with working advisory locks and fsync (macOS/Linux).

An exclusive lock spans polling and sending. An `attempting` row is flushed and
synced (F_FULLFSYNC on macOS) **before** POST; `sent`, `failed` or `uncertain`
follows. Each commenter gets at most one reply per post; their later comments are
listed as `repeat_commenter`. Every recorded attempt blocks all future automatic
sends for that comment and that commenter. The first unsuccessful send stops the
run (`halted`): HTTP 4xx is `failed`; a timeout, network error, 5xx or a reply
without a message id is `uncertain`. Uncertain sends and crashes between
reservation and result are listed in `needs_human`; reconcile with Instagram
manually and do not delete the reservation to retry.
A malformed/torn ledger blocks sending. No client can atomically commit local
state and Meta's send: this deliberately trades possible missed replies for no
automatic duplicate after an uncertain send. No follow-up messages are sent.
