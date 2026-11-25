---
name: sk-improve
description: Adapts and changes the channel's rules (SOUL.md, docs/soul/, thresholds.json, flows) rather than a single video, including first-time setup of the kit for a new channel, turning a posted video's results into a recorded lesson, adding, editing or retiring a storytelling flow, changing a threshold, or adding a lint check. The user supplies the stats or screenshots; the agent never scrapes them. Use when the user says "the video got N views", "here are my stats", "here's a screenshot of the analytics", "what did this video teach us", "this flow doesn't work", "change the threshold", "drop rule X", "add a new flow", "why did this get zero views", "adapt the rules to my channel", "this rule doesn't fit my niche", "change the voice/style", "set up the kit for my channel", or on first run when SOUL.md has no change-log entries yet.
---

# sk-improve: change the rules, not an old video

**Announce:** "Using sk-improve for <change>."

Rules live in `SOUL.md`, `docs/soul/`, `docs/flows/`. Distribution lessons:
`docs/lessons/for-you-distribution.md`. This skill only fixes the **order** of a
rule change. The § wins over this file.

**SOUL.md is this channel's editable defaults, not a fixed standard.** The kit
ships rules that worked for one channel. Adapt them to yours, and relax or delete
any rule that your own stats or taste contradict. Every change, and its reason,
goes in the change log at the bottom of `SOUL.md`.

## First run: make SOUL yours

Use when `SOUL.md`'s change log has no entries, or the user asks to set up the kit.

1. **Ask, one short round:** niche and audience; language (BCP-47) and caption
   language; platforms (TikTok, Shorts, Reels); voice (engine, voice id, tempo;
   offer the default for their language from §4: English `edge`, Vietnamese
   `vieneu`, and keep whatever they pick instead);
   tone (dry, warm, irreverent; whether strong words are acceptable); target video
   length; anything in the defaults they already know they dislike.
2. **Edit the data half** in `docs/soul/thresholds.json`, for example:
   - `targetDurationSeconds` / `maxDurationSeconds` to their length and platform;
   - `strongWords.max` above 0 only if they want it (default off);
   - `bannedPhrases` swapped for filler typical of their language and niche;
   - sentence-length keys, ideally measured with `docs/lessons/style-measurement.md`
     rather than guessed.
3. **Edit the reasoning half** to match: §1 voice and tone, §3b sentence style, §4
   engine and pronunciation notes for their language, §7 caption language, §11
   platform spec. Rewrite the `why` of each changed key.
4. **Set defaults for new videos**: the `voice` and `language` in
   `src/videos/_template/narration.json`.
5. **Log every change** in the `SOUL.md` change log: date, rule (§ or key), old,
   new, why ("user's choice: <reason>"). One line each.
6. Run `bun run lint example` and `bun run check`; then hand back to `sk-pipeline`.

## A rule lives in two halves; change both

| Half | Where | Read by |
|---|---|---|
| the reasoning, the why, traps already hit | the § in `docs/soul/`, or `docs/flows/<flow>.md` | people and agents |
| the number, list or switch | `docs/soul/thresholds.json` (`value`, `rule`, `why`) | `bun run lint` |

Changing one half and not the other means lint enforces a dead rule or ignores a
live one, both silently.

## After the user posts

1. **Ask for the numbers; do not fetch them.** The user pastes stats or attaches
   screenshots (views, average watch time, retention curve, share of traffic from
   the For You / Shorts feed, likes, shares, comments). Read screenshots carefully
   and restate the figures before reasoning from them.
2. **Compare against earlier videos of the same flow**, using the flow file's
   "Cases run" table, not memory. Zero or near-zero views usually means
   distribution, not content: check `docs/lessons/for-you-distribution.md` first.
3. **Write the lesson as one sentence** before opening any file. If it will not fit
   in one sentence it is a feeling, not a lesson. One video is an anecdote; say so
   when the evidence is one data point.
4. **Record it** as one row in the "Cases run" table of `docs/flows/<flow>.md`:
   video id, date, the result, what it taught about the *flow*. Also fill the
   brief's "Posted" section (link, cover text, first caption line used), so the
   next video is compared against it rather than guessed at. A lesson left in a
   TSX comment is one the next video never reads.
5. **Is the lesson a new rule, or a reason to relax or delete one?** If yes,
   continue below. If not, stop here.

## Adding, removing or reordering a pipeline step

The steps the preview shows (and the `sk-pipeline` table) come from
`docs/pipeline.json`. To add a step, add one entry with `key`, `n` (its position: 11.5
sits between 11 and 12), `label`, `skill`, `command` (use `{id}`), and an `evidence`
rule the preview can check on disk: `{"file": "out/{id}/x.png"}`,
`{"glob": "out/{id}/*-yt.mp4"}`, or `{"json": "src/videos/{id}/x.json", "nonEmpty": "items"}`.
To drop a step, delete its entry. Then add the row to the `sk-pipeline` table, say in
which skill the step is done, log the change in `SOUL.md`, and open `bun run preview` to
check the step appears with the right status.

## Changing a rule

1. **Find every place it lives:**
   `grep -rn "<keyword>" SOUL.md docs/soul docs/flows scripts .claude/skills`.
   Old rules often live in more than one place.
2. **Edit the data first** (`thresholds.json`, or the flow file's front matter),
   because that is the half a machine checks. Keep `rule` pointing at the § and
   `why` as one honest line.
3. **Edit the prose to match**: the §, the flow file, the checklist line in
   `SOUL.md`. Do not copy a number into prose if it already lives in
   `thresholds.json`; point at the key.
4. **A new machine-checkable rule** gets a check in the lint script that reads its
   number from `thresholds.json`. Never hard-code a number in the script.
5. **Run** `bun run lint <id>` on recent videos and `bun run check`. Read every line
   that changed, not the totals. Old videos failing the new rule is expected.
6. **Log it** in the change log at the bottom of `SOUL.md` (and the flow file's
   change log for flow rules): date, what changed, which video or stats prompted it.
7. **One commit per rule change**, separate from video work, so history shows when
   a rule changed and why.

## Relaxing or deleting a rule

Allowed, and expected, when the user's own stats or taste contradict a default.
Same order as above: data half and § together, never one alone. Deleting a rule
means removing its key from `thresholds.json`, its § text and its checklist line,
and any lint check that reads it. The reason goes in the change log (e.g. "three
videos at 120 s held retention as well as 70 s ones", or "user prefers longer
sentences"), so a later session does not reintroduce it.

## Never rewrite old videos

A posted video is history. New rules apply to the **next** video. An old video
that now fails lint stays as it is; note "made before rule" in its "Cases run"
row if needed. Remaking a topic means a new id (§13), never overwriting.

## Do not

- Copy rules into skills. Skills order steps; the § holds the rule.
- Rename or re-id a flow that already has videos. Retire it and open a new one.
- Generate the reasoning half automatically. The why is written by a person.
- Add scraping, analytics APIs or upload automation to "close the loop". The user
  brings the numbers.

Next: open the skill of the step the change affects (`sk-brief` for flows,
`sk-narration` / `sk-style` for wording) and check its commands still hold.
