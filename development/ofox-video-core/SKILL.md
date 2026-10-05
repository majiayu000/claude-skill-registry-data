---
name: ofox-video-core
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai. Shared execution layer for the Ofox video generation API (api.ofox.ai) — creates a video job, polls it to completion, downloads the finished mp4 from a persistent CDN URL, and reports the real cost. This is a library skill, not a standalone user-facing one — it is invoked by scenario skills such as seedance-short-drama, seedance-ad-creative, and seedance-product-video, which build model/prompt/resolution choices for a specific use case and then call into this skill's script rather than re-implementing the API calls. Load this skill directly only when a user explicitly names the Ofox video API, asks to call it with specific low-level parameters, or asks to debug/resume a stuck or failed Ofox video job by job id — for a plain scenario request ("make me a short drama scene", "generate a cinematic ad clip"), use the relevant scenario skill instead, which itself depends on this one.
license: MIT
version: "2.0.3"
homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-video-core
metadata:
  author: ofoxai
  version: "2.0.3"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🎬"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-video-core
---

# ofox-video-core: Ofox video API execution layer

Wraps the Ofox video generation API (`https://api.ofox.ai/v1/videos`) behind
one script: submit a job, poll it to a terminal state, download the result,
report the exact cost. Scenario skills (`seedance-short-drama`,
`seedance-ad-creative`) call into this rather than duplicating API logic.

## Safety contract (non-negotiable)

- **The script never reads a dotenv file.** `references/ofox-video.sh` resolves
  `OFOX_API_KEY` from the shell environment only, and the key is never
  hardcoded in a script or a skill file.
- **You may load the key from a dotenv file once the user has authorized it.**
  Locate it (`.env` at the repo root is the usual spot), then
  `set -a; . <path>; set +a` in the shell you'll call the script from. Sourcing
  a dotenv pulls in *every* variable in the file, not just the key —
  `OFOX_API_BASE_URL` is one this script reads, and it redirects every API call
  — so read the file before you load it. Never echo the value.
- **The key goes to exactly one host, and you are told when that host is not
  Ofox.** Since 1.30.0 `OFOX_API_BASE_URL` must be `https://` (a loopback host
  may be `http://`, for a local test server) and an override prints a `NOTE:`
  on stderr naming the host that will receive the key. Relay that line if you
  see it: it is the difference between "we are talking to Ofox" and "we are
  talking to whatever that variable says". And the `polling_url` the API
  returns in its create response — which the poll loop authenticates to — is
  followed only when it is on the same scheme/host/port as the base. A
  response pointing somewhere else stops the run with the job id printed, so
  the job you already paid for is collected with `poll`, not abandoned.
- **Never print, log, or echo the raw key value** — not in chat, not in a
  file, not in a command you show the user, not in verbose curl output.
  `references/ofox-video.sh` never uses `curl -v`/`--trace` for exactly this
  reason (those would print the `Authorization` header). If you need to
  show that a key is configured, say "OFOX_API_KEY is set" — never the value.
- Never write the key into any file this skill (or a skill built on it)
  creates, including logs, cost reports, or committed code.
- **Check once, then proceed.** Run the availability/key check at most once
  per session (see below). If it passes, don't re-prompt for the key on
  every subsequent call in that session.
- **Fail open on a missing key** — guide the user to get one, don't dead-end
  the conversation. A missing key means "can't call the paid API yet," not
  "stop talking to me."

## Which model, and what it costs

`bash references/ofox-video.sh models` lists every video model Ofox serves with
its duration range, resolutions, modes and base per-second price. It needs
**no API key** — `GET /v1/models` is public — so it is safe to run before the
user has signed up, and it costs nothing.

⚠️ **The `modes` column under-reports, so do not read it as a capability
list.** Every model's entry says `t2v i2v v2v` and nothing else, and
reference-to-video through `input_references` was measured working on
`bytedance/seedance-2.5` on 2026-09-16 (job `0f5c8b4e`, two image references,
44 cents, billed at the plain t2v rate). The duration, resolution and
aspect-ratio columns are a different matter — those are what the script
enforces against and they have held up. Detail, and what the same session
measured about the `mode` request field — accepted, discarded, and therefore
no route to extend or edit — is in
[`references/api-params.md`](references/api-params.md).

The rate `models` prints is the one at each model's **own default
resolution**, and that default is not the same tier for every model. It ranks
models; it does not quote them. For the rate at the tier you are actually
about to send, run `providers MODEL` — it prints the per-resolution,
per-upstream matrix, and that is the quotable source:

```bash
bash references/ofox-video.sh models                              # rank
bash references/ofox-video.sh providers bytedance/seedance-2.0-mini  # then quote
```

⚠️ **`providers` with no model argument prints the flagship's matrix, not the
catalog.** Pass the id you mean.

The spread between the cheap end and the flagship is large — several times the
per-second rate at the same resolution — which is why, when a user is going to
generate several takes and keep one, drafting on a cheap model and rendering
the keeper on `seedance-2.5` costs a fraction of drafting everything on 2.5.
Say so when it's relevant, with numbers you just read rather than remembered,
and don't switch models on someone's behalf: the model changes the look, not
just the price.

Parameter limits differ per model — duration range, resolution tiers and
aspect-ratio list all vary, and they vary *within* a family, so `wan-*` or
`seedance-2.0-*` is not a safe thing to generalise over. The script enforces
the real per-model ones and `models` prints them; read it rather than
recalling a range. The limits come from the live model list, cached for
24 hours, falling back to a bundled snapshot when offline — a fallback is
always announced on stderr, never silent.

## Multi-shot sequences (`chain`)

One job is one 4-30 second clip, and that clip **can** hold several hard-cut
shots marked with timestamps — verified on this path, with the job ids and
the untested range in `references/prompt-structure.md`, "Several shots in one
job". So a multi-shot sequence does not automatically mean several jobs.

`chain` is for **continuity across jobs**: when a sequence runs past one
job's duration ceiling, or when each shot needs its own approval, seed or
resolution. Separate jobs share nothing, so left alone their set, lighting
and framing drift apart; `chain` carries each shot's closing frame into the
next one as its opening frame. The two mechanisms combine rather than compete
— every job in a chain can itself contain several timestamped shots:

```bash
bash references/ofox-video.sh chain --approved \
  --shot "a white cup on a dark table, steam rising, static camera" \
  --shot "the camera pushes in slowly toward the same cup" \
  --duration 4 --resolution 480p
```

Or `--shots-file shots.txt`, one prompt per line (blank lines and `#`
comments ignored). Capped at 10 shots per run.

⚠️ **One prompt per line means one prompt per line — a templated prompt does
not go in this file.** `references/prompt-structure.md` teaches prompts
written across several lines (`STYLE:` / `SUBJECT:` / `SCENE:` / `CAMERA:` /
`CONSISTENCY:` / `SOUND:` / `AVOID:`, plus a timestamped body), and every
scenario skill writes them that way. Put one of those in a shots file and
each *line* becomes its own separately billed job: a 5-line prompt priced out
at $34.80 for five 29-second jobs, and the estimate looked entirely ordinary,
because a fragment is a valid prompt — nothing crashes, you just buy five
quarter-sentences at full length.

So the script now **refuses** a shots file whose lines open with an ALL-CAPS
label, naming the offending line, before the estimate is printed and before
anything is submitted. It does not try to re-join the lines for you: guessing
at what someone meant, with their money, is worse than stopping.

The signal is deliberately broad — any leading `[A-Z ]+:` — so a genuine
one-line prompt that opens with a label (`CLOSE UP: a mug on a table`) is
caught too. That trade is on purpose: a false positive costs one edit to the
command, a false negative costs a job per line. `--shot` takes such a prompt
as written, and `SHOT 1: ...` is not caught at all, since a digit ends the
label.

**For a multi-line prompt, use a repeated `--shot`** — one `--shot` value is
one prompt however many newlines it contains, which is the case a shots file
cannot express:

```bash
bash references/ofox-video.sh chain --approved \
  --shot "$(cat shot1.txt)" \
  --shot "$(cat shot2.txt)" \
  --duration 8 --resolution 480p
```

A shots file is for the other case: short one-line prompts, one per shot,
which is what the example above is.

**Verified behavior**: shot 2 opens on very nearly the exact frame it was
fed — cup position and scale, window frame, table grain, light direction all
carried over — and then follows its own prompt from there. This is real
continuity, not just matched framing. Brightness can shift slightly across a
seam.

What it does:

- Estimates the whole sequence before spending, then reports real per-shot
  cost from each job's `usage.video_cost`.
- **Stops on the first failure.** Shots already generated are kept, downloaded
  and listed with their real cost; the remaining shots are never submitted.
- Joins the finished shots into one file with ffmpeg (`--no-concat` to skip),
  re-encoding only if the clips' codecs differ. Fails open: no join, never a
  lost shot.
- Shot 1 takes a normal `--aspect-ratio`. Shots 2+ are image-to-video: on
  Seedance 2.5 the API requires `adaptive` there, so they inherit framing from
  the fed frame whatever you passed; on another model they inherit it only when
  you passed no `--aspect-ratio` and that model offers `adaptive` (an explicit
  ratio is kept on every shot instead). Either way the sequence stays
  dimensionally consistent, and each shot prints which of the two it did.

`chain` needs `ffmpeg`, and checks for it **before** submitting anything, so
a missing dependency never costs a paid shot.

### The one hard limit: real people, unless they are yours to use

**Seedance 2.5 image-to-video rejects reference frames containing a real
person** — `HTTP 400 / input_moderation_failed`, "may contain real person".
Nothing is generated and nothing is billed, but the chain stops there.

So by default chaining works for products, landscapes, illustration and
anime, and **does not work for live-action human sequences** on this model.
That is why `seedance-anime-drama` can open each of its shots on a generated
frame of the character while a short-drama sequence cannot.

**`--real-person true` lifts that refusal on 2.5 — measured 2026-09-16 — and
it is an authorization mechanism, not a way past the check.** Ofox's own words
for it are "privacy-preserving preprocessing for AUTHORIZED real-person
references": setting it asserts that the user has the right to use that
likeness. So it opens a real-person chain **only for footage the user may
actually use**, and only after they have said so. Never set it to make a
refused job go through, never offer it as a retry for
`input_moderation_failed`, and never for an identifiable public figure — the
flag asserts authorization, it cannot create it. The A/B behind this, and the
five things it does not establish (one upstream, one tier and mode, a
synthetic portrait rather than a real photograph, likeness fidelity, one
model), are in
[`references/api-params.md`](references/api-params.md) →
"`--real-person true` lifts that refusal on 2.5".

### Extracting a frame on its own

```bash
bash references/ofox-video.sh last-frame clip.mp4 [--out-dir DIR]
```

No API call, no key, no cost. Grabs a frame just before the end (the literal
final frame is often a fade), for feeding into a later `generate` by hand.

**"Just before" is 0.1 second.** The step-back is not a guess you have to
make — it seeks to `duration - 0.1s`, reading the duration from `ffprobe`,
and takes the first frame at or after that point. So on a clip whose frame
interval is under 0.1s the frame is within one frame of the end, and it is
never the literal last frame unless that frame happens to land exactly there.
Measured on a 2.000s clip at 10fps: the frame returned is the one at 1.9s.

**The fallback is 0.5 second**, and only runs when `ffprobe` reports no
duration or that seek yields no frame: `-sseof -0.5` takes the first frame of
the final half second. Same clip, that branch returns the frame at 1.5s.

Why the number matters: what you extract here is what a later job opens on,
so it fixes the seam. Carry the original clip whole and append the new one and
the overlap is that 0.1s (or 0.5s on the fallback), not a duration you have to
work out. `frame-at`, below, is the command for stepping back further on
purpose.

### Grabbing the frame at a chosen second

```bash
bash references/ofox-video.sh frame-at clip.mp4 --at 3.2 [--out-dir DIR]
```

No API call, no key, no cost. `last-frame` answers *where did this clip end*;
`frame-at` answers *what did it look like at second 3.2* — which is what you
need to re-shoot a clip from a chosen point rather than only past its end.

`--at` is required rather than defaulted: this frame is usually about to be
fed to a paid image-to-video job, so a guessed timestamp is a job billed for
the wrong picture. A timestamp at or past the end is an error naming the
clip's real duration, not an empty file.

What it does **not** give you: re-shooting from second 3.2 regenerates
everything after 3.2. There is no mechanism here for changing the middle of a
clip and keeping the ending you already have.

## Generating several takes (`batch`)

Video generation is a slot machine: you generate several, keep one. `batch`
makes that one command, and — the part nobody else does — tells you what it
actually cost.

```bash
bash references/ofox-video.sh batch --approved --prompt "..." --takes 3 [OPTIONS]
```

Every option `generate` takes works here. What `batch` adds:

- **An estimate before it spends anything**, and a real total afterward built
  from each job's own `usage.video_cost` — never from the estimate.
- **Every take reports its seed** (`TAKE 3 <job-id> seed=1852049 <cost> <path>`).
  The takes differ only by seed, so the seed is how "take 3 was the good one"
  gets recorded at all — without it there is nothing to name a take by. It is
  **not** a guarantee: re-running the same prompt and seed at a higher
  resolution aims at that take, and a fixed seed has been measured returning a
  visibly different clip on an identical request. See "Re-attempting a shot"
  before promising a user their take back.
- **`BATCH_COST_TOTAL` is the number to quote**, not `BATCH_COST_PER_TAKE`.
  Gacha means most takes go in the bin: if one take in three is usable, that
  clip cost you the whole total, because you paid for the two you threw away.
  `BATCH_COST_PER_TAKE` is just the total divided by the count — useful for
  sanity-checking the bill, misleading as a cost-per-usable-clip figure. The
  total is what compares meaningfully across models and settings.
- **A contact sheet** (`--no-contact-sheet` to skip): three frames from each
  take, tiled one row per take, so a human can pick a winner from one image
  instead of opening N files. Needs `ffmpeg`; without it the sheet is skipped
  with a reason and the videos are untouched.
- **A stop on first failure — at submission.** If take 2's create is
  rejected, takes 3..N are not submitted. Whatever broke it will almost
  certainly break the rest, and each attempt is real money. A take that fails
  *after* submission is a different case and does not stop the others; see
  "Multiple takes of one prompt" below.
- **A warning if you pass `--seed`**, since a fixed seed makes every take ask
  for the same generation — billed N times for variation you did not choose.
  (Not "N identical clips": they may still differ, because a fixed seed does
  not make this API reproducible. The advice is the same either way.)

Takes are **created one at a time and waited for concurrently**, each as its
own job through the same path a single `generate` uses. The sequential half is
what keeps the money guard exact; the concurrent half is where the ten minutes
per clip used to be multiplied by the take count. `--concurrency` caps the
waiting (default 4); the reasoning behind that number is under "Waiting in
parallel".

`--takes` is capped at 10 per run.

### The pattern worth suggesting

Draft cheap, render the keeper expensive:

```bash
# 5 drafts at 480p on the cheapest model — about 40 cents
bash references/ofox-video.sh batch --approved --prompt "..." --takes 5 \
  --model bytedance/seedance-2.0-mini --resolution 480p --duration 4

# then the winner, on the good model
bash references/ofox-video.sh generate --approved --prompt "<the one that worked>" \
  --model bytedance/seedance-2.5 --resolution 1080p --duration 4
```

The same five drafts on `seedance-2.5` at 720p would be $4.80. Offer the
ladder — but let the user choose the model, since a different model is a
different look, not just a different price. All five drafts are waited for at
once, so the ladder costs one clip's wall clock for its first rung rather than
five.

### Re-tiling videos you already have

```bash
bash references/ofox-video.sh contact-sheet clip1.mp4 clip2.mp4 [--out-dir DIR]
```

No API call, no key, no cost. Useful for comparing takes from separate runs,
or rebuilding a sheet you skipped.

### Putting your own audio on a clip

```bash
bash references/ofox-video.sh mux-audio clip.mp4 track.mp3 [--out-dir DIR]
```

No API call, no key, no cost — and **the only way to get a specific audio
track onto a clip.** Sending the audio to the API as an `input_references`
element does not do it: the field is parsed, validated and fetched, and the
delivered clip still carries a model-generated track. That is measured, not
inferred — see `references/api-params.md`.

It **replaces** the clip's own audio rather than mixing with it: generated
clips arrive with a model-made soundtrack, and layering two is never what the
caller meant.

The result runs to the shorter of the two inputs. When they differ by more
than half a second the command says which one was cut and by how much, and
still writes the file — a mismatch is a note, not a failure.

## How long this blocks, and why that matters

`generate` waits for the job: it polls until the video is ready, up to
`--max-wait` seconds (default **540**, i.e. nine minutes). A 4-second 480p clip
usually lands in one to three minutes; longer and higher-resolution jobs take
longer.

**That is longer than most agent tool calls allow by default.** Claude Code's
Bash tool defaults to a 120-second timeout and caps at 600. If your tool call
dies while `generate` is still polling, you land in the one genuinely bad
state: the job was created and is billable, and its id was never printed, so
you cannot poll for it and cannot tell the user where their video went.

Two ways to stay out of that, in order of preference:

**1. Submit and wait separately.** `create` does the submit and returns
immediately — seconds, not minutes — printing the job id. Then poll in
however many short calls it takes:

```bash
bash references/ofox-video.sh create --approved --prompt "..." --duration 15 --out-dir ./out
# -> STATUS submitted
#    JOB_ID 7b41f0c9-...
#    POLLING_URL https://api.ofox.ai/v1/videos/7b41f0c9-...

bash references/ofox-video.sh poll 7b41f0c9-... --out-dir ./out
```

The job id exists on disk in your transcript the moment it is created, so no
timeout can strand it. This is the right shape whenever you cannot raise your
own tool timeout.

**2. Raise the timeout for the call.** If your harness lets you set a
per-call timeout, give `generate` at least `--max-wait` plus a margin.

**`batch` still needs this attention most**, even though its waiting is now
concurrent. Four takes finish in about the time of one, but that one is still
minutes — a 15-second 720p job measured **over 600 seconds** of wall clock on
2026-09-05, which is more than any single Bash tool call can be given. Either
lower `--max-wait` (a 4-second draft rarely needs 540s; 240 is generous), or
`create` each take and poll them yourself. Tell the user roughly how long it
will take before starting.

## Waiting in parallel

The wall clock is the binding constraint on a multi-clip session, and it is
not the API's fault. The account this was measured on allows **100 requests
per minute**, while a polling job issues one request per `--poll-interval` —
ten a minute at the default. Nothing about the rate limit required waiting for
clips one at a time; the old serial `batch` simply did.

### Across clips: parallelise, always

N independent clips are N `create` calls (seconds each) and then **one** `poll`
over every job id:

```bash
# submit all three; each returns in seconds with its own job id
bash references/ofox-video.sh create --approved --prompt "<shot A>" --duration 15 \
  --resolution 720p --name "kitchen argument" --out-dir ./out
bash references/ofox-video.sh create --approved --prompt "<shot B>" --duration 15 \
  --resolution 720p --name "she walks out" --out-dir ./out
bash references/ofox-video.sh create --approved --prompt "<shot C>" --duration 15 \
  --resolution 720p --name "the station" --out-dir ./out

# then wait for all three at once, not one after another
bash references/ofox-video.sh poll 7b41f0c9-... 2c8e5511-... 9ad0b7e3-... \
  --out-dir ./out
```

Each job's own output is replayed under a `=== JOB i/N <id> ===` delimiter in
**the order the ids were given**, whatever order they finished in, so
`VIDEO_PATH` and `VIDEO_COST` read exactly as they do for a single poll.
`POLL_COST_TOTAL` sums the real bills. Exit is 0 when all completed, 3 if any
job failed (a failure needs a new prompt), 4 if any is merely still running (a
timeout needs another poll).

This primitive is not new — `create` and `poll` have been separate subcommands
for as long as they have existed, and until 2026-09-05 no agent used them this
way. Three 15-second clips serially is half an hour; the same three this way
is ten minutes.

### Within one clip: you cannot, so don't try

Image-to-video has a hard dependency in the middle of it: the first frame has
to **exist** before the video job can be submitted. `seedance-anime-drama`'s
two phases, and any `--frame-first-image` flow, are image → then video, and
that ordering is the whole mechanism. `chain` is the same shape — each shot
opens on the previous shot's closing frame, so shot 2 cannot be submitted
until shot 1 has been downloaded and its last frame extracted.

So that stretch of wall clock is irreducible. What is parallelisable is
everything *across* those pipelines: four clips that each need an image can
have all four images generated, then all four videos created, then all four
polled together.

### Multiple takes of one prompt is the highest-value case

Video generation is a slot machine, and the reason to pull the lever more than
once is not variety — it is that a take can quietly fail to render what the
prompt asked for. Measured on 2026-09-05: job
`60fbea52-b14b-4796-80bf-03afe0aa4fa0` came back technically clean with its
written climax missing — a drop that was supposed to fall never detached from
the surface. Nothing was wrong with the prompt, the parameters or the bill.

Serially, the answer to that was a re-run and another ten minutes. Concurrently
it costs the same wall clock as the first attempt:

```bash
bash references/ofox-video.sh batch --approved --prompt "..." --takes 3 \
  --duration 15 --resolution 720p --out-dir ./out
```

`batch` now **creates one take at a time and waits for all of them at once**.
The two halves are deliberately different, and the difference is the money
guard: a create answers in seconds, so serialising it is nearly free and it is
the only ordering in which "take 2 was rejected, so takes 3..N were never
sent" can be true. Firing N creates at once would spend N times to learn the
first one was going to fail.

What follows from the split:

- **A take rejected at submission stops the run.** Takes already submitted are
  still waited for and downloaded — they are billable whether or not you
  collect them, and abandoning a paid job is not a saving.
- **A take that fails after submission** (a generation-time or moderation
  failure) does not touch the others. It is reported as `TAKE 2 <id>
  seed=<n> FAILED exit=3`, keeping its take number, id and seed, and the rest
  complete normally. A job that ends `failed` carries no `usage` and is not
  billed.
- **`STATUS batch_partial`** replaces `batch_completed` whenever the run is
  not what was asked for, alongside explicit `TAKES_SUBMITTED`,
  `TAKES_COMPLETED`, `TAKES_FAILED`, `TAKES_RUNNING` and
  `TAKES_NOT_SUBMITTED` counts. Don't read a partial run as a complete one.
- **Attribution is by take, not by finish order.** Takes land in whatever
  order the API feels like; the seed printed against take 3 is take 3's, or
  "re-render take 3 at 1080p" spends money on the wrong clip.

### `--concurrency`: the number, and where it comes from

`--concurrency N` (also `OFOX_POLL_CONCURRENCY`) caps how many jobs are
**waited for** at once, on both `batch` and a multi-id `poll`. Default **4**,
ceiling **10**.

Both numbers are requests per minute, not a guess at what feels safe. One
polling job issues at most one GET per `--poll-interval`, so at the default 6s
it spends 10 of the account's 100 RPM. Ten concurrent polls is therefore
exactly the whole limit, which is why 10 is the ceiling and never the default.
Four is 40%, and the other 60% is not spare: a batch's creates go out first, a
429 or a 5xx retries at the same cadence, and an agent commonly has another
Ofox call in flight in the same session.

Lowering `--poll-interval` multiplies the rate — four polls a second apart is
240 RPM — so the script computes the implied rate and says so when the
combination crowds the limit. It warns rather than blocks: rate limiting costs
a poll cycle per job, which is time, not money, and each job backs off further
on each consecutive 429 until a request gets through.

### Money is the constraint, not the rate

Concurrency does not make a batch cheaper. It makes **N bills arrive at once**,
which is exactly why the cost table has to be on screen before it starts, not
after. `batch --dry-run` prints one `Estimated cost:` line for the whole batch
plus a `CONCURRENCY` line; that total is what
[`references/approval-gate.md`](./references/approval-gate.md) requires you to
quote, itemised, with the takes as rows — never `BATCH_COST_PER_TAKE`.
`--takes` is still capped at 10 for the same reason it always was: a cap on how
much one command can spend.

## Quote the price before you spend it

**Never submit a paid job until the user has seen a cost table and said yes.**
The rule and the table format are shared by every Ofox skill in this repo and
written down once, in
[`references/approval-gate.md`](references/approval-gate.md) — required
columns, where the numbers must come from, how to itemise a batch, what to do
when no estimate is possible, and how a two-phase (image then video) flow
splits into two approvals. This section is the mechanics that feed it.

`generate`, `batch` and `chain` all take **`--dry-run`**: they parse arguments,
validate every parameter against the chosen model, resolve the upstream, build
the payload and print the cost estimate — then stop. No request is sent and
nothing is billed.

That flow is the one to follow whenever real money is involved:

```bash
# 1. price it
bash references/ofox-video.sh generate --dry-run --prompt "..." --duration 15 --resolution 720p
#    -> Estimated cost: ~$3.60 (15s x 24 cents/s)...
#    -> DRY RUN — nothing was submitted and nothing was billed.

# 2. tell the user the number, get a yes

# 3. run the identical command with --dry-run swapped for --approved
bash references/ofox-video.sh generate --approved --prompt "..." --duration 15 --resolution 720p
```

**Do not skip step 2.** The estimate a real run prints appears microseconds
before the request goes out — by the time you could relay it, the job exists
and is billable. `--dry-run` is what makes quoting-then-confirming possible.

### `--approved` is required, and `--dry-run` never needs it

Since 2.0.0 the four subcommands that can bill — `generate`, `create`, `batch`,
`chain` — refuse to run without **`--approved`**, printing the three steps
above and submitting nothing. Nothing else is gated: `check`, `models`,
`providers`, the four local ffmpeg tools, and — deliberately — **`poll`**,
which is the command that collects a job you have already paid for.

Be accurate about what the flag is. **It records a stance; it cannot prove
one.** No shell script can see the conversation between an agent and its user,
and an agent is perfectly able to type `--approved` without ever showing anyone
a price. What changed is that spending without quoting is no longer what
happens by default — it now has to be written into the command, where a
transcript shows it and a reviewer can object to it. Do not describe this as
"approval is enforced".

`--dry-run` works with no `--approved` and no API key, because the quote is how
the number being approved is produced; a gate in front of it would close the
only route through itself.

A dry run also catches a bad parameter for free, so an invalid combination
costs a message instead of a job.

Every run prints exactly one `Estimated cost:` line, including when it cannot
compute one — it says why (no `--duration`, or no verified rate for that
model/resolution). Relay whichever line you get; never substitute a number of
your own, and never present an estimate as the bill.

## Which upstream serves the job

Seedance is served by two upstreams, and by default Ofox picks one by weight —
its docs say outright that "which provider serves any single request is not
predictable". They moderate differently, so an unpinned job that comes back
`output_moderation_failed` may just have landed on the stricter one, with
nothing for the user to point at.

**This skill pins Seedance to `byteplus`.** No flag needed, no network call to
decide it.

| | `volcengine` | `byteplus` (default) |
|---|---|---|
| Platform | Volcengine Ark, mainland China | BytePlus, markets outside mainland China |
| Moderation | Standard | More permissive |
| Price | identical | identical |

Pricing is identical across the two — this is a region and moderation choice,
never a cost one. Say so if a user asks which is cheaper.

```bash
bash references/ofox-video.sh generate --approved --provider volcengine ...  # mainland
bash references/ofox-video.sh generate --approved --provider auto ...        # let Ofox route
export OFOX_VIDEO_PROVIDER=volcengine                             # persistent default
bash references/ofox-video.sh providers                           # see a model's upstreams
```

Models with only one upstream (`alibaba/*` today) get no pin — routing there
is already deterministic.

If a job fails `output_moderation_failed`, retrying on the other upstream is a
real fix and is worth offering: the rejected job was never billed, and a retry
is a new request, not a resubmission.

## No key? You can still get a price

`models`, `providers` and any `--dry-run` all work with `OFOX_API_KEY` unset.
They hit public endpoints or make no request at all, so someone who has not
signed up can price a job, compare resolutions, and cost out a batch before
deciding whether to register.

**When a user has no key, quote first and point at signup second.** Opening
with "go get an API key" sends someone to a form before they know whether the
thing is worth 44 cents or $7.20. Run the dry run, show them the number, then
point at [app.ofox.ai](https://app.ofox.ai) if they want to proceed.

## Availability check

Before the first call in a session, verify the environment:

```bash
bash references/ofox-video.sh check
```

This checks `curl`, `jq`, and `OFOX_API_KEY` and exits `0` only if all three
are present — it makes no network call. Handle each failure mode plainly:

- **`curl` missing** (rare — usually preinstalled): `brew install curl`
  (macOS) or `sudo apt-get install curl` (Debian/Ubuntu), else
  https://curl.se/download.html.
- **`jq` missing**: `brew install jq` (macOS) or `sudo apt-get install jq`
  (Debian/Ubuntu), else https://jqlang.org/download/.
- **`OFOX_API_KEY` missing**: two paths, and the second one is the one
  agents forget. If the user has no key, they get one at
  `https://app.ofox.ai` (log in → Settings → API Keys → Create New Key,
  shown once) and `export OFOX_API_KEY=...` in their shell. If they say the
  key already lives in a file, don't send them back to the terminal to
  re-type it — load it yourself with `set -a; . <path>; set +a` in the shell
  you'll call the script from (see the safety contract: authorization first,
  read the file before sourcing it, never echo the value). Offer this once,
  plainly, and move on — don't repeat the pitch on every message.

## Invoking the script

```bash
bash references/ofox-video.sh models
bash references/ofox-video.sh generate --dry-run --prompt "..." [OPTIONS]
bash references/ofox-video.sh generate --approved --prompt "..." [OPTIONS]
bash references/ofox-video.sh poll JOB_ID [--out-dir DIR] [--name TEXT]
bash references/ofox-video.sh poll JOB_ID JOB_ID JOB_ID [--concurrency N]
```

`generate` builds the request, validates parameters client-side against the
chosen model's real limits (rejecting a bad `resolution`/`aspect_ratio`/
`duration` before any network call), submits it, polls to a terminal state,
downloads the video into `--out-dir` (default: the current directory), and
prints:

```
STATUS completed
JOB_ID <id>
VIDEO_PATH <path/to/file.mp4>
SIDECAR_PATH <path/to/file.json>
VIDEO_SECONDS <billed seconds>
VIDEO_COST <exact cost from usage.video_cost>
```

## Name the output file

Pass `--name` with a short description of what the clip actually is:

```bash
bash references/ofox-video.sh generate --approved --prompt "..." --name "convenience store breakup"
```

The file lands as `convenience-store-breakup-d12c2787.mp4` instead of a bare
job id, with a `convenience-store-breakup-d12c2787.json` sidecar beside it.

Without `--name` the slug is derived from the prompt, so a `poll JOB_ID` run
in a fresh shell still produces something readable. That fallback is a
consolation prize, not the goal: prompts open on setting and lighting, so the
derived name usually describes the room rather than the scene. **A scenario
skill always knows the better name — pass it.**

The 8-hex suffix keeps two runs of the same prompt from overwriting each
other. It is not a way back to the job: nothing expands a prefix into a full
id. A recent job can often be recovered anyway by listing `GET /v1/videos`
and matching the prefix — see "The recovery step" — but only while it is
still on the list, so that is a rescue, not the record. The sidecar carries
the full `job_id`, the prompt, the real cost, and the `request` as submitted —
the only place `resolution`, `aspect_ratio` and `seed` are recorded, since the
poll response echoes none of them. Full field table in
[`references/api-params.md`](references/api-params.md).

## Re-attempting a shot

Every job now has a seed: without `--seed` the script rolls one, sends it,
and prints it as `SEED <n>`. Before, the server picked a seed and reported it
nowhere, so a take could not even be described after the fact, let alone
aimed at again. **Recording the request is what the seed buys — not a
guarantee, see below.**

That seed and the rest of the request land in the sidecar, so re-submitting
the same shot at a higher resolution is a matter of reading it back:

```bash
jq -r '.request | "--prompt \(.prompt|@sh) --seed \(.seed) --aspect-ratio \(.aspect_ratio)"' out/my-shot-3e830902.json
```

`create` + `poll` keeps this intact across the two processes by leaving the
payload in `<out-dir>/.ofox-request-<job id>.json` for the poll to pick up
and clean away. Poll into a different `--out-dir` and the handoff is simply
not found — the sidecar omits `request`, nothing fails.

### A fixed seed does not make this API reproducible

Not even with a byte-identical prompt. **Measured 2026-09-15**: three jobs on
`bytedance/seedance-2.0-mini`, 4s / 480p / 16:9, seed `424242`, the same
one-sentence prompt submitted verbatim each time.

| Job | Outcome |
|---|---|
| `2e45464c-9ea7-4836-96dd-93dffb5ef58d` | completed, 8 cents |
| `cf877512-3faf-42b5-92ad-2e83fa55dabf` | **failed** `output_moderation_failed`, not billed |
| `ef83ccb8-7147-416f-a4af-e2fb04a618d1` | completed, 8 cents |

The two that completed are not the same clip. Locating the single red balloon
in extracted frames: at t=1s it sits at (484, 419) with 23,668 red pixels in
one and at (431, 335) with 1,785 in the other — a different position and
**13x the area**. Same at t=3s. That is a different generation, not encoding
noise. The middle row is the sharper point: one of three runs of an identical
request did not come back at all.

Measured on that model, at that duration and tier. Nothing here says a
different model is better behaved — but nothing in this repo ever measured one
that was, either, and the claim this passage used to make had never been
tested on any model.

#### The content is irreproducible. The frame size is not — keep them apart

Everything above is about what the clip **shows**. Its **dimensions** behave
the opposite way, and the two must not be allowed to erode each other. The
same 720x480 (3:2) frame, fed to `bytedance/seedance-2.5` at 480p in two
independent jobs — `35b6aed1` and `69bc799d` — came back **794x530 both
times**. Output size is decided by the resolution tier and the frame's ratio,
not by the input file's pixel count and not by the seed.

So an editor planning a join can rely on the geometry while relying on nothing
else about the take, and "you cannot get the same clip twice" is a statement
about the picture only. Do not stretch it into "the size might change", and do
not read the stable size as evidence that anything else is reproducible.

**A byte-identical prompt is still necessary; it is just not sufficient.**
Measured on 2026-09-05: two jobs ran the same seed `642303335` at the same
duration, resolution, aspect ratio and model, differing only in the wording of
one paragraph in the middle of the prompt — and they came back with visibly
*different subjects*, not merely different takes on one subject (a wide steel
collar on a short body versus a narrow collar on a longer body, with the one
asymmetric feature pointing the other way). Jobs
`1cf5ac46-058f-4615-a47b-067743f76f8c` and
`50f623b2-c54a-4d9d-9646-31dd06e2a926`. That run tested *changed prompt →
changed result* and established it. Until 2026-09-15 this document read the
converse off it — "the seed reproduces a take when the prompt is
byte-identical" — which nobody had tested. It is false.

So what the seed is actually for:

- **Recording what was sent.** A job whose seed nobody knows cannot even be
  described, let alone re-attempted. That is why the script rolls and prints
  one.
- **Re-attempting a take** — the same prompt, the same seed, `--resolution`
  stepped up. Treat it as another roll aimed at the same shot, not as the same
  clip larger, and **say so to the user before they pay for it**. A
  re-render that comes back different is the documented behaviour, not a
  fault.
- It is **not** a handle for "that one was good, now fix the third shot".
  Editing the prompt and keeping the seed preserves nothing you liked — that
  is the 2026-09-05 measurement — and even leaving the prompt alone does not.

Read the prompt back out of the sidecar rather than retyping it, which is what
the `jq` line above is for; a retyped prompt is a new prompt, and starting
from a new prompt removes the one condition that is at least necessary.

A sidecar that cannot be written is a warning, never a failed download — the
video is what the user paid for.

Download source: `mirror_urls` (CDN-signed, persistent) when present,
falling back to `unsigned_urls` (documented as temporary, may expire within
24h) when `mirror_urls` is absent or empty — this is not just a theoretical
fallback, real completed jobs have been observed with no `mirror_urls` field
at all. Once downloaded, the result is a local file either way, so a video
saved from `unsigned_urls` should be treated identically to one saved from
`mirror_urls` from this point on — the expiry window no longer matters once
the file is on disk.

Key flags: `--model` (default `bytedance/seedance-2.5`), `--duration`,
`--resolution`, `--aspect-ratio` (includes `adaptive` — see below), `--size`,
`--generate-audio true|false`, `--seed`, `--frame-first-image URL|PATH`,
`--frame-last-image URL|PATH`, `--real-person true|false` (**an authorization
assertion about the attached likeness, not a moderation switch** — read the
real-person section of `references/api-params.md` before you pass it),
`--callback-url`, `--extra-json '<json>'` (a JSON **object** of fields not covered
by a flag, e.g. `input_references`, `provider.options` — it may not be empty, and
it may not set a field that has a flag; see below),
`--max-wait SECONDS` (default 540),
`--poll-interval SECONDS` (default 6). Full parameter reference:
`references/api-params.md`. Pricing and the cost-estimate formula:
`references/pricing.md`.

### Video references: rerender and continuation are different prompts

A video inside `input_references` is a measured route, not only a documented
field. Two 4-second / 480p Seedance 2.5 jobs on `byteplus` established two
different prompt contracts: one preserved four compositions, their order,
motion directions and hard boundaries while changing the visual treatment;
the other began from the source's final state and continued into new space
without replaying its earlier layouts. The jobs, artifact-level readings and
untested range are in `references/api-params.md`.

This does **not** make video input a precise frame anchor. It is one measured
pair on one synthetic control, model, upstream, duration and tier. A video
must be supplied as a public web URL: the current route rejected a small
`data:video/mp4` URI before job creation. The core also refuses a video
reference together with `frame_images` before estimate or submission. That
last statement is a shipped-client boundary, not a claim about direct API
calls that bypass this script. For the scenario workflow and manual
frame-by-frame review, use
[`previs-rerender`](../previs-rerender/SKILL.md).

⚠️ **There is no way to supply the audio.** `input_references` documents an
audio allowance and the server really does accept, validate and fetch an
`audio_url` — and then generates its own track anyway: a real speech clip was
supplied and the delivered audio is not it (measured, job
`d8561509-dcc6-4f2c-8864-a193cd239b14`). No lip-sync, no voice-over input. Use
`--generate-audio` and the prompt for what the clip says; add a supplied voice
track in an editor afterwards. Details in `references/api-params.md`.

### Image-to-video: local files, remote URLs, and the `adaptive` aspect ratio

`--frame-first-image`/`--frame-last-image` accept either a remote
`http://`/`https://` URL (used as-is) or a local, readable file path — the
script auto-detects a local file and base64-encodes it into a
`data:image/<ext>;base64,...` URI before building the request (content-type
inferred from the file extension, `image/jpeg` as the safe default when the
extension isn't recognized). **Prefer a local file when one is available**:
real testing found at least one otherwise-valid, publicly reachable image
URL rejected by the upstream provider with a download-failure-shaped error,
while the same image worked reliably once base64-encoded — likely
bot/hotlink protection on some hosts, not something under our control.

Local files of any realistic size are supported: the base64 data URI is
built into the request body via a temp file and `jq --rawfile`/`--slurpfile`
and posted to the API via `curl --data-binary @file`, never via a `jq
--arg`/`--argjson` or `curl -d` **command-line** value. An earlier version
of this script did the latter and broke on any real photo whose base64
encoding exceeded the OS's `ARG_MAX` (roughly any real photo over ~750KB) —
seen with a real 885KB PNG (1,179,996-byte base64 encoding) producing
`jq: Argument list too long`. Fixed 2026-08-29, and re-verified 2026-09-17
on a 1.9 MB PNG: the payload really carries the full 2,515,046-byte data
URI. See `.trellis/spec/skills/external-api-integration.md` for the general
lesson.

🚨 **Do not read that as "ARG_MAX fails loudly and stops you."** The
2026-08-29 write-up says the old code failed "before any network call was
made", and what was actually recorded is a **stderr line**, not an exit
status — nobody wrote down whether that run aborted or carried on. The
distinction turned out to matter, because the same wall on the **caller's**
side of the fence did *not* stop anything:

> Building a `data:` URI into `--extra-json` yourself — the documented route
> for `input_references` — passes that URI to `jq` as a command-line
> argument. Over `ARG_MAX`, `jq` never runs, the command substitution yields
> an empty string, `--extra-json ""` was treated as **not passed**, and the
> job was submitted and billed with **no references in it at all**. One line
> on stderr, exit `0`. Measured 2026-09-17.

**Closed in 1.30.0**: an `--extra-json` that was *written on the command line*
but is empty is now an error (exit 1, nothing submitted), while omitting the
flag is byte-for-byte what it always was. The script cannot tell an empty
value from an absent one by looking at the value, so it remembers whether the
flag was typed. The ARG_MAX wall itself is still there — this stops it costing
money, it does not make a 2.5 MB argument work. Keep a reference small enough
to pass (a 768 px long edge is tens of kilobytes), or attach it with
`--frame-first-image`, which encodes through a temp file and has no such
limit. The two paths are still asymmetric at the same file size; only the
failure is now loud on both. Full reproduction in
[`references/api-params.md`](references/api-params.md).

**An attached frame changes what happens to `aspect_ratio`, and it is not
the same on every model.** `bytedance/seedance-2.5` (the default model)
**requires** `aspect_ratio: "adaptive"` for any image-to-video request —
every other value fails, verified across multiple real attempts. Other
models merely **offer** `adaptive`. The script treats those two differently
on purpose, and announces every branch with a one-line `NOTE:` on stderr —
it never changes, or declines to change, your aspect ratio silently:

| Case | What the script sends |
|---|---|
| `bytedance/seedance-2.5` + a frame | `adaptive`, **overriding** any `--aspect-ratio` you passed. API requirement. |
| another model + a frame + no `--aspect-ratio` | `adaptive`, when that model's catalog entry lists it — so the clip follows the frame's shape instead of the API's own default |
| another model + a frame + an explicit `--aspect-ratio` | your value, untouched. These models do not require `adaptive`, so overriding your choice would be the tool overreaching. Pass `--aspect-ratio adaptive` if you want the frame's shape. |
| a model whose catalog entry has no `adaptive`, or no catalog entry at all | no `aspect_ratio` field at all — never a value the model might reject |

"Does this model offer `adaptive`" is read from the same live catalog
(`video_attributes.aspect_ratios`, cache → live → stale cache → bundled
snapshot) the rest of the validation uses, not from a hardcoded list, so a
model Ofox adds tomorrow is handled without a script change.

Report results honestly, the same way `cloudflare-drop` reports its mode:
state which model/resolution/duration/aspect ratio were **actually used**
(not just requested) and the **actual** `VIDEO_COST` — never invent a cost
number or claim a video is ready without a real `VIDEO_PATH` from the
script.

**Always state the full `VIDEO_PATH` as its own standalone line in your
reply to the user** — not folded into a sentence or buried mid-paragraph.
The script always resolves `--out-dir` to an absolute path before printing
`VIDEO_PATH`, so relay that absolute path exactly as printed; the file's
location is the actual deliverable here, and the user should be able to
find it without re-deriving your working directory.

## The no-resubmit rule (non-negotiable)

**Never re-run `generate` for the same logical request just because it's
taking a while or a tool call timed out.** A create call that gets any HTTP
response has already either made the job (billable) or been rejected
(not billable) — running `generate` again for "the same video" risks a
second, separately billed job.

If `generate`'s own poll loop hits its time budget (job still
`pending`/`queued`/`in_progress`), it exits with the job id and prints
exactly this instruction — follow it:

```bash
bash references/ofox-video.sh poll JOB_ID
```

If a Claude Code tool call itself times out while `generate` is still
running (the script hasn't printed a result yet), the job may still be
mid-flight upstream — you won't have the job id from stdout in that case.
Don't guess or re-submit; **list the recent jobs and look** (below), or tell
the user to check `https://app.ofox.ai`, and resume the id you find with
`poll`.

**`batch` prints its own resume command the moment its takes are submitted**,
before the waiting starts — a single `poll` over every take's job id, with the
out-dir already filled in. That line exists so a tool-call timeout during the
concurrent wait never costs you the job ids of takes you have already paid
for. Use it; never re-run `batch`.

If the create call itself gets an ambiguous network failure (curl exits
nonzero with **no HTTP response at all** — exit code `5`), the script
explicitly refuses to guess whether a job was created. Don't auto-retry —
find out, with the step below.

### The recovery step: list the jobs, compare, then decide

**`GET /v1/videos` returns HTTP 200 and a list of your jobs** — measured
2026-09-16, and it replaces a claim this skill used to make that the only way
to check was the web dashboard. Each entry carries `created_at`, `id`,
`model`, `prompt`, `status` and `usage`, which is everything needed to answer
"did my create actually land":

```bash
curl -s -H "Authorization: Bearer $OFOX_API_KEY" \
  "https://api.ofox.ai/v1/videos?limit=5" | jq '.'
```

Read the newest entry's `created_at`, `status` and `id` off that — the exact
envelope is not restated here, since printing it and looking is both free and
more reliable than a filter written against a remembered shape. (`/v1/jobs` is
404; `/v1/videos` is the one.) The endpoint needs the key, unlike `models` and
`providers`, so the safety contract applies — reference the environment
variable as above and never echo its value.

**Use it like this after a transport fault:** list, compare the newest entry's
`created_at` against the moment your create died, and only then decide. If
nothing newer than your own earlier work is on the list, no job was created
and a retry is safe. If something is there, you have its id — `poll` it, never
`generate` again.

That is exactly how the 2026-09-16 case was settled: a create lost its
connection with no HTTP response, the script exited `5` and refused to guess
(correctly), the list's newest entry was still hours old, and the retry went
ahead knowing rather than hoping.

**This does not weaken the no-resubmit rule; it is what the rule was
missing.** The reason never to blind-retry was that nobody could tell whether
a job existed. Now somebody can — so "don't guess" stops being a dead end and
becomes "go and find out, then act on what you found". Blind retries are still
never acceptable.

### The rule has now survived a real transport fault

Until 2026-09-05 every clause above was a rule with no live test behind it —
reasoned from the API's shape, never exercised by an actual broken
connection. Two jobs that day dropped their TLS connection mid-poll, and a
third did the same on 2026-09-06:

```
curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to api.ofox.ai:443
WARN: poll request failed (curl exit 35). Retrying the POLL (not create) in 6s...
```

**All three recovered on the retry and completed normally**, videos
downloaded, costs reported. Jobs `1cf5ac46-058f-4615-a47b-067743f76f8c`,
`50f623b2-c54a-4d9d-9646-31dd06e2a926` and
`8efeb556-bf38-45ec-940b-a792ef74bfcf`, 2.88 USD each.

Two things that confirms. The poll retry is the right response to a transport
fault — the job was running the whole time and the connection, not the job,
was what broke. And the parenthetical in that warning line ("not create") is
doing real work: a resubmit at any of those moments would have created a
second billable job and doubled a 2.88 USD spend, on a fault that cleared by
itself in six seconds. A dropped connection while polling is **never**
evidence about the job's state — three for three now, on separate days.

**2026-09-16 added three more `curl (35)` events in a single session** — one
on a create, two on polls — and both halves of the script behaved correctly
each time: the polls retried the poll and their jobs completed; the create
refused to guess and exited `5`, which is what sent someone looking for the
job list in the first place. Six events on four days is enough to say plainly
that **this API's transport layer is flaky**, and that neither the
no-resubmit rule nor the recovery step above is over-engineering. Budget for
a dropped connection in any session that spends real money; it is normal
here, and it says nothing about the job.

## Error handling

The script maps every documented `error.code` to a fixed, actionable
message and a distinct exit code. `error.message` (the upstream's own free
text) is **not** a stable contract to branch logic on, but it can carry a
specific, useful detail the generic mapped explanation doesn't (e.g. a
minimum reference-image width) — so the script always prints it too,
labeled `Upstream message: ...`, alongside the mapped explanation, not only
when `error.code` itself is absent or unrecognized.

| Exit | Meaning |
|---|---|
| `0` | Success — video downloaded, cost printed. |
| `1` | Usage/parameter validation error — no network call was made. Fix the flag and retry `generate` freely. |
| `2` | Environment error — `curl`/`jq`/`OFOX_API_KEY` missing. Fix the environment, no job was attempted. |
| `3` | The API rejected the request, or the job ended `failed`/`cancelled`/`expired`. The mapped message explains why (see `references/api-params.md` for the full error-code table). Includes `output_moderation_failed` — a **post-generation** failure (the job ran, its output failed a content check afterward), **not billed** (no `usage` field on the response), safe to fix by submitting a new `generate` call with a different prompt/reference — that's a new request, not a resubmission of the failed one. |
| `4` | Timed out waiting for a terminal state. The job is still running — `poll JOB_ID`, do not `generate` again. |
| `5` | Ambiguous network failure on create — no HTTP response received. Do not auto-retry; list `GET /v1/videos` (see "The recovery step") or check the dashboard, and retry only once you know nothing was created. |
| `6` | `--out-dir` could not be created or entered (bad path, permissions) — a local filesystem problem, not an API problem. If this happened during `generate`, the job itself is unaffected (already created or still running server-side); do not re-run `generate`. Fix `--out-dir` and re-run `poll JOB_ID --out-dir <a writable directory>`. |

(That `6` row used to sit *below* a paragraph about `batch`, which broke the
table; the paragraph is now where it belongs, underneath.)

**`batch` and a multi-id `poll` collapse several jobs' outcomes into one exit
code, and pick the most severe actionable one.** `3` if anything failed —
a rejected submission, or a take that ended `failed` after being submitted —
because a failure needs a different prompt. `4` if nothing failed but something
is still running, because that needs another poll and nothing else. `0` only
when every requested take is on disk. Either way the takes that did complete
are downloaded and listed with their real cost, and the counts
(`TAKES_COMPLETED`, `TAKES_FAILED`, `TAKES_RUNNING`, `TAKES_NOT_SUBMITTED`)
say which case you are in — a partial run is reported honestly rather than
discarded.

## For scenario skills built on this

`seedance-short-drama`, `seedance-ad-creative`, `seedance-anime-drama` and
`seedance-product-video` invoke this skill's script rather than duplicating
any of the request-building, polling, error-mapping, or download logic above.
They own the scenario-specific prompt template and recommended parameter
defaults; this skill owns the mechanics of talking to the API correctly and
safely, and the numbers that go in front of the user.

**The path they invoke it by is a probe, not a constant.** Their examples are
written `../ofox-video-core/references/ofox-video.sh`, which resolves under
skills.sh, ClawHub and `npx ofox-skills`, where a skill's directory is named
after the skill. It does not resolve on LobeHub, which unpacks each skill to
`~/.agents/skills/ofoxai-skills-<name>` — the sibling there is
`ofoxai-skills-ofox-video-core`, so a scenario skill hits `No such file or
directory` with this skill sitting right next to it. Each scenario skill
therefore carries a "Where the core skill lives" section — "Where the two
core skills live" in `seedance-anime-drama`, which probes for
`ofox-image-core` alongside — that runs the probe before the first call and
substitutes what it finds:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/ofox-video.sh" ] && echo "$d" && break
done
```

A new scenario skill built on this one wants that section too — the relative
path on its own is a contract only with the installers that name directories
after skills.

**Don't restate the approval rules in a scenario skill.** Link
[`references/approval-gate.md`](references/approval-gate.md) and add only what
is scenario-specific (which command to dry-run, which parameters matter). The
four scenario skills each used to carry their own prose version of "quote it,
get a yes" and they had already begun to diverge — the shared file exists so
that stops happening.

### Writing the prompt: one shared structure reference

**Load [`references/prompt-structure.md`](references/prompt-structure.md)
before writing a prompt.** It is the prompt-structure reference shared by
every Seedance scenario skill: the vendor's own formula, the header-manifest
-> timeline -> closing-block skeleton, when and how to timestamp segments,
how many shots a clip of a given length actually carries in the gallery,
transition and camera vocabularies, **why a camera move needs its waypoint
frames and not just a verb**, pacing, consistency locks
and negative lists, dialogue density by tier, the two meanings of an attached
image (frame lock vs. identity reference, and the `--extra-json` form for the
latter), and endings — every item tagged with the gallery cases it was
observed in, or with the Ofox job ids it was measured on. A
scenario skill keeps only its own template and links that file for the rest,
exactly as it links `approval-gate.md` for the spend rule. This `SKILL.md`
does not restate it: the script runs whatever `--prompt` it is given, and the
shape of that text is the scenario layer's job.

### Asking before writing: one shared brief reference

**Load [`references/creative-brief.md`](references/creative-brief.md) before
asking the user anything.** It is the shared rule for the pre-generation
brief: the three tiers of axis, one `AskUserQuestion` round of at most four
questions, the shape of a question, the "Let the AI decide" discipline, the
generic skip rows, how the brief recap rides along with the cost table, the
fallback when the runtime has no `AskUserQuestion`, and the anti-patterns. A
scenario skill keeps only its own question set, its scenario-specific
inference rows, its answer-to-prompt map and a worked recap. Three shared
files, three jobs: what to ask (`creative-brief.md`), how to write
(`prompt-structure.md`), what to show before spending
(`approval-gate.md`).

## Compatible with existing prompt-writing skills

This skill is an execution layer, not a director layer — it does not compete
with skills that specialize in writing Seedance prompts, it just runs
whatever prompt it's given. If the user already has a well-crafted prompt
from a "director" skill such as
[`LeoYeAI/seedance-skills`](https://github.com/LeoYeAI/seedance-skills) or
[`liyue-aigc/seedance-2-5-video-director`](https://github.com/liyue-aigc/seedance-2-5-video-director),
pass that prompt straight to `ofox-video.sh generate` — there's no need to
run this repo's own scenario-specific prompt-crafting steps (the ones
`seedance-short-drama`/`seedance-ad-creative`/`seedance-product-video`/
`seedance-anime-drama` each document) on top of a prompt that's already been
written. Those scenario skills exist for users who don't already have a
prompt and want one built for them; treat an existing director-skill output
as a ready-to-use prompt, not raw material to rewrite.
