---
name: ui-walkthrough
description: Make a narrated video of what a merged pull request changed in a web app's UI — recordings of the real running app, before and after, with voiceover and captions — instead of reading code. Use when asked for a PR video, UI walkthrough, "what changed" video, release demo or before/after recording of a merged PR.
model: sonnet
---

# UI walkthrough video

> Copied from [The-Utopia-Studio/ui-walkthrough](https://github.com/The-Utopia-Studio/ui-walkthrough) v0.7.1 (`5894b90`), also installable whole as the `prview` plugin. Change it there, then copy it here again.

Turn a merged pull request into a short narrated video that **shows the app**: the screens that changed, recorded from the real app running locally, the old version beside or above the new one. The viewer should come away knowing what looks or works differently and how to use it, without reading code.

**Output:** `.ui-walkthrough/out/pr-<n>-walkthrough.mp4` in the repo: 1920×1080, 30 fps, usually 1–3 minutes, voiceover and captions. `--preview` makes a quick 720p draft first.

**Command:** everything runs through one script, called `uiw` below:

```bash
uiw() { UI_WALK_CACHE="${CLAUDE_PLUGIN_DATA}" node "${CLAUDE_PLUGIN_ROOT}/skills/ui-walkthrough/scripts/cli.mjs" "$@"; }
```

If those `${CLAUDE_PLUGIN_…}` variables appear literally (the skill was copied in rather than installed as a plugin), use `node <this skill's folder>/scripts/cli.mjs`. Run it from inside the repository whose PR you are filming. Needs Node 20+, git, ffmpeg and the GitHub CLI (`gh`, signed in).

## Rules

- **Show, don't read code.** Every content slide is a recording of the app, or a short list or text slide for what a recording can't show. No code on screen.
- **Never type a password.** The person signs in themselves (`uiw sign-in <n>` opens a browser for them). Never create accounts on hosted services.
- **Record on test data.** Real names and data end up in the video. Use test accounts and test records; say which ones you used.
- **Look, don't change** by default. A tour may change something only if it can be undone, has no side effects (no emails, messages, payments, provisioning; read the code that runs first), and the clip puts it back, on camera or in `teardown`. Never submit forms, send, approve or pay. Afterwards, check the data is back as it was.
- **Local only.** Record against the local copies `prepare` makes. Don't start anything that deploys, migrates or pushes schema from those copies (for example a backend dev command that syncs functions to a shared deployment).
- **Follow the repo's notes.** If `ui-walkthrough.config.json` names a `notes` file, read it first: it holds that repo's test accounts, data not to touch, and banners to dismiss.

## Workflow

### 0. First time in a repo

If there's no `ui-walkthrough.config.json` at the repo root, set one up with the person (`references/config.md`):

1. **Ask which voice they want**, and offer both:
	- **Free default** (Kokoro `am_echo`): no setup, runs on their machine. If they want to hear other free voices first, run `uiw voices` and send them the samples, then set `voice.kokoro` to their pick.
	- **Deepgram Aura-2**: the most natural. **Thalia is the default**; offer it first, then other Deepgram voices if they want one (Andromeda, Helena, Apollo, Orion, Zeus, or any Aura-2 name; with their key, `uiw voices --deepgram` makes samples of all of them, Thalia first). They add `DEEPGRAM_API_KEY=<their key>` to `.env.local` **themselves**: never paste a key into the chat.
2. Run `uiw init --voice free`, or `uiw init --voice deepgram` (Thalia), or `uiw init --voice deepgram --deepgram-voice orion` for another.
3. Fill in which folder holds the web app, the command that starts its dev server, env files to copy, and where sign-in lives.
4. Run `uiw doctor`: it shows which voice will be used and whether the key was found (it never prints the key). Then ask them to commit the config.

The voice can be changed any time in the config's `voice` section.

### 1. Prepare (about a minute)

```bash
uiw prepare <n>
```

Exports the code just **before** the merge (the merge commit's first parent) and just **after** it into copies outside the repo, reuses `node_modules` by copy-on-write clone (or installs, if the lockfile changed), copies the env files, and writes `.ui-walkthrough/pr-<n>/` with `pr.json` (commits, UI files changed, PR text) and starter `narration.json`, `tour.json`, `manifest.json`. `.ui-walkthrough/` is kept out of git automatically.

Start both servers: in Claude Code desktop with `preview_start` on `ui-walkthrough-before` and `ui-walkthrough-after` (written to `.claude/launch.json` when `.claude/` exists); otherwise `uiw serve <n>` (`uiw serve <n> --stop` afterwards). Then, if there's no saved session or the app needs one, **ask the person to sign in**: `uiw sign-in <n>`. (Unattended runs use `uiw auth <n>` instead; see below.)

### 2. Decide what to show

Start with `uiw changes <n>`: for each UI file it prints the pages it shows up on, the user-facing text it added or removed, and how many other lines changed. Read the PR text in `pr.json`, then open a file only where its other changed lines could change what is on screen or what a click does. It only sees text, so a file with a lot of other changes may still be a layout or behaviour change worth filming. Before a tour changes data, still read the code that click runs. List:

- **Which screens changed**, for which kind of user, and what a user would do there to see the change.
- **Before/after or after only.** Redesigns and replaced controls: before/after. New screens: after only.
- **Knock-on effects** in other parts of the app (an admin setting that changes what end users see): film both sides. Put a state change in a clip's `setup` and undo it in `teardown`.
- **What can't be filmed** (emails, background jobs, roles you have no session for): a closing `list` slide.

If nothing user-visible changed, say so and stop.

### 3. Write narration, tour and manifest

All three live in `.ui-walkthrough/pr-<n>/`.

- **`narration.json`**: `{ "slides": ["…", "…"] }`, one line of speech per narrated slide, in order. Plain, friendly product language: what you see, what you can do, why it matters. Name controls exactly as the UI labels them. No file or function names. Say numbers the way they should be heard ("one twenty two").
- **`tour.json`**: the clips to film (`references/tour.md`). `setup` runs off camera; `steps` are filmed with a visible cursor. Before and after clips of one comparison get the same steps (`"side": "before"` films the old version). Clips that change data need `teardown`, or `"changes": true` if they undo it on camera. Inspect the page first so targets are exact: `uiw inspect <n> <path>` (add `--side before` for the old version) prints what it offers to click, in the landmarks and dialogs it sits in, and notes where a target needs `nth` or `exact`. It saves the full tree (grep it for text, rows and cells) and a screenshot of the first screen to `inspect/`; look at the screenshot when layout matters, such as choosing a `crop`. `--full` prints the whole tree and screenshots the whole page.
- **`manifest.json`**: the slides in order (`references/slides.md`): mostly `compare` and `clip`, with titles that say whose screen it is. `crop` zooms a comparison in on what changed; wide crops stack Before above After automatically. Durations can stay out: each slide fits its narration.

A good order: intro (one sentence) → the main before/after → the new behaviour, one idea per clip → knock-on effects → what couldn't be shown → one-line summary → outro.

Then run `uiw check-tour <n>`: it runs every clip's setup, steps and teardown quickly, without filming, and for a failed step prints which step it was and what the page offered at that moment. Fix and re-run it with the failing clip ids until it passes. It clicks for real, so the same rules apply as for recording.

### 4. Make

```bash
uiw make <n> --preview     # quick 720p draft: check timing and layout
uiw make <n>               # final 1080p
```

| Stage | What happens | Reused on re-runs |
|---|---|---|
| Check plan | Narration, tour and slides checked against each other: missing lines or clips, a Before clip filming the new version, unknown slide types. Errors stop here, before anything is voiced or filmed; warnings (lines nobody hears, clips nobody sees) don't. Also `uiw check-plan <n>` on its own. | — |
| Voice | One clip per narration line: Deepgram when `DEEPGRAM_API_KEY` is set, otherwise the free local Kokoro voice (`am_echo`) with no setup (`references/config.md`) | Lines whose text and voice are unchanged |
| Warm | Opens every page the tour visits, so the dev server compiles it now, not on camera | — |
| Record | One 2560×1440 MP4 per clip from Chrome's screencast | Clips whose definition is unchanged (`--force` re-records) |
| Render | Composes the slides, captions from local whisper, renders with HyperFrames (3 workers), encodes once | Caption transcripts |
| Check | Sound check, 8-frame contact sheet, the caption words that differ from the script, and any recording that hit the speed limit | — |

Recordings longer than their narration are sped up to fit (up to 1.8x). A clip that would need more should lose some pauses in its tour. A fresh 2-minute video takes roughly 15–20 minutes; re-runs after small edits take a few.

### 5. Check, fix, hand over

Read `check/sheet.png` and what the check printed. It lists only the caption words that differ from the script, because whisper mishears names ("Utopia OS", "Qatari reels" for riyals): add `captionFixes` to `manifest.json` and `make` again. Only the render re-runs. Every caption line is in `check/captions.txt` if you need it. A **too fast** line names a recording that plays at the fastest speed allowed and still runs past its narration, so it is hard to follow: cut pauses or steps from that clip, or split it. Check the recordings open on the right screen and text is readable.

Confirm anything a tour changed is back as it was. Send the video with what it covers, what it leaves out and why, and which records it used.

To post it on the PR, **ask first** (it's visible to everyone with access to the repo), then write a short `publish.md` note (what it covers, what it leaves out, which test records it used) and run `uiw publish <n>`: it uploads the MP4 as a release asset and comments on the PR with a link, editing the same comment on later runs.

When done, stop the servers and run `uiw clean <n>` to delete the copies. Stop the servers as soon as recording is finished (rendering doesn't need them): dev servers' build caches grow while they run, by gigabytes over a few hours with Next.js and Turbopack.

## Unattended runs (CI)

When `UI_WALK_UNATTENDED=1` (set by `examples/github-action.yml`, see `references/ci.md`), no person is there to answer or review:

- The workflow has already run `prepare`, `serve` and `auth`: the servers are up and the test user is signed in. Don't start or stop servers, and don't run `make` or `publish`: the workflow runs them after you, because they take longer than a command may.
- **Don't ask questions.** Decide, and say what you decided in `publish.md`.
- **Your tools are limited on purpose**: you can read the code (the old version is in the before copy, under `$UI_WALK_HOME`), write only in `.ui-walkthrough/pr-<n>/`, and run only the `uiw` CLI. Env files and the saved sign-in are off limits. Check pages with `uiw inspect <n> <path>` and read its screenshot, not with scripts of your own.
- **Plan as usual** (steps 2 and 3), using the repo's notes file for test accounts and data. Check targets on the live pages before writing them, and run `uiw check-tour <n>` until it passes. You may record one or two clips (`uiw record <n> <clip-id>`) and look at their frames to check a tour, but not the whole tour.
- **Write `publish.md`**: two or three sentences for the PR comment: what the video shows, anything it couldn't show, and the test records used.
- **Nothing to film?** If the PR changed nothing a user would see, or the app can't run, write a one-sentence reason to `.ui-walkthrough/pr-<n>/skip.txt` and stop. The workflow will comment that reason instead of a video.
- **Never weaken the rules** to get a video: no real records, no side effects, and every data change undone in `teardown`.

## Files

- `scripts/cli.mjs`: the `uiw` command.
- `scripts/lib/`: `prepare`, `changes`, `inspect`, `plan-check`, `serve`, `signin`, `auth`, `voice`, `warm`, `record` (+ `steps`; also `check-tour`), `compose`, `render`, `check`, `publish`, `reel` (the reel skill's scan and make: several published videos → one of 3 minutes at most).
- `references/config.md`: `ui-walkthrough.config.json` and voice providers.
- `references/tour.md`: clips, steps and targets.
- `references/slides.md`: slide types, crop, layout, captions.
- `references/ci.md`: a video for every merged PR with GitHub Actions; `auth` for unattended sign-in.
- `references/notes-template.md`: a starting point for a repo's own notes file.
